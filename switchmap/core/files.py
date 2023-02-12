"""Switchmap files library."""

import os
import sys
import subprocess

# PIP imports
import yaml

# Application libraries
from switchmap.core import log


class _Directory:
    """A class for creating the names of hidden directories."""

    def __init__(self, config):
        """Initialize the class.

        Args:
            config: Config object

        Returns:
            None

        """
        # Initialize key variables
        self._system_root = config.daemon_directory()

    def pid(self):
        """Define the hidden pid directory.

        Args:
            None

        Returns:
            value: pid directory

        """
        # Return
        value = "{}{}pid".format(self._system_root, os.sep)
        return value

    def lock(self):
        """Define the hidden lock directory.

        Args:
            None

        Returns:
            value: lock directory

        """
        # Return
        value = "{}{}lock".format(self._system_root, os.sep)
        return value

    def snmp(self):
        """Method for defining the hidden snmp directory.

        Args:
            None

        Returns:
            value: snmp directory

        """
        # Return
        value = "{}{}snmp".format(self._system_root, os.sep)
        return value


class _File:
    """A class for creating the names of hidden files."""

    def __init__(self, config):
        """Initialize the class.

        Args:
            config: Config object

        Returns:
            None

        """
        # Initialize key variables
        self._directory = _Directory(config)

    def pid(self, prefix):
        """Define the hidden pid directory.

        Args:
            prefix: Prefix of file

        Returns:
            value: pid directory

        """
        # Return
        mkdir(self._directory.pid())
        value = "{}{}{}.pid".format(self._directory.pid(), os.sep, prefix)
        return value

    def lock(self, prefix):
        """Define the hidden lock directory.

        Args:
            prefix: Prefix of file

        Returns:
            value: lock directory

        """
        # Return
        mkdir(self._directory.lock())
        value = "{}{}{}.lock".format(self._directory.lock(), os.sep, prefix)
        return value

    def snmp(self, prefix, create=True):
        """Method for defining the hidden snmp directory.

        Args:
            prefix: Prefix of file
            create: Create file if True

        Returns:
            value: snmp directory

        """
        # Return
        if create is True:
            mkdir(self._directory.snmp())
        value = "{}{}{}.snmp".format(self._directory.snmp(), os.sep, prefix)
        return value


def read_yaml_files(directories):
    """Read the contents of all yaml files in a directory.

    Args:
        directories: List of directory names with configuration files

    Returns:
        config_dict: Dict of yaml read

    """
    # Initialize key variables
    yaml_found = False
    yaml_from_file = ""
    all_yaml_read = ""

    # Check each directory in sequence
    for config_directory in directories:
        # Check if config_directory exists
        if os.path.isdir(config_directory) is False:
            log_message = (
                'Configuration directory "{}" '
                "doesn't exist!".format(config_directory)
            )
            log.log2die_safe(1009, log_message)

        # Cycle through list of files in directory
        for filename in os.listdir(config_directory):
            # Examine all the '.yaml' files in directory
            if filename.endswith(".yaml"):
                # Read YAML data
                filepath = "{}/{}".format(config_directory, filename)
                yaml_from_file = read_yaml_file(filepath, as_string=True)
                yaml_found = True

                # Append yaml from file to all yaml previously read
                all_yaml_read = "{}\n{}".format(all_yaml_read, yaml_from_file)

        # Verify YAML files found in directory
        if yaml_found is False:
            log_message = (
                'No files found in directory "{}" with ".yaml" '
                "extension.".format(config_directory)
            )
            log.log2die_safe(1010, log_message)

    # Return
    config_dict = yaml.safe_load(all_yaml_read)
    return config_dict


