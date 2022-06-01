#!/usr/bin/env python3
"""Switchmap files library."""

import os
import time
import sys
from random import random
import subprocess

# PIP imports
import yaml

# Pattoo libraries
from switchmap.core import log
from switchmap.core import data


class _Directory():
    """A class for creating the names of hidden directories."""

    def __init__(self, config):
        """Initialize the class.

        Args:
            config: Config object

        Returns:
            None

        """
        # Initialize key variables
        self._root = config.daemon_directory()
        self._system_root = config.system_daemon_directory()
        self._cache = config.cache_directory()

    def pid(self):
        """Define the hidden pid directory.

        Args:
            None

        Returns:
            value: pid directory

        """
        # Return
        value = '{}{}pid'.format(self._system_root, os.sep)
        return value

    def lock(self):
        """Define the hidden lock directory.

        Args:
            None

        Returns:
            value: lock directory

        """
        # Return
        value = '{}{}lock'.format(self._system_root, os.sep)
        return value

    def agent_id(self):
        """Define the hidden agent_id directory.

        Args:
            None

        Returns:
            value: agent_id directory

        """
        # Return
        value = '{}{}agent_id'.format(self._root, os.sep)
        return value


class _File():
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
        value = '{}{}{}.pid'.format(self._directory.pid(), os.sep, prefix)
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
        value = '{}{}{}.lock'.format(self._directory.lock(), os.sep, prefix)
        return value

    def agent_id(self, agent_name):
        """Define the hidden agent_id directory.

        Args:
            agent_name: Agent name

        Returns:
            value: agent_id directory

        """
        # Return
        mkdir(self._directory.agent_id())
        value = ('''{}{}{}.agent_id\
'''.format(self._directory.agent_id(), os.sep, agent_name))
        return value


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
        result = ''

    # Read file
    if filepath.endswith('.yaml'):
        try:
            with open(filepath, 'r') as file_handle:
                yaml_from_file = file_handle.read()
        except:
            log_message = (
                'Error reading file {}. Check permissions, '
                'existence and file syntax.'
                ''.format(filepath))
            if bool(die) is True:
                log.log2die_safe(1006, log_message)
            else:
                log.log2debug(1014, log_message)
                return {}

        # Get result
        if as_string is False:
            try:
                result = yaml.safe_load(yaml_from_file)
            except:
                log_message = (
                    'Error reading file {}. Check permissions, '
                    'existence and file syntax.'
                    ''.format(filepath))
                if bool(die) is True:
                    log.log2die_safe(1001, log_message)
                else:
                    log.log2debug(1002, log_message)
                    return {}
        else:
            result = yaml_from_file

    else:
        # Die if not a YAML file
        log_message = '{} is not a YAML file.'.format(filepath)
        if bool(die) is True:
            log.log2die_safe(1065, log_message)
        else:
            log.log2debug(1005, log_message)
            if bool(as_string) is False:
                return {}
            else:
                return ''

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
            log_message = (
                'Cannot create directory {}.'
                ''.format(directory))
            log.log2die(1090, log_message)

    # Fail if not a directory
    if os.path.isdir(directory) is False:
        log_message = (
            '{} is not a directory.'
            ''.format(directory))
        log.log2die(1043, log_message)


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


def agent_id_file(agent_name, config):
    """Get the agent_idfile for an agent.

    Args:
        agent_name: Agent name
        config: Config object


    Returns:
        result: Name of agent_id file

    """
    # Return
    f_obj = _File(config)
    result = f_obj.agent_id(agent_name)
    return result


def get_agent_id(agent_name, config):
    """Create a permanent UID for the agent_name.

    Args:
        agent_name: Agent name
        config: Config object

    Returns:
        agent_id: UID for agent

    """
    # Initialize key variables
    filename = agent_id_file(agent_name, config)

    # Read environment file with UID if it exists
    if os.path.isfile(filename):
        with open(filename) as f_handle:
            agent_id = f_handle.readline()
    else:
        # Create a UID and save
        agent_id = _generate_agent_id()
        with open(filename, 'w+') as env:
            env.write(str(agent_id))

    # Return
    return agent_id


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
    stdoutdata = ''.encode()
    stderrdata = ''.encode()
    returncode = 1

    # Run update_targets script
    do_command_list = list(command.split(' '))

    # Create the subprocess object
    try:
        process = subprocess.Popen(
            do_command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate()
        returncode = process.returncode
    except:
        (etype, evalue, etraceback) = sys.exc_info()
        log_message = ('''\
Command failure: [Exception:{}, Exception Instance: {}, Stack Trace: {}]\
'''.format(etype, evalue, etraceback))
        log.log2warning(1052, log_message)

    # Crash if the return code is not 0
    if returncode != 0:
        # Print the Return Code header
        messages.append(
            'Return code:{}'.format(returncode)
        )

        # Print the STDOUT
        for line in stdoutdata.decode().split('\n'):
            messages.append(
                'STDOUT: {}'.format(line)
            )

        # Print the STDERR
        for line in stderrdata.decode().split('\n'):
            messages.append(
                'STDERR: {}'.format(line)
            )

        # Log message
        for log_message in messages:
            log.log2warning(1042, log_message)

        # Die if required after error found
        if bool(die) is True:
            log.log2die(1044, 'Command Failed: {}'.format(command))

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
    result = '{}{}config.yaml'.format(
        os.environ['SWITCHMAP_CONFIGDIR'], os.sep)
    return result


def _generate_agent_id():
    """Generate a UID.

    Args:
        None

    Returns:
        agent_id: the UID

    """
    # Create a UID and save
    prehash = '{}{}{}{}{}'.format(
        random(), random(), random(), random(), time.time())
    agent_id = data.hashstring(prehash)

    # Return
    return agent_id
