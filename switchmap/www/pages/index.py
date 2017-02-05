#!usr/bin/env python3
"""Class for creating home web pages."""

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap.constants import SITE_PREFIX


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


class HomePage(object):
    """Class that creates the homepages's various HTML tables."""

    def __init__(self, hostnames):
        """Initialize the class.

        Args:
            host: Hostname to process

        Returns:
            None

        """
        # Initialize key variables
        self.hostnames = hostnames

    def data(self):
        """Create data table for the devices.

        Args:
            None

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        data = Device(self.hostnames).data()

        # Populate the table
        table = DeviceTable(data)

        # Get HTML
        html = table.__html__()

        # Return
        return html


class DeviceTable(Table):
    """Declaration of the columns in the Devices table."""

    # Initialize class variables
    col0 = _RawCol('')
    col1 = _RawCol('')
    col2 = _RawCol('')
    col3 = _RawCol('')

    # Define the CSS class to use for the header row
    classes = ['table']


class DeviceRow(object):
    """Declaration of the rows in the Devices table."""

    def __init__(self, row_data):
        """Method initializing the class.

        Args:
            row_data: Row data

        Returns:
            None

        """
        # Initialize key variables
        self.col0 = row_data[0]
        self.col1 = row_data[1]
        self.col2 = row_data[2]
        self.col3 = row_data[3]


class Device(object):
    """Class that creates the data to be presented for the devices."""

    def __init__(self, hostnames):
        """Method instantiating the class.

        Args:
            hostnames: A list of hostnames

        Returns:
            None

        """
        # Initialize key variables
        self.hostnames = hostnames

    def data(self):
        """Return data for the device's system information.

        Args:
            None

        Returns:
            rows: List of Col objects

        """
        # Initialize key variables
        rows = []
        links = []
        column = 0
        max_columns = 3

        # Create list of links for table
        for hostname in self.hostnames:
            # Get URL link for device page
            url = '{}/devices/{}'.format(SITE_PREFIX, hostname)
            link = '<a href="{}">{}</a>'.format(url, hostname)
            links.append(link)

        # Add links to table rows
        row_data = [''] * (max_columns + 1)
        for index, link in enumerate(links):
            row_data[column] = links[index]

            # Create new row when max number of columns reached
            column += 1
            if column > max_columns:
                rows.append(DeviceRow(row_data))
                row_data = [''] * (max_columns + 1)
                column = 0

        # Append a row if max number of columns wasn't reached before
        if column > 0 and column <= max_columns:
            rows.append(DeviceRow(row_data))

        # Return
        return rows