def read_yaml_file(filepath, as_string=False, die=True):
    """Read the contents of a YAML file.

    Args:
        filepath: Path to file to be read
        as_string: Return a string if True
        die: Die if there is an error

    Returns:
        result: Dict of yaml read

    """
    # Initialize key variables
    if as_string is False:
        result = {}
    else:
        result = ""

    # Read file
    if filepath.endswith(".yaml"):
        # Get result
        if as_string is False:
            try:
                with open(filepath, "r") as yaml_from_file:
                    result = yaml.safe_load(yaml_from_file)
            except:
                log_message = (
                    "Error reading file {}. Check permissions, "
                    "existence and file syntax."
                    "".format(filepath)
                )
                if bool(die) is True:
                    log.log2die_safe(1001, log_message)
                else:
                    log.log2debug(1002, log_message)
                    return {}

        else:
            try:
                with open(filepath, "r") as file_handle:
                    result = file_handle.read()
            except:
                log_message = (
                    "Error reading file {}. Check permissions, "
                    "existence and file syntax."
                    "".format(filepath)
                )
                if bool(die) is True:
                    log.log2die_safe(2006, log_message)
                else:
                    log.log2debug(1056, log_message)
                    return {}

    else:
        # Die if not a YAML file
        log_message = "{} is not a YAML file.".format(filepath)
        if bool(die) is True:
            log.log2die_safe(1164, log_message)
        else:
            log.log2debug(1047, log_message)
            if bool(as_string) is False:
                return {}
            else:
                return ""

    # Return
    return result


def mkdir(directory):
    """Create a directory if it doesn't already exist.

    Args:
        directory: Directory name

    Returns:
        None

    """
    # Do work
    if os.path.exists(directory) is False:
        try:
            os.makedirs(directory, mode=0o775)
        except:
            log_message = "Cannot create directory {}." "".format(directory)
            log.log2die(1121, log_message)

    # Fail if not a directory
    if os.path.isdir(directory) is False:
        log_message = "{} is not a directory." "".format(directory)
        log.log2die(1158, log_message)


def pid_file(agent_name, config):
    """Get the pidfile for an agent.

    Args:
        agent_name: Agent name
        config: Config object

    Returns:
        result: Name of pid file

    """
    # Return
    f_obj = _File(config)
    result = f_obj.pid(agent_name)
    return result


def lock_file(agent_name, config):
    """Get the lockfile for an agent.

    Args:
        agent_name: Agent name
        config: Config object

    Returns:
        result: Name of lock file

    """
    # Return
    f_obj = _File(config)
    result = f_obj.lock(agent_name)
    return result


def snmp_file(hostname, config):
    """Get the snmpfile for an agent.

    Args:
        hostname: hostname
        config: Config object

    Returns:
        result: Name of snmp file

    """
    # Return
    f_obj = _File(config)
    result = f_obj.snmp(hostname)
    return result


def execute(command, die=True):
    """Run the command UNIX CLI command and record output.

    Args:
        command: CLI command to execute
        die: Die if errors found

    Returns:
        returncode: Return code of command execution

    """
    # Initialize key variables
    messages = []
    stdoutdata = "".encode()
    stderrdata = "".encode()
    returncode = 1

    # Run update_targets script
    do_command_list = list(command.split(" "))

    # Create the subprocess object
    try:
        process = subprocess.Popen(
            do_command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdoutdata, stderrdata = process.communicate()
        returncode = process.returncode
    except:
        (etype, evalue, etraceback) = sys.exc_info()
        log_message = """\
Command failure: [Exception:{}, Exception Instance: {}, Stack Trace: {}]\
""".format(
            etype, evalue, etraceback
        )
        log.log2warning(1161, log_message)

    # Crash if the return code is not 0
    if returncode != 0:
        # Print the Return Code header
        messages.append("Return code:{}".format(returncode))

        # Print the STDOUT
        for line in stdoutdata.decode().split("\n"):
            messages.append("STDOUT: {}".format(line))

        # Print the STDERR
        for line in stderrdata.decode().split("\n"):
            messages.append("STDERR: {}".format(line))

        # Log message
        for log_message in messages:
            log.log2warning(1153, log_message)

        # Die if required after error found
        if bool(die) is True:
            log.log2die(1044, "Command Failed: {}".format(command))

    # Return
    return returncode


def config_filepath():
    """Get the configuration filename.

    Args:
        None

    Returns:
        result: Filename

    """
    # Get the directory of the switchmap library
    directory = log.check_environment()
    result = "{}{}config.yaml".format(directory, os.sep)
    return result
