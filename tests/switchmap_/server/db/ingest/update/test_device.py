#!/usr/bin/env python3
"""Test the topology module."""

import os
import sys
import unittest
from copy import deepcopy
from operator import attrgetter


from sqlalchemy import select

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(
                            os.path.join(
                                os.path.abspath(
                                    os.path.join(
                                        os.path.abspath(
                                            os.path.join(EXEC_DIR, os.pardir)
                                        ),
                                        os.pardir,
                                    )
                                ),
                                os.pardir,
                            )
                        ),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}ingest{0}update""".format(
    os.sep
)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)


# Create the necessary configuration
from tests.testlib_ import setup
from tests.testlib_ import data

CONFIG = setup.config()
CONFIG.save()

from switchmap.poller.update import device
from switchmap.server.db.ingest.update import device as testimport
from switchmap.server.db.ingest.update import zone as zone_update
from switchmap.server.db.ingest import ingest
from switchmap.server.db.table import zone
from switchmap.server.db.table import oui
from switchmap.server.db.table import event
from switchmap.server.db import db
from switchmap.server.db import models
from switchmap.server.db.models import VlanPort
from switchmap.server.db.models import MacPort
from switchmap.server.db.models import Vlan
from switchmap.server.db.models import L1Interface
from switchmap.server.db.models import Device
from switchmap.server.db.table import RMacPort
from switchmap.server.db.table import RVlanPort
from switchmap.server.db.table import RVlan
from switchmap.server.db.table import RL1Interface
from switchmap.server.db.table import RDevice
from switchmap.server.db.table import IZone
from switchmap.server.db.table import IOui

from tests.testlib_ import db as dblib
from tests.testlib_ import data as datalib


def _polled_data():
    """Create prerequisite data.

    Strip out all l1_ keys from the data

    Args:
        None

    Returns:
        result: Stripped data

    """
    # Get data
    result = deepcopy(datalib.polled_data())
    return result


def _reset_db():
    """Reset the database.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    idx_zone = 1

    # Load the configuration in case it's been deleted after loading the
    # configuration above. Sometimes this happens when running
    # `python3 -m unittest discover` where another the tearDownClass of
    # another test module prematurely deletes the configuration required
    # for this module
    config = setup.config()
    config.save()

    # Drop tables
    database = dblib.Database()
    database.drop()

    # Create database tables
    models.create_all_tables()

    # Create a zone
    event_name = data.random_string()
    row = event.create(name=event_name)
    zone.insert_row(
        IZone(
            idx_event=row.idx_event,
            name=data.random_string(),
            notes=data.random_string(),
            enabled=1,
        )
    )

    # Create an OUI entry
    oui.insert_row(IOui(oui="testing", organization="testing", enabled=1))

    # Process the device
    _device = device.Device(_polled_data())
    device_data = _device.process()

    # Update the Zone ARP table
    _zone = zone_update.Topology(device_data, idx_zone)
    ingest.insert_arptable(_zone.process(), test=True)


class TestPollUpdateTopologyFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    idx_zone = 1
    max_loops = 10

    @classmethod
    def setUp(cls):
        """Execute these steps before starting tests."""
        # Reset the database
        _reset_db()

    @classmethod
    def tearDown(cls):
        """Execute these steps when all tests are completed."""
        # Drop tables
        database = dblib.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_process(self):
        """Testing function process."""
        pass

    def test_device(self):
        """Testing function device."""
        # Initialize key variables
        result = []
        expected = [
            RDevice(
                idx_device=1,
                idx_zone=1,
                sys_name="device-08.example.org",
                hostname="device-08.example.org",
                name="device-08.example.org",
                sys_description="a8b19bed-d300-40eb-bafc-b99dedb94414",
                sys_objectid=".1.3.6.1.4.1.9.1.516",
                sys_uptime=300982385,
                last_polled=1656692061,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            )
        ]

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Process all the pre-requisite updates
        testimport.device(self.idx_zone, data)

        # Verify macport data
        statement = select(Device)
        rows = db.db_select_row(1184, statement)

        # Return
        for row in rows:
            result.append(
                RDevice(
                    idx_device=row.idx_device,
                    idx_zone=row.idx_zone,
                    sys_name=(
                        None
                        if bool(row.sys_name) is False
                        else row.sys_name.decode()
                    ),
                    hostname=(
                        None
                        if bool(row.hostname) is False
                        else row.hostname.decode()
                    ),
                    name=(
                        None if bool(row.name) is False else row.name.decode()
                    ),
                    sys_description=(
                        None
                        if bool(row.sys_description) is False
                        else row.sys_description.decode()
                    ),
                    sys_objectid=(
                        None
                        if bool(row.sys_objectid) is False
                        else row.sys_objectid.decode()
                    ),
                    sys_uptime=row.sys_uptime,
                    last_polled=row.last_polled,
                    enabled=row.enabled,
                    ts_created=None,
                    ts_modified=None,
                )
            )
        self.assertEqual(result[: self.max_loops], expected)


