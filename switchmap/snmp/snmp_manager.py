#!/usr/bin/env python3
"""SNMP manager class."""

import os

import easysnmp
from easysnmp import exceptions

# Import project libraries
from switchmap.utils import log
from switchmap.utils import daemon
from switchmap.snmp import iana_enterprise


class Validate(object):
    """Class Verify SNMP data."""

    def __init__(self, hostname, snmp_config):
        """Intialize the class.

        Args:
            hostname: Name of host
            snmp_config: List of dicts of possible snmp configurations

        Returns:
            None

        """
        # Initialize key variables
        self.snmp_config = snmp_config
        self.hostname = hostname

    def credentials(self):
        """Determine the valid SNMP credentials for a host.

        Args:
            None

        Returns:
            credentials: Dict of snmp_credentials to use

        """
        # Initialize key variables
        cache_exists = False
        group_key = 'group_name'

        # Create cache directory / file if not yet created
        filename = daemon.snmp_file(self.hostname)
        if os.path.exists(filename) is True:
            cache_exists = True

        # Create file if necessary
        if cache_exists is False:
            # Get credentials
            credentials = self._credentials()

            # Save credentials if successful
            if credentials is not None:
                _update_cache(filename, credentials[group_key])

        else:
            # Read credentials from cache
            if os.path.isfile(filename):
                with open(filename) as f_handle:
                    group_name = f_handle.readline()

            # Get credentials
            credentials = self._credentials(group_name)

            # Try the rest if these credentials fail
            if credentials is None:
                credentials = self._credentials()

            # Update cache if found
            if credentials is not None:
                _update_cache(filename, credentials[group_key])

        # Return
        return credentials

    def _credentials(self, group=None):
        """Determine the valid SNMP credentials for a host.

        Args:
            group: SNMP group name to try

        Returns:
            credentials: Dict of snmp_credentials to use

        """
        # Initialize key variables
        credentials = None

        # Probe device with all SNMP options
        for params_dict in self.snmp_config:
            # Only process enabled SNMP values
            if bool(params_dict['enabled']) is False:
                continue

            # Update credentials
            params_dict['snmp_hostname'] = self.hostname

            # Setup contact with the remote device
            device = Interact(params_dict)

            # Try successive groups
            if group is None:
                # Verify connectivity
                if device.contactable() is True:
                    credentials = params_dict
                    break
            else:
                if params_dict['group_name'] == group:
                    # Verify connectivity
                    if device.contactable() is True:
                        credentials = params_dict

        # Return
        return credentials


