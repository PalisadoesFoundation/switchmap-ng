"""Nagios check general library."""

import sys
import datetime
import time
import getpass
import logging
import threading
import traceback


# Switchmap-NG libraries
from switchmap.utils import configuration

# Define global variable
LOGGER = {}


class GetLog(object):
    """Class to manage the logging without duplicates."""

    def __init__(self):
        """Initialize the class."""
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
        config = configuration.Config()
        log_file = config.log_file()
        config_log_level = config.log_level()

        # Set logging level
        if config_log_level in levels:
            log_level = levels[config_log_level]
        else:
            log_level = levels["debug"]

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


class LogThread(threading.Thread):
    """LogThread should always be used in preference to threading.Thread.

    The interface provided by LogThread is identical to that of threading.
    Thread, however, if an exception occurs in the thread the error will be
    logged (using logging.exception) rather than printed to stderr.

    This is important in daemon style applications where stderr is redirected
    to /dev/null.

    """

    def __init__(self, **kwargs):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Run stuff
        super().__init__(**kwargs)
        self._real_run = self.run
        self.run = self._wrap_run

    def _wrap_run(self):
        try:
            self._real_run()
        except:
            # logging.exception('Exception during LogThread.run')
            log2warning(
                1116,
                (
                    "{}\n{}\n{}\n{}".format(
                        sys.exc_info()[0],
                        sys.exc_info()[1],
                        sys.exc_info()[2],
                        traceback.print_exc(),
                    )
                ),
            )


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
    _logit(code, message, error=False)


def log2see_safe(code, message):
    """Log message to STDOUT only and die.

    Args:
        code: Message code
        message: Message text

    Returns:
        None

    """
    # Initialize key variables
    output = _message(code, message, error=False)
    print(output)


def log2die(code, message):
    """Log to STDOUT and file, then die.

    Args:
        code: Error number
        message: Descriptive error string

    Returns:
        None
    """
    _logit(code, message, error=True)


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
        LOGGER = GetLog()
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
