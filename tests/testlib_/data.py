"""Module for handling data required for testing."""

# Import libraries
import random
from collections import namedtuple
from string import ascii_uppercase
from io import StringIO
from copy import deepcopy
import os
import binascii
import socket
import struct

import yaml

_CONFIG_YAML = """
core:
  system_directory: XXX
  log_directory: YYY
  log_level: debug
  polling_interval: 21600
  username: switchmap
server:
  bind_port: 9000
  listen_address: localhost
  db_host: localhost
  db_name: switchmap_unittest
  db_user: travis
  db_pass: 7F4Gj7HJIDT5xJPs
poller:
  bind_port: 9001
  listen_address: localhost
  hostnames:
    - unittest-01.example.org
    - unittest-02.example.org
  snmp_groups:
    - group_name: h55wJy4JkfSJnhZT
      snmp_authpassword: v29AbLMwxu7gnGyz
      snmp_authprotocol: sha
      snmp_community: null
      snmp_port: 161
      snmp_privpassword: sh4gPe7MKG2dst2X
      snmp_privprotocol: aes
      snmp_secname: 76v4PjWHpDmzy6cx
      snmp_version: 3
"""

_CONFIG_TESTER_YAML = """
core:
  agent_subprocesses: 35
  log_level: info
  username: 7gnv2Mwxu9AbLGyz
  log_directory: YYY
  system_directory: XXX

server:
  bind_port: 7027
  listen_address: MKG2dst7sh4gPe2X
  db_host: Mwxu7gnv29AbLGyz
  db_name: JkfSJnhZTh55wJy4
  db_user: 7MKG2dstsh4gPe2X
  db_pass: nhZThsh4gPMwxu75

dashboard:
  bind_port: 8034
  listen_address: t7sh4gPe2XMKG2ds

poller:
  ingest_interval: 98712
  polling_interval: 21600
  server_address: bwSeAzPmAygg8rcJ
  server_bind_port: 9876
  server_username: null
  server_password: None
  server_https: False
  zones:
    - zone: SITE-A
      hostnames:
        - hostname1
        - hostname2
        - hostname3
    - zone: SITE-B
      hostnames:
        - hostnameA
        - hostnameB
        - hostnameC
    - zone: SITE-C
      hostnames:
    - zone:
  snmp_groups:
    - group_name: zg8rcJPmAygbwSeA
      snmp_authpassword: Gnn5999YqCMbre9W
      snmp_authprotocol: sha
      snmp_community: null
      snmp_port: 161
      snmp_privpassword: Jgt8MFTEhyh9s2ju
      snmp_privprotocol: aes
      snmp_secname: NT9degJu9NBWbxRK
      snmp_version: 3
    - group_name: PmAygbwzg8rcJSeA
      snmp_authpassword: 9YqCMGnn599bre9W
      snmp_authprotocol: sha
      snmp_community: null
      snmp_port: 3456
      snmp_privpassword: FTEhyh9sJgt8M2ju
      snmp_privprotocol: aes
      snmp_secname: degJu9NNT9BWbxRK
      snmp_version: 2

"""


def configtester():
    """Convert the config YAML to a dict.

    Args:
        None

    Returns:
        result

    """
    # Return
    return _dict(_CONFIG_TESTER_YAML)


def config():
    """Convert the config YAML to a dict.

    Args:
        None

    Returns:
        result

    """
    # Return
    return _dict(_CONFIG_YAML)


def polled_data(strip=True):
    """Read the test data file into a dict.

    The YAML file was created from a dump of the SNMP dict created
    from polling a device. It therefore has keys that this application adds for
    ease of processing. Most notably Layer 1 keys that start with 'l1_'

    Args:
        strip: Strip l1 keys if True

    Returns:
        result

    """
    # Read test data file
    filepath = "{0}{1}testdata_{1}device-01.yaml".format(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.sep
    )
    with open(filepath, "r") as stream:
        item = yaml.safe_load(stream)

    # Convert all the integer string keys to integer
    result = _walk_dict(item)

    # Remove all the extraneous L1 keys that start with 'l1_'
    if bool(strip) is True:
        for ifindex, ifdata in result["layer1"].items():
            if isinstance(ifdata, dict) is True:
                newifdata = {}
                for key, value in ifdata.items():
                    # L1_macs is not a calculated field from other L1 data.
                    # So it must remain.
                    if key == "l1_macs":
                        newifdata[key] = value

                    # Remove all other 'l1_' keys
                    if key.startswith("l1_") is False:
                        newifdata[key] = value
                result["layer1"][ifindex] = newifdata

    # Return
    return result


def random_string(length=10):
    """Create a random string.

    Args:
        length: Desired string length

    Returns:
        result: Random string of "length"

    """
    # Return
    result = "".join(random.choice(ascii_uppercase) for i in range(length))
    return result


def _dict(item):
    """Convert YAML to a dict.

    Args:
        item: String to convert to a dict

    Returns:
        result: dict

    """
    # Return
    with StringIO(item) as _stream:
        result = yaml.safe_load(_stream)
    return result


def _walk_dict(_data):
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
            walk_result = _walk_dict(value)
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


def mac():
    """Generate a random mac address.

    Args:
        None

    Returns:
        result: Mac address

    """
    # Return
    result = binascii.b2a_hex(os.urandom(30)).decode()[:12]
    return result


def ipv4():
    """Generate a random IPv4 address.

    Args:
        None

    Returns:
        result: IPv4 address

    """
    # Return
    result = socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xFFFFFFFF)))
    return result


def ipv6():
    """Generate a random IPv6 address.

    Args:
        None

    Returns:
        result: IPv6 address

    """
    # Return
    bits = 16**4
    result = ":".join(
        ("{:02x}".format(random.randint(0, bits)).zfill(4) for i in range(8))
    )
    return result


def ip_():
    """Generate a random IPv6 / IPv4 address.

    Args:
        None

    Returns:
        result: IP object

    """
    # Initialize key variables
    IP = namedtuple("IP", "address version")
    version = [4, 6][int(random.randint(0, 1))]
    if version == 4:
        result = IP(address=ipv4(), version=version)
    else:
        result = IP(address=ipv6(), version=version)
    return result
