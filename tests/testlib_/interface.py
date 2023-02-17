"""Create prerequisites for DB interface testing."""

import random
from collections import namedtuple


from switchmap.server.db.table import vlanport
from switchmap.server.db.table import vlan
from switchmap.server.db.table import macport
from switchmap.server.db.table import zone
from switchmap.server.db.table import oui
from switchmap.server.db.table import mac
from switchmap.server.db.table import macip
from switchmap.server.db.table import event
from switchmap.server.db.table import device
from switchmap.server.db.table import l1interface
from switchmap.server.db.table import IMacPort
from switchmap.server.db.table import IVlanPort
from switchmap.server.db.table import IVlan
from switchmap.server.db.table import IMac
from switchmap.server.db.table import IZone
from switchmap.server.db.table import IOui
from switchmap.server.db.table import IDevice
from switchmap.server.db.table import IL1Interface
from switchmap.server.db.table import IMacIp
from switchmap.server.db.table import IEvent
from switchmap import MacDetail

from tests.testlib_ import data


MAXMAC = 100
OUIS = list(set([data.mac()[:6] for _ in range(MAXMAC * 10)]))[:MAXMAC]
MACS = ["{0}{1}".format(_, data.mac()[:6]) for _ in OUIS]
HOSTNAMES = list(set([data.random_string() for _ in range(MAXMAC * 2)]))[
    :MAXMAC
]
IFALIASES = ["ALIAS_{0}".format(data.random_string()) for _ in range(MAXMAC)]
ORGANIZATIONS = ["ORG_{0}".format(data.random_string()) for _ in range(MAXMAC)]
IPADDRESSES = list(set([data.ip_() for _ in range(MAXMAC * 2)]))[:MAXMAC]
IDX_MACS = [random.randint(1, MAXMAC) for _ in range(MAXMAC)]
RANDOM_INDEX = [random.randint(1, MAXMAC) for _ in range(MAXMAC)]


def prerequisites():
    """Create prerequisite rows.

    Args:
        None

    Returns:
        result: dict {idx_mac: [List of MacDetail objects]}

    """
    # Initialize key variables
    macresult = {}
    vlanresult = {}
    Result = namedtuple("Result", "idx_mac idx_l1interface")

    # Insert the necessary rows
    event_name = data.random_string()
    zone_name = data.random_string()
    device_name = data.random_string()
    event.insert_row(IEvent(name=event_name, enabled=1))
    row = event.exists(event_name)
    zone.insert_row(
        IZone(
            idx_event=row.idx_event,
            name=zone_name,
            company_name=data.random_string(),
            address_0=data.random_string(),
            address_1=data.random_string(),
            address_2=data.random_string(),
            city=data.random_string(),
            state=data.random_string(),
            country=data.random_string(),
            postal_code=data.random_string(),
            phone=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
    )
    zone_row = zone.exists(zone_name)

    oui.insert_row(
        [
            IOui(oui=OUIS[key], organization=value, enabled=1)
            for key, value in enumerate(ORGANIZATIONS)
        ]
    )
    mac.insert_row(
        [
            IMac(
                idx_oui=key + 1,
                idx_zone=zone_row.idx_zone,
                mac=value,
                enabled=1,
            )
            for key, value in enumerate(MACS)
        ]
    )
    device.insert_row(
        IDevice(
            idx_zone=zone_row.idx_zone,
            sys_name=data.random_string(),
            hostname=device_name,
            name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=random.randint(0, 1000000),
            last_polled=random.randint(0, 1000000),
            enabled=1,
        )
    )
    device_row = device.exists(zone_row.idx_zone, device_name)

    # Insert VLANs
    vlans = [
        IVlan(
            idx_device=device_row.idx_device,
            vlan=idx + 1,
            name=data.random_string(),
            state=1,
            enabled=1,
        )
        for idx in range(MAXMAC)
    ]
    vlan.insert_row(vlans)

    # Insert interfaces
    l1interface.insert_row(
        [
            IL1Interface(
                idx_device=device_row.idx_device,
                ifindex=random.randint(0, 1000000),
                duplex=random.randint(0, 1000000),
                ethernet=1,
                nativevlan=random.randint(0, 1000000),
                trunk=1,
                ifspeed=random.randint(0, 1000000),
                ifalias=value,
                ifdescr=data.random_string(),
                ifadminstatus=random.randint(0, 1000000),
                ifoperstatus=random.randint(0, 1000000),
                ts_idle=random.randint(0, 1000000),
                cdpcachedeviceid=data.random_string(),
                cdpcachedeviceport=data.random_string(),
                cdpcacheplatform=data.random_string(),
                lldpremportdesc=data.random_string(),
                lldpremsyscapenabled=data.random_string(),
                lldpremsysdesc=data.random_string(),
                lldpremsysname=data.random_string(),
                enabled=1,
            )
            for _, value in enumerate(IFALIASES)
        ]
    )

    # Insert VlanPort entries
    vlanports = [
        IVlanPort(idx_l1interface=value, idx_vlan=key + 1, enabled=1)
        for key, value in enumerate(RANDOM_INDEX)
    ]
    vlanport.insert_row(vlanports)

    # Track Vlan assignments
    for _, value in enumerate(vlanports):
        idx_l1interface = value.idx_l1interface
        idx_vlan = value.idx_vlan
        found = vlanresult.get(idx_l1interface)
        if bool(found) is True:
            vlanresult[idx_l1interface].append(idx_vlan)
        else:
            vlanresult[idx_l1interface] = [idx_vlan]

    # Insert MacPort entries
    macports_ = [
        IMacPort(idx_l1interface=value, idx_mac=key + 1, enabled=1)
        for key, value in enumerate(RANDOM_INDEX)
    ]
    macport.insert_row(macports_)

    # Insert MacIp entries
    macips_ = [
        IMacIp(
            idx_device=1,
            idx_mac=value,
            ip_=IPADDRESSES[key].address,
            version=IPADDRESSES[key].version,
            hostname=HOSTNAMES[key],
            enabled=1,
        )
        for key, value in enumerate(IDX_MACS)
    ]
    macip.insert_row(macips_)

    # Track MacIP assignments
    for key, item in enumerate(macips_):
        detail = MacDetail(
            hostname=item.hostname,
            ip_=item.ip_,
            idx_mac=item.idx_mac,
            organization=ORGANIZATIONS[item.idx_mac - 1],
            idx_l1interface=RANDOM_INDEX[item.idx_mac - 1],
            mac=MACS[item.idx_mac - 1],
        )

        found = macresult.get(detail.idx_mac)
        if bool(found) is True:
            macresult[item.idx_mac].append(detail)
        else:
            macresult[item.idx_mac] = [detail]

    # Return
    result = Result(idx_mac=macresult, idx_l1interface=vlanresult)
    return result
