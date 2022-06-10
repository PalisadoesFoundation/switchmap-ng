#!/usr/bin/env python3
"""Class used to create the configuration file used for unittesting.

NOTE!! This script CANNOT import any switchmap libraries. Doing so risks
libraries trying to access a configuration or configuration directory that
doesn't yet exist. This is especially important when running cloud based
automated tests such as 'Travis CI'

"""

# Standard imports
import tempfile
import os
import sys
import yaml
import socket
import struct

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

# Initialize GLOBAL variables
CONFIG_SUFFIX = '.switchmap_unittests/config'
CONFIG_DIRECTORY = '{}/{}'.format(os.environ['HOME'], CONFIG_SUFFIX)


class TestConfig(object):
    """Creates configuration for testing."""

    def __init__(self):
        """Method initializing the class."""
        # Set global variables
        global CONFIG_DIRECTORY
        self._log_directory = tempfile.mkdtemp()
        self._ingest_cache_directory = tempfile.mkdtemp()

        # Make sure the environmental variables are OK
        _environment()

        # Make sure the configuration directory is OK
        self._config_directory = CONFIG_DIRECTORY
        if os.path.isdir(CONFIG_DIRECTORY) is False:
            os.makedirs(CONFIG_DIRECTORY, mode=0o750, exist_ok=True)

        self._config = {
            'main': {
                'log_directory': self._log_directory,
                'log_level': 'debug',
                'ingest_cache_directory': self._ingest_cache_directory,
                'ingest_pool_size': 20,
                'bind_port': 3000,
                'interval': 300,
                'sqlalchemy_pool_size': 10,
                'sqlalchemy_max_overflow': 10,
                'db_hostname': 'localhost',
                'db_username': 'travis',
                'db_password': '',
                'db_name': 'test_switchmap'
            }
        }

    def create(self):
        """Create a good config and set the SWITCHMAP_CONFIGDIR variable.

        Args:
            None

        Returns:
            self.config_directory: Directory where the config is placed

        """
        # Initialize key variables
        config_file = '{}/test_config.yaml'.format(self._config_directory)

        # Write good_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(self._config, f_handle, default_flow_style=False)

        # Return
        return self._config_directory

    def cleanup(self):
        """Remove all residual directories.

        Args:
            None

        Returns:
            None

        """
        # Delete directories
        directories = [
            self._log_directory,
            self._ingest_cache_directory,
            self._config_directory]
        for directory in directories:
            _delete_files(directory)


def _delete_files(directory):
    """Delete all files in directory."""
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


def _environment():
    """Make sure environmental variables are OK.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    global CONFIG_DIRECTORY
    os.environ['INFOSET_CONFIGDIR'] = CONFIG_DIRECTORY

    # Make sure the SWITCHMAP_CONFIGDIR environment variable is set
    if 'SWITCHMAP_CONFIGDIR' not in os.environ:
        log_message = (
            '\nThe SWITCHMAP_CONFIGDIR is set to the wrong directory. '
            'Run this command to do so:\n\n'
            '$ export SWITCHMAP_CONFIGDIR={}'
            '\n\nThen run this command again, followed by.\n\n'
            '$ ./_do_all_tests.py\n'
            ''.format(CONFIG_DIRECTORY))
        print(log_message)
        sys.exit(2)

    # Make sure the SWITCHMAP_CONFIGDIR environment variable is set correctly
    if os.environ['SWITCHMAP_CONFIGDIR'] != CONFIG_DIRECTORY:
        log_message = (
            '\nThe SWITCHMAP_CONFIGDIR is set to the wrong directory ("{}"). '
            'Run this command to do so:\n\n'
            '$ export SWITCHMAP_CONFIGDIR={}'
            '\n\nThen run this command again, followed by.\n\n'
            ''.format(
                os.environ['SWITCHMAP_CONFIGDIR'], CONFIG_DIRECTORY))
        print(log_message)
        sys.exit(2)


def ip2long(ipv4):
    """Convert an IP string to long."""
    packed_ip = socket.inet_aton(ipv4)
    return struct.unpack('!L', packed_ip)[0]


def ready():
    """Verify that we are ready to run tests."""
    # Check environment
    _environment()

    # Create configuration
    TestConfig().create()


def main():
    """Verify that we are ready to run tests."""
    # Check environment
    config = TestConfig()
    config.create()


if __name__ == '__main__':
    # Do the unit test
    main()
