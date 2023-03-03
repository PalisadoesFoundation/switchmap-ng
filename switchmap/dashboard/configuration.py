"""switchmap classes that manage various configurations."""

import os.path
import os

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
                'No "{}:" section found in the configuration file(s)'.format(
                    section
                )
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

    def api_log_file(self):
        """Get api_log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = "{}{}switchmap-dashboard.log".format(
            self.log_directory(), os.sep
        )

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
        result = self._config_dashboard.get("username", "switchmap")
        return result
