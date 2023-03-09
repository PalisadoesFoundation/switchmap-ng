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
        _interfaces = interfaces(data)

        # Populate the table
        if bool(_interfaces) is True:
            table = InterfaceTable(_interfaces)

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
        data = System(self._data).data()

        # Populate the table
        table = SystemTable(data)

        # Get HTML
        html = table.__html__()

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
            rows.append(row)
    return rows


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
            row = Row(
                port=self._interface.get("ifname", "N/A"),
                vlan=vlan.string,
                state=self.state().string,
                days_inactive="None",
                speed=self.speed(),
                duplex=self.duplex(),
                label=self._interface.get("ifalias", "N/A"),
                trunk=bool(vlan.count > 1),
                cdp=self.cdp(),
                lldp=self.lldp(),
                mac_address="None",
                manufacturer="None",
                ip_address="None",
                hostname="None",
            )

            # Convert to the ordered list InterfaceRow expects
            result = InterfaceRow(
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
        found = self._interface.get("lldpremsysdesc")

        # Determine whether CDP is enabled and update string
        if bool(found) is True:
            value = "{}<br>{}<br>{}".format(
                self._interface.get("lldpremsysname", ""),
                self._interface.get("lldpremportdesc", ""),
                self._interface.get("lldpremsysdesc", ""),
            )
        else:
            value = ""

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
        result = self._interface.get("ifspeed", 0) * 1000000

        # Process
        if bool(result) is True:
            result = general.human_readable(result, suffix="", storage=False)
            result = result.replace(".0", "")
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
        _up = False

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
        vlan_ports = self._interface.get("vlanports", 0)
        nativevlan = self._interface.get("nativevlan", 0)

        # Process the VLANs
        if bool(vlan_ports) is True:
            for vlan_port in vlan_ports:
                for _, value in vlan_port.items():
                    vlan = value.get("vlan")
                    if bool(vlan) is True:
                        vlans.append(vlan)

        # Add the native VLAN
        if bool(nativevlan) and len(vlans) > 1:
            vlans.append(nativevlan)

        # Group VLANs
        group = general.group_consecutive(vlans)
        stringy = ", ".join(
            [
                str(_) if isinstance(_, int) else "{}-{}".format(_[0], _[1])
                for _ in group[:10]
            ]
        )
        if len(group) > 10:
            stringy = "{} plus more".format(stringy)

        # Return
        result = VlanState(group=group, string=stringy, count=len(vlans))
        return result


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


class System:
    """Class that creates the data to be presented for the device's ports."""

    def __init__(self, system_data):
        """Instantiate the class.

        Args:
            system_data: Dictionary of system data

        Returns:
            None

        """
        # Initialize key variables
        self._data = system_data

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
        rows.append(SystemRow("System Name", self.sysname()))

        # System IP Address / Hostname
        rows.append(SystemRow("System Hostname", self.hostname()))

        # System Description
        rows.append(
            SystemRow(
                "System Description",
                textwrap.fill(self.sysdescription()).replace("\n", "<br>"),
            )
        )

        # System Object ID
        rows.append(SystemRow("System sysObjectID", self.sysobjectid()))

        # System Uptime
        rows.append(SystemRow("System Uptime", self.sysuptime()))

        # Last time polled
        rows.append(SystemRow("Time Last Polled", self.last_polled()))

        # Return
        return rows

    def hostname(self):
        """Return hostname.

        Args:
            None

        Returns:
            result: hostname

        """
        # Return
        result = self._data.get("hostname", "")
        return result

    def last_polled(self):
        """Return last_polled.

        Args:
            None

        Returns:
            result: last_polled

        """
        # Return
        timestamp = self._data.get("lastPolled", 0)
        result = datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return result

    def sysdescription(self):
        """Return sysdescription.

        Args:
            None

        Returns:
            result: sysdescription

        """
        # Return
        result = self._data.get("sysDescription", "")
        return result

    def sysname(self):
        """Return sysname.

        Args:
            None

        Returns:
            result: sysname

        """
        # Return
        result = self._data.get("sysName", "")
        return result

    def sysobjectid(self):
        """Return sysobjectid.

        Args:
            None

        Returns:
            result: sysobjectid

        """
        # Return
        result = self._data.get("sysObjectid", "")
        return result

    def sysuptime(self):
        """Return sysuptime.

        Args:
            None

        Returns:
            result: sysuptime

        """
        # Return
        seconds = self._data.get("sysUptime", "")

        # Parse the time
        (minutes, remainder_seconds) = divmod(seconds / 100, 60)
        (hours, remainder_minutes) = divmod(minutes, 60)
        (days, remainder_hours) = divmod(hours, 24)

        # Return
        result = "{:,} Days, {:02d}:{:02d}:{:02d}".format(
            int(days),
            int(remainder_hours),
            int(remainder_minutes),
            int(remainder_seconds),
        )
        return result
