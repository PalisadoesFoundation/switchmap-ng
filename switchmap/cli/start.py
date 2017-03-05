#!/usr/bin/env python3
"""switchmap  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys

# Switchmap-NG imports
from switchmap.main.agent import Agent, AgentAPI, AgentDaemon
from switchmap.constants import (
    API_EXECUTABLE, API_GUNICORN_AGENT, POLLER_EXECUTABLE)


def run(parser, args):
    """Process 'start' command.

    Args:
        parser: Argparse parser
        args: Argparse arguments

    Returns:
        None

    """
    # Process 'show api' command
    if args.qualifier == 'api':
        api()
    elif args.qualifier == 'poller':
        poller()

    # Show help if there are no matches
    parser.print_help()
    sys.exit(2)


def api():
    """Process 'start api' commands.

    Args:
        None

    Returns:
        None

    """
    # Create agent objects
    agent_gunicorn = Agent(API_GUNICORN_AGENT)
    agent_api = AgentAPI(API_EXECUTABLE, API_GUNICORN_AGENT)

    # Start daemons
    daemon_gunicorn = AgentDaemon(agent_gunicorn)
    daemon_gunicorn.start()
    daemon_api = AgentDaemon(agent_api)
    daemon_api.start()

    # Done
    sys.exit(0)


def poller():
    """Process 'start poller' commands.

    Args:
        None

    Returns:
        None

    """
    # Create agent object
    agent_poller = Agent(POLLER_EXECUTABLE)

    # Start agent
    daemon_poller = AgentDaemon(agent_poller)
    daemon_poller.start()

    # Done
    sys.exit(0)
