#!/usr/bin/env python3
"""Switchmap-NG  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys
import getpass
import subprocess


def main():
    """Run basic tests.

    Args:
        None

    Returns:
        None

    """
    # Test validity
    version = _Version()
    version.version()


class _Version(object):
    """Class to test setup."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.username = getpass.getuser()

    def version(self):
        """Determine versions.

        Args:
            None

        Returns:
            None

        """
        # Run tests
        valid_list = [self._python()]

    def _python(self):
        """Determine Python version.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = True
        major = 3
        minor = 5
        major_installed = sys.version_info[0]
        minor_installed = sys.version_info[1]

        # Exit if python version is too low
        if major_installed < major:
            valid = False
        elif major_installed == major and minor_installed < minor:
            valid = False
        if valid is False:
            log_message = (
                'Required python version must be >= {}.{}. '
                'Python version {}.{} installed'
                ''.format(major, minor, major_installed, minor_installed))
            print(log_message)
        else:
            log_message = (
                'Python version {}.{} OK'
                ''.format(major_installed, minor_installed))
            print(log_message)

        # Return
        return valid


if __name__ == '__main__':
    # Run main
    main()
