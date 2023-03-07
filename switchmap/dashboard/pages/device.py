"""Class for creating device web pages."""

import textwrap
from datetime import datetime
from collections import namedtuple

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap.core import general
from switchmap.dashboard import InterfaceState
from switchmap.dashboard import VlanState


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


class Device(object):
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
            html: HTML table string

        """
        # Initialize key variables
        interfaces = self._data.get("l1interfaces")

        # Populate the table
        if bool(interfaces) is True:
            table = InterfaceTable(interfaces)

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


class InterfaceRow(object):
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


def interfaces(_interfaces):
    """Get Interface data from the device

    Args:
        _interfaces: Interface dict

    Returns:
        results: list of InterfaceRow objects

    """
    # Initialize key variables
    results = []

    # Process each interface
    for interface in _interfaces:
        obj = Interface(interface)
        ntuple = obj.row()
        if bool(ntuple) is True:
            results.append(InterfaceRow(ntuple._asdict()))
    return results


class Interface:
    """Class to create an InterfaceRow."""

    def __init__(self, interface):
        """Instantiate the class.

        Args:
            interface: Interface dict

        Returns:
            None

        """
        # Initialize key variables
        self._interface = interface

    def row(self):
        """Get Row data.

        Args:
            None

        Returns:
            result

        """
        # Initialize key variables
        Row = namedtuple(
            "Row",
            "port vlan state days_inactive speed duplex label "
            "trunk cdp lldp mac_address manufacturer ip_address hostname",
        )

        # Get Vlan Data
        vlan = self.vlan()

        ethernet = self._interface.get("iftype")
        if ethernet == 6:
            result = Row(
                port=self._interface.get("ifname", "N/A"),
                vlan=vlan.string,
                state=self.state().string,
                days_inactive="None",
                speed=self.speed(),
                duplex=self.duplex(),
                label=self._interface.get("ifalias", "N/A"),
                trunk=bool(len(vlan.group) > 1),
                cdp=self.cdp(),
                lldp=self.lldp(),
                mac_address="None",
                manufacturer="None",
                ip_address="None",
                hostname="None",
            )
        else:
            result = None
        return result

    def cdp(self):
        """Return port CDP HTML string.

        Args:
            None

        Returns:
            value: required string

        """
        # Assign key variables
        found = self._interface.get("cdpcachedeviceid")

        # Determine whether CDP is enabled and update string
        if bool(found) is True:
            value = "{}<br>{}<br>{}".format(
                self._interface.get("cdpcachedeviceid", ""),
                self._interface.get("cdpcacheplatform", ""),
                self._interface.get("cdpcachedeviceport", ""),
            )
        else:
            value = ""

        # Return
        return value

    def duplex(self):
        """Return port duplex string.

        Args:
            None

        Returns:
            duplex: Duplex string

        """
        # Assign key variables
        duplex = "Unknown"
        options = {
            0: "Unknown",
            1: "Half",
            2: "Full",
            3: "Half-Auto",
            4: "Full-Auto",
        }

        # Assign duplex
        if bool(self.state().up) is False:
            duplex = "N/A"
        else:
            duplex = options.get(self._interface.get("duplex", 0), 0)

        # Return
        return duplex

    def lldp(self):
        """Return port LLDP HTML string.

        Args:
            None

        Returns:
            value: required string

        """
        # Assign key variables
        port_data = self.port_data
        value = ""

        # Determine whether LLDP is enabled and update string
        if "lldpremsysdesc" in port_data:
            value = "{}<br>{}<br>{}".format(
                port_data["lldpremsysname"],
                port_data["lldpremportdesc"],
                port_data["lldpremsysdesc"],
            )

        # Return
        return value

    def speed(self):
        """Return port speed.

        Args:
            None

        Returns:
            result: Port speed

        """
        # Assign key variables
        result = self._interface.get("speed", 0)

        # Process
        if bool(result) is True:
            result = "{}G".format(int(int(result) / 1000))
        return result

    def state(self):
        """Return InterfaceState object.

        Args:
            None

        Returns:
            state: InterfaceState object

        """
        # Initialize key variables
        enabled = self._interface.get("ifadminstatus", 0) == 1

        # Process
        if bool(enabled) is True:
            _up = self._interface.get("ifoperstatus", 0) == 1
            if bool(_up) is True:
                result = "Active"
            else:
                result = "Inactive"
        else:
            result = "Disabled"

        # Return
        state = InterfaceState(up=bool(_up), string=result)
        return state

    def vlan(self):
        """Return VLAN number.

        Args:
            None

        Returns:
            result: VlanState object

        """
        # Assign key variables
        vlans = []
        group = []
        stringy = ""

        # Get VLANs
        vlan_ports = bool(self._interface.get("vlanports", 0))
        nativevlan = bool(self._interface.get("nativevlan", 0))

        # Process the VLANs
        if bool(vlan_ports) is True:
            for _, value in vlan_ports.items():
                vlan = value.get("vlan")
                if bool(vlan) is True:
                    vlans.append(vlan)

        # Add the native VLAN
        if bool(nativevlan):
            vlans.append(nativevlan)

        # Group VLANs
        group = general.group_consecutive(vlans)
        stringy = ", ".join(
            [
                str(_) if isinstance(_, int) else "{}-{}".format(_[0], _[1])
                for _ in group
            ]
        )

        # Return
        result = VlanState(group=group, string=stringy)
        return result


class SystemTable(Table):
    """Declaration of the columns in the Systems table."""

    # Initialize class variables
    parameter = Col("Parameter")
    value = _RawCol("Value")

    # Define the CSS class to use for the header row
    thead_classes = ["tblHead"]
    classes = ["table"]


class SystemRow(object):
    """Declaration of the rows in the Systems table."""

    def __init__(self, parameter, value):
        """Initialize the class.

        Args:
            parameter: System parameter string
            value: System parameter value string

        Returns:
            None

        """
        # Initialize key variables
        self.parameter = parameter
        self.value = value


class System(object):
    """Class that creates the data to be presented for the device's ports."""

    def __init__(self, system_data):
        """Instantiate the class.

        Args:
            system_data: Dictionary of system data

        Returns:
            None

        """
        # Initialize key variables
        self.system_data = system_data

    def data(self):
        """Return data for the device's system information.

        Args:
            None

        Returns:
            rows: List of Col objects

        """
        # Initialize key variables
        rows = []

        # Configured name
        rows.append(SystemRow("System Name", self.system_data["sysName"]))

        # System IP Address / Hostname
        rows.append(SystemRow("System Hostname", self.system_data["hostname"]))

        # System Description
        rows.append(
            SystemRow(
                "System Description",
                textwrap.fill(self.system_data["sysDescr"]).replace(
                    "\n", "<br>"
                ),
            )
        )

        # System Object ID
        rows.append(
            SystemRow("System sysObjectID", self.system_data["sysObjectID"])
        )

        # System Uptime
        rows.append(
            SystemRow("System Uptime", _uptime(self.system_data["sysUpTime"]))
        )

        # Last time polled
        timestamp = int(self.system_data["timestamp"])
        date_string = datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        rows.append(SystemRow("Time Last Polled", date_string))

        # Return
        return rows


