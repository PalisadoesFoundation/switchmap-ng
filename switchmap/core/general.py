"""Module with general purpose functions."""

import sys
import getpass
import os
import random

# Application libraries
from switchmap.core import log
from switchmap import Config


def check_user():
    """Check to make sure the user environment is correct.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    username = getpass.getuser()
    config = Config()
    configured_username = config.username()

    # Prevent running as sudo user
    check_sudo()

    # Prevent others from running the script
    if username != configured_username:
        log_message = (
            'You can only run this script as user \'{}\' '
            'in the configuration file. Try running the command like this:\n'
            '').format(configured_username)
        print(log_message)
        fixed_command = (
            '$ su -c \'{}\' {}\n'.format(
                ' '.join(sys.argv[:]), configured_username))
        print(fixed_command)
        sys.exit(2)


def check_sudo():
    """Check user isn't running as sudo.

    Args:
        None

    Returns:
        None

    """
    # Prevent running as sudo user
    if 'SUDO_UID' in os.environ:
        log_message = (
            'Cannot run script using "sudo".')
        log.log2die(1108, log_message)


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


def octetstr_2_string(bytes_string):
    """Convert SNMP OCTETSTR to string.

    Args:
        bytes_string: Binary value to convert

    Returns:
        result: String equivalent of bytes_string

    """
    # Initialize key variables
    octet_string = bytes_string.decode('utf-8')

    # Convert and return
    result = ''.join(
        ['%0.2x' % ord(_) for _ in octet_string])
    return result.lower()


def random_hash():
    """Create a random Hex hash.

    Args:
        None

    Returns:
        result: Hex hash

    """
    # create result and return
    result = '{:032X}'.format(random.getrandbits(128))
    return result
