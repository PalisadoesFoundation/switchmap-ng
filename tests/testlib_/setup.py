"""Class used to create the configuration file used for unittesting.

NOTE!! This script CANNOT import any switchmap libraries. Doing so risks
libraries trying to access a configuration or configuration directory that
doesn't yet exist. This is especially important when running cloud based
automated tests such as 'Travis CI'

"""

# Standard imports
import os
import copy
import random
import string
from collections import namedtuple
from copy import deepcopy

import yaml


# Initialize GLOBAL variables
_UNITTEST_DIRECTORY = (
    '{}{}.switchmap_unittests'.format(os.environ['HOME'], os.sep)
)

# Application imports
from . import data


class Config():
    """Creates configuration for testing."""

    def __init__(self, _config, randomizer=False):
        """Initialize the class.

        Args:
            _config: Configuration dict
            randomizer: Create a random config directory if True

        Returns:
            None

        """
        # Initialize key variables
        self._randomizer = randomizer
        Metadata = namedtuple(
            'Metadata',
            '''\
config log_directory daemon_directory config_directory base_directory''')
        config_ = copy.deepcopy(_config)
        if bool(randomizer) is False:
            base_directory = _UNITTEST_DIRECTORY
        else:
            base_directory = (
                '{1}{0}tmp{0}{2}'.format(
                    os.sep, _UNITTEST_DIRECTORY,
                    ''.join(random.choices(
                        string.ascii_uppercase + string.digits, k=10))))

        # Set global variables
        log_directory = (
            '{}{}log'.format(base_directory, os.sep))
        config_directory = (
            '{}{}etc'.format(base_directory, os.sep))
        daemon_directory = (
            '{}{}daemon'.format(base_directory, os.sep))

        # Make sure the configuration directory is OK
        if os.path.isdir(config_directory) is False:
            os.makedirs(config_directory, mode=0o750, exist_ok=True)
            os.makedirs(log_directory, mode=0o750, exist_ok=True)
            os.makedirs(daemon_directory, mode=0o750, exist_ok=True)

        # Update configuration
        config_['main']['log_directory'] = log_directory
        config_['main']['daemon_directory'] = daemon_directory

        # Create the metadata object
        self.metadata = Metadata(
            config=config_,
            log_directory=log_directory,
            daemon_directory=daemon_directory,
            config_directory=config_directory,
            base_directory=base_directory
        )
        # Set the environment for the configuration
        os.environ['SWITCHMAP_CONFIGDIR'] = config_directory

    def save(self):
        """Save a good config and set the SWITCHMAP_CONFIGDIR variable.

        Args:
            None

        Returns:
            config_directory: Directory where the config is placed

        """
        # Initialize key variables
        config_file = '{}/config.yaml'.format(self.metadata.config_directory)

        # Write good_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(self.metadata.config, f_handle, default_flow_style=False)

        # Return
        return self.metadata.config_directory

    def cleanup(self):
        """Remove all residual directories.

        Args:
            None

        Returns:
            None

        """
        # Delete directories
        directories = [
            self.metadata.log_directory,
            self.metadata.daemon_directory,
            self.metadata.config_directory,
            ]
        for directory in directories:
            _delete_files(directory)
        if self._randomizer is True:
            _delete_files(self.metadata.base_directory)


def travis_config():
    """Create the CI/CD configuration.

    Args:
        None

    Returns:
        result: Config object

    """
    # Return result
    _config = deepcopy(data.config())
    _config['db_pass'] = ''
    _config['db_user'] = 'travis'
    result = Config(_config)
    return result


def config():
    """Create testing configuration.

    Args:
        None

    Returns:
        config: Config object

    """
    # Return result
    _config = deepcopy(data.config())
    result = Config(_config)
    return result


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
