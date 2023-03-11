"""Test module for db."""

from __future__ import print_function
import random
import socket
import struct
import ipaddress

# PIP3 imports
from sqlalchemy.orm import Session

# Application imports
from switchmap.server.db import models
from switchmap.server.db import ENGINE

from switchmap.server.db.table import vlanport
from switchmap.server.db.table import vlan
from switchmap.server.db.table import macport
from switchmap.server.db.table import zone
from switchmap.server.db.table import oui
from switchmap.server.db.table import mac
from switchmap.server.db.table import ip
from switchmap.server.db.table import macip
from switchmap.server.db.table import event
from switchmap.server.db.table import device
from switchmap.server.db.table import ipport
from switchmap.server.db.table import root
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
from switchmap.server.db.table import IRoot
from switchmap.server.db.table import IIp
from switchmap.server.db.table import IIpPort

from switchmap.server.configuration import ConfigServer
from switchmap.core import log

from . import data

TEST_MAXIMUM = 20


class Database:
    """Database class."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Make sure we are doing operations only on a test database
        expected = "switchmap_unittest"
        config = ConfigServer()
        if config.db_name() != expected:
            log_message = """\
The database under test must be named {}""".format(
                expected
            )
            log.log2die(1174, log_message)

    def drop(self):
        """Drop database.

        Args:
            None

        Returns:
            None

        """
        # Drop all the tables
        with ENGINE.connect() as connection:
            with Session(bind=connection) as session:
                models.BASE.metadata.drop_all(session.get_bind())

    def create(self):
        """Create database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key values
        models.create_all_tables()


def populate():
    """Create prerequisite rows.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    macips_ = []
    ips = []
    ip_versions = [4, 6]
    maximum = TEST_MAXIMUM
    _ouis = list(set([data.mac()[:6] for _ in range(maximum * 10)]))[:maximum]

    # MACs that match the inserted OUIs
    _macs = ["{0}{1}".format(_, data.mac()[:6]) for _ in _ouis]

    # Insert the necessary rows
    zone_name = data.random_string()
    device_name = data.random_string()

    for _ in list(range(2)):
        # Create Event records
        row = event.create()

        # Create Root record
        root.insert_row(
            IRoot(
                idx_event=row.idx_event, name=data.random_string(), enabled=1
            )
        )

    # Create Zone record
    zone.insert_row(
        IZone(
            idx_event=row.idx_event,
            name=zone_name,
            notes=data.random_string(),
            enabled=1,
        )
    )
    zone_row = zone.exists(row.idx_event, zone_name)

    # Create Device record
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

    # Create VLAN records
    vlans = [
        IVlan(
            idx_device=device_row.idx_device,
            vlan=(idx + 1) * 1000,
            name=data.random_string(),
            state=1,
            enabled=1,
        )
        for idx in range(maximum)
    ]
    vlan.insert_row(vlans)

    # Insert OUIs
    oui.insert_row(
        [
            IOui(
                oui=_,
                organization="ORG_{0}".format(data.random_string()),
                enabled=1,
            )
            for _ in _ouis
        ]
    )

    # Insert MACs
    mac.insert_row(
        [
            IMac(
                idx_oui=key + 1,
                idx_zone=zone_row.idx_zone,
                mac=data.mac(),
                enabled=1,
            )
            for key, value in enumerate(_macs)
        ]
    )

    # # Insert MacIp entries
    # for key, _ in enumerate(_macs):
    #     ip_version = ip_versions[random.randint(0, 1)]
    #     if ip_version == 4:
    #         ip_ = socket.inet_ntoa(
    #             struct.pack(">I", random.randint(1, 0xFFFFFFFE))
    #         )
    #     else:
    #         ip_ = ipaddress.ip_address(
    #             ":".join(("%x" % random.randint(0, 16**4) for i in range(8)))
    #         ).exploded
    #     macips_.append(
    #         IMacIp(
    #             idx_device=device_row.idx_device,
    #             idx_mac=key + 1,
    #             ip_=ip_,
    #             version=ip_version,
    #             hostname="hostname_{}".format(data.random_string()),
    #             enabled=1,
    #         )
    #     )
    # macip.insert_row(macips_)

    # Insert Ip entries
    for key, _ in enumerate(_macs):
        ip_version = ip_versions[random.randint(0, 1)]
        if ip_version == 4:
            ip_address = socket.inet_ntoa(
                struct.pack(">I", random.randint(1, 0xFFFFFFFE))
            )
        else:
            ip_address = ipaddress.ip_address(
                ":".join(("%x" % random.randint(0, 16**4) for i in range(8)))
            ).exploded
        ips.append(
            IIp(
                idx_zone=zone_row.idx_zone,
                address=ip_address,
                version=ip_version,
                hostname="hostname_{}".format(data.random_string()),
                enabled=1,
            )
        )
    ip.insert_row(ips)

    # Insert MacIp entries
    for key, _ in enumerate(_macs):
        macips_.append(
            IMacIp(
                idx_ip=key + 1,
                idx_mac=key + 1,
                enabled=1,
            )
        )
    macip.insert_row(macips_)

    # Insert interfaces
    l1interface.insert_row(
        [
            IL1Interface(
                idx_device=device_row.idx_device,
                ifindex=random.randint(0, 1000000),
                duplex=random.randint(0, 1000000),
                ethernet=1,
                nativevlan=random.randint(0, 1000000),
                trunk=0,
                iftype=random.randint(0, 1000000),
                ifspeed=random.randint(0, 1000000),
                ifalias="IfAlias_{}".format(data.random_string()),
                ifname="IfName_{}".format(data.random_string()),
                ifdescr="IfDescr_{}".format(data.random_string()),
                ifadminstatus=random.randint(0, 1000000),
                ifoperstatus=random.randint(0, 1000000),
                ts_idle=random.randint(0, 1000000),
                cdpcachedeviceid="cdpcachedeviceid_{}".format(
                    data.random_string()
                ),
                cdpcachedeviceport="cdpcachedeviceport_{}".format(
                    data.random_string()
                ),
                cdpcacheplatform="cdpcacheplatform_{}".format(
                    data.random_string()
                ),
                lldpremportdesc="lldpremportdesc_{}".format(
                    data.random_string()
                ),
                lldpremsyscapenabled="lldpremsyscapenabled_{}".format(
                    data.random_string()
                ),
                lldpremsysdesc="lldpremsysdesc_{}".format(
                    data.random_string()
                ),
                lldpremsysname="lldpremsysname_{}".format(
                    data.random_string()
                ),
                enabled=1,
            )
            for _ in range(maximum)
        ]
    )

    # Insert VlanPort entries. Assign a random VLAN to each interface
    vlanports = [
        IVlanPort(
            idx_l1interface=key + 1,
            idx_vlan=random.randint(1, maximum),
            enabled=1,
        )
        for key in range(maximum)
    ]
    vlanport.insert_row(vlanports)

    # Insert MacPort entries. Assign a random mac to each interface
    macports_ = [
        IMacPort(
            idx_l1interface=key + 1,
            idx_mac=random.randint(1, maximum),
            enabled=1,
        )
        for key in range(maximum)
    ]
    macport.insert_row(macports_)

    # Insert IpPort entries. Assign a random IP to each interface
    ipports_ = [
        IIpPort(
            idx_l1interface=key + 1,
            idx_ip=random.randint(1, maximum),
            enabled=1,
        )
        for key in range(maximum)
    ]
    ipport.insert_row(ipports_)
