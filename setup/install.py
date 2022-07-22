#!/usr/bin/env python3
"""Application  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys
import os
from collections import defaultdict
import getpass
from pwd import getpwnam
import grp
import re

# PIP3 libraries
###############################################################################
# YAML needs to be installed for the general library to be used
###############################################################################
try:
    import yaml
except ImportError:
    import pip

    _USERNAME = getpass.getuser()
    _PACKAGES = ["PyYAML", "setuptools"]
    for _PACKAGE in _PACKAGES:
        # Install package globally if user 'root'
        if _USERNAME == "root":
            pip.main(["install", _PACKAGE])
        else:
            pip.main(["install", "--user", _PACKAGE])
    print(
        "\nNew Python packages installed. Please run this script again to "
        "complete the Switchmap-NG installation.\n"
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


# Do switchmap-ng imports
from switchmap import CONFIG
from switchmap.utils import log
from setup import setup
from switchmap.utils import general
from switchmap.utils import daemon as daemon_lib


class _DaemonSystemD(object):
    """Class to setup switchmap-ng daemon."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        running_username = getpass.getuser()
        daemon_username = CONFIG.username()
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
                log.log2die_safe(1129, log_message)
        else:
            self.switchmap_user = daemon_username

        # If running as the root user, then the switchmap user needs to exist
        if running_username == "root":
            self.running_as_root = True
            return

    def enable(self):
        """Enable systemd.

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
            log.log2die_safe(1130, log_message)

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
        poller_service = "switchmap-ng-poller.service"
        api_service = "switchmap-ng-api.service"

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


class _Daemons(object):
    """Class to start switchmap-ng daemons."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """

    def start(self):
        """Write the config to file.

        Args:
            None


        Returns:
            None
        """
        # Get daemon status
        daemons = ["switchmap-ng-api", "switchmap-ng-poller"]
        for daemon in daemons:
            # Initialize key variables
            success = False
            running = self._running(daemon)

            # Prompt to restart if already running
            if running is True:
                restart = input(
                    "\nINPUT - Daemon {} is running. Restart? [Y/n] "
                    "".format(daemon)
                )
                if bool(restart) is False:
                    success = self._restart(daemon)
                    if success is True:
                        setup.print_ok(
                            "Successfully restarted daemon {}.".format(daemon)
                        )
                elif restart[0].lower() != "n":
                    success = self._restart(daemon)
                    if success is True:
                        setup.print_ok(
                            "Successfully restarted daemon {}.".format(daemon)
                        )
                else:
                    setup.print_ok(
                        "Leaving daemon {} unchanged.".format(daemon)
                    )
                    success = True
            else:
                success = self._start(daemon)
                if success is True:
                    setup.print_ok(
                        "Successfully started daemon {}.".format(daemon)
                    )

            # Message if no success
            if success is False:
                log_message = "Failed to start daemon {}.".format(daemon)
                log.log2see_safe(1001, log_message)

    def _restart(self, daemon):
        """Start or restart daemon.

        Args:
            daemon: Name of daemon

        Returns:
            None

        """
        # restart
        return self._start(daemon, restart=True)

    def _start(self, daemon, restart=False):
        """Start or restart daemon.

        Args:
            daemon: Name of daemon
            restart: Restart if True

        Returns:
            None

        """
        # Initialize key variables
        username = getpass.getuser()
        running = False
        if restart is True:
            attempt = "restart"
        else:
            attempt = "start"

        # Get status
        root_directory = general.root_directory()
        if restart is False:
            if username == "root":
                script_name = "/bin/systemctl start {}.service".format(daemon)
            else:
                script_name = "{}/bin/systemd/{} --start".format(
                    root_directory, daemon
                )
        else:
            if username == "root":
                script_name = "/bin/systemctl restart {}.service".format(
                    daemon
                )
            else:
                script_name = "{}/bin/systemd/{} --restart --force" "".format(
                    root_directory, daemon
                )

        # Attempt to restart / start
        response = general.run_script(script_name, die=False)
        if bool(response["returncode"]) is True:
            log_message = "Could not {} daemon {}.".format(attempt, daemon)
            log.log2see_safe(1127, log_message)

        # Return after waiting for daemons to startup properly
        running = self._running(daemon)
        return running

    def _running(self, daemon):
        """Determine status of daemon.

        Args:
            daemon: Name of daemon

        Returns:
            running: True if running

        """
        # Initialize key variables
        running = False

        # Get status of file (Don't create directories)
        if daemon_lib.pid_file_exists(daemon) is True:
            running = True

        # Return
        return running


