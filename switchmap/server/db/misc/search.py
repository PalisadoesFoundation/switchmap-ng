"""switchmap.Search class.

Description:

    This files has classes that process searches for:
        1) IP and MAC address
        2) Port names
        3) Hostnames

"""
from collections import namedtuple

# Switchmap-NG imports
from switchmap import Found
from switchmap.core import general as _general
from switchmap.server.db.table import mac
from switchmap.server.db.table import zone
from switchmap.server.db.table import device
from switchmap.server.db.table import macport
from switchmap.server.db.table import macip
from switchmap.server.db.table import l1interface


# Define useful tuples for search
SearchEvent = namedtuple(
    "SearchEvent", "string idx_event idx_devices idx_zones"
)


class Search:
    """Class that manages searches.

    Methods return lists of Found objects for the idx_l1interface table entries
    where there are matches.

    """

    def __init__(self, idx_event, searchstring):
        """Initialize the class.

        Args:
            idx_event: Event index
            searchstring: search string to look for

        Returns:
            None

        """
        # Generate prerequisite data for doing a search
        idx_devices = []
        idx_zones = [_.idx_zone for _ in zone.zones(idx_event)]
        for idx_zone in idx_zones:
            devices = device.devices(idx_zone)
            idx_devices.extend([_.idx_device for _ in devices])

        # Publish the search metadata
        self._search = SearchEvent(
            idx_event=idx_event,
            idx_devices=idx_devices,
            idx_zones=idx_zones,
            string=str(searchstring),
        )

    def find(self):
        """Find search string.

        Args:
            None

        Returns:
            result: List of Found objects of interfaces that have data matching
                the search string

        """
        # Initialize key variables
        result = []

        # Do each successive search
        result.extend(self.macaddress())
        result.extend(self.ifalias())
        result.extend(self.ipaddress())
        result.extend(self.hostname())

        # Remove duplicates
        result = list(set(result))

        # Return
        return result

    def macaddress(self):
        """Search for macaddress.

        Args:
            None

        Returns:
            result: List of Found objects of interfaces that have data matching
                the search string

        """
        # Initialize key variables
        result = []
        founds = []

        # Find the MAC
        _mac = _general.mac(self._search.string)

        for idx_zone in self._search.idx_zones:
            exists = mac.findmac(idx_zone, _mac)
            if bool(exists) is True:
                founds.extend(exists)

        # Find the interface information
        for found in founds:
            _macport = macport.find_idx_mac(found.idx_mac)
            if bool(_macport) is True:
                for item in _macport:
                    result.append(Found(idx_l1interface=item.idx_l1interface))

        # Return
        return result

    def ipaddress(self):
        """Search for ipaddress.

        Args:
            None

        Returns:
            result: List of Found objects of interfaces that have data matching
                the search string

        """
        # Initialize key variables
        result = []
        founds = []

        # Find MAC for IP address in ARP table
        ip_ = _general.ipaddress(self._search.string)

        if bool(ip_) is True:
            for idx_device in self._search.idx_devices:
                exists = macip.findip(idx_device, ip_.address)
                if bool(exists) is True:
                    founds.extend(exists)

            # Search for MAC on interfaces
            for found in founds:
                macports_ = macport.find_idx_mac(found.idx_mac)
                for macport_ in macports_:
                    result.append(
                        Found(idx_l1interface=macport_.idx_l1interface)
                    )

        # Return
        return result

    def ifalias(self):
        """Search for string in ifalias names.

        Args:
            None

        Returns:
            result: List of Found objects of interfaces that have data matching
                the search string

        """
        # Initialize key variables
        result = []
        founds = []

        # Find Hostname for IP address in ARP table
        for idx_device in self._search.idx_devices:
            found = l1interface.findifalias(idx_device, self._search.string)
            if bool(found) is True:
                founds.extend(found)

        # Search for ifalias on interfaces
        for found in founds:
            result.append(Found(idx_l1interface=found.idx_l1interface))

        # Return
        return result

    def hostname(self):
        """Search for string hostnames.

        Args:
            None

        Returns:
            result: List of Found objects of interfaces that have data matching
                the search string

        """
        # Initialize key variables
        result = []
        founds = []

        # Find Hostname for IP address in ARP table
        for idx_device in self._search.idx_devices:
            found = macip.findhostname(idx_device, self._search.string)
            if bool(found) is True:
                founds.extend(found)

        # Search for Hostname on interfaces
        for found in founds:
            macports_ = macport.find_idx_mac(found.idx_mac)
            for macport_ in macports_:
                result.append(Found(idx_l1interface=macport_.idx_l1interface))

        # Return
        return result
