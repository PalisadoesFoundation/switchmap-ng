#!/usr/bin/env python3
"""switchmap  classes.

Manages the verification of required packages.

"""

# Main python libraries
import textwrap
import sys
import subprocess
import argparse
import os
from collections import defaultdict
import getpass


# Try to create a working PYTHONPATH
script_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(script_directory, os.pardir))
if script_directory.endswith('/switchmap-ng/bin') is True:
    sys.path.append(root_directory)
else:
    print(
        'This script is not installed in the "switchmap-ng/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Do switchmap-ng imports
from switchmap.utils import log
from switchmap.utils import general
from switchmap.utils import setup
from switchmap.utils import input_output
from switchmap.utils import configuration


def main():
    """Run basic tests.

    Args:
        None

    Returns:
        None

    """
    # Run stuff
    cli = CLI()
    cli.process()


class CLI(object):
    """Class that manages the CLI."""

    def __init__(self, additional_help=''):
        """Method initializing the class.

        Args:
            additional_help: String for additional help information

        Returns:
            None

        """
        # Header for the help menu of the application
        self.parser = argparse.ArgumentParser(
            prog='switchmap-ng-cli',
            description=additional_help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Subparser for subcommands
        subparsers = self.parser.add_subparsers(dest='action')

        # Parse install parameters
        _Install(subparsers)

        # Parse log parameters
        _Logs(subparsers)

        # Return the CLI arguments
        self.args = self.parser.parse_args()

    def process(self):
        """Act on CLI arguments.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        args = self.args
        parser = self.parser

        # Process each option
        if args.action == 'install':
            self._install_cli()
            sys.exit(0)
        elif args.action == 'serve':
            self._serve_cli()
            sys.exit(0)
        elif args.action == 'logs':
            # Process log files
            config = configuration.Config()
            if args.poller is True:
                filename = config.log_file()
                self._logs_cli(filename)
                sys.exit(0)
            elif args.api is True:
                filename = config.web_log_file()
                self._logs_cli(filename)
                sys.exit(0)
        elif args.action == 'test':
            self._test_cli()
            sys.exit(0)

        # Show help otherwise
        parser.print_help()
        sys.exit(2)

    def _logo(self):
        pass

    def _install_cli(self):
        """Install switchmap-ng.

        Args:
            None

        Returns:
            None

        """
        #######################################################################
        # Check prerequisite package versions
        #######################################################################
        # Do precheck
        precheck = _PreCheck()
        precheck.validate()

        # Create a configuration
        config = _Config()
        config.validate()
        config.write()

        # Run setup
        setup.run()

        # Start daemons
        daemon = _Daemon()
        daemon.start()

        # Run the post check
        postcheck = _PostCheck()
        postcheck.validate()

    def _serve_cli(self):
        pass

    def _logs_cli(self, filename):
        tail = input_output.File(filename)
        tail.tail()

    def _test_cli(self):
        print('Test')


class _Install(object):
    """Class processes CLI 'install' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        subparsers.add_parser(
            'install',
            help=textwrap.fill(
                'Build and installs switchmap-ng dependencies.', width=width)
        )


class _Logs(object):
    """Class processes CLI 'log' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        parser = subparsers.add_parser(
            'logs',
            help=textwrap.fill(
                'Read the most recent entries in a log file. '
                'Equivalent to Linux "tail -f" command.', width=width)
        )

        # Tail the API logs
        parser.add_argument(
            '--api',
            help=textwrap.fill(
                'View most recent entries in the API log file.', width=width),
            action='store_true')

        # Tail the poller logs
        parser.add_argument(
            '--poller',
            help=textwrap.fill(
                'View most recent entries in the poller log file.'
                '', width=width),
            action='store_true')

class _Daemon(object):
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
        daemons = ['switchmap-ng-api', 'switchmap-ng-poller']
        for daemon in daemons:

            running = self._running(daemon)

            # Prompt to restart if already running
            if running is True:
                restart = input(
                    '\nINPUT - Daemon {} is running. Restart? [Y/n] '
                    ''.format(daemon))
                if bool(restart) is False:
                    self._restart(daemon)
                    setup.print_ok(
                        'Successfully restarted daemon {}.'.format(daemon))
                elif restart[0].lower() != 'n':
                    self._restart(daemon)
                    setup.print_ok(
                        'Successfully restarted daemon {}.'.format(daemon))
                else:
                    setup.print_ok(
                        'Leaving daemon {} unchanged.'.format(daemon))
            else:
                self._start(daemon)
                setup.print_ok(
                    'Successfully started daemon {}.'.format(daemon))

    def _restart(self, daemon):
        """Start or restart daemon.

        Args:
            daemon: Name of daemon

        Returns:
            None

        """
        # restart
        self._start(daemon, restart=True)

    def _start(self, daemon, restart=False):
        """Start or restart daemon.

        Args:
            daemon: Name of daemon
            restart: Restart if True

        Returns:
            None

        """
        # Initialize key variables
        running = False
        if restart is True:
            attempt = 'restart'
        else:
            attempt = 'start'

        # Get status
        _root_directory = general.root_directory()
        if restart is False:
            script_name = '{}/bin/{} --start'.format(_root_directory, daemon)
        else:
            script_name = (
                '{}/bin/{} --restart --force'.format(_root_directory, daemon))

        # Attempt to restart / start
        response = _run_script(script_name)
        if bool(response['error_code']) is True:
            log_message = ('Could not {} daemon {}.'.format(attempt, daemon))
            log.log2see_safe(1032, log_message)

        # Return
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

        # Get status
        _root_directory = general.root_directory()
        script_name = '{}/bin/{} --status'.format(_root_directory, daemon)
        response = _run_script(script_name)
        for key, value in response.items():
            if key == 'output':
                if 'running' in str(value).lower():
                    running = True

        # Return
        return running


class _Config(object):
    """Class to test setup."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Do key import
        import yaml

        # Initialize key variables
        valid_directories = []
        config = ("""\
main:
    agent_subprocesses: 20
    bind_port: 7000
    cache_directory:
    hostnames:
      - 1.1.1.1
    listen_address: localhost
    log_directory:
    log_level: debug
    polling_interval: 3600

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
""")
        self.config_dict = yaml.load(config)
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
                if filename.endswith('.yaml'):
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
                        if _sub_key == 'hostnames':
                            # Add newly found hostnames to the
                            # list without duplicates
                            found_hostnames = value
                            existing_hostnames = self.config_dict[
                                _file_key][_sub_key]
                            for hostname in found_hostnames:
                                if hostname not in existing_hostnames:
                                    self.config_dict[_file_key][
                                        _sub_key].append(hostname)
                        else:
                            # Extend other lists that may have been found
                            self.config_dict[
                                _file_key][_sub_key].extend(value)

            elif isinstance(_file_value, list) is True:
                # Process 'snmp_groups:' key
                if _file_key == 'snmp_groups':
                    for item in _file_value:
                        if _snmp_group_found(
                                item, self.config_dict[_file_key]) is False:
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
        # Do key import
        import yaml

        # Initialize key variables
        directory = self.directories[0]

        # Update configuration file if required
        for next_directory in self.directories:
            # Delete all YAML files in the configuration directory
            general.delete_yaml_files(next_directory)

        # Write config back to directory
        filepath = ('%s/config.yaml') % (directory)
        with open(filepath, 'w') as outfile:
            yaml.dump(self.config_dict, outfile, default_flow_style=False)

            # Write status Update
            setup.print_ok('Created configuration file {}.'.format(filepath))


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
        # Find pip3 executable
        cli_string = 'which pip3'
        response = _run_script(cli_string)

        # Not OK if not fount
        if bool(response['error_code']) is True:
            log_message = ('python pip3 not installed.')
            log.log2die_safe(1094, log_message)
        else:
            log_message = 'Python pip3 executable found.'
            setup.print_ok(log_message)

            # install pip3 modules
            modules = ['setuptools', 'PyYAML']
            for module in modules:
                _pip3_install(module)

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
                'Required python version must be >= {}.{}. '
                'Python version {}.{} installed'
                ''.format(major, minor, major_installed, minor_installed))
            log.log2die_safe(1095, log_message)
        else:
            log_message = (
                'Python version {}.{}.'
                ''.format(major_installed, minor_installed))
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
        line = '*' * 80

        prefix = """\
Edit file {}/etc/config.yaml with correct SNMP parameters \
and then restart the daemons.\n""".format(general.root_directory())

        # Give suggestions as to what to do
        if username == 'root':
            suggestions = """{}
You can restart switchmap-ng daemons with these commands:

    # systemctl restart switchmap-ng-web.service
    # systemctl restart switchmap-ng-poller.service

You can enable switchmap-ng daemons to start on system boot \
with these commands:

    # systemctl enable switchmap-ng-web.service
    # systemctl enable switchmap-ng-poller.service""".format(prefix)
        else:
            suggestions = """{}
You can restart switchmap-ng daemons with these commands:

    $ bin/switchmap-ng-api --restart
    $ bin/switchmap-ng-poller --restart

Switchmap-NG will not automatically restart after a reboot. \
You need to re-install as the "root" user for this to occur.""".format(prefix)

        print('{}\n{}\n{}'.format(line, suggestions, line))

        # All done
        setup.print_ok(
            'Installation complete, pending changes mentioned above.')


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
        if next_item['group_name'] == item['group_name']:
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
    # Determine version of pip3
    cli_string = 'pip3 --version'
    response = os.popen(cli_string).read()
    version = response.split()[1]

    # Attempt to install module
    if version < '9.0.0':
        cli_string = 'pip3 list | grep {}'.format(module)
    else:
        cli_string = 'pip3 list --format columns | grep {}'.format(module)
    response = bool(os.popen(cli_string).read())

    if response is False:
        # YAML is not installed try to install it
        cli_string = 'pip3 install --user {}'.format(module)
        response_install = _run_script(cli_string)

        # Fail if module cannot be installed
        if bool(response_install['error_code']) is True:
            log_message = ('python pip3 cannot install "{}".'.format(module))
            log.log2die_safe(1100, log_message)
        else:
            log_message = (
                'Python module "{}" is installed.'.format(module))
            setup.print_ok(log_message)
    else:
        log_message = 'Python module "{}" is installed.'.format(module)
        setup.print_ok(log_message)


def _run_script(cli_string, shell=False):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        cli_string: Command to run on the CLI
        die: Die if command runs with an error

    Returns:
        None

    """
    # Initialize key variables
    data = {}

    # Create the subprocess object
    if shell is False:
        do_command_list = list(cli_string.split(' '))
        process = subprocess.Popen(
            do_command_list,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(
            cli_string,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    stdoutdata, _ = process.communicate()
    returncode = process.returncode

    # Return
    data = {
        'output': stdoutdata.decode(),
        'error_code': returncode
    }
    return data


if __name__ == '__main__':
    # Run main
    main()
