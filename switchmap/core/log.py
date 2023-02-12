"""Logging module."""

from __future__ import print_function
import sys
import os
import datetime
import time
import getpass
import logging
import traceback

# Define global variable
LOGGER = {}


def check_environment():
    """Check environmental variables. Die if incorrect.

    Args:
        None

    Returns:
        path: Path to the configurtion directory

    """
    # Get environment
    _config_directory = os.environ.get("SWITCHMAP_CONFIGDIR")

    # Verify configuration directory
    if bool(_config_directory) is False:
        log_message = """\
Environment variable $SWITCHMAP_CONFIGDIR needs to be set to the \
configuration directory location."""
        log2die_safe(1159, log_message)

    try:
        path = os.path.abspath(os.path.expanduser(_config_directory))
    except:
        log_message = """\
Environment variable $SWITCHMAP_CONFIGDIR set to invalid directory "{}"\
""".format(
            path
        )
        # Must print statement as logging requires a config directory
        log2die_safe(1086, log_message)

    # Verify configuration directory existence
    if (os.path.exists(path) is False) or (os.path.isdir(path) is False):
        log_message = """\
Environment variable $SWITCHMAP_CONFIGDIR set to directory {} that \
does not exist""".format(
            path
        )
        # Must print statement as logging requires a config directory
        log2die_safe(1020, log_message)

    # Set the path
    os.environ["SWITCHMAP_CONFIGDIR"] = path

    # Return
    return path


class _GetLog:
    """Class to manage the logging without duplicates."""

    def __init__(self):
        """Initialize the class."""
        # Application libraries
        from switchmap.core.configuration import ConfigCore

        # Define key variables
        app_name = "switchmap"
        levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }

        # Get the logging directory
        config = ConfigCore()
        log_file = config.log_file()
        config_log_level = config.log_level()

        # Set logging level
        log_level = levels.get(
            str(config_log_level).lower(), levels.get("debug")
        )

        # create logger with app_name
        self.logger_file = logging.getLogger("{}_file".format(app_name))
        self.logger_stdout = logging.getLogger("{}_console".format(app_name))

        # Set logging levels to file and stdout
        self.logger_stdout.setLevel(log_level)
        self.logger_file.setLevel(log_level)

        # create file handler which logs even debug messages
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        # create console handler with a higher log level
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(log_level)

        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        stdout_handler.setFormatter(formatter)

        # add the handlers to the logger
        self.logger_file.addHandler(file_handler)
        self.logger_stdout.addHandler(stdout_handler)

    def logfile(self):
        """Return logger for file IO.

        Args:
            None

        Returns:
            value: Value of logger

        """
        # Return
        value = self.logger_file
        return value

    def stdout(self):
        """Return logger for terminal IO.

        Args:
            None

        Returns:
            value: Value of logger

        """
        # Return
        value = self.logger_stdout
        return value


def log2console(code, message):
    """Log message to STDOUT only and die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Initialize key variables
    output = _message(code, message, False)
    print(output)


def log2die_safe(code, message):
    """Log message to STDOUT only and die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Initialize key variables
    output = _message(code, message, True)
    print(output)
    sys.exit(2)


def log2warning(code, message):
    """Log warning message to file only, but don't die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Initialize key variables
    _logit(code, message, error=False, verbose=False, level="warning")


def log2debug(code, message):
    """Log debug message to file only, but don't die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Initialize key variables
    _logit(code, message, error=False, verbose=False, level="debug")


def log2info(code, message):
    """Log status message to file only, but don't die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Log to screen and file
    _logit(code, message, error=False, verbose=False, level="info")


def log2see(code, message):
    """Log message to file and STDOUT, but don't die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Log to screen and file
    _logit(code, message, verbose=True, error=False)


def log2die(code, message):
    """Log to STDOUT and file, then die.

    Args:
        code: Error number
        message: Descriptive error string

    Returns:
        None

    """
    _logit(code, message, error=True)


def log2exception_die(code, sys_exc_info, message=None):
    """Log trace message to file and STDOUT, but don't die.

    Args:
        code: Message code
        sys_exc_info: Tuple from exception from sys.exc_info
        message: Descriptive error string

    Returns:
        None

    """
    # Log
    log2exception(code, sys_exc_info, message=message, die=True)


