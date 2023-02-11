#!/usr/bin/env python3
"""Switchmap-NG ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import sys
import os
import getpass
from pwd import getpwnam
import grp
import copy
import re

# Pip3 libraries
try:
    import yaml
except ImportError:
    import pip

    _PACKAGES = ["PyYAML"]
    for _PACKAGE in _PACKAGES:
        pip.main(["install", "--user", _PACKAGE])
    print(
        "New Python packages installed. Please run this script again to "
        "complete the Switchmap-NG installation."
    )
    sys.exit(0)

# Try to create a working PYTHONPATH
_MAINT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_MAINT_DIRECTORY, os.pardir))
if _ROOT_DIRECTORY.endswith("/switchmap-ng") is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'Switchmap-NG is not installed in a "switchmap-ng/" directory. '
        "Please fix."
    )
    sys.exit(2)

# Switchmap-NG libraries
try:
    from switchmap.utils import log
except:
    print(
        "You need to set your PYTHONPATH to include the "
        "switchmap-ng root directory"
    )
    sys.exit(2)
from switchmap.utils import general


class _Configuration(object):
    """Class to setup configuration.

    NOTE! We cannot use the configuration.Config class here. The aim
    of this class is to read in the configuration found in etc/ or
    $SWITCHMAP_CONFIGDIR and set any missing values to values that are
    known to work in most cases.

    """

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Read configuration into dictionary
        self.directories = general.config_directories()
        self.config = general.read_yaml_files(self.directories)

    def setup(self):
        """Update the configuration with good defaults.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = True
        updated_list = []
        config = copy.deepcopy(self.config)
        directory = self.directories[0]
        directory_keys = ["log_directory", "system_directory"]

        # Update log_directory and system_directory
        if isinstance(config, dict) is True:
            if "main" in config:
                for next_key in directory_keys:
                    # Setup the log_directory to a known good default
                    (updated, config) = self._create_directory_entries(
                        next_key, config
                    )
                    updated_list.append(updated)
            else:
                valid = False
        else:
            valid = False

        # Gracefully exit if things are not OK
        if valid is False:
            log_message = (
                "Configuration files found in {} is invalid"
                "".format(self.directories)
            )
            log.log2die_safe(1015, log_message)

        # Update configuration file if required
        if True in updated_list:
            for next_directory in self.directories:
                # Delete all YAML files in the directory
                general.delete_yaml_files(next_directory)

            # Write config back to directory
            filepath = "{}/config.yaml".format(directory)
            with open(filepath, "w") as outfile:
                yaml.dump(config, outfile, default_flow_style=False)

    def _create_directory_entries(self, key, _config):
        """Update the configuration with good defaults for directories.

        Args:
            key: Configuration key related to a directory.
            _config: Configuration dictionary

        Returns:
            updated: True if we have to update a value

        """
        # Initialize key variables
        updated = False
        config = copy.deepcopy(_config)
        dir_dict = {
            "log_directory": "log",
            "system_directory": "system",
        }
        directory = general.root_directory()

        # Setup the key value to a known good default
        if key in config["main"]:
            # Verify whether key value is empty
            if config["main"][key] is not None:
                # Create
                if os.path.isdir(config["main"][key]) is False:
                    config["main"][key] = "{}/{}".format(
                        directory, dir_dict[key]
                    )
                    updated = True
            else:
                config["main"][key] = "{}/{}".format(directory, dir_dict[key])
                updated = True
        else:
            config["main"][key] = "{}/{}".format(directory, dir_dict[key])
            updated = True

        # Return
        return (updated, config)


class _PythonSetup(object):
    """Class to setup Python."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.username = getpass.getuser()
        valid = True
        major = 3
        minor = 5
        major_installed = sys.version_info[0]
        minor_installed = sys.version_info[1]

        # Exit if python version is too low
        if major_installed < major:
            valid = False
        elif major_installed == major and minor_installed < minor:
            valid = False
        if valid is False:
            log_message = (
                "Required python version must be >= {}.{}. "
                "Python version {}.{} installed"
                "".format(major, minor, major_installed, minor_installed)
            )
            log.log2die_safe(1027, log_message)

    def setup(self):
        """Setup Python.

        Args:
            None

        Returns:
            None

        """
        # Run
        self._install_pip3_packages()

    def _install_pip3_packages(self):
        """Install PIP3 packages.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        username = self.username

        # Don't attempt to install packages if running in the Travis CI
        # environment
        if "TRAVIS" in os.environ and "CI" in os.environ:
            return

        # Determine whether PIP3 exists
        print_ok(
            "Installing required pip3 packages from requirements.txt file."
        )
        pip3 = general.search_file("pip3")
        if pip3 is None:
            log_message = 'Cannot find python "pip3". Please install.'
            log.log2die_safe(1052, log_message)

        # Install required PIP packages
        requirements_file = "{}/requirements.txt".format(
            general.root_directory()
        )

        if username == "root":
            script_name = "pip3 install --upgrade --requirement {}" "".format(
                requirements_file
            )
        else:
            script_name = (
                "pip3 install --user --upgrade --requirement {}"
                "".format(requirements_file)
            )
        general.run_script(script_name)


