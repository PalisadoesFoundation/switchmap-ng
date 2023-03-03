"""switchmap classes that manage various configurations."""

import os.path
import os
import multiprocessing

# Import project libraries
from switchmap.core import files
from switchmap.core import log
from switchmap.core import general


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
            result: daemon_directory

        """
        # Get result
        result = self._config_core.get(
            "daemon_directory",
            "{}{}daemon".format(self.system_directory(), os.sep),
        )

        # Create the directory if not found
        if os.path.isdir(result) is False:
            files.mkdir(result)

        # Check if value exists
        if os.path.isdir(result) is False:
            log_message = (
                'daemon_directory: "{}" '
                "in the configuration file(s) doesn't exist!"
            ).format(result)
            log.log2die_safe(1012, log_message)

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

        # Create the directory if not found
        if os.path.isdir(result) is False:
            files.mkdir(result)

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
        result = "{}{}switchmap.log".format(self.log_directory(), os.sep)

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
            api_message = (
                'system_directory: "{}" '
                "in the configuration file(s) doesn't exist!"
            ).format(result)
            log.log2die_safe(1011, api_message)

        # Return
        return result


class ConfigAPIClient(ConfigCore):
    """Class gathers all configuration information."""

    def __init__(self, section):
        """Intialize the class.

        Args:
            section: Section of the config file to read

        Returns:
            None

        """
        # Instantiate sub class
        ConfigCore.__init__(self)

        # Initialize key variables
        self._config_api_client = self._config_complete.get(section)

        # Error if incorrectly configured
        if bool(self._config_api_client) is False:
            log_message = (
                'No "{}:" section found in the configuration file(s)'.format(
                    section
                )
            )
            log.log2die_safe(1013, log_message)

    def server_address(self):
        """Get server_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_client.get("server_address", "localhost")
        return result

    def server_bind_port(self):
        """Get server_bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_client.get("server_bind_port", 7000)
        return result

    def server_https(self):
        """Get server_https.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_client.get("server_https", None)
        result = general.make_bool(result)
        return result

    def server_password(self):
        """Get server_password.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_client.get("server_password", None)
        if result is None:
            result = None
        elif result is False:
            pass
        elif isinstance(result, str):
            if result.lower() == "none":
                result = None
            elif result.lower() == "false":
                result = None
        return result

    def server_username(self):
        """Get server_username.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_client.get("server_username", None)
        if result is None:
            result = None
        elif result is False:
            pass
        elif isinstance(result, str):
            if result.lower() == "none":
                result = None
            elif result.lower() == "false":
                result = None
        return result

    def server_url_root(self):
        """Return server_url_root value.

        Args:
            None

        Returns:
            result: server_url_root value

        """
        # Get parameter
        if self.server_https() is True:
            result = "https://{}:{}".format(
                self.server_address(), self.server_bind_port()
            )
        else:
            result = "http://{}:{}".format(
                self.server_address(), self.server_bind_port()
            )

        # Return
        return result


class ConfigAPI(ConfigCore):
    """Class gathers all configuration information."""

    def __init__(self, section):
        """Intialize the class.

        Args:
            section: Section of the config file to read

        Returns:
            None

        """
        # Instantiate sub class
        ConfigCore.__init__(self)

        # Initialize key variables
        self._config_api_server = self._config_complete.get(section)

        # Error if incorrectly configured
        if bool(self._config_api_server) is False:
            log_message = (
                'No "{}:" section found in the configuration file(s)'.format(
                    section
                )
            )
            log.log2die_safe(1015, log_message)

    def api_listen_address(self):
        """Get api_listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_server.get("api_listen_address", "localhost")
        return result

    def api_https(self):
        """Get api_https.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_server.get("api_https", None)
        result = general.make_bool(result)
        return result

    def api_password(self):
        """Get api_password.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_server.get("api_password", None)
        if result is None:
            result = None
        elif result is False:
            pass
        elif isinstance(result, str):
            if result.lower() == "none":
                result = None
            elif result.lower() == "false":
                result = None
        return result

    def api_username(self):
        """Get api_username.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_api_server.get("api_username", None)
        if result is None:
            result = None
        elif result is False:
            pass
        elif isinstance(result, str):
            if result.lower() == "none":
                result = None
            elif result.lower() == "false":
                result = None
        return result

    def api_url_root(self):
        """Return api_url_root value.

        Args:
            None

        Returns:
            result: api_url_root value

        """
        # Get parameter
        if self.api_https() is True:
            result = "https://{}:{}".format(
                self.api_listen_address(), self.api_bind_port()
            )
        else:
            result = "http://{}:{}".format(
                self.api_listen_address(), self.api_bind_port()
            )

        # Return
        return result
