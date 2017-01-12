#!/usr/bin/env python3

"""switchmap-ng test script."""

# Standard imports
import sys
import argparse

# PIP3 imports

# Try regular imports
try:
    from switchmap.utils import log
except:
    print('You need to set your PYTHONPATH to include the switchmap library')
    sys.exit(2)
from switchmap.utils import configuration
from switchmap.snmp import snmp_manager


def main():
    """Main Function.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    additional_help = """\
Utility script for the project.
"""

    # Get CLI object
    cli_args = _cli(additional_help=additional_help)

    # Process the config
    snmp_config = configuration.ConfigSNMP()
    config = configuration.Config()

    # Test a single host
    if bool(cli_args.host) is True:
        do_test(cli_args.host, snmp_config)
        sys.exit(0)

    # Test all hosts
    if bool(cli_args.all_hosts) is True:
        hosts = config.hostnames()
        for host in hosts:
            do_test(host, snmp_config)


def do_test(host, snmp_config):
    """Test host connectivity.

    Args:
        host: Host to connectivity_check
        snmp_config: SNMP Configuration object

    Returns:
        None
    """
    # Show host information
    validate = snmp_manager.Validate(host, snmp_config.snmp_auth())
    snmp_params = validate.credentials()

    if bool(snmp_params) is True:
        print('Valid credentials found: {}'.format(host))
    else:
        # Error, host problems
        log_message = (
            'Uncontactable host %s or no valid SNMP '
            'credentials found for it.') % (host)
        log.log2see(1026, log_message)


def _cli(additional_help=None):
    """Return all the CLI options.

    Args:
        None

    Returns:
        args: Namespace() containing all of our CLI arguments as objects
            - filename: Path to the configuration file

    """
    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        description=additional_help,
        formatter_class=argparse.RawTextHelpFormatter)

    # CLI argument for starting
    parser.add_argument(
        '--host',
        required=False,
        default=False,
        type=str,
        help='Test a single configured host by name.'
    )

    # CLI argument for stopping
    parser.add_argument(
        '--all_hosts',
        required=False,
        default=False,
        action='store_true',
        help='Test all configured hosts.'
    )

    # Return parser object
    args = parser.parse_args()

    # Test to make sure valid arguments were passed
    if bool(args.all_hosts) is False and bool(args.host) is False:
        parser.print_help()
        sys.exit(0)

    return args


if __name__ == "__main__":
    main()
