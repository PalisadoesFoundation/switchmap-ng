"""Module for getting interface specific mac data."""
# PIP3 imports
from sqlalchemy import select, and_

# Switchmap-NG imports
from switchmap import MacDetail
from switchmap.db.table import mac
from switchmap.db.table import macport

from switchmap.db import db
from switchmap.db.models import Mac as _Mac
from switchmap.db.models import Oui as _Oui
from switchmap.db.models import MacPort as _MacPort
from switchmap.db.models import MacIp as _MacIp


def by_mac(_mac):
    """Search for MAC addresses.

    Args:
        _mac: MAC address

    Returns:
        result: List of MacDetail objects

    """
    # Initialize key variables
    result = []

    # Get MAC information
    macs = mac.findmac(_mac)

    # Do lookups
    for macmeta in macs:
        details = by_idx_mac(macmeta.idx_mac)
        result.extend(details)

    # Return
    return result


def by_idx_mac(idx_mac):
    """Search for MAC addresses.

    Args:
        idx_mac: idx_mac

    Returns:
        result: List of MacDetail objects

    """
    # Initialize key variables
    mac_rows = []
    macdetails = []
    result = []

    # Get MacPort data
    _macports = macport.find_idx_mac(idx_mac)

    # Get MacIp and MacPort information
    for _macport in _macports:
        statement = select(
            _Oui.organization, _Mac.mac).where(
                and_(
                    _MacPort.idx_l1interface == _macport.idx_l1interface,
                    _MacPort.idx_mac == _macport.idx_mac,
                    _MacPort.idx_mac == _Mac.idx_mac,
                    _Oui.idx_oui == _Mac.idx_oui,
                )
            )
        mac_rows = db.db_select(1198, statement)
        for row in mac_rows:
            macdetails.append(
                MacDetail(
                    hostname=None,
                    ip_=None,
                    organization=row.organization.decode(),
                    idx_l1interface=_macport.idx_l1interface,
                    idx_mac=_macport.idx_mac,
                    mac=row.mac.decode()))

        # Get the updated MacDetails for the interface
        for item in macdetails:
            statement = select(_MacIp).where(
                _MacIp.idx_mac == item.idx_mac)
            detail_rows = db.db_select_row(1202, statement)
            if bool(detail_rows):
                for row in detail_rows:
                    result.append(
                        MacDetail(
                            hostname=row.hostname.decode(),
                            ip_=row.ip_.decode(),
                            organization=item.organization,
                            idx_l1interface=item.idx_l1interface,
                            idx_mac=item.idx_mac,
                            mac=item.mac)
                    )
            else:
                result.append(item)

    # Return
    return result
