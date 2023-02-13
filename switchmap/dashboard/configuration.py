"""switchmap.classes that manage various configurations."""

import os.path
import os

# Import project libraries
from switchmap.core.configuration import ConfigCore
from switchmap.core import log


class ConfigDashboard(ConfigCore):
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
        section = "dashboard"
        self._config_dashboard = self._config_complete.get(section)

        # Error if incorrectly configured
        if bool(self._config_dashboard) is False:
            log_message = (
                'No "{}:" section found in the configuration file(s)'.format(
                    section
                )
            )
            log.log2die_safe(1016, log_message)

    def bind_port(self):
        """Get bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_dashboard.get("bind_port", 7001)
        return result

    def listen_address(self):
        """Get listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_dashboard.get("listen_address", "0.0.0.0")
        return result

    def daemon_log_file(self):
        """Get daemon_log_file.

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
