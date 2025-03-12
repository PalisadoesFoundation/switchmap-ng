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
_EXPECTED = (
    "{0}switchmap-ng{0}tests{0}switchmap_{0}"
    "dashboard{0}net{0}html{0}pages".format(os.sep)
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

from switchmap.dashboard.net.html.pages import device as testimport


def device_data():
    """Get device data and filter the number of interfaces we use.

    Args:
        None

    Returns:
        device_: dict

    """
    # Initialize key variable
    ifnames = ["Gi1/0/1"]
    new_interfaces = []

    # Get the dashboard data
    device_ = data.dashboard_data()

    # Get the required interface data
    interfaces = device_.get("l1interfaces")
    for interface in interfaces:
        if interface.get("ifname") in ifnames:
            new_interfaces.append(interface)

    # Trim Interfaces
    device_["l1interfaces"] = new_interfaces

    return device_


class Test_RawCol(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

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

    def test_td_format(self):
        """Testing function td_format."""
        pass


class TestDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    device = testimport.Device(device_data())

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

    def test_hostname(self):
        """Testing function hostname."""
        # Initialize key variables
        expected = "device-01.example.org"
        result = self.device.hostname()
        self.assertEqual(result, expected)

    def test_interfaces(self):
        """Testing function interfaces."""
        # Initialize key variables
        expected = """<table class="table">
<thead><tr><th>Port</th><th>VLAN</th><th>State</th><th>Days Inactive</th><th>\
Speed</th><th>Duplex</th><th>Port Label</th><th>Trunk</th><th>CDP</th><th>LLDP\
</th><th>Mac Address</th><th>Manufacturer</th><th>IP Address</th><th>DNS Name\
</th></tr></thead>
<tbody>
<tr class="success"><td>Gi1/0/1</td><td>21</td><td>Active</td><td></td><td>1G\
</td><td>Full</td><td>Alias F12</td><td>False</td><td></td><td></td>\
<td>d05099dad28b</td><td></td><td><p></p></td><td><p></p></td></tr>
</tbody>
</table>"""
        result = self.device.interfaces()
        self.assertEqual(result, expected)

    def test_system(self):
        """Testing function system."""
        # Initialize key variables
        expected = """<table class="table">
<thead class="tblHead"><tr><th>Parameter</th><th>Value</th></tr></thead>
<tbody>
<tr><td>System Name</td><td>device-01.example.org</td></tr>
<tr><td>System Hostname</td><td>device-01.example.org</td></tr>
<tr><td>System Description</td><td>Cisco IOS Software, C3750E Software \
(C3750E-UNIVERSALK9-M), Version<br>15.0(2)SE11, RELEASE SOFTWARE (fc3) \
Technical Support:<br>http://www.cisco.com/techsupport Copyright (c) \
1986-2017 by Cisco<br>Systems, Inc. Compiled Sat 19-Aug-17 08:39 by \
prod_rel_team</td></tr>
<tr><td>System sysObjectID</td><td>.1.3.6.1.4.1.9.1.516</td></tr>
<tr><td>System Uptime</td><td>94 Days, 18:39:06</td></tr>
<tr><td>Time Last Polled</td><td>2023-02-23 00:13:37</td></tr>
</tbody>
</table>"""
        result = self.device.system()

        # Split the lines, ignore the time last polled as it can be
        # different based on the timezone of the test
        rlines = result.splitlines()
        elines = expected.splitlines()
        for row, content in enumerate(rlines):
            if "Polled" in content:
                continue
            self.assertEqual(content, elines[row])


class TestInterfaceTable(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

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

    def test_get_tr_attrs(self):
        """Testing function get_tr_attrs."""
        pass


class TestInterfaceRow(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

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

    def test_active(self):
        """Testing function active."""
        pass

    def test_enabled(self):
        """Testing function enabled."""
        pass


class TestSystemRow(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

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


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
