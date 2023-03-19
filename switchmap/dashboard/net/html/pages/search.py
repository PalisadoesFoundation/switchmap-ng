"""Class for creating search web pages."""

# Import switchmap.libraries
from switchmap.dashboard.table.search import Search as SearchTable
from switchmap.dashboard.net.html.pages import layouts


class SearchPage:
    """Class that creates the search's various HTML tables."""

    def __init__(self, data, hostname=None):
        """Initialize the class.

        Args:
            search: Search dictionary
            hostname: The name of the Device

        Returns:
            None

        """
        # Process YAML file for host
        self._table = SearchTable(data)
        self._hostname = hostname

    def html(self):
        """Create the ports table for the search.

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
            if bool(self._hostname) is True:
                html = layouts.table_wrapper(self._hostname, html, strip=False)
        else:
            html = ""

        # Return
        return html
