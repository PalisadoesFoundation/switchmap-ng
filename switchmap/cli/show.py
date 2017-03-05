#!/usr/bin/env python3
"""switchmap  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys

# Switchmap-NG imports
from switchmap.utils import configuration
from switchmap.utils import input_output
from switchmap.main.agent import Agent, AgentAPI, AgentDaemon
from switchmap.constants import (
    API_EXECUTABLE, API_GUNICORN_AGENT, POLLER_EXECUTABLE)


def run(parser, args):
    """Process 'show' command.

    Args:
        parser: Argparse parser
        args: Argparse arguments

    Returns:
        None

    """
    # Process 'show api' command
    if args.qualifier == 'api':
        api(args)
    elif args.qualifier == 'poller':
        poller(args)

    # Show help if there are no matches
    parser.print_help()
    sys.exit(2)


def api(args):
    """Process 'show api' commands.

    Args:
        args: Argparse arguments

    Returns:
        None

    """
    if args.subqualifier == 'logs':
        # Process logs
        config = configuration.Config()
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


def poller(args):
    """Process 'show poller' commands.

    Args:
        args: Argparse arguments

    Returns:
        None

    """
    if args.subqualifier == 'logs':
        # Process logs
        config = configuration.Config()
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
