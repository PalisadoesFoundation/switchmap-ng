"""switchmap classes that manage various configurations."""

# Import project libraries
from switchmap.core.configuration import ConfigAPIClient, ConfigAPI
from switchmap.core import log


class ConfigDashboard(ConfigAPIClient, ConfigAPI):
    """Class gathers all configuration information."""

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        section = "dashboard"

        # Instantiate sub class
        ConfigAPIClient.__init__(self, section)
        ConfigAPI.__init__(self, section)
        self._config_dashboard = self._config_complete.get(section)

        # Error if incorrectly configured
        if bool(self._config_dashboard) is False:
            log_message = (
                f'No "{section}:" section found in the configuration file(s)'
            )
            log.log2die_safe(1016, log_message)

    def api_bind_port(self):
        """Get api_bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_dashboard.get("api_bind_port", 7001)
        return result

    def username(self):
        """Get username.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_dashboard.get("username", "switchmap")
        return result
