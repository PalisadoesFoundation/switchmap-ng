#!/usr/bin/env python3
"""Test the topology module."""

import os
import sys
import unittest

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(os.path.join(EXEC_DIR, os.pardir)),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}dashboard{0}data".format(
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
from tests.testlib_ import data

CONFIG = setup.config()
CONFIG.save()

from switchmap.dashboard.data import mac as testimport
from switchmap.dashboard import MacState
from switchmap.dashboard import IpState


def interfaces():
    """Get interface data.

    Args:
        None

    Returns:
        results: dict

    """
    # Initialize key variable
    results = []
    ifnames = ["Gi1/0/47"]

    # Get the dashboard data
    device = data.dashboard_data()

    # Get the required interface data
    interfaces = device.get("l1interfaces")
    for interface in interfaces:
        if interface.get("ifname") in ifnames:
            results.append(interface)
    return results


class TestMac(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    interfaces_ = interfaces()

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_macs(self):
        """Testing function macs."""
        # Initialize key varialbes
        expecteds = [
            [
                MacState(mac="00005e00010a", manufacturer=None),
                MacState(mac="000573a00001", manufacturer=None),
                MacState(mac="00163e000044", manufacturer=None),
                MacState(mac="001c27160b04", manufacturer=None),
                MacState(mac="001c27160b05", manufacturer=None),
                MacState(mac="001c27160b08", manufacturer=None),
                MacState(mac="001c27160b0e", manufacturer=None),
                MacState(mac="001c27160e95", manufacturer=None),
                MacState(mac="001c27160e98", manufacturer=None),
                MacState(mac="001c27160e9d", manufacturer=None),
                MacState(mac="001c2716ef15", manufacturer=None),
                MacState(mac="001c2716ef16", manufacturer=None),
                MacState(mac="001c2716ef1d", manufacturer=None),
                MacState(mac="001c2716ef1f", manufacturer=None),
                MacState(mac="001f9edf1a69", manufacturer=None),
                MacState(mac="001f9edf1a7f", manufacturer=None),
                MacState(mac="06b7ed05f507", manufacturer=None),
                MacState(mac="086ac586f0f1", manufacturer=None),
                MacState(mac="0e46e6ad05f3", manufacturer=None),
                MacState(mac="18568073d78c", manufacturer=None),
                MacState(mac="1c9957d78bba", manufacturer=None),
                MacState(mac="26833e4f5e4c", manufacturer=None),
                MacState(mac="38f9d3b082df", manufacturer=None),
                MacState(mac="3e462a54f1b2", manufacturer=None),
                MacState(mac="42c843ad3c77", manufacturer=None),
                MacState(mac="468b65c22b2c", manufacturer=None),
                MacState(mac="48701e3c6535", manufacturer=None),
                MacState(mac="50579cdf0547", manufacturer=None),
                MacState(mac="5a07e5c1fceb", manufacturer=None),
                MacState(mac="5ce91e86b8fa", manufacturer=None),
                MacState(mac="64167f05640c", manufacturer=None),
                MacState(mac="6e7a47aeecc9", manufacturer=None),
                MacState(mac="6e8ec145dcdc", manufacturer=None),
                MacState(mac="74867ae400a2", manufacturer=None),
                MacState(mac="8843e18db83f", manufacturer=None),
                MacState(mac="88665a155204", manufacturer=None),
                MacState(mac="8c8590bca7b0", manufacturer=None),
                MacState(mac="8e5f1069b02e", manufacturer=None),
                MacState(mac="8ead3d4403b8", manufacturer=None),
                MacState(mac="a07817acfc95", manufacturer=None),
                MacState(mac="a2a1e55b4e31", manufacturer=None),
                MacState(mac="a483e7d1aaf9", manufacturer=None),
                MacState(mac="aabb538be783", manufacturer=None),
                MacState(mac="aacd36263b62", manufacturer=None),
                MacState(mac="accc8e09db51", manufacturer=None),
                MacState(mac="accc8e09db52", manufacturer=None),
                MacState(mac="accc8e09db53", manufacturer=None),
                MacState(mac="accc8e09db54", manufacturer=None),
                MacState(mac="accc8e0a18b7", manufacturer=None),
                MacState(mac="accc8e0a18b8", manufacturer=None),
                MacState(mac="accc8e0a18b9", manufacturer=None),
                MacState(mac="accc8e0a18ba", manufacturer=None),
                MacState(mac="accc8efe904c", manufacturer=None),
                MacState(mac="ae724c975cda", manufacturer=None),
                MacState(mac="b03cdc0a9484", manufacturer=None),
                MacState(mac="b083fed679aa", manufacturer=None),
                MacState(mac="b46bfc6c4c65", manufacturer=None),
                MacState(mac="b634a2f041d5", manufacturer=None),
                MacState(mac="b8a44f03f1ba", manufacturer=None),
                MacState(mac="b8a44f03f1e6", manufacturer=None),
                MacState(mac="b8a44f03f201", manufacturer=None),
                MacState(mac="b8a44f0856f6", manufacturer=None),
                MacState(mac="b8a44f143d9a", manufacturer=None),
                MacState(mac="b8a44f15af9f", manufacturer=None),
                MacState(mac="b8a44f16f19e", manufacturer=None),
                MacState(mac="baa350428471", manufacturer=None),
                MacState(mac="bc305bf57ac4", manufacturer=None),
                MacState(mac="c61a2b13c3f9", manufacturer=None),
                MacState(mac="c69ba2fdf973", manufacturer=None),
                MacState(mac="c6acee1745ef", manufacturer=None),
                MacState(mac="c6eae3fd2417", manufacturer=None),
                MacState(mac="c8e26556778c", manufacturer=None),
                MacState(mac="c8f3197192e9", manufacturer=None),
                MacState(mac="ccf9e497f45a", manufacturer=None),
                MacState(mac="d05099dca4ff", manufacturer=None),
                MacState(mac="e24e6c7ca216", manufacturer=None),
                MacState(mac="e454e8cd1bf1", manufacturer=None),
                MacState(mac="e45f01672013", manufacturer=None),
                MacState(mac="e8eecc33a5d1", manufacturer=None),
                MacState(mac="f02f4b0abba5", manufacturer=None),
                MacState(mac="f84d89913c00", manufacturer=None),
            ],
        ]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Mac(interface)
            result = tester.macs()
            self.assertEqual(result, expecteds[key])

    def test_ips(self):
        """Testing function ips."""
        # Initialize key varialbes
        expecteds = [
            [
                IpState(hostname="", address="192.168.0.129"),
                IpState(
                    hostname="",
                    address="A025:80FA:0000:0900:0000:0000:0000:0003",
                ),
                IpState(
                    hostname="",
                    address="fe80:0000:0000:0000:0005:73ff:fea0:0001",
                ),
            ],
        ]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Mac(interface)
            result = tester.ips()
            self.assertEqual(result, expecteds[key])


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
