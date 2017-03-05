"""Generic linux daemon base class for python 3.x."""

import atexit
import signal
import sys
import os
import time

# Switchmap-NG imports
from switchmap.utils import log
from switchmap.utils import general


class Daemon(object):
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method.

    Modified from http://www.jejik.com/files/examples/daemon3x.py

    """

    def __init__(self, agent):
        """Method for intializing the class.

        Args:
            agent: Agent object

        Returns:
            None

        """
        self.name = agent.name()
        self.pidfile = agent.pidfile_parent
        self.lockfile = agent.lockfile_parent

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism.

        Args:
            None

        Returns:
            None

        """
        # Create a parent process that will manage the child
        # when the code using this class is done.
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as err:
            log_message = ('Daemon fork #1 failed: %s') % (err)
            log_message = ('%s - PID file: %s') % (log_message, self.pidfile)
            log.log2die(1060, log_message)

        # Decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:

                # exit from second parent
                sys.exit(0)
        except OSError as err:
            log_message = ('Daemon fork #2 failed: %s') % (err)
            log_message = ('%s - PID file: %s') % (log_message, self.pidfile)
            log.log2die(1061, log_message)

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        f_handle_si = open(os.devnull, 'r')
        # f_handle_so = open(os.devnull, 'a+')
        f_handle_so = open(os.devnull, 'a+')
        f_handle_se = open(os.devnull, 'a+')

        os.dup2(f_handle_si.fileno(), sys.stdin.fileno())
        # os.dup2(f_handle_so.fileno(), sys.stdout.fileno())
        os.dup2(f_handle_so.fileno(), sys.stdout.fileno())
        os.dup2(f_handle_se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f_handle:
            f_handle.write(pid + '\n')

    def delpid(self):
        """Delete the PID file.

        Args:
            None

        Returns:
            None

        """
        # Delete file
        if os.path.exists(self.pidfile) is True:
            os.remove(self.pidfile)

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

        """
        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf_handle:
                pid = int(pf_handle.read().strip())

        except IOError:
            pid = None

        if pid:
            log_message = (
                'PID file: %s already exists. Daemon already running?'
                '') % (self.pidfile)
            log.log2die(1062, log_message)

        # Start the daemon
        self.daemonize()

        # Log success
        log_message = (
            'Daemon {} started - PID file: {}'
            ''.format(self.name, self.pidfile))
        log.log2info(1070, log_message)

        # Run code for daemon
        self.run()

    def force(self):
        """Stop the daemon by deleting the lock file first.

        Args:
            None

        Returns:

        """
        # Delete lock file and stop
        self.dellock()
        self.stop()

    def stop(self):
        """Stop the daemon.

        Args:
            None

        Returns:

        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf_handle:
                pid = int(pf_handle.read().strip())
        except IOError:
            pid = None

        if not pid:
            log_message = (
                'PID file: %s does not exist. Daemon not running?'
                '') % (self.pidfile)
            log.log2warning(1063, log_message)
            # Not an error in a restart
            return

        # Try killing the daemon process
        try:
            while 1:
                if self.lockfile is None:
                    os.kill(pid, signal.SIGTERM)
                else:
                    time.sleep(0.3)
                    if os.path.exists(self.lockfile) is True:
                        continue
                    else:
                        os.kill(pid, signal.SIGTERM)
                time.sleep(0.3)
        except OSError as err:
            error = str(err.args)
            if error.find("No such process") > 0:
                self.delpid()
                self.dellock()
            else:
                log_message = (str(err.args))
                log_message = (
                    '%s - PID file: %s') % (log_message, self.pidfile)
                log.log2die(1068, log_message)
        except:
            log_message = (
                'Unknown daemon "stop" error for PID file: %s'
                '') % (self.pidfile)
            log.log2die(1066, log_message)

        # Log success
        self.delpid()
        self.dellock()
        log_message = (
            'Daemon {} stopped - PID file: {}'
            ''.format(self.name, self.pidfile))
        log.log2info(1071, log_message)

    def restart(self):
        """Restart the daemon.

        Args:
            None

        Returns:

        """
        # Restart
        self.stop()
        self.start()

    def status(self):
        """Get daemon status.

        Args:
            None

        Returns:

        """
        # Get status
        if os.path.exists(self.pidfile) is True:
            print('Daemon is running - {}'.format(self.name))
        else:
            print('Daemon is stopped - {}'.format(self.name))

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart().
        """
        # Simple comment to pass linter
        pass


class _Directory:
    """A class for creating the names of hidden directories."""

    def __init__(self):
        """Method for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.root = ('%s/.switchmap') % (general.root_directory())

    def snmp(self):
        """Method for defining the hidden snmp directory.

        Args:
            None

        Returns:
            value: snmp directory

        """
        # Return
        value = ('%s/snmp') % self.root
        return value

    def pid(self):
        """Method for defining the hidden pid directory.

        Args:
            None

        Returns:
            value: pid directory

        """
        # Return
        value = ('%s/pid') % self.root
        return value

    def lock(self):
        """Method for defining the hidden lock directory.

        Args:
            None

        Returns:
            value: lock directory

        """
        # Return
        value = ('%s/lock') % self.root
        return value


class _File:
    """A class for creating the names of hidden files."""

    def __init__(self):
        """Method for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.directory = _Directory()

    def pid(self, prefix):
        """Method for defining the hidden pid directory.

        Args:
            prefix: Prefix of file

        Returns:
            value: pid directory

        """
        # Return
        _mkdir(self.directory.pid())
        value = ('%s/%s.pid') % (self.directory.pid(), prefix)
        return value

    def snmp(self, prefix):
        """Method for defining the hidden snmp directory.

        Args:
            prefix: Prefix of file

        Returns:
            value: snmp directory

        """
        # Return
        _mkdir(self.directory.snmp())
        value = ('%s/%s.snmp') % (self.directory.snmp(), prefix)
        return value

    def lock(self, prefix):
        """Method for defining the hidden lock directory.

        Args:
            prefix: Prefix of file

        Returns:
            value: lock directory

        """
        # Return
        _mkdir(self.directory.lock())
        value = ('%s/%s.lock') % (self.directory.lock(), prefix)
        return value


class _Touch:
    """A class for updating modifed times for hidden files."""

    def __init__(self):
        """Method for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.filez = _File()

    def pid(self, prefix):
        """Method for updating the hidden pid file.

        Args:
            prefix: Prefix of file

        Returns:
            None

        """
        # Return
        timestamp = int(time.time())
        filename = self.filez.pid(prefix)
        os.utime(filename, (timestamp, timestamp))


def lock_file(agent_name):
    """Get the lockfile for an agent.

    Args:
        agent_name: Agent name

    Returns:
        result: Name of lock file

    """
    # Return
    f_obj = _File()
    result = f_obj.lock(agent_name)
    return result


def pid_file(agent_name):
    """Get the pidfile for an agent.

    Args:
        agent_name: Agent name

    Returns:
        result: Name of pid file

    """
    # Return
    f_obj = _File()
    result = f_obj.pid(agent_name)
    return result


def snmp_file(hostname):
    """Get the snmpfile for an agent.

    Args:
        hostname: hostname

    Returns:
        result: Name of snmp file

    """
    # Return
    f_obj = _File()
    result = f_obj.snmp(hostname)
    return result


def update_pid(agent_name):
    """Update the PID for agent.

    Args:
        agent_name: Agent name

    Returns:
        None

    """
    # Update the PID file timestamp (important)
    update = _Touch()
    update.pid(agent_name)


def _mkdir(directory):
    """Create a directory if it doesn't already exist.

    Args:
        directory: Directory name

    Returns:
        None

    """
    # Do work
    if os.path.exists(directory) is False:
        os.makedirs(directory, mode=0o775)
    else:
        if os.path.isfile(directory) is True:
            log_message = (
                '%s is not a directory.'
                '') % (directory)
            log.log2die(1043, log_message)
