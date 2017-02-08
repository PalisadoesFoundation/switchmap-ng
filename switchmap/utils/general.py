#!/usr/bin/env python3
"""Switchmap-NG general library."""

import os
import subprocess
import locale
import json
import shutil

# PIP libraries
import yaml

# Switchmap-NG libraries
from switchmap.utils import log
from switchmap.utils import configuration
from switchmap import switchmap


def root_directory():
    """Getermine the root directory in which switchmap.is installed.

    Args:
        None

    Returns:
        root_dir: Root directory

    """
    # Get the directory of the switchmap library
    switchmap_dir = switchmap.__path__[0]
    components = switchmap_dir.split(os.sep)

    # Determint the directory two levels above
    root_dir = os.sep.join(components[0:-2])

    # Return
    return root_dir


def get_hosts():
    """Get hosts listed in toplogy YAML files.

    Args:
        None

    Returns:
        hosts: List of hostnames

    """
    # Read configuration
    hosts = []
    topology_directory = configuration.Config().topology_directory()

    # Cycle through list of files in directory
    for filename in os.listdir(topology_directory):
        if filename.endswith('.yaml'):
            hostname = filename[:-5]
            hosts.append(hostname)
    return sorted(hosts)


def read_yaml_file(filepath, as_string=False):
    """Read the contents of a YAML file.

    Args:
        filepath: Path to file to be read
        as_string: Return a string if True

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
                'Error reading file %s. Check permissions, '
                'existence and file syntax.'
                '') % (filepath)
            log.log2die_safe(1024, log_message)

        # Get result
        if as_string is False:
            result = yaml.load(yaml_from_file)
        else:
            result = yaml_from_file

    else:
        # Die if not a YAML file
        log_message = '{} is not a YAML file.'.format(filepath)
        log.log2die_safe(1065, log_message)

    # Return
    return result


def read_yaml_files(directories):
    """Read the contents of all yaml files in a directory.

    Args:
        directories: List of directory names with configuration files

    Returns:
        config_dict: Dict of yaml read

    """
    # Initialize key variables
    yaml_found = False
    yaml_from_file = ''
    all_yaml_read = ''

    # Check each directory in sequence
    for config_directory in directories:
        # Check if config_directory exists
        if os.path.isdir(config_directory) is False:
            log_message = (
                'Configuration directory "%s" '
                'doesn\'t exist!' % config_directory)
            log.log2die_safe(1009, log_message)

        # Cycle through list of files in directory
        for filename in os.listdir(config_directory):
            # Examine all the '.yaml' files in directory
            if filename.endswith('.yaml'):
                # Read YAML data
                filepath = ('%s/%s') % (config_directory, filename)
                yaml_from_file = read_yaml_file(filepath, as_string=True)
                yaml_found = True

                # Append yaml from file to all yaml previously read
                all_yaml_read = ('%s\n%s') % (all_yaml_read, yaml_from_file)

        # Verify YAML files found in directory
        if yaml_found is False:
            log_message = (
                'No files found in directory "%s" with ".yaml" '
                'extension.') % (config_directory)
            log.log2die_safe(1010, log_message)

    # Return
    config_dict = yaml.load(all_yaml_read)
    return config_dict


def dict2yaml(data_dict):
    """Convert a dict to a YAML string.

    Args:
        data_dict: Data dict to convert

    Returns:
        yaml_string: YAML output
    """
    # Process data
    json_string = json.dumps(data_dict)
    yaml_string = yaml.dump(yaml.load(json_string), default_flow_style=False)

    # Return
    return yaml_string


def run_script(cli_string, shell=False, die=True):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        cli_string: Command to run on the CLI
        die: Die if command runs with an error

    Returns:
        None

    """
    # Initialize key variables
    encoding = locale.getdefaultlocale()[1]
    header_returncode = ('[Return Code]')
    header_stdout = ('[Output]')
    header_stderr = ('[Error Message]')
    header_bad_cmd = ('[ERROR: Bad Command]')
    log_message = ''

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
    stdoutdata, stderrdata = process.communicate()
    returncode = process.returncode

    # Crash if the return code is not 0
    if die is True:
        if returncode != 0:
            # Print the Return Code header, Return Code, STDOUT header
            string2print = ('%s %s %s %s') % (
                header_bad_cmd, cli_string,
                header_returncode, returncode)
            log_message = ('%s%s') % (log_message, string2print)

            # Print the STDERR
            string2print = ('%s') % (header_stderr)
            log_message = ('%s %s') % (log_message, string2print)
            for line in stderrdata.decode(encoding).split('\n'):
                string2print = ('%s') % (line)
                log_message = ('%s %s') % (log_message, string2print)

            # Print the STDOUT
            string2print = ('%s') % (header_stdout)
            log_message = ('%s %s') % (log_message, string2print)
            for line in stdoutdata.decode(encoding).split('\n'):
                string2print = ('%s') % (line)
                log_message = ('%s %s') % (log_message, string2print)

            # All done
            log.log2die(1074, log_message)

    # Return
    return stdoutdata


