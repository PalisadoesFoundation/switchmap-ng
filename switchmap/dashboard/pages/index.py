"""Class for creating home web pages."""

# Standard imports
from collections import namedtuple

# PIP3 imports
from flask_table import Table, Col, create_table, NestedTableCol

# Import switchmap.libraries
from switchmap import SITE_PREFIX

DeviceMeta = namedtuple("DeviceMeta", "hostname idx_device")


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


class HomePage:
    """Class that creates the homepages's various HTML tables."""

    def __init__(self, zones):
        """Initialize the class.

        Args:
            host: Hostname to process

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
            html: HTML table string

        """
        # Initialize key variables
        html_list = []

        # Iterate over the zones
        for item in self._zones:
            # Initialize loop variables
            devices = []

            # Create a table for each zone
            zone = item.get("name")
            ZoneTable = create_table("ZoneTable").add_column("zone", Col(zone))
            ZoneTable.objects = NestedTableCol("objects", DeviceTable)

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
            table = DeviceTable(device_rows)

            # Convert the table to HTML, add the HTML to a list
            html_list.append(wrapper(zone, table.__html__()))

        # Return tables
        html = "".join(html_list)
        return html


class ZoneRow:
    """Declaration of the rows in the Zone table."""

    def __init__(self, zone, device_rows):
        """Initialize the class.

        Args:
            zone: Name of zone
            device_rows: List of DeviceRows objects

        Returns:
            None

        """
        # Initialize key variables
        self.zone = zone
        self.device_rows = device_rows


class DeviceTable(Table):
    """Declaration of the columns in the Devices table."""

    # Initialize class variables
    col0 = _RawCol("")
    col1 = _RawCol("")
    col2 = _RawCol("")
    col3 = _RawCol("")

    # Define the CSS class to use for the header row
    classes = ["table"]


class DevicesRow:
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
    column = 0
    max_columns = 3

    # Create list of links for table
    for device in devices:
        # Get URL link for device page
        url = "{}/devices/{}".format(SITE_PREFIX, device.idx_device)
        link = '<a href="{}">{}</a>'.format(url, device.hostname)
        links.append(link)

    # Add links to table rows
    row_data = [""] * (max_columns + 1)
    for index, link in enumerate(links):
        row_data[column] = links[index]

        # Create new row when max number of columns reached
        column += 1
        if column > max_columns:
            _rows.append(DevicesRow(row_data))
            row_data = [""] * (max_columns + 1)
            column = 0

    # Append a row if max number of columns wasn't reached before
    if column > 0 and column <= max_columns:
        _rows.append(DevicesRow(row_data))

    # Return
    return _rows


def wrapper(zone, table):
    """Wrap the data in HTML stuff.

    Args:
        zone: zone
        table: Table HTML

    Returns:
        result: HTML

    """

    result = """
    <div class="row">
      <div class="col-lg-12">
          <div class="panel panel-default">
              <div class="panel-heading">
                  {}
              </div>
              <!-- /.panel-heading -->
              <div class="panel-body">
                  <div class="table-responsive table-bordered">
                      {}
                  </div>
                  <!-- /.table-responsive -->
              </div>
              <!-- /.panel-body -->
          </div>
          <!-- /.panel -->
      </div>
    </div>
""".format(
        zone, table
    )
    result = result.replace(
        "<thead><tr><th></th><th></th><th></th><th></th></tr></thead>", ""
    )
    return result
