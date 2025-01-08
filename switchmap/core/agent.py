"""Module to manage Agent classes.

Description:

    This module:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""

# Standard libraries
import textwrap
import sys
import argparse
import ipaddress
import multiprocessing
from datetime import datetime


# PIP3 libraries
from gunicorn.app.base import BaseApplication

# Application libraries
from switchmap.core.daemon import Daemon, GracefulDaemon
from switchmap.core import files
from switchmap.core import log
from switchmap.core.configuration import ConfigCore
from switchmap.core.variables import AgentAPIVariable


class Agent:
    """Agent class for daemons."""

    def __init__(self, parent, child=None, config=None):
        """Initialize the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon
            config: ConfigCore object

        Returns:
            None

        """
        # Initialize key variables (Parent)
        if config is None:
            self.config = ConfigCore()
        else:
            self.config = config
        self.parent = parent
        self.pidfile = files.pid_file(parent, self.config)
        self.lockfile = files.lock_file(parent, self.config)
        self.skipfile = files.skip_file(parent, self.config)

        # Initialize key variables (Child)
        if bool(child) is None:
            self._pidfile_child = None
        else:
            self._pidfile_child = files.pid_file(child, self.config)

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
        """Create placeholder method. Do not delete.

        Args:
            None
        Returns:
            None
        """
        # Do nothing
        pass


class _AgentRun:
    """Class that defines basic run function for AgentDaemons."""

    def __init__(self, agent):
        """Initialize the class.

        Args:
            agent: agent object

        Returns:
            None

        """
        # Initialize key variables
        self._agent_ = agent

    def run(self):
        """Start Polling.

        Args:
            None

        Returns:
            None

        """
        # Start polling. (Poller decides frequency)
        while True:
            self._agent_.query()


class AgentDaemon(_AgentRun, Daemon):
    """Class that manages base agent daemonization."""

    def __init__(self, agent):
        """Initialize the class.

        Args:
            agent: agent object

        Returns:
            None

        """
        # Initialize variables to be used by daemon
        self.agent = agent

        # Instantiate daemon superclass
        _AgentRun.__init__(self, agent)
        Daemon.__init__(self, agent)


class GracefulAgentDaemon(_AgentRun, GracefulDaemon):
    """Class that manages graceful agent daemonization."""

    def __init__(self, agent, timeout=30):
        """Initialize the class.

        Args:
            agent: agent object

        Returns:
            None

        """
        # Initialize variables to be used by daemon
        self.agent = agent

        # Instantiate daemon superclass
        _AgentRun.__init__(self, agent)
        GracefulDaemon.__init__(self, agent, timeout=timeout)


class AgentCLI:
    """Class that manages the agent CLI.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, graceful=False):
        """Initialize the class.

        Args:
            graceful: True if graceful restart is required

        Returns:
            None

        """
        # Initialize key variables
        self.parser = None
        self._graceful = graceful

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

    def control(self, agent, timeout=60):
        """Control the agent from the CLI.

        Args:
            agent: Agent object

        Returns:
            None

        """
        # Get the CLI arguments
        self.process()
        parser = self.parser
        args = parser.parse_args()

        # Instantiate agent daemon
        if self._graceful is False:
            _daemon = AgentDaemon(agent)
        else:
            _daemon = GracefulAgentDaemon(agent, timeout=timeout)

        # Run daemon
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
    """Applcication API agent that serves web pages.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, parent, child, app, config=None):
        """Initialize the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon
            app: Flask App
            config: ConfigCore object

        Returns:
            None

        """
        # Initialize key variables
        self._parent = parent
        if config is None:
            _config = ConfigCore()
        else:
            _config = config

        # Apply inheritance
        Agent.__init__(self, parent, child=child, config=_config)
        self._app = app
        self._agent_api_variable = AgentAPIVariable(
            ip_bind_port=_config.api_bind_port(),
            ip_listen_address=_config.api_listen_address(),
        )

    def query(self):
        """Query all remote targets for data.

        Args:
            None

        Returns:
            None

        """
        ######################################################################
        #
        # Assign options in format that the Gunicorn WSGI will accept
        #
        # NOTE! to get a full set of valid options pprint(self.cfg.settings)
        # in the instantiation of _StandaloneApplication. The option names
        # do not exactly match the CLI options found at
        # http://docs.gunicorn.org/en/stable/settings.html
        #
        ######################################################################
        options = {
            "bind": _ip_binding(self._agent_api_variable),
            "accesslog": self.config.api_log_file(self._parent),
            "errorlog": self.config.api_log_file(self._parent),
            "capture_output": True,
            "pidfile": self._pidfile_child,
            "loglevel": self.config.log_level(),
            "workers": _number_of_workers(),
            "umask": 0o0007,
        }

        # Log so that user running the script from the CLI knows that something
        # is happening
        log_message = "API running on {}:{} and logging to file {}." "".format(
            self._agent_api_variable.ip_listen_address,
            self._agent_api_variable.ip_bind_port,
            self.config.api_log_file(self._parent),
        )
        log.log2info(1088, log_message)

        # Run
        _StandaloneApplication(self._app, self.parent, options=options).run()


class _StandaloneApplication(BaseApplication):
    """Class to integrate the Gunicorn WSGI with the Flask application.

    Modified from: http://docs.gunicorn.org/en/latest/custom.html

    """

    def __init__(self, app, parent, options=None):
        """Initialize the class.

        Args:
            app: Flask application object of type Flask(__name__)
            parent: Name of parent process that is invoking the API
            options: Gunicorn CLI options
        Returns:
            None

        """
        # Initialize key variables
        self.options = options or {}
        self.parent = parent
        self.application = app
        super(_StandaloneApplication, self).__init__()

    def load_config(self):
        """Load the configuration.

        Args:
            None
        Returns:
            None
        """
        # Initialize key variables
        now = datetime.now()
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

        # Print configuration dictionary settings
        print(
            """{} Agent {} - Gunicorn configuration\
""".format(
                now.strftime("%Y-%m-%d %H:%M:%S.%f"), self.parent
            )
        )
        for name, value in self.cfg.settings.items():
            print("  {} = {}".format(name, value.get()))

    def load(self):
        """Run the Flask application throught the Gunicorn WSGI.

        Args:
            None

        Returns:
            self.application: Flask application object

        """
        return self.application


def _number_of_workers():
    """Get the number of CPU cores on this server."""
    return (multiprocessing.cpu_count() * 2) + 1


def _ip_binding(aav):
    """Create IPv4 / IPv6 binding for Gunicorn.

    Args:
        aav: AgentAPIVariable object

    Returns:
        result: bind

    """
    # Initialize key variables
    ip_address = aav.ip_listen_address
    ip_bind_port = aav.ip_bind_port
    result = None

    # Check IP address type
    try:
        ip_object = ipaddress.ip_address(ip_address)
    except:
        result = "{}:{}".format(ip_address, ip_bind_port)

    if bool(result) is False:
        # Is this an IPv4 address?
        ipv4 = isinstance(ip_object, ipaddress.IPv4Address)
        if ipv4 is True:
            result = "{}:{}".format(ip_address, ip_bind_port)
        else:
            result = "[{}]:{}".format(ip_address, ip_bind_port)

    # Return result
    return result
