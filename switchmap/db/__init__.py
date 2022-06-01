#!/usr/bin/env python3
"""Slurpy ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy.pool import QueuePool

# Slurpy libraries
from switchmap import Config
from switchmap.core import log

#############################################################################
# Setup a global pool for database connections
#############################################################################
ENGINE = None
SCOPED_SESSION = None


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Initialize constants
    use_mysql = True
    global ENGINE
    global SCOPED_SESSION

    # Initialize variables
    pool_timeout = 30
    pool_recycle = min(10, pool_timeout - 10)
    db_url = None

    # Define SQLAlchemy parameters from configuration
    config = Config()
    pool_size = config.db_pool_size()
    max_overflow = config.db_max_overflow()

    # Create DB connection pool
    if use_mysql is True:
        db_url = ('mysql+pymysql://{}:{}@{}/{}'.format(
            config.db_user(), config.db_pass(),
            config.db_host(), config.db_name()))

        # Fix for multiprocessing on pools
        _add_engine_pidguard(QueuePool)

        # Add MySQL to the pool
        if 'create_db_tables.py' in sys.argv[0]:
            # Create engine without 'future' flag
            # (Remove after SQLALchemy v2.0)
            ENGINE = create_engine(
                db_url,
                echo=False,
                echo_pool=False,
                max_overflow=max_overflow,
                poolclass=QueuePool,
                pool_pre_ping=True,
                pool_recycle=pool_recycle,
                pool_size=pool_size,
                pool_timeout=pool_timeout,
                pool_use_lifo=True)
        else:
            ENGINE = create_engine(
                db_url,
                echo=False,
                echo_pool=False,
                max_overflow=max_overflow,
                poolclass=QueuePool,
                pool_pre_ping=True,
                pool_recycle=pool_recycle,
                pool_size=pool_size,
                pool_timeout=pool_timeout,
                pool_use_lifo=True,
                future=True)

        # Fix for multiprocessing on engines
        _add_engine_pidguard(ENGINE)

        # Create a scoped session for GRAPHQL and ORM operations
        session = sessionmaker(
            autoflush=True,
            autocommit=False,
            bind=ENGINE
        )
        SCOPED_SESSION = scoped_session(session)

    else:
        ENGINE = None
        SCOPED_SESSION = None


def _add_engine_pidguard(engine):
    """Add multiprocessing guards.

    Forces a connection to be reconnected if it is detected
    as having been shared to a sub-process.

    source
    ------

    http://docs.sqlalchemy.org/en/latest/faq/connections.html
    "How do I use engines / connections / sessions with
    Python multiprocessing, or os.fork()?"

    Args:
        engine: SQLalchemy engine instance

    Returns:
        None

    """
    @event.listens_for(engine, 'connect')
    def connect(dbapi_connection, connection_record):
        """Get the PID of the sub-process for connections.

        Args:
            dbapi_connection: A SqlALchemy DBAPI connection.
            connection_record: The SqlALchemy _ConnectionRecord managing the
                DBAPI connection.

        Returns:
            None

        """
        # Update the connection_record variable for later
        connection_record.info['pid'] = os.getpid()

    @event.listens_for(engine, 'checkout')
    def checkout(dbapi_connection, connection_record, connection_proxy):
        """Checkout sub-processes connection for sub-processing if needed.

            Checkout is called when a connection is retrieved from the Pool.

        Args:
            dbapi_connection: A SqlALchemy DBAPI connection.
            connection_record: The SqlALchemy _ConnectionRecord managing the
                DBAPI connection.
            connection_proxy: The SqlALchemy _ConnectionFairy object which
                will proxy the public interface of the DBAPI connection for the
                lifespan of the checkout.

        Returns:
            None

        """
        # Get PID of main process
        pid = os.getpid()

        # Detect if this is a sub-process
        if connection_record.info['pid'] != pid:
            # substitute log.debug() or similar here as desired
            log_message = ('''\
Parent process {} forked ({}) with an open database connection, \
which is being discarded and recreated.\
'''.format(connection_record.info['pid'], pid))
            log.log2debug(1079, log_message)

            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError('''\
Connection record belongs to pid {}, attempting to check out in pid {}\
'''.format(connection_record.info['pid'], pid))


if __name__ == 'switchmap.db':
    main()
