"""Class for creating search web pages."""

# Import switchmap.libraries
from switchmap.dashboard.table import interfaces as interfaces_


class Search:
    """Class that creates the search's various HTML tables."""

    def __init__(self, data):
        """Initialize the class.

        Args:
            search: Search dictionary

        Returns:
            None

        """
        # Process YAML file for host
        self._data = data

    def interfaces(self):
        """Create the ports table for the search.

        Args:
            None

        Returns:
            table: Interface table

        """
        # Initialize key variables
        data = self._data
        table = None

        # Get the flask table
        if bool(data) is True:
            table = interfaces_.table(data)

        # Return the table
        return table
