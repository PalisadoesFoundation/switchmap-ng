"""Class for creating device web pages."""

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap.dashboard.data.interface import Interface
from switchmap.dashboard.data.system import System


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


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
        data = self._data.get("l1interfaces")
        rows = interfaces(data)

        # Populate the table
        if bool(rows) is True:
            table = InterfaceTable(rows)

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
        system = System(self._data)
        rows = system.rows()

        # Populate the table
        if bool(rows) is True:
            table = SystemTable(rows)

            # Get HTML
            html = table.__html__()
        else:
            html = ""

        # Return
        return html


class InterfaceTable(Table):
    """Declaration of the columns in the Ports table."""

    # Initialize class variables
    port = Col("Port")
    vlan = Col("VLAN")
    state = Col("State")
    days_inactive = Col("Days Inactive")
    speed = Col("Speed")
    duplex = Col("Duplex")
    label = Col("Port Label")
    trunk = _RawCol("Trunk")
    cdp = _RawCol("CDP")
    lldp = _RawCol("LLDP")
    mac_address = _RawCol("Mac Address")
    manufacturer = _RawCol("Manufacturer")
    ip_address = _RawCol("IP Address")
    hostname = _RawCol("DNS Name")

    # Define the CSS class to use for the header row
    classes = ["table"]

    def get_tr_attrs(self, item):
        """Apply CSS class attributes to regular table row.

        Args:
            item: Row of data

        Returns:
            class of active stuff

        """
        # Special treatment for rows of enabled ports
        if item.enabled() is True:
            if item.active() is True:
                # Port with link
                return {"class": "success"}
            else:
                # Port without link
                return {"class": "info"}
        else:
            # Disabled port
            return {"class": "warning"}


class InterfaceRow:
    """Declaration of the rows in the Interfaces table."""

    def __init__(self, row):
        """Initialize the class.

        Args:
            row: List of row values
                port: Interface name string
                vlan: VLAN of port string
                state: State of port string
                days_inactive: Number of days the port's inactive string
                speed: Speed of port string
                duplex: Duplex of port string
                label: Label given to the port by the network manager
                trunk: Whether a trunk or not
                cdp: CDP data string
                lldp: LLDP data string
                mac_address: MAC Address
                manufacturer: Name of the manufacturer

        Returns:
            None

        """
        # Initialize key variables
        [
            self.port,
            self.vlan,
            self.state,
            self.days_inactive,
            self.speed,
            self.duplex,
            self.label,
            self.trunk,
            self.cdp,
            self.lldp,
            self.mac_address,
            self.manufacturer,
            self.ip_address,
            self.hostname,
        ] = row

    def active(self):
        """Active ports."""
        return bool(self.state == "Active")

    def enabled(self):
        """Enable ports."""
        return bool(self.state != "Disabled")


class SystemTable(Table):
    """Declaration of the columns in the Systems table."""

    # Initialize class variables
    parameter = Col("Parameter")
    value = _RawCol("Value")

    # Define the CSS class to use for the header row
    thead_classes = ["tblHead"]
    classes = ["table"]


class SystemRow:
    """Declaration of the rows in the Systems table."""

    def __init__(self, row):
        """Initialize the class.

        Args:
            row: SystemDataRow object

        Returns:
            None

        """
        # Initialize key variables
        [row.parameter, row.value] = row


def interfaces(_interfaces):
    """Get Interface data from the device

    Args:
        _interfaces: Interface dict

    Returns:
        rows: list of InterfaceRow objects

    """
    # Initialize key variables
    rows = []

    # Process each interface
    for interface in _interfaces:
        obj = Interface(interface)
        row = obj.row()
        if bool(row) is True:
            rows.append(
                InterfaceRow(
                    [
                        row.port,
                        row.vlan,
                        row.state,
                        row.days_inactive,
                        row.speed,
                        row.duplex,
                        row.label,
                        row.trunk,
                        row.cdp,
                        row.lldp,
                        row.mac_address,
                        row.manufacturer,
                        row.ip_address,
                        row.hostname,
                    ]
                )
            )
    return rows


def systems(system):
    """Get System data from the device

    Args:
        system: System dict

    Returns:
        rows: list of SystemRow objects

    """
    # Initialize key variables
    rows = []

    # Process each system
    obj = System(system)
    systemrows = obj.rows()
    if bool(systemrows) is True:
        for row in rows:
            rows.append(SystemRow([row.parameter, row.value]))
    return rows