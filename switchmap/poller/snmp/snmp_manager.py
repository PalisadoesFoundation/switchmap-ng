"""SNMP manager class."""

import os
import sys

import easysnmp
from easysnmp import exceptions

# Import project libraries
from switchmap.poller.configuration import ConfigPoller
from switchmap.poller import POLL
from switchmap.core import log
from switchmap.core import files
from . import iana_enterprise


class Validate:
    """Class Verify SNMP data."""

    def __init__(self, options):
        """Initialize the Validate class.

        Args:
            options: POLLING_OPTIONS object containing SNMP configuration

        Returns:
            None
        """
        # Initialize key variables
        self._options = options

    def credentials(self):
        """Determine valid SNMP credentials for a host.

        Args:
            None

        Returns:
            authentication: SNMP authorization object containing valid
                credentials, or None if no valid credentials found
        """
        # Initialize key variables
        cache_exists = False

        # Create cache directory / file if not yet created
        filename = files.snmp_file(self._options.hostname, ConfigPoller())
        if os.path.exists(filename) is True:
            cache_exists = True

        # Create file if necessary
        if cache_exists is False:
            # Get credentials
            authentication = self.validation()

            # Save credentials if successful
            if bool(authentication):
                _update_cache(filename, authentication.group)

        else:
            # Read credentials from cache
            if os.path.isfile(filename):
                with open(filename) as f_handle:
                    group = f_handle.readline()

            # Get credentials
            authentication = self.validation(group)

            # Try the rest if these credentials fail
            if bool(authentication) is False:
                authentication = self.validation()

            # Update cache if found
            if bool(authentication):
                _update_cache(filename, authentication.group)

        # Return
        return authentication

    def validation(self, group=None):
        """Determine valid SNMP authorization for a host.

        Args:
            group: String containing SNMP group name to try, or None to try all
                groups

        Returns:
            result: SNMP authorization object if valid credentials found,
                None otherwise
        """
        # Initialize key variables
        result = None

        # Probe device with all SNMP options
        for authorization in self._options.authorizations:
            # Only process enabled SNMP values
            if bool(authorization.enabled) is False:
                continue

            # Setup contact with the remote device
            device = Interact(
                POLL(
                    hostname=self._options.hostname,
                    authorization=authorization,
                )
            )

            # Try successive groups
            if group is None:
                # Verify connectivity
                if device.contactable() is True:
                    result = authorization
                    break
            else:
                if authorization.group == group:
                    # Verify connectivity
                    if device.contactable() is True:
                        result = authorization

        # Return
        return result


