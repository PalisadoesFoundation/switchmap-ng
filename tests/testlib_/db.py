"""Test module for db."""

from __future__ import print_function

# PIP3 imports
from sqlalchemy.orm import Session

# Application imports
from switchmap.db import models
from switchmap.db import ENGINE

from switchmap.core.configuration import Config
from switchmap.core import log


class Database:
    """Database class."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Make sure we are doing operations only on a test database
        expected = "switchmap_unittest"
        config = Config()
        if config.db_name() != expected:
            log_message = """\
The database under test must be named {}""".format(
                expected
            )
            log.log2die(1174, log_message)

    def drop(self):
        """Drop database.

        Args:
            None

        Returns:
            None

        """
        # Drop all the tables
        with ENGINE.connect() as connection:
            with Session(bind=connection) as session:
                models.BASE.metadata.drop_all(session.get_bind())

    def create(self):
        """Create database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key values
        models.create_all_tables()
