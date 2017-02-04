#!/usr/bin/env python3
"""SNMP manager class."""

import os

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1905
from pysnmp.proto import rfc1902
from pysnmp.smi import rfc1902 as smi

# Import project libraries
from switchmap.utils import log
from switchmap.utils import daemon
from switchmap.snmp import iana_enterprise


class Validate(object):
    """Class Verify SNMP data.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        oid_exists:
        walk:
        get:
        query:
    """

    def __init__(self, hostname, snmp_config):
        """Function for intializing the class."""
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
            # Update credentials
            params_dict['snmp_hostname'] = self.hostname

            # Try successive groups
            if group is None:
                # Verify connectivity
                if _contactable(params_dict) is True:
                    credentials = params_dict
                    break
            else:
                if params_dict['group_name'] == group:
                    # Verify connectivity
                    if _contactable(params_dict) is True:
                        credentials = params_dict

        # Return
        return credentials


class Interact(object):
    """Class Gets SNMP data.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        oid_exists:
        walk:
        get:
        query:
    """

    def __init__(self, snmp_parameters):
        """Function for intializing the class."""
        # Initialize key variables
        self.snmp_params = {}

        # Assign variables
        self.snmp_params = snmp_parameters

        # Fail if snmp_parameters dictionary is empty
        if snmp_parameters['snmp_version'] is None:
            log_message = (
                'SNMP version is "None". Non existent host? - %s'
                '') % (snmp_parameters['snmp_hostname'])
            log.log2die(1004, log_message)

        # Fail if snmp_parameters dictionary is empty
        if not snmp_parameters:
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
        hostname = self.snmp_params['snmp_hostname']

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
            result = self.sysobjectid(connectivity_check=True)
            if bool(result) is True:
                contactable = True

        except Exception as _:
            # Not contactable
            contactable = False

        except:
            # Log a message
            log_message = ('Unexpected SNMP error for device %s') % (
                self.snmp_params['snmp_hostname'])
            log.log2die(1008, log_message)

        # Return
        return contactable

    def sysobjectid(self, connectivity_check=False):
        """Get the sysObjectID of the device.

        Args:
            connectivity_check:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
        Returns:
            object_id: sysObjectID value

        """
        # Initialize key variables
        oid = '.1.3.6.1.2.1.1.2.0'
        object_id = None

        # Get sysObjectID
        results = self.get(oid, connectivity_check=connectivity_check)
        if bool(results) is True:
            object_id = ('.%s') % (results[oid].decode('utf-8'))

        # Return
        return object_id

    def oid_exists(self, oid_to_get):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get

        Returns:
            validity: True if exists

        """
        # Initialize key variables
        validity = False

        # Validate OID
        if self.oid_exists_get(oid_to_get) is True:
            validity = True

        if validity is False:
            if self.oid_exists_walk(oid_to_get) is True:
                validity = True

        # Return
        return validity

    def oid_exists_get(self, oid_to_get):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get

        Returns:
            validity: True if exists

        """
        # Initialize key variables
        validity = False

        # Process
        results = self.get(oid_to_get, connectivity_check=True)
        if _instance_found(results) is True:
            validity = True

        # Return
        return validity

    def oid_exists_walk(self, oid_to_get):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get

        Returns:
            validity: True if exists

        """
        # Initialize key variables
        validity = False

        # Process
        results = self.walk(oid_to_get, connectivity_check=True)
        if _instance_found(results) is True:
            validity = True

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
        # Initialize key variables
        results = {}

        # Process data
        data = self.walk(
            oid_to_get,
            normalized=normalized, connectivity_check=True,
            context_name=context_name)

        # If oid not found then return blank dict
        for value in data.values():
            if isinstance(value, rfc1905.NoSuchInstance) is False:
                results = data
            # If nothing is retuned, then fail
            elif bool(value) is True:
                results = data
            break

        # Return
        return results

    def walk(
            self, oid_to_get, normalized=False,
            connectivity_check=False, context_name=''):
        """Do an SNMPwalk.

        Args:
            oid_to_get: OID to walk
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
            connectivity_check:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            Dictionary of tuples (OID, value)

        """
        return self.query(
            oid_to_get, get=False,
            connectivity_check=connectivity_check,
            normalized=normalized, context_name=context_name)

    def get(
            self, oid_to_get, connectivity_check=False,
            normalized=False, context_name=''):
        """Do an SNMPget.

        Args:
            oid_to_get: OID to get
            connectivity_check:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
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
        return self.query(
            oid_to_get, get=True,
            connectivity_check=connectivity_check, normalized=normalized,
            context_name=context_name)

    def query(
            self, oid_to_get, get=False, connectivity_check=False,
            normalized=False, context_name=''):
        """Do an SNMP query.

        Args:
            oid_to_get: OID to walk
            get: Flag determining whether to do a GET or WALK
            connectivity_check:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
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
        return_results = {}
        snmp_params = self.snmp_params

        # Check if OID is valid
        valid_format = oid_valid_format(oid_to_get)
        if valid_format is False:
            log_message = ('OID %s has an invalid format') % (oid_to_get)
            log.log2die(1020, log_message)

        # Create the object
        snmp_object = cmdgen.CommandGenerator()

        # Setup Transport object
        transport_object = cmdgen.UdpTransportTarget(
            (snmp_params['snmp_hostname'], snmp_params['snmp_port']))

        # Create the auth object
        authentication_object = _get_auth_object(snmp_params)

        # Fill the results object by getting OID data
        try:
            # Get the data
            if get is True:
                (session_error_string, session_error_status,
                 session_error_index, var_binds) = \
                    snmp_object.getCmd(
                        authentication_object, transport_object, oid_to_get,
                        contextName=context_name)

            else:
                (session_error_string, session_error_status,
                 session_error_index, var_binds) = \
                    snmp_object.nextCmd(
                        authentication_object, transport_object, oid_to_get,
                        contextName=context_name)

        # Do something here
        except Exception as exception_error:
            # Check for errors and print out results
            log_message = (
                'Error occurred during SNMPget on host '
                'OID %s from %s: (%s)') % (oid_to_get,
                                           snmp_params['snmp_hostname'],
                                           exception_error)
            log.log2die(1023, log_message)
        except:
            log_message = ('Unexpected error')
            log.log2die(1002, log_message)

        # Crash on error, return blank results if doing certain types of
        # connectivity checks
        if session_error_string:
            log_message = (
                'Error occurred for OID %s on host %s: '
                '(%s) ErrorNum: %s, ErrorInd: '
                '%s') % (oid_to_get,
                         snmp_params['snmp_hostname'],
                         session_error_string,
                         session_error_status, session_error_index)

            return _process_error(
                connectivity_check=connectivity_check,
                session_error_status=session_error_status,
                session_error_index=session_error_index,
                get=get,
                log_message=log_message)

        # Format results
        return_results = _format_results(
            normalized=normalized, get=get, var_binds=var_binds)

        # Return
        return return_results


def _process_error(
        connectivity_check=False, session_error_status=None,
        session_error_index=None, get=False,
        log_message=None):
    """Process errors received.

    Args:
        connectivity_check:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
        session_error_status: Error status
        session_error_index: Error index
        get: True if formatting the results of an SNMP get

    Returns:
        results:

    """
    # Initialize key variables
    results = {}

    # Timeout contacting device
    # (Timeout as OID requested does not exist, not because the
    # device is uncontactable)
    # The device must be checked for connectivity before hand. If it
    # can connect but some additional OID is unavailable, then this is
    # invoked. This is used to determine whether a device has 64 bit
    # IFMIB octet counters
    if connectivity_check is False:
        if (session_error_status == 0) and (
                session_error_index == -24):

            # Return blank results
            return results

    if connectivity_check is True:
        # Bad SNMP authentication during authentication check
        if (session_error_status == 0) and (
                session_error_index == -4):
            # Return blank results
            return results

        # Device completely off the air (SNMP timeout)
        if (session_error_status == 0) and (
                session_error_index == 0):
            # Return blank results
            return results

    # Otherwise Fail
    if get is True:
        action_taken = 'SNMPget'
    else:
        action_taken = 'SNMPwalk'
    log_message = ('%s - %s') % (action_taken, log_message)
    log.log2die(1003, log_message)


def _format_results(normalized=False, get=False, var_binds=None):
    """Normalize the results of an walk.

    Args:
        normalized: If True, then return results as a dict keyed by
            only the last node of an OID, otherwise return results
            keyed by the entire OID string. Normalization is useful
            when trying to create multidimensional dicts where the
            primary key is a universal value such as IF-MIB::ifIndex
            or BRIDGE-MIB::dot1dBasePort
        get: True if formatting the results of an SNMP get
        var_binds: Dict of results

    Returns:
        return_results: Dict of results

    """
    # Initialize key variables
    return_results = {}

    # ### Start ##########################################################
    # ####################################################################
    # You can determine the class of value as value.__class__.__name__
    # This is good for troubleshooting
    # ####################################################################
    # Construct the results to return
    if get is True:
        # Returns a single tuple
        for oid_returned, value in var_binds:
            oid_fixed = ('.%s') % (oid_returned)
            return_results[oid_fixed] = _convert(value)
    else:
        # Returns a list of tuples
        for var_row in var_binds:
            for oid_returned, value in var_row:
                oid_fixed = ('.%s') % (oid_returned)
                return_results[oid_fixed] = _convert(value)
    # ####################################################################
    # ### Stop ###########################################################

    # Return normalized results if required
    if normalized is True:
        return_results = _normalized_walk(return_results)

    # Return
    return return_results


def _convert(value):
    """Convert value from pysnmp object to standard python types.

    Args:
        value: Value to convert

    Returns:
        converted: converted value. Only returns BYTES and INTEGERS

    """
    # Initialieze key values
    converted = None

    # Convert string type values to bytes
    if isinstance(value, rfc1902.OctetString) is True:
        converted = bytes(value)
    elif isinstance(value, rfc1902.Opaque) is True:
        converted = bytes(value)
    elif isinstance(value, rfc1902.Bits) is True:
        converted = bytes(value)
    elif isinstance(value, rfc1902.IpAddress) is True:
        converted = bytes(value)
    elif isinstance(value, smi.ObjectIdentity) is True:
        # DO NOT CHANGE !!!
        converted = bytes(str(value), 'utf-8')
    elif isinstance(value, rfc1905.NoSuchObject) is True:
        # Nothing if OID not found
        converted = None
    elif isinstance(value, rfc1905.NoSuchInstance) is True:
        # Nothing if OID not found
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


def _get_auth_object(snmp_params):
    """Get the authentication object to be used by cmdgen library.

    Args:
        snmp_params: Dict of SNMP parameters

    Returns:
        authentication_object: Auth object for query

    """
    # Initialize key variables
    authentication_object = None

    # Process SNMPv2
    if snmp_params['snmp_version'] == 2:
        # Setup SNMPv2 authentication object
        authentication_object = cmdgen.CommunityData(
            snmp_params['snmp_community'])

    # Process SNMPv3
    else:
        # Setup AuthProtocol (Default SHA)
        if snmp_params['snmp_authprotocol'] is None:
            authproto_object = cmdgen.usmNoAuthProtocol
        else:
            if snmp_params['snmp_authprotocol'].lower() == 'md5':
                authproto_object = cmdgen.usmHMACMD5AuthProtocol
            else:
                authproto_object = cmdgen.usmHMACSHAAuthProtocol

        # Setup privProtocol (Default AES256)
        if snmp_params['snmp_privprotocol'] is None:
            privproto_object = cmdgen.usmNoPrivProtocol
        else:
            if snmp_params['snmp_privprotocol'].lower() == 'des':
                privproto_object = cmdgen.usmDESPrivProtocol
            elif snmp_params['snmp_privprotocol'].lower() == '3des':
                privproto_object = cmdgen.usm3DESEDEPrivProtocol
            elif snmp_params['snmp_privprotocol'].lower() == 'aes':
                privproto_object = cmdgen.usmAesCfb128Protocol
            elif snmp_params['snmp_privprotocol'].lower() == 'aes128':
                privproto_object = cmdgen.usmAesCfb128Protocol
            elif snmp_params['snmp_privprotocol'].lower() == 'aes192':
                privproto_object = cmdgen.usmAesCfb192Protocol
            else:
                privproto_object = cmdgen.usmAesCfb256Protocol

        # Setup SNMPv3 authentication object
        authentication_object = cmdgen.UsmUserData(
            snmp_params['snmp_secname'],
            snmp_params['snmp_authpassword'],
            snmp_params['snmp_privpassword'],
            authProtocol=authproto_object,
            privProtocol=privproto_object)

    # Return
    return authentication_object


def _normalized_walk(walk_results):
    """Normalize the results of an walk.

    Args:
        walk_results: Results of an walk

    Returns:
        result: Dict of the format {'ifindex', 'oid_value')

    """
    # Initialize key variables
    result = {}

    # Create the result
    for key, value in walk_results.items():
        octets = key.split('.')
        result[octets[-1]] = value

    # Return result
    return result


def _instance_found(results):
    """Determine if an instance of the OID was found based on the results.

    Args:
        results: Results of an walk

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False

    # Process
    for value in results.values():
        # If oid not found message, then fail
        if (isinstance(value, rfc1905.NoSuchInstance) is True) or (
                (isinstance(value, rfc1905.NoSuchObject) is True)):
            found = False
        elif isinstance(value, int) is True:
            found = True
        elif bool(value) is True:
            found = True
        break

    # Return
    return found


def oid_valid_format(oid):
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


def _contactable(params_dict):
    """Determine whether host is contactable.

    Args:
        params_dict: Dict of SNMP parameters to try

    Returns:
        alive: True if contactable

    """
    # Initialize key variables
    alive = False

    # Verify connectivity
    query = Interact(params_dict)
    if query.contactable() is True:
        alive = True

    # Return
    return alive
