#!/usr/bin/env python3
"""Test the jm_general module."""

import socket
import unittest

from switchmap.db import db_host


class TestGetIDX(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_host_good = 1
    good_host = db_host.GetIDX(idx_host_good)

    # Create a dict of all the expected values
    expected = {
        'hostname': socket.getfqdn(),
        'ip_address': None,
        'snmp_enabled': False,
        'description': 'Infoset Server',
        'enabled': True
    }

    def test_init(self):
        """Testing method init."""
        # Test with non existent HostIDX
        with self.assertRaises(SystemExit):
            _ = db_host.GetIDX(-1)

    def test_hostname(self):
        """Testing method hostname."""
        # Testing with known good value
        result = self.good_host.hostname()
        self.assertEqual(result, self.expected['hostname'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.hostname()
        self.assertNotEqual(result, expected)

    def test_description(self):
        """Testing function description."""
        # Testing with known good value
        result = self.good_host.description()
        self.assertEqual(result, self.expected['description'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.description()
        self.assertNotEqual(result, expected)

    def test_enabled(self):
        """Testing function enabled."""
        # Testing with known good value
        result = self.good_host.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.enabled()
        self.assertNotEqual(result, expected)

    def test_ip_address(self):
        """Testing function ip_address."""
        # Testing with known good value
        result = self.good_host.ip_address()
        self.assertEqual(result, self.expected['ip_address'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.ip_address()
        self.assertNotEqual(result, expected)

    def test_snmp_enabled(self):
        """Testing function snmp_enabled."""
        # Testing with known good value
        result = self.good_host.snmp_enabled()
        self.assertEqual(result, self.expected['snmp_enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.snmp_enabled()
        self.assertNotEqual(result, expected)


class TestGetHost(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_host_good = 1
    good_host = db_host.GetHost(socket.getfqdn())

    # Create a dict of all the expected values
    expected = {
        'idx': idx_host_good,
        'ip_address': None,
        'snmp_enabled': False,
        'description': 'Infoset Server',
        'enabled': True
    }

    def test___init__(self):
        """Testing function __init__."""
        # Test with non existent HostIDX
        with self.assertRaises(SystemExit):
            _ = db_host.GetHost('bogus')

        # Test with non existent HostIDX
        with self.assertRaises(SystemExit):
            _ = db_host.GetHost(-1)

    def test_idx(self):
        """Testing method hostname."""
        # Testing with known good value
        result = self.good_host.idx()
        self.assertEqual(result, self.expected['idx'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.hostname()
        self.assertNotEqual(result, expected)

    def test_description(self):
        """Testing function description."""
        # Testing with known good value
        result = self.good_host.description()
        self.assertEqual(result, self.expected['description'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.description()
        self.assertNotEqual(result, expected)

    def test_enabled(self):
        """Testing function enabled."""
        # Testing with known good value
        result = self.good_host.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.enabled()
        self.assertNotEqual(result, expected)

    def test_ip_address(self):
        """Testing function ip_address."""
        # Testing with known good value
        result = self.good_host.ip_address()
        self.assertEqual(result, self.expected['ip_address'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.ip_address()
        self.assertNotEqual(result, expected)

    def test_snmp_enabled(self):
        """Testing function snmp_enabled."""
        # Testing with known good value
        result = self.good_host.snmp_enabled()
        self.assertEqual(result, self.expected['snmp_enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_host.snmp_enabled()
        self.assertNotEqual(result, expected)


class TestOther(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_host_good = 1
    good_host = db_host.GetIDX(idx_host_good)

    def test_all_hosts(self):
        """Testing function all_hosts."""
        pass

    def test_hostname_exists(self):
        """Testing function hostname_exists."""
        pass

    def test_idx_exists(self):
        """Testing function idx_exists."""
        pass

if __name__ == '__main__':

    # Do the unit test
    unittest.main()
