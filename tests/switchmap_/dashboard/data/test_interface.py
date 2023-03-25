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

from switchmap.dashboard.data import interface as testimport
from switchmap.dashboard import InterfaceDataRow
from switchmap.dashboard import InterfaceState
from switchmap.dashboard import VlanState


def interfaces():
    """Get interface data.

    Args:
        None

    Returns:
        results: dict

    """
    # Initialize key variable
    results = []
    ifnames = ["Gi1/0/48"]

    # Get the dashboard data
    device = data.dashboard_data()

    # Get the required interface data
    interfaces = device.get("l1interfaces")
    for interface in interfaces:
        if interface.get("ifname") in ifnames:
            results.append(interface)
    return results


class TestInterface(unittest.TestCase):
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

    def test_row(self):
        """Testing function row."""
        # Initialize key variables
        expecteds = [
            InterfaceDataRow(
                port="Gi1/0/48",
                vlan="1-8, 13-15, 17-24, 29-31, 33-40, 45-47, 49-56, 61-63, "
                "65-72, 77-79 and more. Total 1404.",
                state="Active",
                days_inactive="None",
                speed="1G",
                duplex="Full",
                label="Link to dbrt02.example.org  Gig 1/45",
                trunk=True,
                cdp="<p>dbrt02.example.org</p><p>cisco WS-C4948</p>"
                "<p>GigabitEthernet1/41</p>",
                lldp="<p>dbrt02.example.org</p><p>GigabitEthernet1/41"
                "</p><p>Cisco IOS Software, Catalyst 4500 L3 Switch "
                "Software (cat4500-ENTSERVICESK9-M), Version 12.2(54)SG1, "
                "RELEASE SOFTWARE (fc1) Technical Support: "
                "http://www.cisco.com/techsupport Copyright (c) 1986-2011 by "
                "Cisco Systems, Inc. Compiled Thu 27-Jan-11 11:39 by</p>",
                mac_address="",
                organization="",
                ip_address="",
                hostname="",
            ),
        ]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Interface(interface)
            result = tester.row()
            self.assertEqual(result, expecteds[key])

    def test_cdp(self):
        """Testing function cdp."""
        # Initialize key variables
        expecteds = [
            "<p>dbrt02.example.org</p><p>cisco "
            "WS-C4948</p><p>GigabitEthernet1/41</p>",
        ]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Interface(interface)
            result = tester.cdp()
            self.assertEqual(result, expecteds[key])

    def test_duplex(self):
        """Testing function duplex."""
        # Initialize key variables

        expecteds = [
            "Full",
        ]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Interface(interface)
            result = tester.duplex()
            self.assertEqual(result, expecteds[key])

    def test_lldp(self):
        """Testing function lldp."""
        # Initialize key variables
        expecteds = [
            "<p>dbrt02.example.org</p><p>GigabitEthernet1/41</p><p>Cisco "
            "IOS Software, Catalyst 4500 L3 Switch Software "
            "(cat4500-ENTSERVICESK9-M), Version 12.2(54)SG1, RELEASE SOFTWARE "
            "(fc1) Technical Support: http://www.cisco.com/techsupport "
            "Copyright (c) 1986-2011 by Cisco Systems, Inc. Compiled "
            "Thu 27-Jan-11 11:39 by</p>",
        ]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Interface(interface)
            result = tester.lldp()
            self.assertEqual(result, expecteds[key])

    def test_speed(self):
        """Testing function speed."""
        # Initialize key variables
        expecteds = ["1G"]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Interface(interface)
            result = tester.speed()
            self.assertEqual(result, expecteds[key])

    def test_state(self):
        """Testing function state."""
        # Initialize key variables
        expecteds = [InterfaceState(up=True, string="Active")]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Interface(interface)
            result = tester.state()
            self.assertEqual(result, expecteds[key])

    def test_vlan(self):
        """Testing function vlan."""
        # Initialize key variables
        expecteds = [
            VlanState(
                group=[
                    (1, 8),
                    (13, 15),
                    (17, 24),
                    (29, 31),
                    (33, 40),
                    (45, 47),
                    (49, 56),
                    (61, 63),
                    (65, 72),
                    (77, 79),
                ],
                string="1-8, 13-15, 17-24, 29-31, 33-40, 45-47, 49-56, "
                "61-63, 65-72, 77-79 and more. Total 1404.",
                count=1404,
            ),
        ]

        # Process
        for key, interface in enumerate(self.interfaces_):
            tester = testimport.Interface(interface)
            result = tester.vlan()
            self.assertEqual(result, expecteds[key])


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
