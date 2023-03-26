"""Module with general purpose functions."""

import sys
import getpass
import os
import random
import re
import ipaddress as ipaddress_
from copy import deepcopy

# PIP3 libraries
import more_itertools as mit

# Application libraries
from switchmap.core import log
from switchmap import IP
from switchmap import MacAddress


def check_user(config):
    """Check to make sure the user environment is correct.

    Args:
        config: Config object

    Returns:
        None

    """
    # Initialize key variables
    username = getpass.getuser()
    configured_username = config.username()

    # Prevent running as sudo user
    check_sudo()

    # Prevent others from running the script
    if username != configured_username:
        log_message = (
            "You can only run this script as user '{}' "
            "in the configuration file. Try running the command like this:\n"
            ""
        ).format(configured_username)
        print(log_message)
        fixed_command = "$ su -c '{}' {}\n".format(
            " ".join(sys.argv[:]), configured_username
        )
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
    if "SUDO_UID" in os.environ:
        log_message = 'Cannot run script using "sudo".'
        log.log2die(1108, log_message)


def cleanstring(data):
    """Remove multiple whitespaces and linefeeds from string.

    Args:
        data: String to process

    Returns:
        result: Stipped data

    """
    # Initialize key variables
    nolinefeeds = data.replace("\n", " ").replace("\r", "").strip()
    words = nolinefeeds.split()
    result = " ".join(words)

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
    octet_string = bytes_string.decode("utf-8")

    # Convert and return
    result = "".join(["%0.2x" % ord(_) for _ in octet_string])
    return result.lower()


def random_hash():
    """Create a random Hex hash.

    Args:
        None

    Returns:
        result: Hex hash

    """
    # create result and return
    result = "{:032X}".format(random.getrandbits(128))
    return result


def mac(_mac):
    """Convert MAC address to a standardized format.

    Args:
        _mac: MAC address

    Returns:
        result: MacAddress object

    """
    # Initialize key variables
    result = MacAddress(mac=_mac, valid=False)

    if isinstance(_mac, str):
        regex = re.compile("[^a-fA-F0-9]")
        mac_check = regex.sub("", _mac).lower()

        # Test validity
        if mac_check == "000000000000":
            valid = True
        else:
            try:
                # Test if Hex
                valid = bool(int(mac_check, 16))
            except:
                valid = False

        # Make sure the result is 12 characters
        if len(mac_check) != 12:
            valid = False

        if bool(valid) is True:
            result = MacAddress(mac=mac_check, valid=valid)

    return result


def root_directory():
    """Determine the root directory in which switchmap is installed.

    Args:
        None

    Returns:
        result: Root directory

    """
    # Get the directory of the switchmap library
    libdir = os.path.dirname(os.path.realpath(__file__))
    result = os.path.dirname(os.path.dirname(libdir))

    # Return
    return result


def ipaddress(_ip):
    """Validate an IP address.

    Args:
        _ip: IP address

    Returns:
        result: IP Object

    """
    # Initialize key variables
    valid = False
    address = None

    # Check validity
    try:
        meta = ipaddress_.ip_address(_ip)
        valid = True
    except ValueError:
        valid = False
    except:
        valid = False

    # Return
    if bool(valid) is False:
        result = None
    else:
        # Create IP record
        address = meta.exploded.lower()
        result = IP(address=address, version=meta.version)
    return result


def make_bool(result):
    """Create a boolean version of the argument.

    Args:
        result: Object to transform

    Returns:
        result: boolean

    """
    # Process
    if result is None:
        result = False
    elif result is False:
        pass
    elif isinstance(result, str):
        if result.lower() == "none":
            result = False
        elif result.lower() == "false":
            result = False
        elif result.lower() == "true":
            result = True
    return bool(result)


def consistent_keys(_data):
    """Convert dict keys to ints if possible.

    Args:
        _data: Multidimensional dict

    Returns:
        result: dict

    """
    # Initialize key variables
    result = {}
    _data = deepcopy(_data)

    # Recursively get data
    for key, value in _data.items():
        if isinstance(value, dict):
            walk_result = consistent_keys(value)
            result[key] = _key_to_int(walk_result)
        else:
            result[key] = value

    # Return
    return result


def _key_to_int(_data):
    """Convert dict keys to ints if possible.

    Args:
        _data: dict

    Returns:
        result: dict

    """
    # Initialize key variables
    result = {}
    _data = deepcopy(_data)

    if isinstance(_data, dict):
        for key, value in _data.items():
            try:
                fixed_key = int(key)
            except:
                fixed_key = key
            result[fixed_key] = value
    else:
        result = _data
    return result


def group_consecutive(data):
    """Group consecutive numbers in a list.

    https://stackoverflow.com/questions/2154249/
        identify-groups-of-consecutive-numbers-in-a-list

    Args:
        data: list

    Returns:
        ranges: List of lists

    """
    # Initialize key variables
    if bool(isinstance(data, list)) is False:
        data = [data]

    # Return
    ranges = list(_find_ranges(data))
    return ranges


def _find_ranges(iterable):
    """Yield range of consecutive numbers."""
    for group in mit.consecutive_groups(sorted(set(iterable))):
        group = list(group)
        if len(group) == 1:
            yield group[0]
        else:
            yield group[0], group[-1]


def human_readable(num, suffix="B", storage=False):
    """Convert number to human readable value.

    https://stackoverflow.com/questions/1094841/
        get-human-readable-version-of-file-size

    Args:
        num: Number to convert

    Returns:
        result: Numeric string

    """
    # Initialize key variables
    if bool(storage) is True:
        limit = 1024
    else:
        limit = 1000

    # Process
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < limit:
            return f"{num:3.1f}{unit}{suffix}"
        num /= limit
    result = f"{num:.1f}Yi{suffix}"
    return result


def padded_list_of_lists(data, width=4, pad=None):
    """Create a padded list of list.

    Args:
        data: List to process
        width: Width of the list of lists
        pad: Value to pad the last row of the list of lists with

    Returns:
        result: list of lists

    """
    # Create a list of lists of width 'width'
    result = [data[i : i + width] for i in range(0, len(data), width)]

    # Make sure each row is at lease max_colums wide. Pad with "" values if not
    for key, value in enumerate(result):
        result[key] = value + [pad] * (width - len(value))

    return result