class _Config(object):
    """Class to test setup."""

    def __init__(self, daemon_username):
        """Function for intializing the class.

        Args:
            daemon_username: Username to run scripts as

        Returns:
            None

        """
        # Initialize key variables
        valid_directories = []
        config = (
            """\
main:
    username: {}
    agent_subprocesses: 20
    bind_port: 7000
    cache_directory:
    hostnames:
      - {}
      - {}
    listen_address: localhost
    log_directory:
    log_level: debug
    polling_interval: 86400

snmp_groups:
    - group_name: SAMPLE_SNMPv2
      snmp_version: 2
      snmp_secname:
      snmp_community: SAMPLE
      snmp_port: 161
      snmp_authprotocol:
      snmp_authpassword:
      snmp_privprotocol:
      snmp_privpassword:
      enabled: False

    - group_name: SAMPLE_SNMPv3
      snmp_version: 3
      snmp_secname: SAMPLE
      snmp_community:
      snmp_port: 161
      snmp_authprotocol: SAMPLE
      snmp_authpassword: SAMPLE
      snmp_privprotocol: SAMPLE
      snmp_privpassword: SAMPLE
      enabled: False
"""
        ).format(daemon_username, None, None)

        self.config_dict = yaml.safe_load(config)
        directory_dict = defaultdict(lambda: defaultdict(dict))

        # Read yaml files from configuration directory
        self.directories = general.config_directories()

        # Check each directory in sequence
        for config_directory in self.directories:
            # Check if config_directory exists
            if os.path.isdir(config_directory) is False:
                continue

            # Cycle through list of files in directory
            for filename in os.listdir(config_directory):
                # Examine all the '.yaml' files in directory
                if filename.endswith(".yaml"):
                    # YAML files found
                    valid_directories.append(config_directory)

        if bool(valid_directories) is True:
            directory_dict = general.read_yaml_files(valid_directories)

        # Populate config_dict with any values found in directory_dict
        for _file_key, _file_value in directory_dict.items():
            if isinstance(_file_value, dict) is True:
                # Process the subkeys under the primary key
                for _sub_key, value in _file_value.items():
                    # Add values from file to the seeded self.config_dict
                    # configuration value
                    if isinstance(value, list) is False:
                        self.config_dict[_file_key][_sub_key] = value
                    else:
                        if _sub_key == "hostnames":
                            # Add newly found hostnames to the
                            # list without duplicates
                            found_hostnames = value
                            existing_hostnames = self.config_dict[_file_key][
                                _sub_key
                            ]
                            for hostname in found_hostnames:
                                if hostname not in existing_hostnames:
                                    self.config_dict[_file_key][
                                        _sub_key
                                    ].append(hostname)
                        else:
                            # Extend other lists that may have been found
                            self.config_dict[_file_key][_sub_key].extend(value)

            elif isinstance(_file_value, list) is True:
                # Process 'snmp_groups:' key
                if _file_key == "snmp_groups":
                    for item in _file_value:
                        if (
                            _snmp_group_found(
                                item, self.config_dict[_file_key]
                            )
                            is False
                        ):
                            self.config_dict[_file_key].append(item)
                else:
                    self.config_dict[_file_key].extend(_file_value)

    def validate(self):
        """Validate all pre-requisites are OK.

        Args:
            None

        Returns:
            None

        """
        # Returns
        pass

    def write(self):
        """Write the config to file.

        Args:
            None


        Returns:
            None
        """
        # Initialize key variables
        directory = self.directories[0]

        # Update configuration file if required
        for next_directory in self.directories:
            # Delete all YAML files in the configuration directory
            general.delete_yaml_files(next_directory)

        # Write config back to directory
        filepath = "{}/config.yaml".format(directory)
        with open(filepath, "w") as outfile:
            yaml.dump(self.config_dict, outfile, default_flow_style=False)

            # Write status Update
            setup.print_ok("Created configuration file {}.".format(filepath))


class _PreCheck(object):
    """Class to test setup."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """

    def validate(self):
        """Validate all pre-requisites are OK.

        Args:
            None

        Returns:
            None

        """
        # Test systemd is present
        self._systemd()

        # Test Python version
        self._python()

        # Test Python pip version
        self._pip()

    def _pip(self):
        """Determine pip3 version.

        Args:
            None

        Returns:
            None

        """
        # install pip3 modules
        modules = ["setuptools", "PyYAML"]
        for module in modules:
            _pip3_install(module)

    def _systemd(self):
        """Determine whether systemd is installed.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables.
        directory = "/etc/systemd/system"

        # Do nothing if this is not the root user.
        username = getpass.getuser()
        if username != "root":
            return

        # Test
        if os.path.isdir(directory) is True:
            setup.print_ok("Systemd installed.")
        else:
            log_message = "Systemd not installed. Directory {} not found"
            log.log2die_safe(1234, log_message)

    def _python(self):
        """Determine Python version.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = True
        major = 3
        minor = 5
        major_installed = sys.version_info[0]
        minor_installed = sys.version_info[1]

        # Determine whether python version is too low
        if major_installed < major:
            valid = False
        elif major_installed == major and minor_installed < minor:
            valid = False

        # Process validity
        if valid is False:
            log_message = (
                "Required python version must be >= {}.{}. "
                "Python version {}.{} installed"
                "".format(major, minor, major_installed, minor_installed)
            )
            log.log2die_safe(1095, log_message)
        else:
            log_message = "Python version {}.{}." "".format(
                major_installed, minor_installed
            )
            setup.print_ok(log_message)


