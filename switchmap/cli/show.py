#!/usr/bin/env python3
"""switchmap CLI funtions for 'show'.

Functions to show operational data

"""

# Main python libraries
import sys
from pprint import pprint

# Switchmap-NG imports
from switchmap.constants import CONFIG
from switchmap.utils import input_output
from switchmap.utils import general
from switchmap.main.agent import Agent, AgentAPI, AgentDaemon
from switchmap.constants import (
    API_EXECUTABLE, API_GUNICORN_AGENT, POLLER_EXECUTABLE)


def run(args):
    """Process 'show' command.

    Args:
        args: Argparse arguments

    Returns:
        None

    """
    # Show help if no arguments provided
    if args.qualifier is None:
        general.cli_help()

    # Process 'show api' command
    if args.qualifier == 'api':
        api(args)
    elif args.qualifier == 'poller':
        poller(args)
    elif args.qualifier == 'hostnames':
        _hostnames()
    elif args.qualifier == 'configuration':
        _configuration()

    # Show help if there are no matches
    general.cli_help()


def _hostnames():
    """Process 'show hostnames' commands.

    Args:
        None

    Returns:
        None

    """
    config = CONFIG
    _hostnames = config.hostnames()
    for _hostname in _hostnames:
        print(_hostname)

    # Done
    sys.exit(0)


def _configuration():
    """Process 'show hostnames' commands.

    Args:
        None

    Returns:
        None

    """
    config = CONFIG
    contents = config.configuration()
    print('')
    pprint(contents, indent=2)
    print(
        '\n# Configuration read from directory: {}\n'
        ''.format(config.configuration_directory()))

    # Done
    sys.exit(0)


def api(args):
    """Process 'show api' commands.

    Args:
        args: Argparse arguments

    Returns:
        None

    """
    if args.subqualifier == 'logs':
        # Process logs
        config = CONFIG
        filename = config.web_log_file()
        tail = input_output.File(filename)
        tail.tail()

        # Done
        sys.exit(0)

    elif args.subqualifier == 'status':
        # Create agent objects
        agent_gunicorn = Agent(API_GUNICORN_AGENT)
        agent_api = AgentAPI(API_EXECUTABLE, API_GUNICORN_AGENT)

        # Get agent status
        daemon_gunicorn = AgentDaemon(agent_gunicorn)
        daemon_gunicorn.status()
        daemon_api = AgentDaemon(agent_api)
        daemon_api.status()

        # Done
        sys.exit(0)

    # Show help if there are no matches
    general.cli_help()


def poller(args):
    """Process 'show poller' commands.

    Args:
        args: Argparse arguments

    Returns:
        None

    """
    if args.subqualifier == 'logs':
        # Process logs
        config = CONFIG
        filename = config.log_file()
        tail = input_output.File(filename)
        tail.tail()

        # Done
        sys.exit(0)

    elif args.subqualifier == 'status':
        # Create agent objects
        agent_poller = Agent(POLLER_EXECUTABLE)

        # Get agent status
        daemon_poller = AgentDaemon(agent_poller)
        daemon_poller.status()

        # Done
        sys.exit(0)

    # Show help if there are no matches
    general.cli_help()
