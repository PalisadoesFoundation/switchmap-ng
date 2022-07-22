"""Module with general purpose functions."""

import sys
import getpass
import os
import random
import re
import ipaddress as ipaddress_

# Application libraries
from switchmap.core import log
from switchmap import Config
from switchmap import IP


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
        result: Fixed mac address

    """
    # Initialize key variables
    result = ""

    if isinstance(_mac, str):
        regex = re.compile("[^a-fA-F0-9]")
        result = regex.sub("", _mac)[:12].lower()
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