def delete_files(directory, extension='.yaml'):
    """Delete all files of a specfic extension in a directory.

    Args:
        directory: Directory name
        extension: File extension

    Returns:
        None

    """
    # Determine whether directory is valid
    if os.path.isdir(directory) is False:
        log_message = ('Directory %s does not exist') % (directory)
        log.log2die_safe(1007, log_message)

    # Get list of files
    filelist = [
        next_file for next_file in os.listdir(
            directory) if next_file.endswith(extension)]

    # Delete files
    for delete_file in filelist:
        file_path = ('%s/%s') % (directory, delete_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as exception_error:
            log_message = ('Error: deleting files in %s. Error: %s') % (
                directory, exception_error)
            log.log2die_safe(1014, log_message)
        except:
            log_message = ('Unexpected error')
            log.log2die_safe(1006, log_message)


def delete_yaml_files(directory):
    """Delete all yaml files in a directory.

    Args:
        directory: Directory name

    Returns:
        None

    """
    # Delete files
    delete_files(directory, extension='.yaml')


def config_directories():
    """Get the directories where we expect to find configuration files.

    Args:
        None

    Returns:
        directories: List of directories

    """
    #####################################################################
    # Update the configuration directory
    # 'SWITCHMAP_CONFIGDIR' is used for setting a non-default config
    # directory location. A good example of this is using a new config
    # directory for unit testing
    #####################################################################
    if 'SWITCHMAP_CONFIGDIR' in os.environ:
        config_directory = os.environ['SWITCHMAP_CONFIGDIR']
    else:
        config_directory = ('%s/etc') % (root_directory())
    directories = [config_directory]

    # Return
    return directories


def cleanstring(data):
    """Remove multiple whitespaces and linefeeds from string.

    Args:
        data: String to process

    Returns:
        result: Stipped data

    """
    # Initialize key variables
    nolinefeeds = data.replace('\n', ' ').replace('\r', '').strip()
    words = nolinefeeds.split()
    result = ' '.join(words)

    # Return
    return result


def search_file(filename):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        filename: File to find

    Returns:
        result: Result

    """
    # Initialize key variables
    result = None
    search_path = os.environ['PATH']

    paths = search_path.split(os.pathsep)
    for path in paths:
        if os.path.exists(os.path.join(path, filename)) is True:
            result = os.path.abspath(os.path.join(path, filename))
            break

    # Return
    return result


def move_files(source_dir, target_dir):
    """Delete files in a directory.

    Args:
        source_dir: Directory where files are currently
        target_dir: Directory where files need to be

    Returns:
        Nothing

    """
    # Make sure source directory exists
    if os.path.exists(source_dir) is False:
        log_message = ('Directory %s does not exist.') % (
            source_dir)
        log.log2die(1435, log_message)

    # Make sure target directory exists
    if os.path.exists(target_dir) is False:
        log_message = ('Directory %s does not exist.') % (
            target_dir)
        log.log2die(1436, log_message)

    source_files = os.listdir(source_dir)
    for filename in source_files:
        full_path = ('%s/%s') % (source_dir, filename)
        if os.path.isfile(full_path) is True:
            shutil.move(full_path, target_dir)


def create_yaml_file(data_dict, filepath, ignore_blanks=True):
    """Initialize the class.

    Args:
        data_dict: Dictionary to write
        filepath: Name of output file
        ignore_blanks: Write file even if data_dict is empty

    Returns:
        None

    """
    # Determine whether file should be created
    if ignore_blanks is False and bool(data_dict) is True:
        return

    # Create file
    yaml_string = dict2yaml(data_dict)
    with open(filepath, 'w') as file_handle:
        file_handle.write(yaml_string)
