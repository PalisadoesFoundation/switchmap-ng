#!/usr/bin/env python3
"""switchmap.Agent class.

Description:

    This script:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import textwrap
import os
import sys
import logging
import time
import argparse
import queue as Queue
import threading

# pip3 libraries

# switchmap.libraries
from switchmap.utils import daemon
from switchmap.utils.daemon import Daemon
from switchmap.utils import log
from switchmap.utils import configuration

# Define a key global variable
THREAD_QUEUE = Queue.Queue()

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)


class AgentDaemon(Daemon):
    """Class that manages polling.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, poller):
        """Method initializing the class.

        Args:
            poller: PollingAgent object

        Returns:
            None

        """
        # Instantiate poller
        self.poller = poller

        # Get PID filename
        agent_name = self.poller.name()
        pidfile = daemon.pid_file(agent_name)
        lockfile = daemon.lock_file(agent_name)

        # Call up the base daemon
        Daemon.__init__(self, pidfile, lockfile=lockfile)

    def run(self):
        """Start polling.

        Args:
            None

        Returns:
            None

        """
        # Start polling. (Poller decides frequency)
        while True:
            self.poller.query()


class AgentCLI(object):
    """Class that manages the agent CLI.

    Args:
        None

    Returns:
        None

    """

    def __init__(self):
        """Method initializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.parser = None

    def process(self, additional_help=None):
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
            '--start',
            required=False,
            default=False,
            action='store_true',
            help='Start the agent daemon.'
        )

        # CLI argument for stopping
        parser.add_argument(
            '--stop',
            required=False,
            default=False,
            action='store_true',
            help='Stop the agent daemon.'
        )

        # CLI argument for getting the status of the daemon
        parser.add_argument(
            '--status',
            required=False,
            default=False,
            action='store_true',
            help='Get daemon daemon status.'
        )

        # CLI argument for restarting
        parser.add_argument(
            '--restart',
            required=False,
            default=False,
            action='store_true',
            help='Restart the agent daemon.'
        )

        # CLI argument for stopping
        parser.add_argument(
            '--force',
            required=False,
            default=False,
            action='store_true',
            help=textwrap.fill(
                'Stops or restarts the agent daemon ungracefully when '
                'used with --stop or --restart.', width=80)
        )

        # Get the parser value
        self.parser = parser

    def control(self, poller):
        """Start the switchmap.agent.

        Args:
            poller: PollingAgent object

        Returns:
            None

        """
        # Get the CLI arguments
        self.process()
        parser = self.parser
        args = parser.parse_args()

        # Run daemon
        _daemon = AgentDaemon(poller)
        if args.start is True:
            _daemon.start()
        elif args.stop is True:
            if args.force is True:
                _daemon.force()
            else:
                _daemon.stop()
        elif args.restart is True:
            if args.force is True:
                _daemon.force()
                _daemon.start()
            else:
                _daemon.restart()
        elif args.status is True:
            _daemon.status()
        else:
            parser.print_help()
            sys.exit(2)


def agent_sleep(agent_name, seconds=300):
    """Make agent sleep for a specified time, while updating PID every 300s.

    Args:
        agent_name: Name of agent
        seconds: number of seconds to sleep

    Returns:
        uid: UID for agent

    """
    # Initialize key variables
    interval = 300
    remaining = seconds

    # Start processing
    while True:
        # Update the PID file timestamp (important)
        daemon.update_pid(agent_name)

        # Sleep for at least "interval" number of seconds
        if remaining < interval:
            time.sleep(remaining)
            break
        else:
            time.sleep(interval)

        # Decrement remaining time
        remaining = remaining - interval