def log2exception(code, sys_exc_info, message=None, die=False):
    """Log trace message to file and STDOUT, but don't die.

    Args:
        code: Message code
        sys_exc_info: Tuple from exception from sys.exc_info
        die: Die if True

    Returns:
        None

    """
    # Initialize key variables
    (exc_type, exc_value, exc_traceback) = sys_exc_info
    log_message = """\
Bug: Exception Type:{}, Exception Instance: {}, Stack Trace Object: {}]\
""".format(
        exc_type, exc_value, exc_traceback
    )
    log2warning(code, log_message)
    if bool(message) is True:
        log2warning(code, message)

    # Write trace to log file
    from switchmap.core.configuration import ConfigCore

    config = ConfigCore()
    log_file = config.log_file()
    with open(log_file, "a+") as _fh:
        traceback.print_tb(exc_traceback, file=_fh)

    # Die
    if bool(die) is True:
        log2die(code, log_message)


def _logit(error_num, error_string, error=False, verbose=False, level="info"):
    """Log errors to file and STDOUT.

    Args:
        error_num: Error number
        error_string: Descriptive error string
        error: Is this an error or not?
        verbose: If True print non errors to STDOUT
        level: Logging level

    Returns:
        None

    """
    # Define key variables
    global LOGGER
    username = getpass.getuser()
    levels = ["debug", "info", "warning", "error", "critical"]

    # Set logging level
    if level in levels:
        log_level = level
    else:
        log_level = "debug"

    # Create logger if it doesn't already exist
    if bool(LOGGER) is False:
        LOGGER = _GetLog()
    logger_file = LOGGER.logfile()
    logger_stdout = LOGGER.stdout()

    # Log the message
    if error:
        log_message = "[{}] ({}E): {}".format(
            username, error_num, error_string
        )
        logger_stdout.critical("%s", log_message)
        logger_file.critical(log_message)

        # All done
        sys.exit(2)
    else:
        log_message = "[{}] ({}S): {}".format(
            username, error_num, error_string
        )
        _logger_file(logger_file, log_message, log_level)
        if verbose:
            _logger_stdout(logger_stdout, log_message, log_level)


def _logger_file(logger_file, log_message, log_level):
    """Log to file at a particular logging level.

    Args:
        logger_file: File logger instance
        log_message: Logging message
        log_level: Logging level

    Returns:
        None

    """
    # Log accordingly
    if log_level == "debug":
        logger_file.debug(log_message)
    elif log_level == "info":
        logger_file.info(log_message)
    elif log_level == "warning":
        logger_file.warning(log_message)
    elif log_level == "error":
        logger_file.error(log_message)
    else:
        logger_file.critical(log_message)


def _logger_stdout(logger_stdout, log_message, log_level):
    """Log to stdout at a particular logging level.

    Args:
        logger_stdout: stdout logger instance
        log_message: Logging message
        log_level: Logging level

    Returns:
        None

    """
    # Log accordingly
    if log_level == "debug":
        logger_stdout.debug(log_message)
    elif log_level == "info":
        logger_stdout.info(log_message)
    elif log_level == "warning":
        logger_stdout.warning(log_message)
    elif log_level == "error":
        logger_stdout.error(log_message)
    else:
        logger_stdout.critical(log_message)


def _message(code, message, error=True):
    """Create a formatted message string.

    Args:
        code: Message code
        message: Message text
        error: If True, create a different message string

    Returns:
        output: Message result

    """
    # Initialize key variables
    time_object = datetime.datetime.fromtimestamp(time.time())
    timestring = time_object.strftime("%Y-%m-%d %H:%M:%S,%f")
    username = getpass.getuser()

    # Format string for error message, print and die
    if error is True:
        prefix = "ERROR"
    else:
        prefix = "STATUS"
    output = "{} - {} - {} - [{}] {}".format(
        timestring, username, prefix, code, message
    )

    # Return
    return output


def env():
    """Check enviroment variables before running scripts.

    Args:
        None

    Returns:
        None

    """
    # Make sure the SWITCHMAP_CONFIGDIR environment variable is set
    if "SWITCHMAP_CONFIGDIR" not in os.environ:
        log_message = "The SWITCHMAP_CONFIGDIR environment variable not set."
        log2die_safe(1150, log_message)

    # Make sure the SWITCHMAP_CONFIGDIR environment variable is set to unittest
    if "unittest" in os.environ["SWITCHMAP_CONFIGDIR"].lower():
        log_message = """\
The SWITCHMAP_CONFIGDIR is set to a unittest directory. Daemon cannot be run\
"""
        log2die_safe(1151, log_message)
