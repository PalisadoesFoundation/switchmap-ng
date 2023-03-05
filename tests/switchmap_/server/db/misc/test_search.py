#!/usr/bin/env python3
"""Test the macport module."""

import os
import sys
import unittest
import random
import time
from collections import namedtuple

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
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}misc""".format(
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


# Create the necessary configuration to load the module
from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.server.db.table import macport
from switchmap.server.db.table import oui
from switchmap.server.db.table import mac
from switchmap.server.db.table import zone
from switchmap.server.db.table import event
from switchmap.server.db.table import macip
from switchmap.server.db.table import l1interface
from switchmap.server.db.table import IMacPort
from switchmap.server.db.table import IMac
from switchmap.server.db.table import IOui
from switchmap.server.db.table import IL1Interface
from switchmap.server.db.table import IMacIp
from switchmap.server.db import models
from switchmap.core import general

from tests.testlib_ import db
from tests.testlib_ import data

from switchmap.server.db.misc import search as testimport

SearchTerms = namedtuple("SearchTerms", "ouis macs ips ifaliases hostnames")

LOOP_MAX = 30


class TestSearch(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting each test."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

        # Drop tables
        database = db.Database()
        database.drop()

        # Create database tables
        models.create_all_tables()

        # Pollinate db with prerequisites
        db.populate()

        # Search specific pollination
        cls.search = search_populate()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps after each tests is completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    # def test___init__(self):
    #     """Testing function __init__."""
    #     pass

    # def test_find(self):
    #     """Testing function find."""
    #     pass

    # def test_macaddress(self):
    #     """Testing function macaddress."""
    #     # Initialize key variables
    #     idx_event = max([_.idx_event for _ in event.events()])
    #     idx_zone = max([_.idx_zone for _ in zone.zones(idx_event)])

    #     # Test
    #     for _mac in self.search.macs[:LOOP_MAX]:
    #         search_ = testimport.Search(idx_event, _mac)
    #         result = search_.macaddress()
    #         self.assertTrue(result)
    #         self.assertEqual(len(result), 1)

    #         # Get the interface of the MAC
    #         exists = mac.findmac(idx_zone, _mac)
    #         self.assertTrue(exists)
    #         self.assertTrue(isinstance(exists, list))
    #         self.assertEqual(len(exists), 1)

    #         # Tie the MAC to a port
    #         _macport = macport.find_idx_mac(exists[0].idx_mac)
    #         self.assertTrue(_macport)
    #         self.assertTrue(isinstance(_macport, list))
    #         self.assertEqual(len(_macport), 1)

    #         # Test
    #         self.assertEqual(
    #             result[0].idx_l1interface, _macport[0].idx_l1interface
    #         )

    # def test_ipaddress(self):
    #     """Testing function ipaddress."""
    #     # Initialize key variables
    #     idx_event = max([_.idx_event for _ in event.events()])
    #     idx_zone = max([_.idx_zone for _ in zone.zones(idx_event)])

    #     # Test
    #     # count = 0
    #     for value in self.search.ips[:LOOP_MAX]:
    #         # count += 1
    #         ip_ = general.ipaddress(value.address)
    #         search_ = testimport.Search(idx_event, ip_.address)
    #         result = search_.ipaddress()
    #         # print(result, count)
    #         self.assertTrue(result)
    #         self.assertEqual(len(result), 1)

    #         # Get the interface of the ipaddress
    #         found = macip.findip(idx_zone, value.address)
    #         self.assertTrue(found)
    #         self.assertEqual(len(found), 1)

    #         expected = macport.find_idx_mac(found[0].idx_mac)
    #         self.assertTrue(expected)
    #         self.assertEqual(len(expected), 1)
    #         self.assertTrue(
    #             result[0].idx_l1interface, expected[0].idx_l1interface
    #         )

    # def test_ifalias(self):
    #     """Testing function ifalias."""
    #     # Initialize key variables
    #     return
    #     idx_event = max([_.idx_event for _ in event.events()])

    #     # Test
    #     for key, value in enumerate(self.search.ifaliases[:LOOP_MAX]):
    #         search_ = testimport.Search(idx_event, value)
    #         result = search_.ifalias()
    #         self.assertTrue(result)
    #         self.assertEqual(len(result), 1)

    #         # Test
    #         self.assertEqual(result[0].idx_l1interface, key + 1)

    # def test_hostname(self):
    #     """Testing function hostname."""
    #     # Initialize key variables
    #     idx_event = max([_.idx_event for _ in event.events()])
    #     idx_zone = max([_.idx_zone for _ in zone.zones(idx_event)])

    #     # Test
    #     count = 1
    #     for value in self.search.hostnames[:LOOP_MAX]:
    #         count += 1
    #         search_ = testimport.Search(idx_event, value)
    #         result = search_.hostname()
    #         print("\n", result, count, value)
    #         self.assertTrue(result)
    #         self.assertEqual(len(result), 1)

    #         # Get the interface of the hostname
    #         found = macip.findhostname(idx_zone, value)
    #         self.assertTrue(found)
    #         self.assertEqual(len(found), 1)

    #         expected = macport.find_idx_mac(found[0].idx_mac)
    #         self.assertTrue(expected)
    #         self.assertEqual(len(expected), 1)
    #         self.assertTrue(
    #             result[0].idx_l1interface, expected[0].idx_l1interface
    #         )


def search_populate():
    """Create prerequisite rows.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    idx_zone = 1
    idx_device = 1
    maximum = 100

    # Search parameters
    ouis = list(set([data.mac()[:6] for _ in range(maximum * 10)]))[:maximum]
    macs = ["{0}{1}".format(_, data.mac()[:6]) for _ in ouis]
    ifaliases = [
        "ALIAS_{0}_{1}".format(int(time.time()), data.random_string())
        for _ in range(maximum)
    ]
    ips = list(set([data.ip_() for _ in range(maximum * 10)]))[:maximum]
    hostnames = list(
        set(
            [
                "HOST_{0}_{1}".format(int(time.time()), data.random_string())
                for _ in range(maximum * 10)
            ]
        )
    )[:maximum]
    random_ifindexes = [random.randint(1, maximum) for _ in range(maximum)]

    # Initialize key variables
    search = SearchTerms(
        ouis=ouis, macs=macs, ifaliases=ifaliases, ips=ips, hostnames=hostnames
    )

    # Insert OUIs
    oui.insert_row(
        [
            IOui(
                oui=_oui,
                organization=data.random_string(),
                enabled=1,
            )
            for _oui in search.ouis
        ]
    )

    # Insert MACs
    for _mac in search.macs:
        _oui = _mac[:6]
        exists = oui.exists(_oui)
        if bool(exists):
            mac.insert_row(
                IMac(
                    idx_oui=exists.idx_oui,
                    idx_zone=idx_zone,
                    mac=_mac,
                    enabled=1,
                )
            )

    # Insert interfaces
    max_ifindex = max([_.ifindex for _ in l1interface.ifindexes(idx_device)])
    l1interface.insert_row(
        [
            IL1Interface(
                idx_device=idx_device,
                ifindex=ifindex + max_ifindex + 1,
                duplex=random.randint(0, 1000000),
                ethernet=1,
                nativevlan=random.randint(0, 1000000),
                trunk=1,
                ifspeed=random.randint(0, 1000000),
                ifalias=ifalias,
                ifdescr=data.random_string(),
                ifname=data.random_string(),
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
            for ifindex, ifalias in enumerate(search.ifaliases)
        ]
    )

    # Insert random MacPorts
    rows = []
    for key, ifindex in enumerate(random_ifindexes):
        rows.append(
            IMacPort(idx_l1interface=ifindex, idx_mac=key + 1, enabled=1)
        )
    macport.insert_row(rows)

    # Insert random MacIPs
    rows = []
    for key, value in enumerate(search.ips):
        rows.append(
            IMacIp(
                idx_device=1,
                idx_mac=key + 1,
                ip_=value.address,
                version=value.version,
                hostname=search.hostnames[key],
                enabled=1,
            )
        )
    macip.insert_row(rows)

    return search


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