class Interact(object):
    """Class Gets SNMP data."""

    def __init__(self, snmp_parameters):
        """Intialize the class.

        Args:
            snmp_parameters: Dict of SNMP parameters to use

        Returns:
            None

        """
        # Initialize key variables
        self._snmp_params = snmp_parameters

        # Fail if snmp_parameters dictionary is empty
        if snmp_parameters['snmp_version'] is None:
            log_message = (
                'SNMP version is "None". Non existent host? - {}'
                ''.format(snmp_parameters['snmp_hostname']))
            log.log2die(1004, log_message)

        # Fail if snmp_parameters dictionary is empty
        if bool(snmp_parameters) is False:
            log_message = ('SNMP parameters provided are blank. '
                           'Non existent host?')
            log.log2die(1005, log_message)

    def enterprise_number(self):
        """Return SNMP enterprise number for the device.

        Args:
            None

        Returns:
            enterprise: SNMP enterprise number

        """
        # Get the sysObjectID.0 value of the device
        sysid = self.sysobjectid()

        # Get the vendor ID
        enterprise_obj = iana_enterprise.Query(sysobjectid=sysid)
        enterprise = enterprise_obj.enterprise()

        # Return
        return enterprise

    def hostname(self):
        """Return SNMP hostname for the interaction.

        Args:
            None

        Returns:
            hostname: SNMP hostname

        """
        # Initialize key variables
        hostname = self._snmp_params['snmp_hostname']

        # Return
        return hostname

    def contactable(self):
        """Check if device is contactable.

        Args:
            device_id: Device ID

        Returns:
            contactable: True if a contactable

        """
        # Define key variables
        contactable = False
        result = None

        # Try to reach device
        try:
            # If we can poll the SNMP sysObjectID,
            # then the device is contactable
            result = self.sysobjectid(check_reachability=True)
            if bool(result) is True:
                contactable = True

        except Exception as _:
            # Not contactable
            contactable = False

        except:
            # Log a message
            log_message = (
                'Unexpected SNMP error for device {}'
                ''.format(self._snmp_params['snmp_hostname']))
            log.log2die(1008, log_message)

        # Return
        return contactable

    def sysobjectid(self, check_reachability=False):
        """Get the sysObjectID of the device.

        Args:
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
        Returns:
            object_id: sysObjectID value

        """
        # Initialize key variables
        oid = '.1.3.6.1.2.1.1.2.0'
        object_id = None

        # Get sysObjectID
        results = self.get(oid, check_reachability=check_reachability)
        if bool(results) is True:
            object_id = results[oid].decode('utf-8')

        # Return
        return object_id

    def oid_exists(self, oid_to_get, context_name=''):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exists

        """
        # Initialize key variables
        validity = False

        # Validate OID
        if self._oid_exists_get(
                oid_to_get, context_name=context_name) is True:
            validity = True

        if validity is False:
            if self._oid_exists_walk(
                    oid_to_get, context_name=context_name) is True:
                validity = True

        # Return
        return validity

    def _oid_exists_get(self, oid_to_get, context_name=''):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exists

        """
        # Initialize key variables
        validity = False

        # Process
        (_, validity, result) = self.query(
            oid_to_get,
            get=True,
            check_reachability=True, context_name=context_name,
            check_existence=True)

        # If we get no result, then override validity
        if result[oid_to_get] is None:
            validity = False

        # Return
        return validity

    def _oid_exists_walk(self, oid_to_get, context_name=''):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exists

        """
        # Initialize key variables
        validity = False

        # Process
        (_, validity, result) = self.query(
            oid_to_get, get=False,
            check_reachability=True,
            context_name=context_name,
            check_existence=True)

        # If we get no result, then override validity
        if bool(result) is False:
            validity = False

        # Return
        return validity

    def swalk(self, oid_to_get, normalized=False, context_name=''):
        """Do a failsafe SNMPwalk.

        Args:
            oid_to_get: OID to get
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            results: Results

        """
        # Process data
        results = self.walk(
            oid_to_get,
            normalized=normalized, check_reachability=True,
            check_existence=True,
            context_name=context_name)

        # Return
        return results

    def walk(
            self, oid_to_get, normalized=False,
            check_reachability=False, check_existence=False, context_name=''):
        """Do an SNMPwalk.

        Args:
            oid_to_get: OID to walk
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence:
                Set if checking for the existence of the OID
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            result: Dictionary of tuples (OID, value)

        """
        (_, _, result) = self.query(
            oid_to_get, get=False,
            check_reachability=check_reachability,
            check_existence=check_existence,
            normalized=normalized, context_name=context_name)
        return result

    def get(
            self, oid_to_get, check_reachability=False, check_existence=False,
            normalized=False, context_name=''):
        """Do an SNMPget.

        Args:
            oid_to_get: OID to get
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence:
                Set if checking for the existence of the OID
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            Dictionary of tuples (OID, value)

        """
        (_, _, result) = self.query(
            oid_to_get, get=True,
            check_reachability=check_reachability,
            check_existence=check_existence,
            normalized=normalized,
            context_name=context_name)
        return result

    def query(
            self, oid_to_get, get=False, check_reachability=False,
            check_existence=False, normalized=False, context_name=''):
        """Do an SNMP query.

        Args:
            oid_to_get: OID to walk
            get: Flag determining whether to do a GET or WALK
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence:
                Set if checking for the existence of the OID
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            Dictionary of tuples (OID, value)

        """
        # Initialize variables
        snmp_params = self._snmp_params
        _contactable = True
        exists = True
        results = []

        # Check if OID is valid
        if _oid_valid_format(oid_to_get) is False:
            log_message = ('OID {} has an invalid format'.format(oid_to_get))
            log.log2die(1020, log_message)

        # Create SNMP session
        session = _Session(snmp_params, context_name=context_name).session

        # Create failure log message
        try_log_message = (
            'Error occurred during SNMP query on host '
            'OID {} from {} for context "{}"'
            ''.format(
                oid_to_get, snmp_params['snmp_hostname'],
                context_name))

        # Fill the results object by getting OID data
        try:
            # Get the data
            if get is True:
                results = [session.get(oid_to_get)]

            else:
                results = session.bulkwalk(
                    oid_to_get, non_repeaters=0, max_repetitions=25)

        # Crash on error, return blank results if doing certain types of
        # connectivity checks
        except (
                exceptions.EasySNMPConnectionError,
                exceptions.EasySNMPTimeoutError,
                exceptions.EasySNMPUnknownObjectIDError,
                exceptions.EasySNMPNoSuchNameError,
                exceptions.EasySNMPNoSuchObjectError,
                exceptions.EasySNMPNoSuchInstanceError,
                exceptions.EasySNMPUndeterminedTypeError) as exception_error:
            (_contactable, exists) = _process_error(
                try_log_message, exception_error,
                check_reachability, check_existence)

        except SystemError as exception_error:
            (_contactable, exists) = _process_error(
                try_log_message, exception_error,
                check_reachability, check_existence, system_error=True)
        except:
            log_message = ('Unexpected error')
            log.log2die(1002, log_message)

        # Format results
        values = _format_results(results, normalized=normalized)

        # Return
        return (_contactable, exists, values)


class _Session(object):
    """Class to create an SNMP session with a device."""

    def __init__(self, snmp_parameters, context_name=''):
        """Initialize the class.

        Args:
            snmp_parameters: Dict of SNMP paramerters
            context_name: Name of context

        Returns:
            session: SNMP session

        """
        # Initialize key variables
        self._snmp_params = {}
        self._context_name = context_name

        # Assign variables
        self._snmp_params = snmp_parameters

        # Fail if snmp_parameters dictionary is empty
        if snmp_parameters['snmp_version'] is None:
            log_message = (
                'SNMP version is "None". Non existent host? - {}'
                ''.format(snmp_parameters['snmp_hostname']))
            log.log2die(1004, log_message)

        # Fail if snmp_parameters dictionary is empty
        if not snmp_parameters:
            log_message = ('SNMP parameters provided are blank. '
                           'Non existent host?')
            log.log2die(1005, log_message)

        # Create SNMP session
        self.session = self._session()

    def _session(self):
        """Create an SNMP session for queries.

        Args:
            None

        Returns:
            session: SNMP session

        """
        # Create session
        if self._snmp_params['snmp_version'] != 3:
            session = easysnmp.Session(
                community=self._snmp_params['snmp_community'],
                hostname=self._snmp_params['snmp_hostname'],
                version=self._snmp_params['snmp_version'],
                remote_port=self._snmp_params['snmp_port'],
                use_numeric=True,
                context=self._context_name
            )
        else:
            session = easysnmp.Session(
                hostname=self._snmp_params['snmp_hostname'],
                version=self._snmp_params['snmp_version'],
                remote_port=self._snmp_params['snmp_port'],
                use_numeric=True,
                context=self._context_name,
                security_level=self._security_level(),
                security_username=self._snmp_params['snmp_secname'],
                privacy_protocol=self._priv_protocol(),
                privacy_password=self._snmp_params['snmp_privpassword'],
                auth_protocol=self._auth_protocol(),
                auth_password=self._snmp_params['snmp_authpassword']
            )

        # Return
        return session

    def _security_level(self):
        """Create string for security level.

        Args:
            snmp_params: Dict of SNMP paramerters

        Returns:
            result: security level

        """
        # Initialize key variables
        snmp_params = self._snmp_params

        # Determine the security level
        if bool(snmp_params['snmp_authprotocol']) is True:
            if bool(snmp_params['snmp_privprotocol']) is True:
                result = 'authPriv'
            else:
                result = 'authNoPriv'
        else:
            result = 'noAuthNoPriv'

        # Return
        return result

    def _auth_protocol(self):
        """Get AuthProtocol to use.

        Args:
            snmp_params: Dict of SNMP paramerters

        Returns:
            result: Protocol to be used in session

        """
        # Initialize key variables
        snmp_params = self._snmp_params
        protocol = snmp_params['snmp_authprotocol']

        # Setup AuthProtocol (Default SHA)
        if bool(protocol) is False:
            result = 'DEFAULT'
        else:
            if protocol.lower() == 'md5':
                result = 'MD5'
            else:
                result = 'SHA'

        # Return
        return result

    def _priv_protocol(self):
        """Get privProtocol to use.

        Args:
            snmp_params: Dict of SNMP paramerters

        Returns:
            result: Protocol to be used in session

        """
        # Initialize key variables
        snmp_params = self._snmp_params
        protocol = snmp_params['snmp_privprotocol']

        # Setup privProtocol (Default AES256)
        if bool(protocol) is False:
            result = 'DEFAULT'
        else:
            if protocol.lower() == 'des':
                result = 'DES'
            else:
                result = 'AES'

        # Return
        return result


def _process_error(
        log_message, exception_error, check_reachability,
        check_existence, system_error=False):
    """Process the SNMP error.

    Args:
        params_dict: Dict of SNMP parameters to try

    Returns:
        alive: True if contactable

    """
    # Initialize key varialbes
    _contactable = True
    exists = True
    if system_error is False:
        error_name = 'EasySNMPError'
    else:
        error_name = 'SystemError'

    # Check existence of OID
    if check_existence is True:
        if system_error is False:
            if type(exception_error) == easysnmp.exceptions.EasySNMPUnknownObjectIDError:
                exists = False
                return (_contactable, exists)
            elif type(exception_error) == easysnmp.exceptions.EasySNMPNoSuchNameError:
                exists = False
                return (_contactable, exists)
            elif type(exception_error) == easysnmp.exceptions.EasySNMPNoSuchObjectError:
                exists = False
                return (_contactable, exists)
            elif type(exception_error) == easysnmp.exceptions.EasySNMPNoSuchInstanceError:
                exists = False
                return (_contactable, exists)
        else:
            exists = False
            return (_contactable, exists)

    # Checking if the device is reachable
    if check_reachability is True:
        _contactable = False
        exists = False
        return (_contactable, exists)

    # Die an agonizing death!
    log_message = '{}: ({})'.format(log_message, error_name)
    log.log2die(1023, log_message)


def _format_results(results, normalized=False):
    """Normalize the results of an walk.

    Args:
        results: List of lists of results
        normalized: If True, then return results as a dict keyed by
            only the last node of an OID, otherwise return results
            keyed by the entire OID string. Normalization is useful
            when trying to create multidimensional dicts where the
            primary key is a universal value such as IF-MIB::ifIndex
            or BRIDGE-MIB::dot1dBasePort

    Returns:
        return_results: Dict of results

    """
    # Initialize key variables
    return_results = {}

    for result in results:
        if normalized is True:
            return_results[result.oid_index] = _convert(result)
        else:
            return_results[
                '{}.{}'.format(
                    result.oid, result.oid_index)] = _convert(result)

    # Return
    return return_results


def _convert(result):
    """Convert value from pysnmp object to standard python types.

    Args:
        result: Named tuple result

    Returns:
        converted: converted value. Only returns BYTES and INTEGERS

    """
    # Initialieze key values
    converted = None
    value = result.value
    snmp_type = result.snmp_type

    # Convert string type values to bytes
    if snmp_type.upper() == 'OCTETSTR':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'OPAQUE':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'BITS':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'IPADDR':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'NETADDR':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'OBJECTID':
        # DO NOT CHANGE !!!
        converted = bytes(str(value), 'utf-8')
    elif snmp_type.upper() == 'NOSUCHOBJECT':
        # Nothing if OID not found
        converted = None
    elif snmp_type.upper() == 'NOSUCHINSTANCE':
        # Nothing if OID not found
        converted = None
    elif snmp_type.upper() == 'ENDOFMIBVIEW':
        # Nothing
        converted = None
    elif snmp_type.upper() == 'NULL':
        # Nothing
        converted = None
    else:
        # Convert everything else into integer values
        # rfc1902.Integer
        # rfc1902.Integer32
        # rfc1902.Counter32
        # rfc1902.Gauge32
        # rfc1902.Unsigned32
        # rfc1902.TimeTicks
        # rfc1902.Counter64
        converted = int(value)

    # Return
    return converted


def _oid_valid_format(oid):
    """Determine whether the format of the oid is correct.

    Args:
        oid: OID string

    Returns:
        True if valid

    """
    # oid cannot be numeric
    if isinstance(oid, str) is False:
        return False

    # Make sure the oid is not blank
    stripped_oid = oid.strip()
    if not stripped_oid:
        return False

    # Must start with a '.'
    if oid[0] != '.':
        return False

    # Must not end with a '.'
    if oid[-1] == '.':
        return False

    # Test each octet to be numeric
    octets = oid.split('.')

    # Remove the first element of the list
    octets.pop(0)
    for value in octets:
        try:
            int(value)
        except:
            return False

    # Otherwise valid
    return True


def _update_cache(filename, snmp_group):
    """Update the SNMP credentials cache file with successful snmp_group.

    Args:
        filename: Cache filename
        group: SNMP group that successfully authenticated

    Returns:
        None

    """
    # Do update
    with open(filename, 'w+') as env:
        env.write(snmp_group)
