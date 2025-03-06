"""Module for parsing Mac address related data from GraphQL JSON."""

from switchmap.dashboard import MacState
from switchmap.dashboard import IpState
from switchmap.dashboard import MacIpState


class Mac:
    """Class to create an InterfaceDataRow data."""

    def __init__(self, interface):
        """Instantiate the class.

        Args:
            interface: Interface dict

        Returns:
            None

        """
        # Initialize key variables
        self._macports = interface.get("macports")
        self._valid = False not in [
            bool(self._macports),
            isinstance(self._macports, list),
        ]

    def macs(self):
        """Get MacState of the interface.

        Args:
            None

        Returns:
            result: List of MacState objects

        """
        # Initialize key variables
        result = []

        # Process
        if bool(self._valid) is True:
            for _macport in self._macports:
                for _, data in sorted(_macport.items()):
                    macstate = _mac_state(data)
                    if bool(macstate) is True:
                        result.append(macstate)
        # Return
        return result

    def ips(self):
        """Get the IpState of the interface.

        Args:
            None

        Returns:
            result: List of IpState objects

        """
        # Initialize key variables
        result = []

        # Process
        if bool(self._valid) is True:
            for _macport in self._macports:
                for _, data in sorted(_macport.items()):
                    ipstate = _ip_state(data)
                    if bool(ipstate) is True:
                        result.extend(ipstate)
        # Return
        return result

    def macips(self):
        """Get the MacIpState of the interface.

        Args:
            None

        Returns:
            result: List of MacIpState objects

        """
        # Initialize key variables
        result = []

        # Process
        if bool(self._valid) is True:
            for _macport in self._macports:
                for _, data in sorted(_macport.items()):
                    # Initialize loop variables
                    hostnames = []
                    addresses = []

                    # Get the interface state
                    macstate = _mac_state(data)
                    ipstate = _ip_state(data)

                    # Process
                    for item in ipstate:
                        hostnames.append(item.hostname)
                        addresses.append(item.address)

                    result.append(
                        MacIpState(
                            mac=macstate.mac,
                            organization=macstate.organization,
                            hostnames=hostnames,
                            addresses=addresses,
                        )
                    )
        # Return
        return result


def _mac_state(data):
    """Return MacState.

    Args:
        data: Dict of device data to process

    Returns:
        result: MacState object

    """
    # Initialize key variables
    result = None

    mac = data.get("mac")
    organization = None
    if bool(mac) is True:
        oui = data.get("oui")
        if bool(oui) is True:
            organization = oui.get("organization")
            result = MacState(mac=mac, organization=organization)

    return result


def _ip_state(data):
    """Return port ips.

    Args:
        data: Dict of data being processed

    Returns:
        result: List of IpState objects

    """
    # Initialize key variables
    result = []

    # Process
    macips = data.get("macips")
    if bool(macips) is True:
        for item in macips:
            ips = item.get("ips")
            if bool(ips) is True:
                result.append(
                    IpState(
                        address=ips.get("address"),
                        hostname=ips.get("hostname"),
                    )
                )
    # Return
    return result


def macips(interface):
    """Get the MacIpState of the interface.

    Args:
        interface: IDX of the interface in the DB

    Returns:
        result: List of MacIpState objects

    """
    # Initialize key variables
    interface_ = Mac(interface)
    result = interface_.macips()
    return result
