"""Module for parsing Mac address related data from GraphQL JSON."""

from switchmap.dashboard import MacState
from switchmap.dashboard import IpState


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
        """Return port macs.

        Args:
            None

        Returns:
            result: List of macs

        """
        # Initialize key variables
        result = []

        # Process
        if bool(self._valid) is True:
            for _macport in self._macports:
                for _, value in sorted(_macport.items()):
                    mac = value.get("mac")
                    manufacturer = None
                    if bool(mac) is True:
                        oui = value.get("oui")
                        if bool(oui) is True:
                            manufacturer = oui.get("manufacturer")
                    result.append(MacState(mac=mac, manufacturer=manufacturer))
        # Return
        return result

    def ips(self):
        """Return port ips.

        Args:
            None

        Returns:
            result: List of ips

        """
        # Initialize key variables
        result = []

        # Process
        if bool(self._valid) is True:
            for _macport in self._macports:
                for _, value in sorted(_macport.items()):
                    macips = value.get("macips")
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

    def manufacturers(self):
        """Return port manufacturers.

        Args:
            None

        Returns:
            result: List of manufacturers

        """
        # Initialize key variables
        result = []

        # Process
        # for item in self.macs
        # if bool(self._valid) is True:
        #     for _macport in self._macports:
        #         for _, value in sorted(_macport.items()):
        #             macips = value.get("macips")
        #             if bool(macips) is True:
        #                 for item in macips:
        #                     ips = item.get("ips")
        #                     if bool(ips) is True:
        #                         result.append(
        #                             IpState(
        #                                 address=ips.get("address"),
        #                                 hostname=ips.get("hostname"),
        #                             )
        #                         )
        # Return
        return result
