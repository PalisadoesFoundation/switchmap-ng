"""Generic linux daemon base class for python 3.x."""

from __future__ import print_function
import atexit
import signal
import sys
import os
import time

# Application imports
from switchmap.core import log


class Daemon:
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method.

    Modified from http://www.jejik.com/files/examples/daemon3x.py

    """

    def __init__(self, agent):
        """Initialize the class.

        Args:
            agent: Agent object

        Returns:
            None

        """
        self.name = agent.name
        self.pidfile = agent.pidfile_parent
        self.lockfile = agent.lockfile_parent
        self._config = agent.config

    def _daemonize(self):
        """Deamonize class. UNIX double fork mechanism.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        daemon_log_file = self._config.log_file()

        # Make sure that the log file is accessible.
        try:
            open(daemon_log_file, "a").close()
        except:
            log_message = """Cannot access daemon log file {}. Please check \
file and directory permissions.""".format(
                daemon_log_file
            )
            log.log2die(1162, log_message)

        # Create a parent process that will manage the child
        # when the code using this class is done.
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as err:
            log_message = "Daemon fork #1 failed: {}".format(err)
            log_message = "{} - PID file: {}".format(log_message, self.pidfile)
            log.log2die(1067, log_message)

        # Decouple from parent environment
        os.chdir("{}".format(os.sep))
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:

                # exit from second parent
                sys.exit(0)
        except OSError as err:
            log_message = "Daemon fork #2 failed: {}".format(err)
            log_message = "{} - PID file: {}".format(log_message, self.pidfile)
            log.log2die(1169, log_message)

        # Redirect standard file descriptors, but first make sure that the
        sys.stdout.flush()
        sys.stderr.flush()
        f_handle_si = open(daemon_log_file, "r")
        f_handle_so = open(daemon_log_file, "a+")
        f_handle_se = open(daemon_log_file, "a+")
        os.dup2(f_handle_si.fileno(), sys.stdin.fileno())
        os.dup2(f_handle_so.fileno(), sys.stdout.fileno())
        os.dup2(f_handle_se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, "w+") as f_handle:
            f_handle.write("{}\n".format(pid))

    def delpid(self):
        """Delete the PID file.

        Args:
            None

        Returns:
            None

        """
        # Delete file
        if os.path.exists(self.pidfile) is True:
            try:
                os.remove(self.pidfile)
            except:
                log_message = "PID file {} already deleted".format(
                    self.pidfile
                )
                log.log2warning(1152, log_message)

    def dellock(self):
        """Delete the lock file.

        Args:
            None

        Returns:
            None

        """
        # Delete file
        if self.lockfile is not None:
            if os.path.exists(self.lockfile) is True:
                os.remove(self.lockfile)

    def start(self):
        """Start the daemon.

        Args:
            None

        Returns:
            None

        """
        # Check for a pidfile to see if the daemon already runs
        pid = _pid(self.pidfile)

        # Die if already running
        if bool(pid) is True:
            log_message = (
                "PID file: {} already exists. Daemon already running?"
                "".format(self.pidfile)
            )
            log.log2die(1170, log_message)

        # Start the daemon
        self._daemonize()

        # Log success
        log_message = "Daemon {} started - PID file: {}" "".format(
            self.name, self.pidfile
        )
        log.log2info(1167, log_message)

        # Run code for daemon
        self.run()

    def force(self):
        """Stop the daemon by deleting the lock file first.

        Args:
            None

        Returns:
            None

        """
        # Delete lock file and stop
        self.dellock()
        self.stop()

    def stop(self):
        """Stop the daemon.

        Args:
            None

        Returns:
            None

        """
        # Check for a pidfile to see if the daemon already runs
        pid = _pid(self.pidfile)
        if bool(pid) is False:
            log_message = (
                "PID file: {} does not exist. Daemon not running?"
                "".format(self.pidfile)
            )
            log.log2warning(1163, log_message)
            # Not an error in a restart
            return

        # Try killing the daemon process
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as err:
            error = str(err.args)
            if error.find("No such process") > 0:
                self.delpid()
                self.dellock()
            else:
                log_message = str(err.args)
                log_message = "{} - PID file: {}".format(
                    log_message, self.pidfile
                )
                log.log2die(1166, log_message)
        except:
            log_message = (
                'Unknown daemon "stopped" error for PID file: {}'
                "".format(self.pidfile)
            )
            log.log2die(1165, log_message)

        # Log success
        self.delpid()
        self.dellock()
        log_message = "Daemon {} stopped - PID file: {}" "".format(
            self.name, self.pidfile
        )
        log.log2info(1168, log_message)

    def restart(self):
        """Restart the daemon.

        Args:
            None

        Returns:
            None

        """
        # Restart with a wait period to make sure things shutdown smoothly
        self.stop()
        time.sleep(3)
        self.start()

    def status(self):
        """Get daemon status.

        Args:
            verbose: Print message if True

        Returns:
            result: True if the PID and PID file exists

        """
        # Determine whether pid file exists
        pid = _pid(self.pidfile)
        if bool(pid) is True:
            print("Daemon is running - {}".format(self.name))
        else:
            print("Daemon is stopped - {}".format(self.name))
        return bool(pid)

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart().
        """
        # Simple comment to pass linter
        pass


class GracefulDaemon(Daemon):
    """Daemon that allows for graceful shutdown

    This daemon should allow for stop/restart commands to perform graceful
    shutdown of a given process. A graceful shutdown involves checking that
    whether a current process is running and only ending the process once the
    current process has completed its currently running task.

    """

    def __init__(self, agent):
        """Initialize the class.

        Args:
            agent: Agent object

        Returns:
            None

        """
        try:
            self.graceful_timeout = agent.config.graceful_timeout()
        except AttributeError as err:
            # Sets default GracefulDaemon shutdown timeout if not defined by the
            # agent configuration
            log_message = """Graceful Timeout configuration not set, {}\n
            Default setting to 10s""".format(
                err
            )
            log.log2info(1100, log_message)

            self.graceful_timeout = 10

        Daemon.__init__(self, agent)

    def __daemon_running(self):
        """Determines if daemon is running

        Daemon is running based on whether it has an associated lockfile

        Args:
            None

        Return:
            running: True if daemon is currently running or conducing a process

        """
        running = False
        if self.lockfile is not None:
            if os.path.exists(self.lockfile) is True:
                running = True

        return running

    def graceful_shutdown(self, callback):
        """Wrapper class that handles graceful_shutdown prior to using
        callaback function `fn`

        Args:
            fn: callback method

        Return:
            wrapper

        """

        def wrapper():
            """Wrapper function"""
            if self.__daemon_running():
                log_message = """{} Lock file exists, Process still
                running""".format(
                    self.name
                )
                log.log2info(1101, log_message)

            # Continually checks if daemon is still running exits loop once
            # instance graceful_timeout limit reached
            timeout_counter = time.time()
            while True:
                # Updating timeout duration
                current_duration = time.time() - timeout_counter - 1
                time.sleep(1)

                if not self.__daemon_running() is True:
                    log_message = """Process {} no longer
                    processing""".format(
                        self.name
                    )
                    log.log2info(1103, log_message)
                    break

                if current_duration >= self.graceful_timeout:
                    log_message = """Process {} failed to shutdown, DUE TO
                    TIMEOUT""".format(
                        self.name
                    )
                    log.log2info(1104, log_message)

                    log_message = """{}, hard shutdown in
                    progress""".format(
                        self.name
                    )
                    log.log2info(1105, log_message)
                    break
            callback()

        return wrapper

    def stop(self):
        """Stop the daemon gracefully.

        Uses parent class stop method after checking that daemon is no longer
        processing data or making use of a resource.

        Args:
            None

        Returns:
            None

        """
        wrapper = self.graceful_shutdown(super(GracefulDaemon, self).stop)
        wrapper()

    def restart(self):
        """Restarts the daemon gracefully.

        Uses parent class restart method after checking that daemon is not
        processing data or making use of a resource.

        Args:
            None

        Returns:
            None

        """
        wrapper = self.graceful_shutdown(super(GracefulDaemon, self).restart)
        wrapper()


def _pid(pidfile):
    """Start the daemon.

    Args:
        pidfile: Name of file containing PID

    Returns:
        result: Value of PID

    """
    # Initialize key varialbes
    result = None

    # Check for a pidfile
    try:
        with open(pidfile, "r") as pf_handle:
            result = int(pf_handle.read().strip())

    except IOError:
        result = None

    # Return
    return result
