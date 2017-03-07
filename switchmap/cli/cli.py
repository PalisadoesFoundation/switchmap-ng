#!/usr/bin/env python3
"""switchmap CLI classes.

Manages basic CLI parsing.

"""

# Main python libraries
import textwrap
import sys
import argparse
from inspect import ismethod

# Do switchmap-ng imports
from switchmap.cli import show, start, test, stop, restart


class CLI(object):
    """Class that manages the CLI."""

    def __init__(self, additional_help=''):
        """Method initializing the class.

        Args:
            additional_help: String for additional help information

        Returns:
            None

        """
        # Header for the help menu of the application
        self.parser = argparse.ArgumentParser(
            prog='switchmap-ng-cli',
            description=additional_help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Subparser for subcommands
        subparsers = self.parser.add_subparsers(dest='action')

        # Parse show parameters
        _Show(subparsers)

        # Parse start parameters
        _Start(subparsers)

        # Parse stop parameters
        _Stop(subparsers)

        # Parse restart parameters
        _Restart(subparsers)

        # Parse test parameters
        _Test(subparsers)

        # Return the CLI arguments
        self.args = self.parser.parse_args()

    def process(self):
        """Act on CLI arguments.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        args = self.args
        parser = self.parser

        # Process each option
        if args.action == 'start':
            # Process start command
            start.run(args)
            sys.exit(0)
        elif args.action == 'stop':
            # Process start command
            stop.run(args)
            sys.exit(0)
        elif args.action == 'restart':
            # Process start command
            restart.run(args)
            sys.exit(0)
        elif args.action == 'show':
            # Process show command
            show.run(args)
            sys.exit(0)
        elif args.action == 'test':
            test.run(args)
            sys.exit(0)

        # Show help otherwise
        parser.print_help()
        sys.exit(2)


class _Show(object):
    """Class handles CLI 'show' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        command = subparsers.add_parser(
            'show',
            help=textwrap.fill('Show operational status.', width=width)
        )

        # Add subparser
        self.subcommand = command.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def api(self, width=80):
        """Process show api CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subcommand.add_parser(
            'api',
            help=textwrap.fill('Show API status.', width=width)
        )

        # Add subparser
        subparsers = parser.add_subparsers(dest='subqualifier')

        # Parse "show API logs", return object used for parser
        _Logs(subparsers, width=width)

        # Parse "show API status", return object used for parser
        _Status(subparsers, width=width)

    def poller(self, width=80):
        """Process show poller CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subcommand.add_parser(
            'poller',
            help=textwrap.fill('Show poller status.', width=width)
        )

        # Add subparser
        subparsers = parser.add_subparsers(dest='subqualifier')

        # Parse "show poller logs", return object used for parser
        _Logs(subparsers, width=width)

        # Parse "show poller status", return object used for parser
        _Status(subparsers, width=width)

    def hostnames(self, width=80):
        """Process show hostnames CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subcommand.add_parser(
            'hostnames',
            help=textwrap.fill('Show configured hostnames.', width=width)
        )

    def configuration(self, width=80):
        """Process 'show configuration' CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subcommand.add_parser(
            'configuration',
            help=textwrap.fill('Show configuration.', width=width)
        )


class _Start(object):
    """Class handles CLI 'start' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        command = subparsers.add_parser(
            'start',
            help=textwrap.fill('Start daemon.', width=width)
        )

        # Add subparser
        self.subcommand = command.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def api(self, width=80):
        """Process start api CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subcommand.add_parser(
            'api',
            help=textwrap.fill('Start API daemon.', width=width)
        )

    def poller(self, width=80):
        """Process start poller CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subcommand.add_parser(
            'poller',
            help=textwrap.fill('Start poller daemon.', width=width)
        )


class _Stop(object):
    """Class handles CLI 'stop' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        command = subparsers.add_parser(
            'stop',
            help=textwrap.fill('Stop daemon.', width=width)
        )

        # Add subparser
        self.subcommand = command.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def api(self, width=80):
        """Process stop api CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subcommand.add_parser(
            'api',
            help=textwrap.fill('Stop API status.', width=width)
        )

        # CLI argument for forced stopping
        parser.add_argument(
            '--force',
            required=False,
            default=False,
            action='store_true',
            help=textwrap.fill(
                'Stops the agent daemon ungracefully when used', width=80)
        )

    def poller(self, width=80):
        """Process stop poller CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subcommand.add_parser(
            'poller',
            help=textwrap.fill('Stop poller status.', width=width)
        )

        # CLI argument for forced stopping
        parser.add_argument(
            '--force',
            required=False,
            default=False,
            action='store_true',
            help=textwrap.fill(
                'Stops the agent daemon ungracefully when used', width=80)
        )


class _Restart(object):
    """Class handles CLI 'restart' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        command = subparsers.add_parser(
            'restart',
            help=textwrap.fill('Restart daemon.', width=width)
        )

        # Add subparser
        self.subcommand = command.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def api(self, width=80):
        """Process restart api CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subcommand.add_parser(
            'api',
            help=textwrap.fill('Restart API status.', width=width)
        )

        # CLI argument for forced restartping
        parser.add_argument(
            '--force',
            required=False,
            default=False,
            action='store_true',
            help=textwrap.fill(
                'Restarts the agent daemon ungracefully when used', width=80)
        )

    def poller(self, width=80):
        """Process restart poller CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subcommand.add_parser(
            'poller',
            help=textwrap.fill('Restart poller status.', width=width)
        )

        # CLI argument for forced restartping
        parser.add_argument(
            '--force',
            required=False,
            default=False,
            action='store_true',
            help=textwrap.fill(
                'Restarts the agent daemon ungracefully when used', width=80)
        )


class _Test(object):
    """Class handles CLI 'test' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        command = subparsers.add_parser(
            'test',
            help=textwrap.fill('Test operational status.', width=width)
        )

        # Add subparser
        self.subcommand = command.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def poller(self, width=80):
        """Process test poller CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subcommand.add_parser(
            'poller',
            help=textwrap.fill('Test poller.', width=width)
        )

        # CLI argument for forced testping
        parser.add_argument(
            '--hostname',
            required=False,
            type=str,
            help=textwrap.fill(
                'Host to test', width=80)
        )

        # CLI argument for forced testping
        parser.add_argument(
            '--all',
            required=False,
            default=False,
            action='store_true',
            help=textwrap.fill(
                'Test all hosts', width=80)
        )


class _Logs(object):
    """Class processes CLI 'show logs' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        subparsers.add_parser(
            'logs',
            help=textwrap.fill(
                'Read the most recent entries in a log file. '
                'Equivalent to Linux "tail -f" command.', width=width)
        )


class _Status(object):
    """Class processes CLI 'show status' option."""

    def __init__(self, subparsers, width=80):
        """Function for intializing the class."""
        # Initialize key variables
        subparsers.add_parser(
            'status',
            help=textwrap.fill(
                'Daemon status', width=width)
        )