def _port_enabled(port_data):
    """Return whether port is enabled.

    Args:
        port_data: Data related to the port

    Returns:
        active: True if active

    """
    # Initialize key variables
    enabled = False

    # Assign state
    if "ifAdminStatus" in port_data:
        value = port_data["ifAdminStatus"]
        if value == 1:
            enabled = True

    # Return
    return enabled


def _port_up(port_data):
    """Return whether port is up.

    Args:
        port_data: Data related to the port

    Returns:
        port_up: True if active

    """
    # Initialize key variables
    port_up = False

    # Assign state
    if _port_enabled(port_data) is True:
        if "ifOperStatus" in port_data:
            if port_data["ifOperStatus"] == 1:
                port_up = True

    # Return
    return port_up


def _uptime(seconds):
    """Return uptime string.

    Args:
        seconds: Seconds of uptime

    Returns:
        result: Uptime string

    """
    # Initialize key variables
    (minutes, remainder_seconds) = divmod(seconds / 100, 60)
    (hours, remainder_minutes) = divmod(minutes, 60)
    (days, remainder_hours) = divmod(hours, 24)

    # Return
    result = ("%.f Days, %d:%02d:%02d") % (
        days,
        remainder_hours,
        remainder_minutes,
        remainder_seconds,
    )
    return result
