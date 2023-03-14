"""Module for parsing interface data from GraphQL JSON."""

# Import switchmap.libraries
from switchmap.core import general
from switchmap.dashboard import InterfaceState
from switchmap.dashboard import VlanState
from switchmap.dashboard import InterfaceDataRow
from switchmap.dashboard.data import mac


class Interface:
    """Class to create an InterfaceDataRow data."""

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
        ethernet = self._interface.get("iftype")

        # Process the data
        if ethernet == 6:
            # Get Vlan Data
            vlan = self.vlan()

            # Define other prerequisites
            trunk = bool(vlan.count > 1)

            # Get the mac to IP address mapping
            if bool(trunk):
                macips = None

            else:
                tester = mac.macips(self._interface)
                macips = tester[0] if bool(tester) else None

            result = InterfaceDataRow(
                port=self._interface.get("ifname", "N/A"),
                vlan=vlan.string,
                state=self.state().string,
                days_inactive="None",
                speed=self.speed(),
                duplex=self.duplex(),
                label=self._interface.get("ifalias", "N/A"),
                trunk=trunk,
                cdp=self.cdp(),
                lldp=self.lldp(),
                mac_address=macips.mac if bool(macips) else "",
                manufacturer=macips.manufacturer if bool(macips) else "",
                ip_address="<p>{}</p>".format("</p><p>".join(macips.addresses))
                if bool(macips)
                else "",
                hostname="<p>{}</p>".format("</p><p>".join(macips.hostnames))
                if bool(macips)
                else "",
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
