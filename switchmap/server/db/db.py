"""Class to process connection."""

import sys

from sqlalchemy.sql import Select, Update, Delete
from sqlalchemy.orm import Session

# Import project libraries
from switchmap.core import log
from switchmap.server.db import ENGINE


def db_select_row(error_code, statement):
    """Support 'Select' actions for __ENTIRE__ row.

    Args:
        error_code: Error code to use in messages
        statement: SqlALchemy statement to execute. This must only reference
            an ORM Row object.

    Returns:
        result: List of objects resulting from Select

    https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session

    """
    # Initialize key variables
    result = []

    # Check to ensure the function executes the correct type of statement
    if isinstance(statement, Select) is False:
        log_message = '''\
Only the "Select" ORM expression is supported. Not "{}"'''.format(
            type(statement)
        )
        log.log2die(error_code, log_message)

    # Process transaction
    with ENGINE.connect() as connection:
        with Session(bind=connection, future=True) as session:
            try:
                result = session.execute(statement).scalars().all()
            except:
                # Log error
                log.log2info(error_code, 'DB "select_row" error.')
                log.log2exception(error_code, sys.exc_info())
                raise

    # Return
    return result


def db_select(error_code, statement):
    """Provide a transactional support for Select actions.

    Args:
        error_code: Error code to use in messages
        statement: SqlALchemy statement to execute

    Returns:
        result: List of objects resulting from Select

    https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session

    """
    # Initialize key variables
    result = []
    iterator_ = []

    # Check to ensure the function executes the correct type of statement
    if isinstance(statement, Select) is False:
        log_message = """\
Only the "Select" ORM expression is supported. Not "{}"\
""".format(
            type(statement)
        )
        log.log2die(error_code, log_message)

    # Process transaction
    with ENGINE.connect() as connection:
        with Session(bind=connection, future=True) as session:
            try:
                iterator_ = session.execute(statement)
            except:
                # Log error
                log.log2info(error_code, 'DB "Select" failure.')
                log.log2exception(error_code, sys.exc_info())
                raise

    # Get named tuple equivalents
    for row in iterator_.mappings():
        result.append(row)

    # Return
    return result


def db_update(error_code, statement, values=None):
    """Provide a transactional support for Update actions.

    Args:
        error_code: Error code to use in messages
        statement: SqlALchemy statement to execute
        values: List of values to insert if required

    Returns:
        result: True if the transaction is successful

    https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session

    """
    # Initialize key variables
    result = False

    # Check to ensure the function executes the correct type of statement
    if isinstance(statement, Update) is False:
        log_message = '''\
Only the "Update" ORM expression is supported. Not "{}"'''.format(
            type(statement)
        )
        log.log2die(error_code, log_message)

    # Process transaction
    with ENGINE.connect() as connection:
        with Session(bind=connection, future=True) as session:
            try:
                if bool(values):
                    session.execute(statement, values)
                else:
                    session.execute(statement)
            except:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "Update" error.')
                log.log2exception(error_code, sys.exc_info())
                raise

            try:
                session.commit()
            except:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "Update" commit error.')
                log.log2exception(error_code, sys.exc_info())
                raise
            else:
                result = True

    # Return
    return result


def db_delete_row(error_code, statement):
    """Support 'Delete' actions for __ENTIRE__ row.

    Args:
        error_code: Error code to use in messages
        statement: SqlALchemy statement to execute. This must only reference
            an ORM Row object.

    Returns:
        result: List of objects resulting from Delete

    https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session

    """
    # Check to ensure the function executes the correct type of statement
    if isinstance(statement, Delete) is False:
        log_message = '''\
Only the "Delete" ORM expression is supported. Not "{}"'''.format(
            type(statement)
        )
        log.log2die(error_code, log_message)

    # Process transaction
    with ENGINE.connect() as connection:
        with Session(bind=connection, future=True) as session:
            try:
                session.execute(statement).scalars().all()
            except:
                # Log error
                log.log2info(error_code, 'DB "delete_row" error.')
                log.log2exception(error_code, sys.exc_info())
                raise

            try:
                session.commit()
            except:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "delete_row" commit error.')
                log.log2exception(error_code, sys.exc_info())
                raise


def db_delete(error_code, statement):
    """Provide a transactional support for Delete actions.

    Args:
        error_code: Error code to use in messages
        statement: SqlALchemy statement to execute

    Returns:
        result: Number of affected rows

    """
    # Initialize key variables
    result = 0

    # Check to ensure the function executes the correct type of statement
    if isinstance(statement, Delete) is False:
        log_message = '''\
Only the "Delete" ORM expression is supported. Not "{}"'''.format(
            type(statement)
        )
        log.log2die(error_code, log_message)

    # Process transaction
    with ENGINE.connect() as connection:
        with Session(bind=connection, future=True) as session:
            try:
                result_ = session.execute(statement)
                result = result_.rowcount
            except:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "Delete" error.')
                log.log2exception(error_code, sys.exc_info())
                raise

            try:
                session.commit()
            except:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "Delete" commit error.')
                log.log2exception(error_code, sys.exc_info())
                raise

    # Return
    return result


def db_add_all(error_code, instances, die=True):
    """Provide a transactional support for Delete actions.

    Args:
        error_code: Error code to use in messages
        instances: List of instances
        die: Die if True

    Returns:
        result: True if successful

    """
    # Initialize key variables
    result = False

    with ENGINE.connect() as connection:
        with Session(bind=connection, future=True) as session:
            try:
                session.add_all(instances)
            except:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "add_all" error.')
                log.log2exception(error_code, sys.exc_info())
                if bool(die):
                    raise
                log.log2debug(error_code, "Continuing processing.")

            # Sometimes the commit fails
            try:
                session.commit()
            except:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "add_all" commit error.')
                log.log2exception(error_code, sys.exc_info())
                if bool(die):
                    raise
                log.log2debug(error_code, "Continuing processing.")
            else:
                result = True

    # Return
    return result


def db_bulk_insert(error_code, mappings, die=True):
    """Perform bulk insert for ORM objects.

    Args:
        error_code: Error code to use in messages
        mappings: List of instances to bulk insert
        die: Whether to raise an exception on failure

    Returns:
        result: True if the transaction is successful
    """
    # Initialize key variables
    result = False

    with ENGINE.connect() as connection:
        with Session(bind=connection, future=True) as session:
            try:
                # Perform bulk save
                session.bulk_save_objects(mappings)
            except Exception as e:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "bulk_insert" error.')
                log.log2exception(error_code, e)
                if bool(die):
                    raise
                log.log2debug(error_code, "Continuing processing.")

            # Commit the transaction
            try:
                session.commit()
            except Exception as e:
                # Recover and log error
                session.rollback()
                log.log2info(error_code, 'DB "bulk_insert" commit error.')
                log.log2exception(error_code, e)
                if bool(die):
                    raise
                log.log2debug(error_code, "Continuing processing.")
            else:
                result = True

    # Return
    return result