class Interact:
    """Class Gets SNMP data."""

    def __init__(self, _poll):
        """Initialize the Interact class.

        Args:
            _poll: POLL object containing SNMP configuration and target info

        Returns:
            None
        """
        # Initialize key variables
        self._poll = _poll

        # Fail if there is no authentication
        if bool(self._poll.authorization) is False:
            log_message = (
                "SNMP parameters provided are blank. " "Non existent host?"
            )
            log.log2die(1045, log_message)

    def enterprise_number(self):
        """Get SNMP enterprise number for the device.

        Args:
            None

        Returns:
            int: SNMP enterprise number identifying the device vendor
        """
        # Get the sysObjectID.0 value of the device
        sysid = self.sysobjectid()

        # Get the vendor ID
        enterprise_obj = iana_enterprise.Query(sysobjectid=sysid)
        enterprise = enterprise_obj.enterprise()

        # Return
        return enterprise

    def hostname(self):
        """Get SNMP hostname for the interaction.

        Args:
            None

        Returns:
            str: Hostname of the target device
        """
        # Initialize key variables
        hostname = self._poll.hostname

        # Return
        return hostname

    def contactable(self):
        """Check if device is reachable via SNMP.

        Args:
            None

        Returns:
            bool: True if device responds to SNMP queries, False otherwise
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

        except Exception:
            # Not contactable
            contactable = False

        except:
            # Log a message
            log_message = "Unexpected SNMP error for device {}" "".format(
                self._poll.hostname
            )
            log.log2die(1008, log_message)

        # Return
        return contactable

    def sysobjectid(self, check_reachability=False):
        """Get the sysObjectID of the device.

        Args:
            check_reachability: Boolean indicating whether to test connectivity.
                Some session errors are ignored to return null result.

        Returns:
            str: sysObjectID value as string, or None if not available
        """
        # Initialize key variables
        oid = ".1.3.6.1.2.1.1.2.0"
        object_id = None

        # Get sysObjectID
        results = self.get(oid, check_reachability=check_reachability)
        if bool(results) is True:
            object_id = results[oid].decode("utf-8")

        # Return
        return object_id

    def oid_exists(self, oid_to_get, context_name=""):
        """Determine if an OID exists on the device.

        Args:
            oid_to_get: String containing OID to check
            context_name: String containing SNMPv3 context name.
                Default is empty string.

        Returns:
            bool: True if OID exists, False otherwise
        """
        # Initialize key variables
        validity = False

        # Validate OID
        if self._oid_exists_get(oid_to_get, context_name=context_name) is True:
            validity = True

        if validity is False:
            if (
                self._oid_exists_walk(oid_to_get, context_name=context_name)
                is True
            ):
                validity = True

        # Return
        return validity

    def _oid_exists_get(self, oid_to_get, context_name=""):
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
            check_reachability=True,
            context_name=context_name,
            check_existence=True,
        )

        # If we get no result, then override validity
        if bool(result) is False:
            validity = False
        elif isinstance(result, dict) is True:
            if result[oid_to_get] is None:
                validity = False

        # Return
        return validity

    def _oid_exists_walk(self, oid_to_get, context_name=""):
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
        (_, validity, results) = self.query(
            oid_to_get,
            get=False,
            check_reachability=True,
            context_name=context_name,
            check_existence=True,
        )

        # If we get no result, then override validity
        if isinstance(results, dict) is True:
            for _, value in results.items():
                if value is None:
                    validity = False
                    break

        # Return
        return validity

    def swalk(self, oid_to_get, normalized=False, context_name=""):
        """Perform a safe SNMPwalk that handles errors gracefully.

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
            dict: Results of SNMP walk as OID-value pairs
        """
        # Process data
        results = self.walk(
            oid_to_get,
            normalized=normalized,
            check_reachability=True,
            check_existence=True,
            context_name=context_name,
            safe=True,
        )

        # Return
        return results

    def walk(
        self,
        oid_to_get,
        normalized=False,
        check_reachability=False,
        check_existence=False,
        context_name="",
        safe=False,
    ):
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
            safe: Safe query if true. If there is an exception, then return \
                blank values.

        Returns:
            result: Dictionary of tuples (OID, value)

        """
        (_, _, result) = self.query(
            oid_to_get,
            get=False,
            check_reachability=check_reachability,
            check_existence=check_existence,
            normalized=normalized,
            context_name=context_name,
            safe=safe,
        )
        return result

    def get(
        self,
        oid_to_get,
        check_reachability=False,
        check_existence=False,
        normalized=False,
        context_name="",
    ):
        """Do an SNMPget.

        Args:
            oid_to_get: OID to get
            check_reachability: Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence: Set if checking for the existence of the OID
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
           result: Dictionary of tuples (OID, value)

        """
        (_, _, result) = self.query(
            oid_to_get,
            get=True,
            check_reachability=check_reachability,
            check_existence=check_existence,
            normalized=normalized,
            context_name=context_name,
        )
        return result

    def query(
        self,
        oid_to_get,
        get=False,
        check_reachability=False,
        check_existence=False,
        normalized=False,
        context_name="",
        safe=False,
    ):
        """Do an SNMP query.

        Args:
            oid_to_get: OID to walk
            get: Flag determining whether to do a GET or WALK
            check_reachability: Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence: Set if checking for the existence of the OID
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.
            safe: Safe query if true. If there is an exception, then return\
                blank values.

        Returns:
            return_value: List of tuples (_contactable, exists, values)

        """
        # Initialize variables
        _contactable = True
        exists = True
        results = []

        # Check if OID is valid
        if _oid_valid_format(oid_to_get) is False:
            log_message = "OID {} has an invalid format".format(oid_to_get)
            log.log2die(1057, log_message)

        # Create SNMP session
        session = _Session(self._poll, context_name=context_name).session

        # Fill the results object by getting OID data
        try:
            # Get the data
            if get is True:
                results = [session.get(oid_to_get)]

            else:
                if self._poll.authorization.version != 1:
                    # Bulkwalk for SNMPv2 and SNMPv3
                    results = session.bulkwalk(
                        oid_to_get, non_repeaters=0, max_repetitions=25
                    )
                else:
                    # Bulkwalk not supported in SNMPv1
                    results = session.walk(oid_to_get)

        # Crash on error, return blank results if doing certain types of
        # connectivity checks
        except (
            exceptions.EasySNMPConnectionError,
            exceptions.EasySNMPTimeoutError,
            exceptions.EasySNMPUnknownObjectIDError,
            exceptions.EasySNMPNoSuchNameError,
            exceptions.EasySNMPNoSuchObjectError,
            exceptions.EasySNMPNoSuchInstanceError,
            exceptions.EasySNMPUndeterminedTypeError,
        ) as exception_error:
            # Update the error message
            log_message = _exception_message(
                self._poll.hostname,
                oid_to_get,
                context_name,
                sys.exc_info(),
            )

            # Process easysnmp errors
            (_contactable, exists) = _process_error(
                log_message,
                exception_error,
                check_reachability,
                check_existence,
            )

        except SystemError as exception_error:
            log_message = _exception_message(
                self._poll.hostname,
                oid_to_get,
                context_name,
                sys.exc_info(),
            )

            # Process easysnmp errors
            (_contactable, exists) = _process_error(
                log_message,
                exception_error,
                check_reachability,
                check_existence,
                system_error=True,
            )

        except:
            # Update the error message
            log_message = _exception_message(
                self._poll.hostname,
                oid_to_get,
                context_name,
                sys.exc_info(),
            )
            if bool(safe):
                _contactable = None
                exists = None
                log.log2info(1209, log_message)
            else:
                log.log2die(1003, log_message)

        # Format results
        values = _format_results(results, oid_to_get, normalized=normalized)

        # Return
        return_value = (_contactable, exists, values)
        return return_value


