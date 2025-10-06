"""Test module for db."""

from __future__ import print_function
import random
from collections import namedtuple

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
from switchmap.server.db.table import ipport
from switchmap.server.db.table import device
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
from switchmap import MacDetail

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
    macresult = {}
    vlanresult = {}
    Result = namedtuple(
        "Result",
        "idx_mac idx_l1interface interfaces devices macs ips idx_event ipports",
    )

    macips_ = []
    r_ips = []
    ip_versions = [4, 6]
    maximum = TEST_MAXIMUM

    # Generate OUIs
    ouis_ = list(set([data.mac()[:6] for _ in range(maximum * 10)]))[:maximum]

    # Organizations that match the OUIs
    orgs_ = ["ORG_{0}".format(data.random_string()) for _ in ouis_]

    # MACs that match the inserted OUIs
    macs_ = ["{0}{1}".format(_, data.mac()[:6]) for _ in ouis_]

    # Insert the necessary rows
    zone_name = data.random_string()
    device_name = data.random_string()

    #########################################################################
    #########################################################################
    #
    # Insert data into the database
    #
    #########################################################################
    #########################################################################

    for _ in list(range(2)):
        # Create Event records
        row = event.create()

        # Create Root record
        root.insert_row(
            IRoot(idx_event=row.idx_event, name=data.random_string(), enabled=1)
        )

    # Create Zone record
    r_zone = IZone(
        idx_event=row.idx_event,
        name=zone_name,
        notes=data.random_string(),
        enabled=1,
    )
    zone.insert_row(r_zone)
    zone_row = zone.exists(row.idx_event, zone_name)

    # Create Device record
    r_devices = [
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
    ]
    device.insert_row(r_devices)
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
    # Loop to make sure we have predictable primary key values
    for item in vlans:
        vlan.insert_row(item)

    # Insert OUIs
    oui.insert_row(
        [
            IOui(
                oui=value,
                organization=orgs_[key],
                enabled=1,
            )
            for key, value in enumerate(ouis_)
        ]
    )

    # Insert MACs
    r_macs = [
        IMac(
            idx_oui=key + 1,
            idx_zone=zone_row.idx_zone,
            mac=value,
            enabled=1,
        )
        for key, value in enumerate(macs_)
    ]
    # Loop to make sure we have predictable primary key values
    for item in r_macs:
        mac.insert_row(item)

    # Insert Ip entries
    for _ in macs_:
        ip_version = ip_versions[random.randint(0, 1)]
        if ip_version == 4:
            ip_address = data.ipv4()
        else:
            ip_address = data.ipv6()
        r_ips.append(
            IIp(
                idx_zone=zone_row.idx_zone,
                address=ip_address,
                version=ip_version,
                hostname="hostname_{}".format(data.random_string()),
                enabled=1,
            )
        )
    # Loop to make sure we have predictable primary key values
    for item in r_ips:
        ip.insert_row(item)

    # Insert MacIp entries
    for key, _ in enumerate(macs_):
        macips_.append(
            IMacIp(
                idx_ip=key + 1,
                idx_mac=key + 1,
                enabled=1,
            )
        )
    # Loop to make sure we have predictable primary key values
    for item in macips_:
        macip.insert_row(item)

    # Insert interfaces
    r_interfaces = [
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
            ifin_ucast_pkts=random.randint(0, 1000000),
            ifout_ucast_pkts=random.randint(0, 1000000),
            ifin_errors=random.randint(0, 1000000),
            ifin_discards=random.randint(0, 1000000),
            ifin_nucast_pkts=random.randint(0, 1000000),
            ifout_nucast_pkts=random.randint(0, 1000000),
            ifout_errors=random.randint(0, 1000000),
            ifout_discards=random.randint(0, 1000000),
            ts_idle=random.randint(0, 1000000),
            cdpcachedeviceid="cdpcachedeviceid_{}".format(data.random_string()),
            cdpcachedeviceport="cdpcachedeviceport_{}".format(
                data.random_string()
            ),
            cdpcacheplatform="cdpcacheplatform_{}".format(data.random_string()),
            lldpremportdesc="lldpremportdesc_{}".format(data.random_string()),
            lldpremsyscapenabled="lldpremsyscapenabled_{}".format(
                data.random_string()
            ),
            lldpremsysdesc="lldpremsysdesc_{}".format(data.random_string()),
            lldpremsysname="lldpremsysname_{}".format(data.random_string()),
            enabled=1,
            ifin_octets=random.randint(0, 10**12),
            ifout_octets=random.randint(0, 10**12),
        )
        for _ in range(maximum)
    ]
    # Loop to make sure we have predictable primary key values
    for item in r_interfaces:
        l1interface.insert_row(item)

    # Insert VlanPort entries. Assign a random VLAN to each interface
    vlanports = [
        IVlanPort(
            idx_l1interface=key + 1,
            idx_vlan=random.randint(1, maximum),
            enabled=1,
        )
        for key in range(maximum)
    ]
    # Loop to make sure we have predictable primary key values
    for item in vlanports:
        vlanport.insert_row(item)

    # Insert MacPort entries. Assign a random mac to each interface
    macports_ = [
        IMacPort(
            idx_l1interface=key + 1,
            idx_mac=random.randint(1, maximum),
            enabled=1,
        )
        for key in range(maximum)
    ]
    # Loop to make sure we have predictable primary key values
    for item in macports_:
        macport.insert_row(item)

    # Insert IpPort entries. Assign a random IP to each interface
    r_ipports = [
        IIpPort(
            idx_l1interface=key + 1,
            idx_ip=random.randint(1, maximum),
            enabled=1,
        )
        for key in range(maximum)
    ]
    # Loop to make sure we have predictable primary key values
    for item in r_ipports:
        ipport.insert_row(item)

    #########################################################################
    #########################################################################
    #
    # Prepare data to retun
    #
    #########################################################################
    #########################################################################

    # Track Vlan assignments
    for _, value in enumerate(vlanports):
        idx_l1interface = value.idx_l1interface
        idx_vlan = value.idx_vlan
        found = vlanresult.get(idx_l1interface)
        if bool(found) is True:
            vlanresult[idx_l1interface].append(idx_vlan)
        else:
            vlanresult[idx_l1interface] = [idx_vlan]

    # Iterate through the mac ports
    for macport_ in macports_:
        # Iterate through the MAC / IP relationships
        for key, item in enumerate(macips_):
            # Find a MAC with an assigned IP
            if item.idx_mac == macport_.idx_mac:
                detail = MacDetail(
                    hostname=r_ips[item.idx_ip - 1].hostname,
                    ip_=r_ips[item.idx_ip - 1].address,
                    idx_mac=item.idx_mac,
                    organization=orgs_[item.idx_ip - 1],
                    idx_l1interface=macport_.idx_l1interface,
                    mac=macs_[item.idx_mac - 1],
                )

                # Update the list of idx_mac entries
                found = macresult.get(detail.idx_mac)
                if bool(found) is True:
                    macresult[detail.idx_mac].append(detail)
                else:
                    macresult[detail.idx_mac] = [detail]

    # Return
    result = Result(
        idx_mac=macresult,
        idx_l1interface=vlanresult,
        interfaces=r_interfaces,
        devices=r_devices,
        macs=r_macs,
        ips=r_ips,
        idx_event=r_zone.idx_event,
        ipports=r_ipports,
    )
    return result
