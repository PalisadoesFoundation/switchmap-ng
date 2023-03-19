"""Class for creating home web pages."""

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap import SITE_PREFIX
from switchmap.dashboard import DeviceMeta
from switchmap.core import general


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


def tables(zones):
    """Create HTML table for the devices.

    Args:
        zones: List of Zones

    Returns:
        results: List of ZoneTable objects

    """
    # Initialize key variables
    results = []

    # Iterate over the zones
    for item in zones:
        # Initialize loop variables
        devices = []

        # Extract the device data to create the table rows.
        for dev_item in item.get("devices"):
            devices.append(
                DeviceMeta(
                    hostname=dev_item.get("hostname"),
                    idx_device=dev_item.get("idxDevice"),
                )
            )
        device_rows = rows(devices)

        # Append the result to create a table object
        results.append(ZoneTable(device_rows))

    # Return tables
    return results


class ZoneTable(Table):
    """Declaration of the columns in the Devices table."""

    # Initialize class variables
    col0 = _RawCol("")
    col1 = _RawCol("")
    col2 = _RawCol("")
    col3 = _RawCol("")
    col4 = _RawCol("")
    col5 = _RawCol("")

    # Define the CSS class to use for the header row
    classes = ["table"]


class ZoneRow:
    """Declaration of the rows in the Devices table."""

    def __init__(self, row_data):
        """Initialize the class.

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
        self.col4 = row_data[4]
        self.col5 = row_data[5]


def rows(devices):
    """Return data for the device's system information.

    Args:
        devices: List of DeviceMeta objects

    Returns:
        rows: List of Col objects

    """
    # Initialize key variables
    _rows = []
    links = []
    width = 6

    # Create list of links for table
    for device in devices:
        # Get URL link for device page
        url = "{}/devices/{}".format(SITE_PREFIX, device.idx_device)
        link = '<a href="{}">{}</a>'.format(url, device.hostname)
        links.append(link)

    # Convert the rows to table rows
    list_of_lists = general.padded_list_of_lists(links, pad="", width=width)
    for item in list_of_lists:
        _rows.append(ZoneRow(item))

    # Return
    return _rows
