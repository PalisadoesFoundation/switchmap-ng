"""switchmap.Agent class.

Description:

    This script:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import textwrap
import sys
import time
import argparse
import multiprocessing
import os
from pprint import pprint

# PIP3 libraries
from gunicorn.app.base import BaseApplication

# switchmap.libraries
from switchmap.utils import daemon
from switchmap.utils.daemon import Daemon
from switchmap import CONFIG
from switchmap.utils import log
from switchmap.www import API


class Agent(object):
    """Agent class for daemons."""

    def __init__(self, parent, child=None):
        """Initialize the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon

        Returns:
            None

        """
        # Initialize key variables (Parent)
        self.parent = parent
        self.pidfile_parent = daemon.pid_file(parent)
        self.lockfile_parent = daemon.lock_file(parent)

        # Initialize key variables (Child)
        if bool(child) is None:
            self.pidfile_child = None
        else:
            self.pidfile_child = daemon.pid_file(child)

    def name(self):
        """Return agent name.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self.parent
        return value

    def query(self):
        """Placeholder method."""
        # Do nothing
        pass


class AgentDaemon(Daemon):
    """Class that manages agent deamonization."""

    def __init__(self, agent):
        """Initialize the class.

        Args:
            agent: agent object

        Returns:
            None

        """
        # Initialize variables to be used by daemon
        self.agent = agent

        # Call up the base daemon
        Daemon.__init__(self, agent)

    def run(self):
        """Start polling.

        Args:
            None

        Returns:
            None

        """
        # Start polling. (Poller decides frequency)
        while True:
            self.agent.query()


class AgentCLI(object):
    """Class that manages the agent CLI.

    Args:
        None

    Returns:
        None

    """

    def __init__(self):
        """Initialize the class.

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
            formatter_class=argparse.RawTextHelpFormatter,
        )

        # CLI argument for starting
        parser.add_argument(
            "--start",
            required=False,
            default=False,
            action="store_true",
            help="Start the agent daemon.",
        )

        # CLI argument for stopping
        parser.add_argument(
            "--stop",
            required=False,
            default=False,
            action="store_true",
            help="Stop the agent daemon.",
        )

        # CLI argument for getting the status of the daemon
        parser.add_argument(
            "--status",
            required=False,
            default=False,
            action="store_true",
            help="Get daemon daemon status.",
        )

        # CLI argument for restarting
        parser.add_argument(
            "--restart",
            required=False,
            default=False,
            action="store_true",
            help="Restart the agent daemon.",
        )

        # CLI argument for stopping
        parser.add_argument(
            "--force",
            required=False,
            default=False,
            action="store_true",
            help=textwrap.fill(
                "Stops or restarts the agent daemon ungracefully when "
                "used with --stop or --restart.",
                width=80,
            ),
        )

        # Get the parser value
        self.parser = parser

    def control(self, agent):
        """Control the switchmap agent from the CLI.

        Args:
            agent: Agent object

        Returns:
            None

        """
        # Get the CLI arguments
        self.process()
        parser = self.parser
        args = parser.parse_args()

        # Run daemon
        _daemon = AgentDaemon(agent)
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


class AgentAPI(Agent):
    """switchmap-ng API agent that serves web pages.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        populate:
        post:
    """

    def __init__(self, parent, child):
        """Initialize the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon

        Returns:
            None

        """
        # Initialize key variables
        Agent.__init__(self, parent, child)
        self.config = CONFIG

    def query(self):
        """Query all remote devices for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        config = self.config

        # Check for lock and pid files
        if os.path.exists(self.lockfile_parent) is True:
            log_message = (
                "Lock file {} exists. Multiple API daemons running "
                "API may have died "
                "catastrophically in the past, in which case the lockfile "
                "should be deleted. "
                "".format(self.lockfile_parent)
            )
            log.log2see(1083, log_message)

        if os.path.exists(self.pidfile_parent) is True:
            log_message = (
                "PID file: {} already exists. Daemon already running? "
                "If not, it may have died catastrophically in the past "
                "in which case you should use --stop --force to fix."
                "".format(self.pidfile_parent)
            )
            log.log2see(1084, log_message)

        ######################################################################
        #
        # Assign options in format that the Gunicorn WSGI will accept
        #
        # NOTE! to get a full set of valid options pprint(self.cfg.settings)
        # in the instantiation of StandaloneApplication. The option names
        # do not exactly match the CLI options found at
        # http://docs.gunicorn.org/en/stable/settings.html
        #
        ######################################################################
        options = {
            "bind": (
                "{}:{}".format(config.listen_address(), config.bind_port())
            ),
            "accesslog": config.web_log_file(),
            "errorlog": config.web_log_file(),
            "capture_output": True,
            "pidfile": self.pidfile_child,
            "loglevel": config.log_level(),
            "workers": _number_of_workers(),
            "umask": 0o0007,
        }

        # Log so that user running the script from the CLI knows that something
        # is happening
        log_message = (
            "Switchmap API running on {}:{} and logging to file {}."
            "".format(
                config.listen_address(),
                config.bind_port(),
                config.web_log_file(),
            )
        )
        log.log2info(1022, log_message)

        # Run
        StandaloneApplication(API, options).run()


class StandaloneApplication(BaseApplication):
    """Class to integrate the Gunicorn WSGI with the Switchmap Flask application.

    Modified from: http://docs.gunicorn.org/en/latest/custom.html

    """

    def __init__(self, app, options=None):
        """Initialize the class.

        args:
            app: Flask application object of type Flask(__name__)
            options: Gunicorn CLI options

        """
        # Initialize key variables
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

        pprint(self.cfg.settings)

    def load_config(self):
        """Load the configuration."""
        # Initialize key variables
        config = dict(
            [
                (key, value)
                for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            ]
        )

        # Assign configuration parameters
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """Run the Flask application throught the Gunicorn WSGI."""
        return self.application


def _number_of_workers():
    """Get the number of CPU cores on this server."""
    return (multiprocessing.cpu_count() * 2) + 1


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
