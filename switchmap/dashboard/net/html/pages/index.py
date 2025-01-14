"""Class for creating home web pages."""

# Import switchmap.libraries
from switchmap.dashboard.net.html.pages import layouts
from switchmap.dashboard.table import index


class IndexPage:
    """Class that creates the homepages's various HTML tables."""

    def __init__(self, zones):
        """Initialize the class.

        Args:
            zones: List of zones

        Returns:
            None

        """
        # Initialize key variables
        self._zones = zones

    def html(self):
        """Create HTML table for the devices.

        Args:
            None

        Returns:
            result: HTML table string

        """
        # Initialize key variables
        html_list = []
        zones = self._zones

        # Get the tables
        tables = index.tables(zones)

        # Create the html
        for key, zone in enumerate(zones):
            html_list.append(
                layouts.table_wrapper(
                    zone.get("name", ""), tables[key].__html__()
                )
            )

        # Return tables
        result = "\n".join(html_list)
        return result
