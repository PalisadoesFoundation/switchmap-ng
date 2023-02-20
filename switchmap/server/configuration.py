"""switchmap classes that manage various configurations."""

import os.path
import os

# Import project libraries
from switchmap.core.configuration import ConfigCore
from switchmap.core import log
from switchmap.core import files


class ConfigServer(ConfigCore):
    """Class gathers all configuration information."""

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate sub class
        ConfigCore.__init__(self)

        # Initialize key variables
        section = "server"
        self._config_server = self._config_complete.get(section)

        # Error if incorrectly configured
        if bool(self._config_server) is False:
            log_message = (
                'No "{}:" section found in the configuration file(s)'.format(
                    section
                )
            )
            log.log2die_safe(1014, log_message)

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

    def cache_directory(self):
        """Determine the cache_directory.

        Args:
            None

        Returns:
            result: configured cache_directory

        """
        # Get result
        result = self._config_core.get(
            "cache_directory",
            "{}{}cache".format(self.system_directory(), os.sep),
        )

        # Create the directory if not found
        if os.path.isdir(result) is False:
            files.mkdir(result)

        # Check if value exists
        if os.path.isdir(result) is False:
            log_message = (
                'cache_directory: "{}" '
                "in the configuration file(s) doesn't exist!"
            ).format(result)
            log.log2die_safe(1040, log_message)

        # Return
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

    def ingest_directory(self):
        """Determine the ingest_directory.

        Args:
            None

        Returns:
            result: configured ingest_directory

        """
        # Get result
        result = self._config_core.get(
            "ingest_directory",
            "{}{}ingest".format(self.system_directory(), os.sep),
        )

        # Create the directory if not found
        if os.path.isdir(result) is False:
            files.mkdir(result)

        # Check if value exists
        if os.path.isdir(result) is False:
            log_message = (
                'ingest_directory: "{}" '
                "in the configuration file(s) doesn't exist!"
            ).format(result)
            log.log2die_safe(1004, log_message)

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
