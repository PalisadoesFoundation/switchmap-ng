"""Module for getting interface specific mac data."""
# PIP3 imports
from sqlalchemy import select, and_

# Switchmap-NG imports
from switchmap import MacDetail
from switchmap.server.db.table import macport

from switchmap.server.db import db
from switchmap.server.db.models import Mac as _Mac
from switchmap.server.db.models import Oui as _Oui
from switchmap.server.db.models import MacPort as _MacPort
from switchmap.server.db.models import MacIp as _MacIp
from switchmap.server.db.models import Ip as _Ip
from switchmap.server.db.models import L1Interface as _L1Interface


def by_idx_mac(idx_mac):
    """Search for MAC addresses.

    Args:
        idx_mac: idx_mac

    Returns:
        result: List of MacDetail objects

    """
    # Initialize key variables
    macdetails = []
    result = []

    # Get MacPort data
    _macports = macport.find_idx_mac(idx_mac)

    if bool(_macports) is True:
        # Though we may have found more than one mac, we only need one
        # to get the OUI information
        statement = select(_Oui.organization, _Mac.mac).where(
            _Oui.idx_oui == _Mac.idx_oui, _Mac.idx_mac == _macports[0].idx_mac
        )
        rows = db.db_select(1198, statement)
        for row in rows:
            organization = row.organization.decode()
            mac = row.mac.decode()
            break

        # Get MacIp and MacPort information
        for _macport in _macports:
            macdetails.append(
                MacDetail(
                    hostname=None,
                    ip_=None,
                    organization=organization,
                    idx_l1interface=_macport.idx_l1interface,
                    idx_mac=_macport.idx_mac,
                    mac=mac,
                )
            )

        # Get the updated MacDetails for the interface
        for item in macdetails:
            # Though we may have found more than one mac, we only need one
            # to get the OUI information
            statement = select(_Ip.hostname, _Ip.address).where(
                and_(
                    _Ip.idx_ip == _MacIp.idx_ip,
                    _MacIp.idx_mac == item.idx_mac,
                    _MacPort.idx_mac == _MacIp.idx_ip,
                    _L1Interface.idx_l1interface == _MacPort.idx_l1interface,
                )
            )
            ipdetails = db.db_select(1202, statement)
            for row in ipdetails:
                hostname = row.hostname.decode() if row.hostname else ""
                ipaddress = row.address.decode() if row.address else ""
                break

            # Details found
            if bool(ipdetails):
                result.append(
                    MacDetail(
                        hostname=hostname,
                        ip_=ipaddress,
                        organization=item.organization,
                        idx_l1interface=item.idx_l1interface,
                        idx_mac=item.idx_mac,
                        mac=item.mac,
                    )
                )
            else:
                result.append(item)

    # Return
    return result
