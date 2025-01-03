#!/usr/bin/env python3
"""Test the topology module."""

import os
import sys
import unittest
from copy import deepcopy

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
from switchmap.server.db.ingest.update import zone as testimport
from switchmap.server.db.table import zone
from switchmap.server.db.table import oui
from switchmap.server.db.table import event
from switchmap.server.db import models
from switchmap.server.db.table import IMac
from switchmap.server.db.table import IIp
from switchmap.server.db.table import IZone
from switchmap.server.db.table import IOui
from switchmap.server import PairMacIp

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


class TestZoneTopology(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    idx_zone = 1
    max_loops = 25

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Reset the database
        _reset_db()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Drop tables
        database = dblib.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test_process(self):
        """Testing function process."""
        pass

    def test_mac(self):
        """Testing function mac."""
        # Initialize key variables
        result = []
        expected = [
            IMac(idx_oui=1, idx_zone=1, mac="000000000000", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="00005e000102", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="00005e000104", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="00005e000107", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="00005e00010a", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="00005e00010f", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0001f08f357e", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="000299153a92", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="000299154506", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="00029915de6c", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="000299176b0a", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="00029917b8fc", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="00029917ebd3", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991b1402", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991bb7a3", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991bbb8a", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c00e8", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c0220", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c0dcf", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c0e00", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c0e31", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c0e37", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c0e4e", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c0e53", enabled=1),
            IMac(idx_oui=1, idx_zone=1, mac="0002991c0e5a", enabled=1),
        ]

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Test transaction
        tester = testimport.Topology(data, self.idx_zone)
        result = tester.mac()
        result.sort(key=lambda x: (x.mac))
        self.assertEqual(result[: self.max_loops], expected)

    def test_ip(self):
        """Testing function ip."""
        # Initialize key variables
        result = []
        expected = [
            IIp(
                idx_zone=1,
                address="192.168.0.1",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.129",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.134",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.135",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.136",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.137",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.138",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.139",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.140",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.141",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.142",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.143",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.144",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.145",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.146",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.147",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.148",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.149",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.150",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.151",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.152",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.153",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.154",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.155",
                version=4,
                hostname=None,
                enabled=1,
            ),
            IIp(
                idx_zone=1,
                address="192.168.0.156",
                version=4,
                hostname=None,
                enabled=1,
            ),
        ]

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Test transaction
        tester = testimport.Topology(data, self.idx_zone, dns=False)
        tester.mac()
        result = tester.ip()
        result.sort(key=lambda x: (x.address))
        self.assertEqual(result[: self.max_loops], expected)

    def test_macip(self):
        """Testing function macip."""
        # Initialize key variables
        result = []
        expected = [
            PairMacIp(
                mac="000000000000", ip="192.168.0.1", ip_version=4, idx_zone=1
            ),
            PairMacIp(
                mac="00005e00010a",
                ip="192.168.0.129",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="00225538543f",
                ip="192.168.0.134",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="8843e109447f",
                ip="192.168.0.135",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="00229074f33f",
                ip="192.168.0.136",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="f0f755482dc1",
                ip="192.168.0.137",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="f0f7554cd839",
                ip="192.168.0.138",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="001e14334a41",
                ip="192.168.0.139",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="003a7d025eb9",
                ip="192.168.0.140",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="00e0860c1f71",
                ip="192.168.0.141",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="00e0860c1fbf",
                ip="192.168.0.142",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="e8b748e87839",
                ip="192.168.0.143",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="e8b748dd0e39",
                ip="192.168.0.144",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="0081c4fe6b39",
                ip="192.168.0.145",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="f872eaa4e039",
                ip="192.168.0.146",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="f80bcba4ae40",
                ip="192.168.0.147",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="58f39ca2b940",
                ip="192.168.0.148",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="acf2c5b1b440",
                ip="192.168.0.149",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="64f69dacd640",
                ip="192.168.0.150",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="6400f1b7ba39",
                ip="192.168.0.151",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="6c2056898db9",
                ip="192.168.0.152",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="881dfce82252",
                ip="192.168.0.153",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="1cdea768cdd2",
                ip="192.168.0.154",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="5057a8f8bd39",
                ip="192.168.0.155",
                ip_version=4,
                idx_zone=1,
            ),
            PairMacIp(
                mac="5475d0a0f4b9",
                ip="192.168.0.156",
                ip_version=4,
                idx_zone=1,
            ),
        ]

        # Process the device
        _device = device.Device(_polled_data())
        data = _device.process()

        # Test transaction
        tester = testimport.Topology(data, self.idx_zone, dns=False)
        tester.mac()
        tester.ip()
        result = tester.macip()

        result.sort(key=lambda x: (x.ip, x.mac))
        self.assertEqual(result[: self.max_loops], expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
