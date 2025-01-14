"""Class for creating device web pages."""

# Import switchmap.libraries
from switchmap.dashboard.table.device import Device as DeviceTable


class Device:
    """Class that creates the device's various HTML tables."""

    def __init__(self, data):
        """Initialize the class.

        Args:
            data: Device dictionary

        Returns:
            None

        """
        # Process YAML file for host
        self._data = data
        self._table = DeviceTable(data)

    def hostname(self):
        """Get the system hostname.

        Args:
            None

        Returns:
            result: The system hostname

        """
        # Return
        result = self._data.get("hostname", "")
        return result

    def interfaces(self):
        """Create the ports table for the device.

        Args:
            None

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        table = self._table.interfaces()

        # Convert to HTML
        if bool(table) is True:
            # Get HTML
            html = table.__html__()
        else:
            html = ""

        # Return
        return html

    def system(self):
        """Create summary table for the devie.

        Args:
            None

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        table = self._table.system()

        # Convert to HTML
        if bool(table) is True:
            # Get HTML
            html = table.__html__()
        else:
            html = ""

        # Return
        return html