class TestPollUpdateTopologyClasses(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    idx_zone = 1
    max_loops = 10

    @classmethod
    def setUp(cls):
        """Execute these steps before starting tests."""
        # Reset the database
        _reset_db()

    @classmethod
    def tearDown(cls):
        """Execute these steps when all tests are completed."""
        # Drop tables
        database = dblib.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_process(self):
        """Testing function process."""
        pass

    def test_l1interface(self):
        """Testing function l1interface."""
        # Initialize key variables
        result = []
        expected = [
            RL1Interface(
                idx_l1interface=1,
                idx_device=1,
                ifindex=1,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="_DISABLED_",
                ifdescr="Vlan1",
                ifname="Vl1",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=2,
                idx_device=1,
                ifindex=4,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN4",
                ifdescr="Vlan4",
                ifname="Vl4",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=3,
                idx_device=1,
                ifindex=10,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN10",
                ifdescr="Vlan10",
                ifname="Vl10",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=4,
                idx_device=1,
                ifindex=11,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN11",
                ifdescr="Vlan11",
                ifname="Vl11",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=5,
                idx_device=1,
                ifindex=12,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN12",
                ifdescr="Vlan12",
                ifname="Vl12",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=6,
                idx_device=1,
                ifindex=13,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN13",
                ifdescr="Vlan13",
                ifname="Vl13",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=7,
                idx_device=1,
                ifindex=14,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN14",
                ifdescr="Vlan14",
                ifname="Vl14",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=8,
                idx_device=1,
                ifindex=15,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN15",
                ifdescr="Vlan15",
                ifname="Vl15",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=9,
                idx_device=1,
                ifindex=16,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN16",
                ifdescr="Vlan16",
                ifname="Vl16",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=10,
                idx_device=1,
                ifindex=17,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN17",
                ifdescr="Vlan17",
                ifname="Vl17",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=11,
                idx_device=1,
                ifindex=18,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN18",
                ifdescr="Vlan18",
                ifname="Vl18",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=12,
                idx_device=1,
                ifindex=19,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN19",
                ifdescr="Vlan19",
                ifname="Vl19",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=13,
                idx_device=1,
                ifindex=20,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN20",
                ifdescr="Vlan20",
                ifname="Vl20",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=14,
                idx_device=1,
                ifindex=21,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN21",
                ifdescr="Vlan21",
                ifname="Vl21",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=15,
                idx_device=1,
                ifindex=24,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN24",
                ifdescr="Vlan24",
                ifname="Vl24",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=16,
                idx_device=1,
                ifindex=30,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN30",
                ifdescr="Vlan30",
                ifname="Vl30",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=17,
                idx_device=1,
                ifindex=31,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="VLAN31",
                ifdescr="Vlan31",
                ifname="Vl31",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=18,
                idx_device=1,
                ifindex=100,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=1000,
                iftype=53,
                ifalias="_MANAGEMENT_VLAN100_ device-08.example.org  ",
                ifdescr="Vlan100",
                ifname="Vl100",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=19,
                idx_device=1,
                ifindex=5001,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=2000,
                iftype=53,
                ifalias="Trunk to device-01.example.org Gi1/0/47 Gi1/0/48",
                ifdescr="Port-channel1",
                ifname="Po1",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=20,
                idx_device=1,
                ifindex=5179,
                duplex=None,
                ethernet=0,
                nativevlan=None,
                trunk=0,
                ifspeed=0,
                iftype=53,
                ifalias="",
                ifdescr="StackPort1",
                ifname="StackPort1",
                ifadminstatus=1,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=21,
                idx_device=1,
                ifindex=10101,
                duplex=2,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=1000,
                iftype=6,
                ifalias="Link to device-15.example.org",
                ifdescr="GigabitEthernet1/0/1",
                ifname="Gi1/0/1",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=22,
                idx_device=1,
                ifindex=10102,
                duplex=2,
                ethernet=1,
                nativevlan=98,
                trunk=1,
                ifspeed=1000,
                iftype=6,
                ifalias="Trunk to device-10.example.org Gi1/0/2",
                ifdescr="GigabitEthernet1/0/2",
                ifname="Gi1/0/2",
                ifadminstatus=1,
                ifoperstatus=1,
                ts_idle=0,
                cdpcachedeviceid="device-10.example.org",
                cdpcachedeviceport="GigabitEthernet1/0/2",
                cdpcacheplatform="cisco WS-C3750X-48",
                lldpremportdesc="Trunk to device-08.example.org Gi1/0/2",
                lldpremsyscapenabled="0010000000000000",
                lldpremsysdesc="a76af21e-9299-4384-af56-283e7f31b585",
                lldpremsysname="device-10.example.org",
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=23,
                idx_device=1,
                ifindex=10103,
                duplex=0,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=10,
                iftype=6,
                ifalias="_DISABLED_",
                ifdescr="GigabitEthernet1/0/3",
                ifname="Gi1/0/3",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=24,
                idx_device=1,
                ifindex=10104,
                duplex=0,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=100,
                iftype=6,
                ifalias="_DISABLED_",
                ifdescr="GigabitEthernet1/0/4",
                ifname="Gi1/0/4",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=25,
                idx_device=1,
                ifindex=10105,
                duplex=0,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=100,
                iftype=6,
                ifalias="_DISABLED_",
                ifdescr="GigabitEthernet1/0/5",
                ifname="Gi1/0/5",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=26,
                idx_device=1,
                ifindex=10106,
                duplex=0,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=100,
                iftype=6,
                ifalias="_DISABLED_",
                ifdescr="GigabitEthernet1/0/6",
                ifname="Gi1/0/6",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=27,
                idx_device=1,
                ifindex=10107,
                duplex=0,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=100,
                iftype=6,
                ifalias="_DISABLED_",
                ifdescr="GigabitEthernet1/0/7",
                ifname="Gi1/0/7",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=28,
                idx_device=1,
                ifindex=10108,
                duplex=0,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=10,
                iftype=6,
                ifalias="_DISABLED_",
                ifdescr="GigabitEthernet1/0/8",
                ifname="Gi1/0/8",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=29,
                idx_device=1,
                ifindex=10109,
                duplex=0,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=100,
                iftype=6,
                ifalias="_DISABLED_",
                ifdescr="GigabitEthernet1/0/9",
                ifname="Gi1/0/9",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RL1Interface(
                idx_l1interface=30,
                idx_device=1,
                ifindex=10110,
                duplex=0,
                ethernet=1,
                nativevlan=1,
                trunk=0,
                ifspeed=100,
                iftype=6,
                ifalias="_DISABLED_",
                ifdescr="GigabitEthernet1/0/10",
                ifname="Gi1/0/10",
                ifadminstatus=2,
                ifoperstatus=2,
                ts_idle=0,
                cdpcachedeviceid=None,
                cdpcachedeviceport=None,
                cdpcacheplatform=None,
                lldpremportdesc=None,
                lldpremsyscapenabled=None,
                lldpremsysdesc=None,
                lldpremsysname=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
        ]

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Make sure the device exists
        exists = testimport.device(self.idx_zone, data)

        # Test transaction
        tester = testimport.Topology(exists, data)
        tester.l1interface(test=True)

        # Verify macport data
        statement = select(L1Interface)
        rows = db.db_select_row(1183, statement)

        # Return
        for row in rows:
            result.append(
                RL1Interface(
                    idx_l1interface=row.idx_l1interface,
                    idx_device=row.idx_device,
                    ifindex=row.ifindex,
                    duplex=row.duplex,
                    ethernet=row.ethernet,
                    nativevlan=row.nativevlan,
                    trunk=row.trunk,
                    ifspeed=row.ifspeed,
                    iftype=row.iftype,
                    ifalias=(
                        None if row.ifalias is None else row.ifalias.decode()
                    ),
                    ifname=(
                        None if row.ifname is None else row.ifname.decode()
                    ),
                    ifdescr=(
                        None if row.ifdescr is None else row.ifdescr.decode()
                    ),
                    ifadminstatus=row.ifadminstatus,
                    ifoperstatus=row.ifoperstatus,
                    # We have to set this to zero as it is calculated using
                    # time.time() and inserted into the database
                    ts_idle=0,
                    cdpcachedeviceid=(
                        None
                        if row.cdpcachedeviceid is None
                        else row.cdpcachedeviceid.decode()
                    ),
                    cdpcachedeviceport=(
                        None
                        if row.cdpcachedeviceport is None
                        else row.cdpcachedeviceport.decode()
                    ),
                    cdpcacheplatform=(
                        None
                        if row.cdpcacheplatform is None
                        else row.cdpcacheplatform.decode()
                    ),
                    lldpremportdesc=(
                        None
                        if row.lldpremportdesc is None
                        else row.lldpremportdesc.decode()
                    ),
                    lldpremsyscapenabled=(
                        None
                        if row.lldpremsyscapenabled is None
                        else row.lldpremsyscapenabled.decode()
                    ),
                    lldpremsysdesc=(
                        None
                        if row.lldpremsysdesc is None
                        else row.lldpremsysdesc.decode()
                    ),
                    lldpremsysname=(
                        None
                        if row.lldpremsysname is None
                        else row.lldpremsysname.decode()
                    ),
                    enabled=row.enabled,
                    ts_created=None,
                    ts_modified=None,
                )
            )
        results = sorted(result, key=attrgetter("ifindex"))

        # Test
        for key, result in enumerate(results[: self.max_loops * 3]):
            self.assertEqual(result, expected[key])

    def test_vlan(self):
        """Testing function vlan."""
        # Initialize key variables
        result = []
        expected = [
            RVlan(
                idx_vlan=1,
                idx_device=1,
                vlan=0,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=2,
                idx_device=1,
                vlan=1,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=3,
                idx_device=1,
                vlan=2,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=4,
                idx_device=1,
                vlan=3,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=5,
                idx_device=1,
                vlan=4,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=6,
                idx_device=1,
                vlan=5,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=7,
                idx_device=1,
                vlan=6,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=8,
                idx_device=1,
                vlan=7,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=9,
                idx_device=1,
                vlan=8,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlan(
                idx_vlan=10,
                idx_device=1,
                vlan=13,
                name=None,
                state=None,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
        ]

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Make sure the device exists
        exists = testimport.device(self.idx_zone, data)

        # Test transaction
        tester = testimport.Topology(exists, data)
        tester.l1interface(test=True)
        tester.vlan(test=True)

        # Verify macport data
        statement = select(Vlan)
        rows = db.db_select_row(1182, statement)

        # Return
        for row in rows:
            result.append(
                RVlan(
                    idx_vlan=row.idx_vlan,
                    idx_device=row.idx_device,
                    vlan=row.vlan,
                    name=row.name if row.name is None else row.name.decode(),
                    state=row.state,
                    enabled=row.enabled,
                    ts_created=None,
                    ts_modified=None,
                )
            )

        # Sort by idx_vlan, idx_device and vlan
        result.sort(key=lambda x: (x.vlan, x.name, x.idx_device))
        self.assertEqual(result[: self.max_loops], expected)

    def test_vlanport(self):
        """Testing function vlanport."""
        # Initialize key variables
        result = []
        expected = [
            RVlanPort(
                idx_vlanport=1,
                idx_l1interface=22,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=2,
                idx_l1interface=43,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=3,
                idx_l1interface=44,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=4,
                idx_l1interface=45,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=5,
                idx_l1interface=47,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=6,
                idx_l1interface=48,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=7,
                idx_l1interface=49,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=8,
                idx_l1interface=65,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=9,
                idx_l1interface=67,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RVlanPort(
                idx_vlanport=10,
                idx_l1interface=68,
                idx_vlan=1,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
        ]

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Make sure the device exists
        exists = testimport.device(self.idx_zone, data)

        # Test transaction
        tester = testimport.Topology(exists, data)
        tester.l1interface(test=True)
        tester.vlan(test=True)
        tester.vlanport(test=True)

        # Verify vlanport data
        statement = select(VlanPort)
        rows = db.db_select_row(1196, statement)

        # Return
        for row in rows:
            result.append(
                RVlanPort(
                    idx_vlanport=row.idx_vlanport,
                    idx_l1interface=row.idx_l1interface,
                    idx_vlan=row.idx_vlan,
                    enabled=row.enabled,
                    ts_created=None,
                    ts_modified=None,
                )
            )

        # Sort by idx_vlanport
        result.sort(key=lambda x: (x.idx_vlanport))
        self.assertEqual(result[: self.max_loops], expected)

    def test_macport(self):
        """Testing function macport."""
        # Initialize key variables
        result = []
        expected = [
            RMacPort(
                idx_macport=1,
                idx_l1interface=21,
                idx_mac=2,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=2,
                idx_l1interface=21,
                idx_mac=3,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=3,
                idx_l1interface=65,
                idx_mac=62,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=4,
                idx_l1interface=43,
                idx_mac=64,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=5,
                idx_l1interface=44,
                idx_mac=65,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=6,
                idx_l1interface=44,
                idx_mac=66,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=7,
                idx_l1interface=48,
                idx_mac=67,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=8,
                idx_l1interface=49,
                idx_mac=68,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=9,
                idx_l1interface=49,
                idx_mac=69,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
            RMacPort(
                idx_macport=10,
                idx_l1interface=48,
                idx_mac=70,
                enabled=1,
                ts_modified=None,
                ts_created=None,
            ),
        ]

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Make sure the device exists
        exists = testimport.device(self.idx_zone, data)

        # Test transaction
        tester = testimport.Topology(exists, data)
        tester.l1interface(test=True)
        tester.vlan(test=True)
        tester.vlanport(test=True)
        tester.macport(test=True)

        # Verify macport data
        statement = select(MacPort)
        rows = db.db_select_row(1176, statement)

        # Return
        for row in rows:
            result.append(
                RMacPort(
                    idx_macport=row.idx_macport,
                    idx_l1interface=row.idx_l1interface,
                    idx_mac=row.idx_mac,
                    enabled=row.enabled,
                    ts_created=None,
                    ts_modified=None,
                )
            )
        # Sort by idx_vlanport
        result.sort(key=lambda x: (x.idx_macport))
        self.assertEqual(result[: self.max_loops], expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
