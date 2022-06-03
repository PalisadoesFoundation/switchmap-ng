#!/usr/bin/env python3
"""switchmap.classes that manage various configurations."""

import os.path
import os
import multiprocessing

# Import project libraries
from switchmap.core import files
from switchmap.core import log


class Config():
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        hosts:
        snmp_auth:
    """

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        filepath = files.config_filepath()
        self._config = files.read_yaml_file(filepath).get('main')

    def agent_threads(self):
        """Get agent_threads.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        configured_value = self._config.get('agent_threads')

        # Default to 20
        if bool(configured_value) is False:
            threads = 20
        elif configured_value <= 0:
            threads = 1
        else:
            threads = configured_value

        # Get CPU cores
        cores = multiprocessing.cpu_count()
        desired_max_threads = max(1, cores - 1)

        # We don't want a value that's too big that the CPU cannot cope
        result = min(threads, desired_max_threads)

        # Return
        return result

    def bind_port(self):
        """Get bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config.get('bind_port', 7000)
        return result

    def daemon_directory(self):
        """Determine the daemon_directory.

        Args:
            None

        Returns:
            result: configured daemon_directory

        """
        # Get result
        result = self._config.get('daemon_directory')

        # Check if value exists
        if os.path.isdir(result) is False:
            daemon_message = (
                'daemon_directory: "{}" '
                'in configuration doesn\'t exist!').format(result)
            log.log2die_safe(1030, daemon_message)

        # Return
        return result

    def db_host(self):
        """Return db_host value.

        Args:
            None

        Returns:
            result: db_host value

        """
        # Get parameter
        result = self._config.get('db_host')

        # Return
        return result

    def db_name(self):
        """Return db_name value.

        Args:
            None

        Returns:
            result: db_name value

        """
        # Get parameter
        result = self._config.get('db_name')

        # Return
        return result

    def db_max_overflow(self):
        """Get DB connection pool overflow size.

        Args:
            None

        Returns:
            result: Configured value

        """
        # Get parameter
        _result = self._config.get('db_max_overflow', 30)
        value = int(_result)

        # Set min / max values
        result = min(abs(value), 50)

        # Return
        return result

    def db_pass(self):
        """Return db_pass value.

        Args:
            None

        Returns:
            result: db_pass value

        """
        # Get parameter
        result = self._config.get('db_pass')

        # Return
        return result

    def db_pool_size(self):
        """Get DB connection pool size.

        Args:
            None

        Returns:
            result: Configured value

        """
        # Get parameter
        _result = self._config.get('db_pool_size', 30)
        value = int(_result)

        # Set min / max values
        result = min(abs(value), 50)

        # Return
        return result

    def db_user(self):
        """Return db_user value.

        Args:
            None

        Returns:
            result: db_user value

        """
        # Get parameter
        result = self._config.get('db_user')

        # Return
        return result

    def hostnames(self):
        """Get hostnames.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = []
        agent_config = self._config.get('hostnames', [])

        # Get result
        if isinstance(agent_config, list) is True:
            agent_config = list(set(agent_config))
            result = sorted(agent_config)

        # Return
        return result

    def listen_address(self):
        """Get listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config.get('listen_address', '0.0.0.0')
        return result

    def log_directory(self):
        """Determine the log_directory.

        Args:
            None

        Returns:
            result: configured log_directory

        """
        # Get result
        result = self._config.get('log_directory')

        # Check if value exists
        if os.path.isdir(result) is False:
            log_message = (
                'log_directory: "{}" '
                'in configuration doesn\'t exist!').format(result)
            log.log2die_safe(1030, log_message)

        # Return
        return result

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = '{}/switchmap-ng.log'.format(self.log_directory())

        # Return
        return result

    def log_level(self):
        """Get log_level.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config.get('log_level', 'debug')

        # Return
        return result

    def polling_interval(self):
        """Get polling_interval.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config.get('polling_interval', 86400)
        return result

    def username(self):
        """Get username.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config.get('username', None)
        return result

    def web_log_file(self):
        """Get web_log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = '{}/switchmap-ng-api.log'.format(self.log_directory())

        # Return
        return result


class ConfigSNMP():
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        hosts:
        snmp_auth:
    """

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        filepath = files.config_filepath()
        self._config = files.read_yaml_file(filepath).get('snmp_groups')

    def snmp_auth(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            snmp_data: List of SNMP data dicts found in configuration file.

        """
        # Initialize key variables
        seed_dict = {}
        seed_dict['snmp_version'] = 2
        seed_dict['snmp_secname'] = None
        seed_dict['snmp_community'] = None
        seed_dict['snmp_authprotocol'] = None
        seed_dict['snmp_authpassword'] = None
        seed_dict['snmp_privprotocol'] = None
        seed_dict['snmp_privpassword'] = None
        seed_dict['snmp_port'] = 161
        seed_dict['group_name'] = None
        seed_dict['enabled'] = True

        # Read configuration's SNMP information. Return 'None' if none found
        if isinstance(self._config, list) is True:
            if len(self._config) < 1:
                return None
        else:
            return None

        # Start populating information
        snmp_data = []
        for read_dict in self._config:
            # Next entry if this is not a dict
            if isinstance(read_dict, dict) is False:
                continue

            # Assign good data
            new_dict = {}
            for key, _ in seed_dict.items():
                if key in read_dict:
                    new_dict[key] = read_dict[key]
                else:
                    new_dict[key] = seed_dict[key]

            # Convert relevant strings to integers
            new_dict['snmp_version'] = int(new_dict['snmp_version'])
            new_dict['snmp_port'] = int(new_dict['snmp_port'])

            # Append data to list
            snmp_data.append(new_dict)

        # Return
        return snmp_data
