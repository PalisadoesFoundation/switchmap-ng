"""switchmap.classes that manage various configurations."""

import os.path
import os
import multiprocessing

# Import project libraries
from switchmap.core import files
from switchmap.core import log


class _Config:
    """Class gathers all configuration information."""

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        filepath = files.config_filepath()
        self._config_complete = files.read_yaml_file(filepath)


class ConfigCore(_Config):
    """Class gathers all configuration information."""

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate sub class
        _Config.__init__(self)

        # Initialize key variables
        section = "core"
        self._config_core = self._config_complete.get(section)

        # Error if incorrectly configured
        if bool(self._config_core) is False:
            log_message = (
                'No "{}:" section found in the configuration file(s)'.format(
                    section
                )
            )
            log.log2die_safe(1006, log_message)

    def agent_subprocesses(self):
        """Get agent_subprocesses.

        Args:
            None

        Returns:
            result: result

        """
        # Get threads
        threads = max(1, self._config_core.get("agent_subprocesses", 20))

        # Get CPU cores
        cores = multiprocessing.cpu_count()
        desired_max_threads = max(1, cores - 1)

        # We don't want a value that's too big that the CPU cannot cope
        result = min(threads, desired_max_threads)

        # Return
        return result

    def daemon_directory(self):
        """Determine the daemon_directory.

        Args:
            None

        Returns:
            result: configured daemon_directory

        """
        # Get result
        result = self._config_core.get(
            "daemon_directory",
            "{}{}daemon".format(self.system_directory(), os.sep),
        )

        # Check if value exists
        if os.path.isdir(result) is False:
            daemon_message = (
                'daemon_directory: "{}" '
                "in the configuration file(s) doesn't exist!"
            ).format(result)
            log.log2die_safe(1089, daemon_message)

        # Return
        return result

    def log_directory(self):
        """Determine the log_directory.

        Args:
            None

        Returns:
            result: configured log_directory

        """
        # Get result
        result = self._config_core.get(
            "log_directory", "{}{}log".format(self.system_directory(), os.sep)
        )

        # Check if value exists
        if os.path.isdir(result) is False:
            log_message = (
                'log_directory: "{}" '
                "in the configuration file(s) doesn't exist!"
            ).format(result)
            log.log2die_safe(1090, log_message)

        # Return
        return result

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = "{}{}switchmap-ng.log".format(self.log_directory(), os.sep)

        # Return
        return result

    def log_level(self):
        """Get log_level.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_core.get("log_level", "debug")

        # Return
        return result

    def system_directory(self):
        """Determine the system_directory.

        Args:
            None

        Returns:
            result: configured system_directory

        """
        # Get result
        result = self._config_core.get("system_directory")
        if bool(result) is False:
            result = "{}{}var".format(
                os.sep.join(os.path.split(__file__)[0].split(os.sep)[:-2]),
                os.sep,
            )

        # Check if value exists
        if os.path.isdir(result) is False:
            daemon_message = (
                'system_directory: "{}" '
                "in the configuration file(s) doesn't exist!"
            ).format(result)
            log.log2die_safe(1011, daemon_message)

        # Return
        return result

    def username(self):
        """Get username.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_core.get("username", None)
        return result