class _Session:
    """Class to create an SNMP session with a device."""

    def __init__(self, _poll, context_name=""):
        """Initialize the _Session class.

        Args:
            _poll: POLL object containing SNMP configuration
            context_name: String containing SNMPv3 context name.
                Default is empty string.

        Returns:
            session: SNMP session

        """
        # Initialize key variables
        self._context_name = context_name

        # Assign variables
        self._poll = _poll

        # Fail if there is no authentication
        if bool(self._poll.authorization) is False:
            log_message = (
                "SNMP parameters provided are blank. " "Non existent host?"
            )
            log.log2die(1046, log_message)

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
        if self._poll.authorization.version != 3:
            session = easysnmp.Session(
                community=self._poll.authorization.community,
                hostname=self._poll.hostname,
                version=self._poll.authorization.version,
                remote_port=self._poll.authorization.port,
                use_numeric=True,
                context=self._context_name,
            )
        else:
            session = easysnmp.Session(
                hostname=self._poll.hostname,
                version=self._poll.authorization.version,
                remote_port=self._poll.authorization.port,
                use_numeric=True,
                context=self._context_name,
                security_level=self._security_level(),
                security_username=self._poll.authorization.secname,
                privacy_protocol=self._priv_protocol(),
                privacy_password=self._poll.authorization.privpassword,
                auth_protocol=self._auth_protocol(),
                auth_password=self._poll.authorization.authpassword,
            )

        # Return
        return session

    def _security_level(self):
        """Determine SNMPv3 security level string.

        Args:
            None

        Returns:
            result: Security level
        """
        # Determine the security level
        if bool(self._poll.authorization.authprotocol) is True:
            if bool(self._poll.authorization.privprotocol) is True:
                result = "authPriv"
            else:
                result = "authNoPriv"
        else:
            result = "noAuthNoPriv"

        # Return
        return result

    def _auth_protocol(self):
        """Get SNMPv3 authentication protocol.

        Args:
            None

        Returns:
            str: Authentication protocol string ('MD5', 'SHA', or 'DEFAULT')
        """
        # Initialize key variables
        protocol = self._poll.authorization.authprotocol

        # Setup AuthProtocol (Default SHA)
        if bool(protocol) is False:
            result = "DEFAULT"
        else:
            if protocol.lower() == "md5":
                result = "MD5"
            else:
                result = "SHA"

        # Return
        return result

    def _priv_protocol(self):
        """Get SNMPv3 privacy protocol.

        Args:
            None

        Returns:
            str: Privacy protocol string ('DES', 'AES', or 'DEFAULT')
        """
        # Initialize key variables
        protocol = self._poll.authorization.privprotocol

        # Setup privProtocol (Default AES256)
        if bool(protocol) is False:
            result = "DEFAULT"
        else:
            if protocol.lower() == "des":
                result = "DES"
            else:
                result = "AES"

        # Return
        return result


def _exception_message(hostname, oid, context, exc_info):
    """Create standardized exception message for SNMP errors.

    Args:
        hostname: Hostname
        oid: OID being polled
        context: SNMP context
        exc_info: Exception information

    Returns:
        str: Formatted error message
    """
    # Create failure log message
    try_log_message = (
        "Error occurred during SNMP query on host "
        'OID {} from {} for context "{}"'
        "".format(oid, hostname, context)
    )

    # Add exception information
    result = """\
{}: [{}, {}, {}]""".format(
        try_log_message,
        exc_info[0],
        exc_info[1],
        exc_info[2],
    )

    # Return
    return result