class _DaemonSetup(object):
    """Class to setup switchmap-ng daemon."""

    def __init__(self, daemon_username):
        """Function for intializing the class.

        Args:
            daemon_username: Username to run as

        Returns:
            None

        """
        # Initialize key variables
        running_username = getpass.getuser()
        self.root_directory = general.root_directory()
        switchmap_user_exists = True
        self.switchmap_user = None
        self.running_as_root = False

        # Set the username we need to be running as
        if running_username == "root":
            try:
                # Get GID and UID for user
                self.switchmap_user = daemon_username
                self.gid = getpwnam(self.switchmap_user).pw_gid
                self.uid = getpwnam(self.switchmap_user).pw_uid
            except KeyError:
                switchmap_user_exists = False

            # Die if user doesn't exist
            if switchmap_user_exists is False:
                log_message = "User {} not found. Please try again." "".format(
                    self.switchmap_user
                )
                log.log2die_safe(1049, log_message)
        else:
            self.switchmap_user = daemon_username

        # If running as the root user, then the switchmap user needs to exist
        if running_username == "root":
            self.running_as_root = True
            return

    def setup(self):
        """Setup daemon scripts and file permissions.

        Args:
            None

        Returns:
            None

        """
        # Return if not running script as root user
        if self.running_as_root is False:
            return

        # Set file permissions
        self._file_permissions()

        # Setup systemd
        self._systemd()

    def _file_permissions(self):
        """Set file permissions.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        switchmap_user = self.switchmap_user
        root_directory = self.root_directory

        # Prompt to change ownership of root_directory
        groupname = grp.getgrgid(self.gid).gr_name
        response = input(
            "Change ownership of {} directory to user:{} group:{} (y,N) ?: "
            "".format(root_directory, switchmap_user, groupname)
        )

        # Abort if necessary
        if response.lower() != "y":
            log_message = "Aborting as per user request."
            log.log2die_safe(1050, log_message)

        # Change ownership of files under root_directory
        for parent_directory, directories, files in os.walk(root_directory):
            for directory in directories:
                os.chown(
                    os.path.join(parent_directory, directory),
                    self.uid,
                    self.gid,
                )
            for next_file in files:
                os.chown(
                    os.path.join(parent_directory, next_file),
                    self.uid,
                    self.gid,
                )

        # Change ownership of root_directory
        os.chown(root_directory, self.uid, self.gid)

    def _systemd(self):
        """Setup systemd configuration.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        username = self.switchmap_user
        groupname = grp.getgrgid(self.gid).gr_name
        system_directory = "/etc/systemd/system"
        system_command = "/bin/systemctl daemon-reload"
        poller_service = "switchmap_poller.service"
        api_service = "switchmap_dashboard.service"

        # Do nothing if systemd isn't installed
        if os.path.isdir(system_directory) is False:
            return

        # Copy system files to systemd directory and activate
        poller_startup_script = "{}/examples/linux/systemd/{}" "".format(
            self.root_directory, poller_service
        )
        api_startup_script = "{}/examples/linux/systemd/{}" "".format(
            self.root_directory, api_service
        )

        # Read in file
        # 1) Convert home directory to that of user
        # 2) Convert username in file
        # 3) Convert group in file
        filenames = [poller_startup_script, api_startup_script]
        for filename in filenames:
            # Read next file
            with open(filename, "r") as f_handle:
                contents = f_handle.read()

            # Substitute home directory
            contents = re.sub(
                r"/home/switchmap-ng", self.root_directory, contents
            )

            # Substitute username
            contents = re.sub(
                "User=switchmap-ng", "User={}".format(username), contents
            )

            # Substitute group
            contents = re.sub(
                "Group=switchmap-ng", "Group={}".format(groupname), contents
            )

            # Write contents
            filepath = "{}/{}".format(
                system_directory, os.path.basename(filename)
            )
            if os.path.isdir(system_directory):
                with open(filepath, "w") as f_handle:
                    f_handle.write(contents)

        # Make systemd recognize new files
        if os.path.isdir(system_directory):
            general.run_script(system_command)

        # Enable serices
        services = [poller_service, api_service]
        for service in services:
            enable_command = "systemctl enable {}".format(service)
            general.run_script(enable_command)


def run(username=None):
    """Process agent data.

    Args:
        username: Username to run as

    Returns:
        None

    """
    # Initialize key variables
    if username is None:
        daemon_username = getpass.getuser()
    else:
        daemon_username = username

    # Determine whether version of python is valid
    _PythonSetup().setup()

    # Update configuration if required
    _Configuration().setup()

    # Do specific setups for root user
    _DaemonSetup(daemon_username).setup()


def print_ok(message):
    """Install python module using pip3.

    Args:
        module: module to install

    Returns:
        None

    """
    # Print message
    print("OK - {}".format(message))


if __name__ == "__main__":
    # Run setup
    run()
