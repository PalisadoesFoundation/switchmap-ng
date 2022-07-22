#!/usr/bin/env python3
"""switchmap.Search class.

Description:

    This files has classes that process searches for:
        1) IP and MAC address
        2) Port names
        3) Hostnames

"""
# PIP3 imports
from sqlalchemy import select, and_

# Switchmap-NG imports
from switchmap import Found, MacDetail
from switchmap.core import general as _general
from switchmap.db.table import mac
from switchmap.db.table import oui
from switchmap.db.table import macport
from switchmap.db.table import macip
from switchmap.db.table import l1interface

from switchmap.db import db
from switchmap.db.models import Mac as _Mac
from switchmap.db.models import Oui as _Oui
from switchmap.db.models import MacPort as _MacPort
from switchmap.db.models import MacIp as _MacIp


class Search:
    """Class that manages searches.

    Methods return lists of Found objects for the idx_l1interface table entries
    where there are matches.

    """

    def __init__(self, searchstring):
        """Initialize the class.

        Args:
            searchstring: search string to look for

        Returns:
            None

        """
        # Generate various possible strings that could be used for searches
        self._search = str(searchstring)

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

        # Find the MAC
        _mac = _general.mac(self._search)
        exists = mac.findmac(_mac)

        # Find the interface information
        if bool(exists) is True:
            for exist in exists:
                _macport = macport.find_idx_mac(exist.idx_mac)
                if bool(_macport) is True:
                    for item in _macport:
                        result.append(
                            Found(idx_l1interface=item.idx_l1interface)
                        )

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

        # Find MAC for IP address in ARP table
        ip_ = _general.ipaddress(self._search)
        founds = macip.findip(ip_.address)

        # Search for MAC on interfaces
        for found in founds:
            macports_ = macport.find_idx_mac(found.idx_mac)
            for macport_ in macports_:
                result.append(Found(idx_l1interface=macport_.idx_l1interface))

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
        ifalias = self._search

        # Find Hostname for IP address in ARP table
        founds = l1interface.findifalias(ifalias)

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
        hostname = self._search

        # Find Hostname for IP address in ARP table
        founds = macip.findhostname(hostname)

        # Search for Hostname on interfaces
        for found in founds:
            macports_ = macport.find_idx_mac(found.idx_mac)
            for macport_ in macports_:
                result.append(Found(idx_l1interface=macport_.idx_l1interface))

        # Return
        return result