def _process_error(
    log_message,
    exception_error,
    check_reachability,
    check_existence,
    system_error=False,
):
    """Process the SNMP error.

    Args:
        log_message: Log message
        exception_error: Exception error object
        check_reachability: Attempt to contact the device if True
        check_existence: Check existence of the device if True
        system_error: True if a System error

    Returns:
        alive: True if contactable

    """
    # Initialize key varialbes
    _contactable = True
    exists = True
    if system_error is False:
        error_name = "EasySNMPError"
    else:
        error_name = "SystemError"

    # Check existence of OID
    if check_existence is True:
        if system_error is False:
            if (
                isinstance(
                    exception_error,
                    easysnmp.exceptions.EasySNMPUnknownObjectIDError,
                )
                is True
            ):
                exists = False
                return (_contactable, exists)
            elif (
                isinstance(
                    exception_error,
                    easysnmp.exceptions.EasySNMPNoSuchNameError,
                )
                is True
            ):
                exists = False
                return (_contactable, exists)
            elif (
                isinstance(
                    exception_error,
                    easysnmp.exceptions.EasySNMPNoSuchObjectError,
                )
                is True
            ):
                exists = False
                return (_contactable, exists)
            elif (
                isinstance(
                    exception_error,
                    easysnmp.exceptions.EasySNMPNoSuchInstanceError,
                )
                is True
            ):
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
    log_message = "{}: {}".format(error_name, log_message)
    log.log2die(1023, log_message)


def _format_results(results, mock_filter, normalized=False):
    """Normalize and format SNMP walk results.

    Args:
        results: List of lists of results
        mock_filter: The original OID to get. Facilitates unittesting by
            filtering Mock values.
        normalized: If True, then return results as a dict keyed by
            only the last node of an OID, otherwise return results
            keyed by the entire OID string. Normalization is useful
            when trying to create multidimensional dicts where the
            primary key is a universal value such as IF-MIB::ifIndex
            or BRIDGE-MIB::dot1dBasePort

    Returns:
        dict: Formatted results as OID-value pairs
    """
    # Initialize key variables
    return_results = {}

    for result in results:
        # Recreate the OID
        oid = "{}.{}".format(result.oid, result.oid_index)

        # Ignore unwanted OIDs
        if mock_filter not in oid:
            continue

        # Process the rest
        if normalized is True:
            return_results[result.oid_index] = _convert(result)
        else:
            return_results[oid] = _convert(result)

    # Return
    return return_results


def _convert(result):
    """Convert SNMP value from pysnmp object to Python type.

    Args:
        result: Named tuple containing SNMP result

    Returns:
        converted: Value converted to appropriate Python type (bytes or int),
            or None for null/empty values
    """
    # Initialieze key values
    converted = None
    value = result.value
    snmp_type = result.snmp_type

    # Convert string type values to bytes
    if snmp_type.upper() == "OCTETSTR":
        converted = bytes(value, "utf-8")
    elif snmp_type.upper() == "OPAQUE":
        converted = bytes(value, "utf-8")
    elif snmp_type.upper() == "BITS":
        converted = bytes(value, "utf-8")
    elif snmp_type.upper() == "IPADDR":
        converted = bytes(value, "utf-8")
    elif snmp_type.upper() == "NETADDR":
        converted = bytes(value, "utf-8")
    elif snmp_type.upper() == "OBJECTID":
        # DO NOT CHANGE !!!
        converted = bytes(str(value), "utf-8")
    elif snmp_type.upper() == "NOSUCHOBJECT":
        # Nothing if OID not found
        converted = None
    elif snmp_type.upper() == "NOSUCHINSTANCE":
        # Nothing if OID not found
        converted = None
    elif snmp_type.upper() == "ENDOFMIBVIEW":
        # Nothing
        converted = None
    elif snmp_type.upper() == "NULL":
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
    """Validate OID string format.

    Args:
        oid: String containing OID to validate

    Returns:
        bool: True if OID format is valid, False otherwise
    """
    # oid cannot be numeric
    if isinstance(oid, str) is False:
        return False

    # Make sure the oid is not blank
    stripped_oid = oid.strip()
    if not stripped_oid:
        return False

    # Must start with a '.'
    if oid[0] != ".":
        return False

    # Must not end with a '.'
    if oid[-1] == ".":
        return False

    # Test each octet to be numeric
    octets = oid.split(".")

    # Remove the first element of the list
    octets.pop(0)
    for value in octets:
        try:
            int(value)
        except:
            return False

    # Otherwise valid
    return True


def _update_cache(filename, group):
    """Update SNMP credentials cache file.

    Args:
        filename: String containing path to cache file
        group: String containing SNMP group name to cache

    Returns:
        None
    """
    # Do update
    with open(filename, "w+") as env:
        env.write(group)
