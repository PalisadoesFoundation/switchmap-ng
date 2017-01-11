#!/usr/bin/env python

"""Calico utility script.
Calico utility script
"""

from pprint import pprint

from infoset.cli import jm_cli
from infoset.configuration import jm_configuration
from infoset.utils import jm_general
from infoset.snmp import poll
from infoset.snmp import snmp_manager
from infoset.snmp import snmp_info
from infoset.web import ws_device

import sys
import yaml


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

    # Process the CLI
    cli_object = jm_cli.Process(additional_help=additional_help)
    cli_args = cli_object.args()

    # Process the config
    config = jm_configuration.Read(cli_args.directory)

    # Show configuration data
    if cli_args.mode == 'config':
        do_config(cli_args, config)

    # Show interesting information
    if cli_args.mode == 'test':
        do_test(cli_args, config)

    # Process hosts
    if cli_args.mode == 'poll':
        do_poll(config, cli_args.verbose)

    # Create pages
    if cli_args.mode == 'pagemaker':
        do_pages(config, cli_args.verbose)


def do_config(cli_args, config):
    """Process 'config' CLI option.
    Args:
        connectivity_check: Set if testing for connectivity
    Returns:
        None
    """
    # Show hosts if required
    if cli_args.hosts is True:
        print('hosts:')
        print(yaml.dump(config.hosts(), default_flow_style=False))

    # Show hosts if required
    if cli_args.snmp_auth is True:
        print('snmp_auth:')
        print(yaml.dump(config.snmp_auth(), default_flow_style=False))


def do_test(cli_args, config):
    """Process 'test' CLI option.
    Args:
        connectivity_check: Set if testing for connectivity
    Returns:
        None
    """
    # Show host information
    validate = snmp_manager.Validate(cli_args.host, config.snmp_auth())
    snmp_params = validate.credentials()
    snmp_object = snmp_manager.Interact(snmp_params)

    if bool(snmp_params) is True:
        print('\nValid credentials found:\n')
        print(yaml.dump(snmp_params, default_flow_style=False))
        print('\n')

        # Get SNMP data and print
        status = snmp_info.Query(snmp_object)
        yaml_data = status.everything()
        print(yaml_data)
    else:
        # Error, host problems
        log_message = (
            'Uncontactable host %s or no valid SNMP '
            'credentials found for it.') % (cli_args.host)
        jm_general.log2die(1026, log_message)


def do_pages(config, verbose=False):
    """Process 'pagemaker' CLI option.
    Args:
        config: Configuration object
        verbose: Verbose output if True
    Returns:
        None
    """
    # Poll
    ws_device.make(config, verbose)


def do_poll(config, verbose=False):
    """Process 'run' CLI option.
    Args:
        config: Configuration object
        verbose: Verbose output if True
    Returns:
        None
    """
    # Poll
    poll.snmp(config, verbose)

def do_rrd_create(config, verbose):
    print("rrd")

if __name__ == "__main__":
    main()
