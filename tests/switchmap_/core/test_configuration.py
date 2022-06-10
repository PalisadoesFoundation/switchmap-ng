#!/usr/bin/env python3
"""Test the configuration module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIR,
            os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}switchmap-ng{0}tests{0}switchmap_{0}core'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from switchmap.core import configuration as test_module
from tests.testlib_ import data


class Test_Config(unittest.TestCase):
    """Checks all class_config methods."""

    #########################################################################
    # General object setup
    #########################################################################

    config = test_module._Config(data.configtester())

    # Required
    maxDiff = None

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_agent_threads(self):
        """Testing function agent_threads."""
        # Run test
        expected = 35
        result = self.config.agent_threads()
        self.assertEqual(result, expected)

    def test_bind_port(self):
        """Testing function bind_port."""
        # Run test
        expected = 7027
        result = self.config.bind_port()
        self.assertEqual(result, expected)

    def test_daemon_directory(self):
        """Testing function daemon_directory."""
        # Run test
        expected = 'XXX'
        result = self.config.daemon_directory()
        self.assertEqual(result, expected)

    def test_db_host(self):
        """Testing function db_host."""
        # Run test
        expected = 'Mwxu7gnv29AbLGyz'
        result = self.config.db_host()
        self.assertEqual(result, expected)

    def test_db_name(self):
        """Testing function db_name."""
        # Run test
        expected = 'JkfSJnhZTh55wJy4'
        result = self.config.agent_threads()
        self.assertEqual(result, expected)

    def test_db_max_overflow(self):
        """Testing function db_max_overflow."""
        # Run test
        expected = 30
        result = self.config.db_max_overflow()
        self.assertEqual(result, expected)

    def test_db_pass(self):
        """Testing function db_pass."""
        # Run test
        expected = 'nhZThsh4gPMwxu75'
        result = self.config.db_pass()
        self.assertEqual(result, expected)

    def test_db_pool_size(self):
        """Testing function db_pool_size."""
        # Run test
        expected = 30
        result = self.config.db_pool_size()
        self.assertEqual(result, expected)

    def test_db_user(self):
        """Testing function db_user."""
        # Run test
        expected = '7MKG2dstsh4gPe2X'
        result = self.config.db_user()
        self.assertEqual(result, expected)

    def test_hostnames(self):
        """Testing function hostnames."""
        # Run test
        expected = ['unittest.example.org']
        result = self.config.hostnames()
        self.assertEqual(result, expected)

    def test_listen_address(self):
        """Testing function listen_address."""
        # Run test
        expected = 'MKG2dst7sh4gPe2X'
        result = self.config.listen_address()
        self.assertEqual(result, expected)

    def test_log_directory(self):
        """Testing function log_directory."""
        # Run test
        expected = 'YYY'
        result = self.config.log_directory()
        self.assertEqual(result, expected)

    def test_log_file(self):
        """Testing function log_file."""
        # Run test
        expected = None
        result = self.config.log_file()
        self.assertEqual(result, expected)

    def test_log_level(self):
        """Testing function log_level."""
        # Run test
        expected = 'debug'
        result = self.config.log_level()
        self.assertEqual(result, expected)

    def test_polling_interval(self):
        """Testing function polling_interval."""
        # Run test
        expected = 21600
        result = self.config.polling_interval()
        self.assertEqual(result, expected)

    def test_username(self):
        """Testing function username."""
        # Run test
        expected = '7gnv2Mwxu9AbLGyz'
        result = self.config.username()
        self.assertEqual(result, expected)

    def test_web_log_file(self):
        """Testing function web_log_file."""
        # Run test
        expected = None
        result = self.config.web_log_file()
        self.assertEqual(result, expected)


class Test_ConfigSNMP(unittest.TestCase):
    """Checks all class_config methods."""

    #########################################################################
    # General object setup
    #########################################################################

    config = test_module._ConfigSNMP(data.configtester())

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_snmp_auth(self):
        """Testing function snmp_auth."""
        # Run test
        expected = [
            {
                'group_name': 'h55wJy4JkfSJnhZT',
                'snmp_authpassword': 'v29AbLMwxu7gnGyz',
                'snmp_authprotocol': 'sha',
                'snmp_community': None,
                'snmp_port': 161,
                'snmp_privpassword': 'sh4gPe7MKG2dst2X',
                'snmp_privprotocol': 'aes',
                'snmp_secname': '76v4PjWHpDmzy6cx',
                'snmp_version': 3
            }
        ]
        result = self.config.snmp_auth()
        self.assertEqual(result, expected)


class TestConfig(unittest.TestCase):
    """Checks all class_config methods."""

    def test___init__(self):
        """Testing function __init__."""
        pass


class TestConfigSNMP(unittest.TestCase):
    """Checks all class_config methods."""

    def test___init__(self):
        """Testing function __init__."""
        pass


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
