"""Class for creating device web pages."""

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap.dashboard.data.interface import Interface


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


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


def table(_interfaces):
    """Get Interface data from the device

    Args:
        _interfaces: Interface dict

    Returns:
        table: InterfaceTable object

    """
    # Initialize key variables
    rows = []
    table = None

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

    # Populate the table
    if bool(rows) is True:
        table = InterfaceTable(rows)

    # Return
    return table