class _PostCheck(object):
    """Class to test post setup."""

    def __init__(self):
        """Method for intializing the class.

        Args:
            None

        Returns:
            None

        """

    def validate(self):
        """Validate .

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        username = getpass.getuser()
        added_suggestions = ""
        line = "*" * 80
        prefix = """\

1) Edit file {}/etc/config.yaml with correct SNMP parameters \
and then restart the daemons.
2) You can restart switchmap-ng daemons with these commands:

   $ bin/switchmap-ng-cil restart api
   $ bin/switchmap-ng-cli restart poller
""".format(
            general.root_directory()
        )

        #######################################################################
        #
        # Give suggestions as to what to do
        #
        # NOTE!
        #
        # The root user should only use the systemctl commands as the daemons
        # could be running as another user and lock and pid files will be owned
        # by that user. We don't want the daemons to crash at some other time
        # because these files are owned by root with denied delete privileges
        #######################################################################
        if username != "root":
            added_suggestions = """{}
3) Switchmap-NG will not automatically restart after a reboot. \
You need to re-install as the "root" user for this to occur.
""".format(
                prefix
            )

            print("{}\n{}\n{}\n".format(line, added_suggestions, line))
        else:
            print("{}\n{}\n{}\n".format(line, prefix, line))

        # All done
        setup.print_ok(
            "Installation complete, pending changes mentioned above."
        )


def _snmp_group_found(item, listing):
    """Install python module using pip3.

    Args:
        module: module to install

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False

    for next_item in listing:
        if next_item["group_name"] == item["group_name"]:
            found = True

    # Return
    return found


def _pip3_install(module):
    """Install python module using pip3.

    Args:
        module: module to install

    Returns:
        None

    """
    # Find pip3 executable
    cli_string = "which pip3"
    response = general.run_script(cli_string, die=False)

    # Not OK if not fount
    if bool(response["returncode"]) is True:
        log_message = "python pip3 not installed."
        log.log2die_safe(1041, log_message)
    else:
        log_message = "Python pip3 executable found."
        setup.print_ok(log_message)

    # Determine version of pip3
    cli_string = "pip3 --version"
    response = os.popen(cli_string).read()
    version = response.split()[1]

    # Attempt to install module
    if version < "9.0.0":
        cli_string = "pip3 list | grep {}".format(module)
    else:
        cli_string = "pip3 list --format columns | grep {}".format(module)
    response = bool(os.popen(cli_string).read())

    if response is False:
        # YAML is not installed try to install it
        cli_string = "pip3 install --user {}".format(module)
        response_install = general.run_script(cli_string, die=False)

        # Fail if module cannot be installed
        if bool(response_install["returncode"]) is True:
            log_message = 'python pip3 cannot install "{}".'.format(module)
            log.log2die_safe(1119, log_message)
        else:
            log_message = 'Python module "{}" is installed.'.format(module)
            setup.print_ok(log_message)
    else:
        log_message = 'Python module "{}" is installed.'.format(module)
        setup.print_ok(log_message)


def _system_daemon_prompt():
    """Prompt user to see whether they want to run as a system daemon.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    running_username = getpass.getuser()

    # Return if running as root. We'll run as a daemon
    if running_username == "root":
        return

    # Get the user's intention
    prompt = input(
        "Do you want switchmap-ng to start automatically "
        "after a reboot?: (Y, N) "
    )
    intention = prompt.strip()
    if bool(intention) is True and len(intention) == 1:
        response = intention.lower()[0]
        if response == "n":
            return
        elif response == "y":
            log_message = (
                'Run this script as the "root" user to '
                "get the automatic functionality."
            )
            log.log2die_safe(1012, log_message)

    log_message = 'Please answer "Y" or "N", and try again.'
    log.log2die_safe(1013, log_message)


def _get_daemon_username():
    """Get the daemon's username.

    Args:
        None

    Returns:
        daemon_username: Username daemon will run as

    """
    # Initialize key variables
    running_username = getpass.getuser()

    # If running as the root user, then the switchmap user needs to exist
    if running_username == "root":
        try:
            daemon_username = input(
                "Please enter the username under which "
                "switchmap-ng will run: "
            )

            # Get GID and UID for user
            _ = getpwnam(daemon_username).pw_gid
        except:
            log_message = "User {} not found. Please try again." "".format(
                daemon_username
            )
            log.log2die_safe(1019, log_message)
    else:
        daemon_username = running_username

    # Return
    return daemon_username


def run():
    """Do the installation.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    running_username = getpass.getuser()

    # Make sure we are not running as sudo
    general.check_sudo()

    # Ask about daemon status
    _system_daemon_prompt()

    # Get the daemon username
    daemon_username = _get_daemon_username()

    # Do precheck
    precheck = _PreCheck()
    precheck.validate()

    # Create a configuration
    config = _Config(daemon_username)
    config.validate()
    config.write()

    # Run setup
    setup.run(daemon_username)

    # Do specific setups for root user
    if running_username != "root":
        _DaemonSystemD().enable()

    # Start daemons
    _Daemons().start()

    # Run the post check
    postcheck = _PostCheck()
    postcheck.validate()


if __name__ == "__main__":
    # Run main
    run()
