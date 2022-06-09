#!/usr/bin/env python3
"""Test the configuration module."""

import multiprocessing
import os
import sys
import os.path
import unittest
import shutil
import random
import string
import tempfile
import yaml

# Try to create a working PYTHONPATH
TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SWITCHMAP_DIRECTORY = os.path.abspath(os.path.join(TEST_DIRECTORY, os.pardir))
ROOT_DIRECTORY = os.path.abspath(os.path.join(SWITCHMAP_DIRECTORY, os.pardir))
if TEST_DIRECTORY.endswith('/switchmap-ng/switchmap/test') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "switchmap-ng/bin" directory. '
        'Please fix.')
    sys.exit(2)

from switchmap.utils import configuration


class TestConfig(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for n in range(9)])

    log_directory = tempfile.mkdtemp()
    cache_directory = tempfile.mkdtemp()
    good_config = ("""\
main:
    log_directory: {}
    cache_directory: {}
    agent_threads: 25
    bind_port: 3000
    hostnames:
    - 192.168.1.1
    - 192.168.1.2
    - 192.168.1.3
    - 192.168.1.4
    listen_address: 0.0.0.0
    log_level: debug
    polling_interval: 20
""".format(log_directory, cache_directory))

    # Convert good_config to dictionary
    good_dict = yaml.safe_load(bytes(good_config, 'utf-8'))

    # Set the environmental variable for the configuration directory
    directory = tempfile.mkdtemp()
    os.environ['SWITCHMAP_CONFIGDIR'] = directory
    config_file = '{}/test_config.yaml'.format(directory)

    # Write good_config to file
    with open(config_file, 'w') as f_handle:
        yaml.dump(good_dict, f_handle, default_flow_style=True)

    # Create configuration object
    config = configuration.Config()

    @classmethod
    def tearDownClass(cls):
        """Post test cleanup."""
        os.rmdir(cls.log_directory)
        os.rmdir(cls.config.topology_directory())
        os.rmdir(cls.config.idle_directory())
        os.rmdir(cls.cache_directory)
        os.remove(cls.config_file)
        os.rmdir(cls.directory)

    def test_init(self):
        """Testing method init."""
        # Testing with non-existant directory
        directory = 'bogus'
        os.environ['SWITCHMAP_CONFIGDIR'] = directory
        with self.assertRaises(SystemExit):
            configuration.Config()

        # Testing with an empty directory
        empty_directory = tempfile.mkdtemp()
        os.environ['SWITCHMAP_CONFIGDIR'] = empty_directory
        with self.assertRaises(SystemExit):
            configuration.Config()

        # Write bad_config to file
        empty_config_file = '{}/test_config.yaml'.format(empty_directory)
        with open(empty_config_file, 'w') as f_handle:
            f_handle.write('')

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.log_file()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_log_file(self):
        """Testing method log_file."""
        # Test the log_file with a good_dict
        # good key and key_value
        result = self.config.log_file()
        self.assertEqual(
            result, '{}/switchmap-ng.log'.format(self.log_directory))

    def test_web_log_file(self):
        """Testing method web_log_file ."""
        # Testing web_log_file with a good dictionary.
        result = self.config.web_log_file()
        self.assertEqual(
            result, '{}/switchmap-ng-api.log'.format(self.log_directory))

    def test_log_level(self):
        """Testing method log_level."""
        # Tesing with a good_dictionary
        # good key and good key_value
        result = self.config.log_level()
        self.assertEqual(result, 'debug')
        self.assertEqual(result, self.good_dict['main']['log_level'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['SWITCHMAP_CONFIGDIR'] = directory
        config_file = '{}/test_config.yaml'.format(directory)

        # Testing log_level with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    {} {}
""".format(key, key_value))
        bad_dict = yaml.safe_load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.log_level()

        # Testing log_level with good key and blank key_value
        key = 'log_level:'
        key_value = ''
        bad_config = ("""\
main:
    {} {}
""".format(key, key_value))
        bad_dict = yaml.safe_load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.log_level()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_cache_directory(self):
        """Testing method cache_directory."""
        # Testing cache_directory with temp directory
        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['SWITCHMAP_CONFIGDIR'] = directory
        config_file = '{}/test_config.yaml'.format(directory)

        # Testing cache_directory with blank key_value(filepath)
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    {} {}
""".format(key, key_value))
        bad_dict = yaml.safe_load(bytes(bad_config, 'utf-8'))

        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.cache_directory()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_agent_threads(self):
        """Testing method agent_threads."""
        # Testing agent_threads with good_dict
        # good key and key_value
        result = self.config.agent_threads()

        # Get CPU cores
        cores = multiprocessing.cpu_count()
        desired_max_threads = max(1, cores - 1)

        # We don't want a value that's too big that the CPU cannot cope
        expected = min(result, desired_max_threads)

        self.assertEqual(result, expected)

    def test_polling_interval(self):
        """Testing method polling_interval."""
        # Testing polling_interval with good_dictionary
        # good key and key_value
        result = self.config.polling_interval()
        self.assertEqual(result, 20)
        self.assertEqual(result, self.good_dict['main']['polling_interval'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['SWITCHMAP_CONFIGDIR'] = directory
        config_file = '{}/test_config.yaml'.format(directory)

        # Testing polling_interval with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    {} {}
""".format(key, key_value))
        bad_dict = yaml.safe_load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.polling_interval()

        # Testing polling_interval with good key and blank key_value
        key = 'polling_interval:'
        key_value = ''
        bad_config = ("""\
main:
    {} {}
""".format(key, key_value))
        bad_dict = yaml.safe_load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        result = config.polling_interval()
        self.assertEqual(result, 86400)

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_bind_port(self):
        """Testing method bind_port."""
        # Testing bind_port with good_dictionary
        # good key and key_value
        result = self.config.bind_port()
        self.assertEqual(result, 3000)
        self.assertEqual(result, self.good_dict['main']['bind_port'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['SWITCHMAP_CONFIGDIR'] = directory
        config_file = '{}/test_config.yaml'.format(directory)

        # Testing bind_port with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    {} {}
""".format(key, key_value))
        bad_dict = yaml.safe_load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.bind_port()

        # Testing bind_port with good key and blank key_value
        key = 'bind_port:'
        key_value = ''
        bad_config = ("""\
main:
    {} {}
""".format(key, key_value))
        bad_dict = yaml.safe_load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        result = config.bind_port()
        self.assertEqual(result, 7000)

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_idle_directory(self):
        """Testing function idle_directory."""
        # Verify that directory exists
        result = self.config.idle_directory()
        self.assertEqual(os.path.exists(result), True)
        self.assertEqual(os.path.isdir(result), True)

        # Doesn't fail because directory now exists
        result = self.config.idle_directory()
        expected = '{}/idle'.format(
            self.good_dict['main']['cache_directory'])
        self.assertEqual(result, expected)

    def test_topology_directory(self):
        """Testing function topology_directory."""
        # Verify that directory exists
        result = self.config.topology_directory()
        self.assertEqual(os.path.exists(result), True)
        self.assertEqual(os.path.isdir(result), True)

        # Doesn't fail because directory now exists
        result = self.config.topology_directory()
        expected = '{}/topology'.format(
            self.good_dict['main']['cache_directory'])
        self.assertEqual(result, expected)

    def test_topology_device_file(self):
        """Testing function topology_device_file."""
        # Recreate the path to the device file
        result = self.config.topology_device_file(self.random_string)
        expected = '{}/{}.yaml'.format(
            self.config.topology_directory(), self.random_string)
        self.assertEqual(result, expected)

    def test_hostnames(self):
        """Testing function hostnames."""
        # Test expected versus returned values
        result = self.config.hostnames()
        expected = sorted(self.good_dict['main']['hostnames'])
        self.assertEqual(result, expected)

    def test_log_directory(self):
        """Testing method log_directory."""
        # Testing log_directory with temp directory
        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['SWITCHMAP_CONFIGDIR'] = directory
        config_file = '{}/test_config.yaml'.format(directory)

        # Testing log_directory with blank key_value(filepath)
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    {} {}
""".format(key, key_value))
        bad_dict = yaml.safe_load(bytes(bad_config, 'utf-8'))

        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.log_directory()

        # Cleanup files in temp directories
        _delete_files(directory)


class TestConfigSNMP(unittest.TestCase):
    """Checks all functions and methods."""

    # ---------------------------------------------------------------------- #
    # General object setup
    # ---------------------------------------------------------------------- #

    # Required
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Setup the environmental before testing begins."""
        # Define agent name
        cls.group_name = ''.join([random.choice(
            string.ascii_letters + string.digits) for n in range(9)])

        # Create logfile
        cls.log_file = tempfile.NamedTemporaryFile(delete=False).name

        # Create temporary configuration directory
        cls.test_config_dir = tempfile.mkdtemp()

        # Initializing key variables
        text_configuration = ("""
            snmp_groups:
                - group_name: {}
                  snmp_version: 3
                  snmp_secname: woohoo
                  snmp_community:
                  snmp_port: 161
                  snmp_authprotocol: sha
                  snmp_authpassword: auth123
                  snmp_privprotocol: des
                  snmp_privpassword: priv123

                - group_name: Remote Sites
                  snmp_version: 3
                  snmp_secname: foobar
                  snmp_community:
                  snmp_port: 161
                  snmp_authprotocol: sha
                  snmp_authpassword: 123auth
                  snmp_privprotocol: aes
                  snmp_privpassword: 123priv
            """.format(cls.group_name))
        cls.configuration_dict = yaml.safe_load(text_configuration)

        # Create the configuration file on disk
        test_config_file = '{}/config.yaml'.format(cls.test_config_dir)
        with open(test_config_file, 'w') as f_handle:
            f_handle.write(text_configuration)

        # Instantiate object to test
        os.environ['SWITCHMAP_CONFIGDIR'] = cls.test_config_dir
        cls.testobj = configuration.ConfigSNMP()

    @classmethod
    def tearDownClass(cls):
        """Cleanup the environmental after testing ends."""
        # Cleanup temporary files when done
        shutil.rmtree(cls.test_config_dir)
        os.remove(cls.log_file)

    def test_snmp_auth(self):
        """Testing method / function snmp_auth."""
        # Initializing key variables
        expected_list = [
            {
                'group_name': 'Remote Sites',
                'snmp_version': 3,
                'snmp_secname': 'foobar',
                'snmp_community': None,
                'snmp_port': 161,
                'snmp_authprotocol': 'sha',
                'snmp_authpassword': '123auth',
                'snmp_privprotocol': 'aes',
                'snmp_privpassword': '123priv'
            },
            {
                'group_name': self.group_name,
                'snmp_version': 3,
                'snmp_secname': 'woohoo',
                'snmp_community': None,
                'snmp_port': 161,
                'snmp_authprotocol': 'sha',
                'snmp_authpassword': 'auth123',
                'snmp_privprotocol': 'des',
                'snmp_privpassword': 'priv123'
            }
            ]

        # Get results from configuration file
        groups = self.testobj.snmp_auth()

        # Iterate through each item in the snmp parameters list received
        for group in groups:
            for expected_dict in expected_list:
                if expected_dict['group_name'] == group['group_name']:
                    for key in expected_dict.keys():
                        self.assertEqual(
                            group[key], expected_dict[key])


def _delete_files(directory):
    """Delete all files in directory."""
    # Verify that directory exists
    if os.path.isdir(directory) is False:
        return

    # Cleanup files in temp directories
    filenames = [filename for filename in os.listdir(
        directory) if os.path.isfile(
            os.path.join(directory, filename))]

    # Get the full filepath for the cache file and remove filepath
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        os.remove(filepath)

    # Remove directory after files are deleted.
    os.rmdir(directory)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
