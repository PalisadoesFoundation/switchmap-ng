"""Class for creating device web pages."""

# Import switchmap.libraries
from switchmap.dashboard.table import interfaces as interfaces_
from switchmap.dashboard.table import system as system_


class Device:
    """Class that creates the device's various HTML tables."""

    def __init__(self, data):
        """Initialize the class.

        Args:
            device: Device dictionary

        Returns:
            None

        """
        # Process YAML file for host
        self._data = data

    def interfaces(self):
        """Create the ports table for the device.

        Args:
            None

        Returns:
            table: Interface table

        """
        # Initialize key variables
        data = self._data.get("l1interfaces")
        table = None

        # Get the flask table
        if bool(data) is True:
            table = interfaces_.table(data)

        # Return the table
        return table

    def system(self):
        """Create summary table for the devie.

        Args:
            None

        Returns:
            table: System table

        """
        # Initialize key variables
        table = None
        data = self._data

        # Populate the table
        if bool(data) is True:
            table = system_.table(data)

        # Return the table
        return table
