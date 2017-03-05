#!/usr/bin/env python3
"""switchmap  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys

# Switchmap-NG imports
from switchmap.utils import configuration
from switchmap.utils import log
from switchmap.snmp import snmp_manager


def run(parser, args):
    """Process 'test' command.

    Args:
        parser: Argparse parser
        args: Argparse arguments

    Returns:
        None

    """
    # Process the config
    snmp_config = configuration.ConfigSNMP()
    config = configuration.Config()

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
                log.log2see(1026, log_message)

        else:
            # No hosts found
            log_message = 'No hosts found in configuration'
            log.log2see(1026, log_message)

    # Show help if there are no matches
    parser.print_help()
    sys.exit(2)


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
        print('Valid credentials found: {}'.format(hostname))
    else:
        # Error, host problems
        log_message = (
            'Uncontactable host %s or no valid SNMP '
            'credentials found for it.') % (hostname)
        log.log2see(1026, log_message)
