"""switchmap.Search class.

Description:

    This files has classes that process searches for:
        1) IP and MAC address
        2) Port names
        3) Hostnames

"""
from collections import namedtuple

# PIP imports
from sqlalchemy import select, and_

# Switchmap-NG imports
from switchmap import Found
from switchmap.core import general as _general
from switchmap.server.db.table import mac
from switchmap.server.db.table import zone
from switchmap.server.db.table import device
from switchmap.server.db.table import root
from switchmap.server.db.table import macport
from switchmap.server.db.table import ip
from switchmap.server.db.table import l1interface
from switchmap.server.db.models import L1Interface
from switchmap.server.db.models import Device
from switchmap.server.db.models import Zone
from switchmap.server.db.models import Ip
from switchmap.server.db.models import IpPort
from switchmap.server.db.misc import rows as _rows
from switchmap.server.db import db


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
            for idx_zone in self._search.idx_zones:
                exists = ip.findip(idx_zone, ip_.address)
                if bool(exists) is True:
                    founds.extend(exists)

            # Search for IP on interfaces
            for found in founds:
                items = find_ip_interface(found.idx_ip)
                for item in items:
                    result.append(Found(idx_l1interface=item.idx_l1interface))

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

        # Find search phrase
        for idx_zone in self._search.idx_zones:
            exists = ip.findhostname(idx_zone, self._search.string)
            if bool(exists) is True:
                founds.extend(exists)

        # Search for IP on interfaces
        for found in founds:
            items = find_ip_interface(found.idx_ip)
            for item in items:
                result.append(Found(idx_l1interface=item.idx_l1interface))

        # Return
        return result


def find_ip_interface(idx_ip):
    """Find all ports on which an specfic IP address has been found.

    Args:
        idx_ip: Ip.idx_ip

    Returns:
        result: RIpPort tuple

    """
    # Initialize key variables
    result = []
    rows = []

    # Get row from dataase
    statement = select(IpPort).where(
        and_(
            IpPort.idx_ip == idx_ip,
            Ip.idx_ip == IpPort.idx_ip,
            Ip.idx_zone == Zone.idx_zone,
            Device.idx_zone == Zone.idx_zone,
            Device.idx_device == L1Interface.idx_device,
            L1Interface.idx_l1interface == IpPort.idx_l1interface,
        )
    )
    rows = db.db_select_row(1062, statement)

    # Return
    for row in rows:
        result.append(_rows.ipport(row))
    return result


def search(idx_root, searchstring):
    """Search based on idx_root values.

    Args:
        idx_root: Root index
        searchstring: search string to look for

    Returns:
        result

    """
    # Initialize key variables
    result = []

    # Search
    found = root.idx_exists(idx_root)
    if bool(found):
        _search = Search(found.idx_event, searchstring)
        result = _search.find()

    # Return
    return result
