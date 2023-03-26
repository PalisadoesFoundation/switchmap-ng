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
from switchmap.dashboard import MacIpState


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
                MacState(mac="00005e00010a", organization=None),
                MacState(mac="000573a00001", organization=None),
                MacState(mac="00163e000044", organization=None),
                MacState(mac="001c27160b04", organization=None),
                MacState(mac="001c27160b05", organization=None),
                MacState(mac="001c27160b08", organization=None),
                MacState(mac="001c27160b0e", organization=None),
                MacState(mac="001c27160e95", organization=None),
                MacState(mac="001c27160e98", organization=None),
                MacState(mac="001c27160e9d", organization=None),
                MacState(mac="001c2716ef15", organization=None),
                MacState(mac="001c2716ef16", organization=None),
                MacState(mac="001c2716ef1d", organization=None),
                MacState(mac="001c2716ef1f", organization=None),
                MacState(mac="001f9edf1a69", organization=None),
                MacState(mac="001f9edf1a7f", organization=None),
                MacState(mac="06b7ed05f507", organization=None),
                MacState(mac="086ac586f0f1", organization=None),
                MacState(mac="0e46e6ad05f3", organization=None),
                MacState(mac="18568073d78c", organization=None),
                MacState(mac="1c9957d78bba", organization=None),
                MacState(mac="26833e4f5e4c", organization=None),
                MacState(mac="38f9d3b082df", organization=None),
                MacState(mac="3e462a54f1b2", organization=None),
                MacState(mac="42c843ad3c77", organization=None),
                MacState(mac="468b65c22b2c", organization=None),
                MacState(mac="48701e3c6535", organization=None),
                MacState(mac="50579cdf0547", organization=None),
                MacState(mac="5a07e5c1fceb", organization=None),
                MacState(mac="5ce91e86b8fa", organization=None),
                MacState(mac="64167f05640c", organization=None),
                MacState(mac="6e7a47aeecc9", organization=None),
                MacState(mac="6e8ec145dcdc", organization=None),
                MacState(mac="74867ae400a2", organization=None),
                MacState(mac="8843e18db83f", organization=None),
                MacState(mac="88665a155204", organization=None),
                MacState(mac="8c8590bca7b0", organization=None),
                MacState(mac="8e5f1069b02e", organization=None),
                MacState(mac="8ead3d4403b8", organization=None),
                MacState(mac="a07817acfc95", organization=None),
                MacState(mac="a2a1e55b4e31", organization=None),
                MacState(mac="a483e7d1aaf9", organization=None),
                MacState(mac="aabb538be783", organization=None),
                MacState(mac="aacd36263b62", organization=None),
                MacState(mac="accc8e09db51", organization=None),
                MacState(mac="accc8e09db52", organization=None),
                MacState(mac="accc8e09db53", organization=None),
                MacState(mac="accc8e09db54", organization=None),
                MacState(mac="accc8e0a18b7", organization=None),
                MacState(mac="accc8e0a18b8", organization=None),
                MacState(mac="accc8e0a18b9", organization=None),
                MacState(mac="accc8e0a18ba", organization=None),
                MacState(mac="accc8efe904c", organization=None),
                MacState(mac="ae724c975cda", organization=None),
                MacState(mac="b03cdc0a9484", organization=None),
                MacState(mac="b083fed679aa", organization=None),
                MacState(mac="b46bfc6c4c65", organization=None),
                MacState(mac="b634a2f041d5", organization=None),
                MacState(mac="b8a44f03f1ba", organization=None),
                MacState(mac="b8a44f03f1e6", organization=None),
                MacState(mac="b8a44f03f201", organization=None),
                MacState(mac="b8a44f0856f6", organization=None),
                MacState(mac="b8a44f143d9a", organization=None),
                MacState(mac="b8a44f15af9f", organization=None),
                MacState(mac="b8a44f16f19e", organization=None),
                MacState(mac="baa350428471", organization=None),
                MacState(mac="bc305bf57ac4", organization=None),
                MacState(mac="c61a2b13c3f9", organization=None),
                MacState(mac="c69ba2fdf973", organization=None),
                MacState(mac="c6acee1745ef", organization=None),
                MacState(mac="c6eae3fd2417", organization=None),
                MacState(mac="c8e26556778c", organization=None),
                MacState(mac="c8f3197192e9", organization=None),
                MacState(mac="ccf9e497f45a", organization=None),
                MacState(mac="d05099dca4ff", organization=None),
                MacState(mac="e24e6c7ca216", organization=None),
                MacState(mac="e454e8cd1bf1", organization=None),
                MacState(mac="e45f01672013", organization=None),
                MacState(mac="e8eecc33a5d1", organization=None),
                MacState(mac="f02f4b0abba5", organization=None),
                MacState(mac="f84d89913c00", organization=None),
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

    def test_macips(self):
        """Testing function macips."""
        # Initialize key varialbes
        expecteds = [
            [
                MacIpState(
                    mac="00005e00010a",
                    organization=None,
                    hostnames=[""],
                    addresses=["192.168.0.129"],
                ),
                MacIpState(
                    mac="000573a00001",
                    organization=None,
                    hostnames=["", ""],
                    addresses=[
                        "A025:80FA:0000:0900:0000:0000:0000:0003",
                        "fe80:0000:0000:0000:0005:73ff:fea0:0001",
                    ],
                ),
                MacIpState(
                    mac="00163e000044",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c27160b04",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c27160b05",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c27160b08",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c27160b0e",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c27160e95",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c27160e98",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c27160e9d",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c2716ef15",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c2716ef16",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c2716ef1d",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001c2716ef1f",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001f9edf1a69",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="001f9edf1a7f",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="06b7ed05f507",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="086ac586f0f1",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="0e46e6ad05f3",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="18568073d78c",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="1c9957d78bba",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="26833e4f5e4c",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="38f9d3b082df",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="3e462a54f1b2",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="42c843ad3c77",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="468b65c22b2c",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="48701e3c6535",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="50579cdf0547",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="5a07e5c1fceb",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="5ce91e86b8fa",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="64167f05640c",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="6e7a47aeecc9",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="6e8ec145dcdc",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="74867ae400a2",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="8843e18db83f",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="88665a155204",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="8c8590bca7b0",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="8e5f1069b02e",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="8ead3d4403b8",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="a07817acfc95",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="a2a1e55b4e31",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="a483e7d1aaf9",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="aabb538be783",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="aacd36263b62",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8e09db51",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8e09db52",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8e09db53",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8e09db54",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8e0a18b7",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8e0a18b8",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8e0a18b9",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8e0a18ba",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="accc8efe904c",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="ae724c975cda",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b03cdc0a9484",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b083fed679aa",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b46bfc6c4c65",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b634a2f041d5",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b8a44f03f1ba",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b8a44f03f1e6",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b8a44f03f201",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b8a44f0856f6",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b8a44f143d9a",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b8a44f15af9f",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="b8a44f16f19e",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="baa350428471",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="bc305bf57ac4",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="c61a2b13c3f9",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="c69ba2fdf973",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="c6acee1745ef",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="c6eae3fd2417",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="c8e26556778c",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="c8f3197192e9",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="ccf9e497f45a",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="d05099dca4ff",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="e24e6c7ca216",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="e454e8cd1bf1",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="e45f01672013",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="e8eecc33a5d1",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="f02f4b0abba5",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
                MacIpState(
                    mac="f84d89913c00",
                    organization=None,
                    hostnames=[],
                    addresses=[],
                ),
            ],
        ]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Mac(interface)
            result = tester.macips()
            self.assertEqual(result, expecteds[key])


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
