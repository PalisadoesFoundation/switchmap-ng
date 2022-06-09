"""Module for handling data required for testing."""

# Import libraries
from io import StringIO
import yaml

_CONFIG_YAML = '''
main:
  bind_port: 7000
  daemon_directory: XXX
  hostnames:
  - unittest.example.org
  listen_address: localhost
  log_directory: XXX
  log_level: debug
  polling_interval: 21600
  username: switchmap
  db_host: localhost
  db_name: switchmap_unittests
  db_user: travis
  db_pass: ABC123
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
'''

_POLLED_DATA_YAML = '''
'''


def config():
    """Convert the config YAML to a dict.

    Args:
        None

    Returns:
        result

    """
    # Return
    return _dict(_CONFIG_YAML)


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
