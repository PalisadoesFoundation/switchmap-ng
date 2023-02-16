"""Test module for db."""

from __future__ import print_function
import random

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

from switchmap.server.configuration import ConfigServer
from switchmap.core import log

from . import data


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
    maximum = 20
    _ouis = list(set([data.mac()[:6] for _ in range(maximum * 10)]))[:maximum]

    # MACs that match the inserted OUIs
    _macs = ["{0}{1}".format(_, data.mac()[:6]) for _ in _ouis]

    # Insert the necessary rows
    event_name = data.random_string()
    zone_name = data.random_string()
    device_name = data.random_string()

    # Create Event record
    event.insert_row(IEvent(name=event_name, enabled=1))
    row = event.exists(event_name)

    # Create Zone record
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
    device_row = device.exists(device_name)

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
            for _ in enumerate(_ouis)
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
                ifalias="IfAlias_{}".format(data.random_string()),
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
            for _ in range(MAXMAC)
        ]
    )

    # Insert VlanPort entries
    vlanports = [
        IVlanPort(idx_l1interface=value, idx_vlan=key + 1, enabled=1)
        for key, value in enumerate(RANDOM_INDEX)
    ]
    vlanport.insert_row(vlanports)

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
