#!/usr/bin/env python3
"""switchmap.classes that manage various configurations."""

import os.path
import os
import multiprocessing

# Import project libraries
from switchmap.core.configuration import Main
from switchmap.core import log


class Server(Main):
    """Class gathers all configuration information."""

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate sub class
        Main.__init__(self)

        # Initialize key variables
        self._config_server = self._config_complete.get("server")

    def bind_port(self):
        """Get bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_server.get("bind_port", 7000)
        return result

    def db_host(self):
        """Return db_host value.

        Args:
            None

        Returns:
            result: db_host value

        """
        # Get parameter
        result = self._config_server.get("db_host", "localhost")

        # Return
        return result

    def db_name(self):
        """Return db_name value.

        Args:
            None

        Returns:
            result: db_name value

        """
        # Get parameter
        result = self._config_server.get("db_name", "switchmap")

        # Return
        return result

    def db_max_overflow(self):
        """Get DB connection pool overflow size.

        Args:
            None

        Returns:
            result: Configured value

        """
        # Get parameter
        _result = self._config_server.get("db_max_overflow", 30)
        value = int(_result)

        # Set min / max values
        result = min(abs(value), 50)

        # Return
        return result

    def db_pass(self):
        """Return db_pass value.

        Args:
            None

        Returns:
            result: db_pass value

        """
        # Get parameter
        result = self._config_server.get("db_pass")

        # Return
        return result

    def db_pool_size(self):
        """Get DB connection pool size.

        Args:
            None

        Returns:
            result: Configured value

        """
        # Get parameter
        _result = self._config_server.get("db_pool_size", 30)
        value = int(_result)

        # Set min / max values
        result = min(abs(value), 50)

        # Return
        return result

    def db_user(self):
        """Return db_user value.

        Args:
            None

        Returns:
            result: db_user value

        """
        # Get parameter
        result = self._config_server.get("db_user", "switchmap")

        # Return
        return result

    def listen_address(self):
        """Get listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_server.get("listen_address", "0.0.0.0")
        return result

    def daemon_log_file(self):
        """Get daemon_log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = "{}{}switchmap-server.log".format(
            self.log_directory(), os.sep
        )

        # Return
        return result
