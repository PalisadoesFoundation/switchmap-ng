"""Class for creating device web pages."""

import textwrap
from datetime import datetime

# Import switchmap.libraries
from switchmap.dashboard import SystemDataRow


class System:
    """Class that creates the data to be presented for the device's ports."""

    def __init__(self, system_data):
        """Instantiate the class.

        Args:
            system_data: Dictionary of system data

        Returns:
            None

        """
        # Initialize key variables
        self._data = system_data

    def rows(self):
        """Return data for the device's system information.

        Args:
            None

        Returns:
            rows: List of Col objects

        """
        # Initialize key variables
        rows = []

        # Configured name
        rows.append(
            SystemDataRow(parameter="System Name", value=self.sysname())
        )

        # System IP Address / Hostname
        rows.append(
            SystemDataRow(parameter="System Hostname", value=self.hostname())
        )

        # System Description
        rows.append(
            SystemDataRow(
                parameter="System Description",
                value=textwrap.fill(self.sysdescription()).replace(
                    "\n", "<br>"
                ),
            )
        )

        # System Object ID
        rows.append(
            SystemDataRow(
                parameter="System sysObjectID", value=self.sysobjectid()
            )
        )

        # System Uptime
        rows.append(
            SystemDataRow(parameter="System Uptime", value=self.sysuptime())
        )

        # Last time polled
        rows.append(
            SystemDataRow(
                parameter="Time Last Polled", value=self.last_polled()
            )
        )

        # Return
        return rows

    def hostname(self):
        """Return hostname.

        Args:
            None

        Returns:
            result: hostname

        """
        # Return
        result = self._data.get("hostname", "")
        return result

    def last_polled(self):
        """Return last_polled.

        Args:
            None

        Returns:
            result: last_polled

        """
        # Return
        timestamp = self._data.get("lastPolled", 0)
        result = datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return result

    def sysdescription(self):
        """Return sysdescription.

        Args:
            None

        Returns:
            result: sysdescription

        """
        # Return
        result = self._data.get("sysDescription", "")
        return result

    def sysname(self):
        """Return sysname.

        Args:
            None

        Returns:
            result: sysname

        """
        # Return
        result = self._data.get("sysName", "")
        return result

    def sysobjectid(self):
        """Return sysobjectid.

        Args:
            None

        Returns:
            result: sysobjectid

        """
        # Return
        result = self._data.get("sysObjectid", "")
        return result

    def sysuptime(self):
        """Return sysuptime.

        Args:
            None

        Returns:
            result: sysuptime

        """
        # Return
        seconds = self._data.get("sysUptime", "")

        # Parse the time
        (minutes, remainder_seconds) = divmod(seconds / 100, 60)
        (hours, remainder_minutes) = divmod(minutes, 60)
        (days, remainder_hours) = divmod(hours, 24)

        # Return
        result = "{:,} Days, {:02d}:{:02d}:{:02d}".format(
            int(days),
            int(remainder_hours),
            int(remainder_minutes),
            int(remainder_seconds),
        )
        return result
