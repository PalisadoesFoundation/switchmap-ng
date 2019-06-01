#!/usr/bin/env python3
"""switchmap CLI classes for 'test'.

Functions to test poller

"""

# Main python libraries
import sys

# Switchmap-NG imports
from switchmap.utils import general
from switchmap.constants import CONFIG_SNMP, CONFIG
from switchmap.utils import log
from switchmap.snmp import snmp_manager


def run(args):
    """Process 'test' command.

    Args:
        parser: Argparse parser
        args: Argparse arguments

    Returns:
        None

    """
    # Process the config
    snmp_config = CONFIG_SNMP
    config = CONFIG

    # Show help if no arguments provided
    if args.qualifier is None:
        general.cli_help()

    # Test a single host
    if bool(args.hostname) is True:
        hostname = args.hostname
        test_hostname(hostname, snmp_config)
        sys.exit(0)

    # Test all hosts
    elif bool(args.all) is True:
        hosts = config.hostnames()
        if isinstance(hosts, list) is True:
            if len(hosts) > 0:
                for host in hosts:
                    test_hostname(host, snmp_config)
                sys.exit(0)
            else:
                # No hosts found
                log_message = 'No hosts found in configuration'
                log.log2see(1038, log_message)

        else:
            # No hosts found
            log_message = 'No hosts found in configuration'
            log.log2see(1039, log_message)

    # Show help if there are no matches
    general.cli_help()


def test_hostname(hostname, snmp_config):
    """Process 'test poller --hostname' commands.

    Args:
        args: Argparse arguments

    Returns:
        None

    """
    # Show host information
    validate = snmp_manager.Validate(hostname, snmp_config.snmp_auth())
    snmp_params = validate.credentials()

    if bool(snmp_params) is True:
        print(
            'OK - Valid credentials found, successfully contacted: {}'
            ''.format(hostname))
    else:
        # Error, host problems
        log_message = (
            'Uncontactable host {} or no valid SNMP '
            'credentials found for it.'.format(hostname))
        log.log2see(1040, log_message)
