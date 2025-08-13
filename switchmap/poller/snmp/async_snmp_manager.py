"""Async SNMP manager class"""

import os
import asyncio


# import project libraries
from switchmap.core import log
from switchmap.core import files
from switchmap.poller import POLL
from switchmap.poller.configuration import ConfigPoller

from . import iana_enterprise

from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    nextCmd,
    bulkCmd,
    UsmUserData,
    # Authentication protocols
    usmHMACMD5AuthProtocol,
    usmHMACSHAAuthProtocol,
    usmHMAC128SHA224AuthProtocol,
    usmHMAC192SHA256AuthProtocol,
    usmHMAC256SHA384AuthProtocol,
    usmHMAC384SHA512AuthProtocol,
    # Privacy protocols
    usmDESPrivProtocol,
    usmAesCfb128Protocol,
    usmAesCfb192Protocol,
    usmAesCfb256Protocol,
)

from pysnmp.error import PySnmpError
from pysnmp.proto.rfc1905 import EndOfMibView, NoSuchInstance, NoSuchObject


class Validate:
    """Class to validate SNMP data asynchronously."""

    def __init__(self, options):
        """Initialize the Validate class.

        Args:
            options: POLLING_OPTIONS object containing SNMP configuration.

        Returns:
           None
        """

        self._options = options

    async def credentials(self):
        """Determine valid SNMP credentials for a host.

        Args:
            None

        Returns:
            authentication: SNMP authorization object containing valid credentials,
            or None if no valid credentials found
        """

        cache_exists = False

        filename = files.snmp_file(self._options.hostname, ConfigPoller())

        if os.path.exists(filename):
            cache_exists = True

        if cache_exists is False:
            authentication = await self.validation()

            # Save credentials if successful
            if bool(authentication):
                _update_cache(filename, authentication.group)
        else:
            # Read credentials from cache
            if os.path.isfile(filename):
                with open(filename) as f_handle:
                    group = f_handle.readline().strip()

            # Get Credentials
            authentication = await self.validation(group)

            # Try the rest if the credentials fail
            if bool(authentication) is False:
                authentication = await self.validation()

            # update cache if found
            if bool(authentication):
                _update_cache(filename, authentication.group)

        return authentication

    async def validation(self, group=None):
        """Determine valid SNMP authorization for a host.

        Args:
            group: String containing SNMP group name to try, or None to try all
               groups

        Returns:
            result: SNMP authorization object if valid credentials found,
                None otherwise
        """

        result = None

        # Probe device with all SNMP options
        for authorization in self._options.authorizations:
            # Only process enabled SNMP values
            if bool(authorization.enabled) is False:
                continue

            # Setup contact with the remote device
            device = Interact(
                POLL(
                    hostname=self._options.hostname, authorization=authorization
                )
            )
            # Try successive groups check if device is contactable
            if group is None:
                if await device.contactable() is True:
                    result = authorization
                    break
            else:
                if authorization.group == group:
                    if await device.contactable() is True:
                        result = authorization

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

        # Rate Limiting
        self._semaphore = asyncio.Semaphore(10)

        # Fail if there is no authentication
        if bool(self._poll.authorization) is False:
            log_message = (
                "SNMP parameters provided are either blank or missing."
                "Non existent host?"
            )
            log.log2die(1045, log_message)

    async def enterprise_number(self):
        """Get SNMP enterprise number for the device.

        Args:
            None

        Returns:
            int: SNMP enterprise number identifying the device vendor
        """
        # Get the sysObjectID.0 value of the device
        sysid = await self.sysobjectid()

        # Get the vendor ID
        enterprise_obj = iana_enterprise.Query(sysobjectid=sysid)
        enterprise = enterprise_obj.enterprise()

        return enterprise

    def hostname(self):
        """Get SNMP hostname for the interaction.

        Args:
            None

        Returns:
            str: Hostname of the target device
        """
        return self._poll.hostname

    async def contactable(self):
        """Check if device is reachable via SNMP.

        Args:
            None

        Returns:
           bool: True if device responds to SNMP queries, False otherwise

        """
        # key variables
        contactable = False
        result = None

        # Try to reach device
        try:
            # Test if we can poll the SNMP sysObjectID
            # if true, then the device is contactable
            result = await self.sysobjectid(check_reachability=True)
            if bool(result) is True:
                contactable = True

        except Exception:
            # Not Contactable
            contactable = False

        return contactable

    async def sysobjectid(self, check_reachability=False):
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
        results = await self.get(oid, check_reachability)
        # Pysnmp already returns out value as value unlike easysnmp
        if bool(results) is True:
            # Both formats: with and without leading dot
            object_id = results.get(oid)
            if object_id is None:
                oid_without_dot = oid.lstrip(".")
                object_id = results.get(oid_without_dot)

            # Convert bytes to string if needed
            if isinstance(object_id, bytes):
                object_id = object_id.decode("utf-8")

        return object_id

    async def oid_exists(self, oid_to_get, context_name=""):
        """Determine if an OID exists on the device.

        Args:
            oid_to_get: String containing OID to check
            context_name: String containing SNMPv3 context name.
                Default is empty string.

        Returns:
            bool: True if OID exists, False otherwise
        """
        try:
            # Initialize key
            validity = False

            # Validate OID
            if (
                await self._oid_exists_get(
                    oid_to_get, context_name=context_name
                )
                is True
            ):
                validity = True
            if validity is False:
                if (
                    await self._oid_exists_walk(
                        oid_to_get, context_name=context_name
                    )
                    is True
                ):
                    validity = True

            return validity
        except Exception as e:
            log.log2warning(
                1305, f"OID existence check failed for {oid_to_get}: {e}"
            )
            return False

    async def _oid_exists_get(self, oid_to_get, context_name=""):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exists

        """
        try:
            validity = False

            (_, exists, result) = await self.query(
                oid_to_get,
                get=True,
                check_reachability=True,
                check_existence=True,
                context_name=context_name,
            )

            if exists and bool(result):
                # Make sure the OID key exists in result
                if isinstance(result, dict) and oid_to_get in result:
                    if result[oid_to_get] is not None:
                        validity = True
                elif isinstance(result, dict) and result:
                    # If result has data but not exact OID, still consider it valid
                    validity = True

            return validity
        except Exception as e:
            log.log2warning(
                1305, f"OID existence check failed for {oid_to_get}: {e}"
            )
            return False

    async def _oid_exists_walk(self, oid_to_get, context_name=""):
        """Check OID existence on device using WALK.

         Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exist
        """

        try:
            (_, exists, results) = await self.query(
                oid_to_get,
                get=False,
                check_existence=True,
                context_name=context_name,
                check_reachability=True,
            )
            # Check if we get valid results
            if exists and isinstance(results, dict) and results:
                return True
            return False
        except Exception as e:
            log.log2warning(
                1306, f"Walk existence check failed for {oid_to_get}: {e}"
            )
            return False

    async def get(
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
           result: Dictionary of {OID: value} pairs

        """
        (_, _, result) = await self.query(
            oid_to_get,
            get=True,
            check_reachability=check_reachability,
            check_existence=check_existence,
            normalized=normalized,
            context_name=context_name,
        )
        return result

    async def walk(
        self,
        oid_to_get,
        normalized=False,
        check_reachability=False,
        check_existence=False,
        context_name="",
        safe=False,
    ):
        """Do an async SNMPwalk
        

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

        (_, _, result) = await self.query(
            oid_to_get,
            get=False,
            check_reachability=check_reachability,
            check_existence=check_existence,
            normalized=normalized,
            context_name=context_name,
            safe=safe,
        )

        return result

    async def swalk(self, oid_to_get, normalized=False, context_name=""):
        """Perform a safe async SNMPwalk that handles errors gracefully.

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
        return await self.walk(
            oid_to_get,
            normalized=normalized,
            check_reachability=True,
            check_existence=True,
            context_name=context_name,
            safe=True,
        )

    async def query(
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
            return_value: Tuple of (_contactable, exists, values)

        """
        # Initialize variables
        _contactable = True
        exists = True
        results = []
        # Initialize formatted_result to avoid undefined variable error
        formatted_result = {}

        # Check if OID is valid
        if _oid_valid_format(oid_to_get) is False:
            log_message = "OID {} has an invalid format".format(oid_to_get)
            log.log2die(1057, log_message)

        # Get session parameters
        async with self._semaphore:
            try:
                # Create SNMP session
                session = Session(self._poll, context_name=context_name)

                # Use shorter timeouts for walk operations
                auth_data, transport_target = await session._session(
                    walk_operation=(not get)
                )
                context_data = ContextData(contextName=context_name)

                # Perform the SNMP operation
                if get is True:
                    results = await session._do_async_get(
                        oid_to_get, auth_data, transport_target, context_data
                    )
                else:
                    results = await session._do_async_walk(
                        oid_to_get, auth_data, transport_target, context_data
                    )

                formatted_result = _format_results(
                    results, oid_to_get, normalized=normalized
                )

            except PySnmpError as exception_error:
                # Handle PySNMP errors similar to sync version
                if check_reachability is True:
                    _contactable = False
                    exists = False
                elif check_existence is True:
                    exists = False
                elif safe is True:
                    _contactable = None
                    exists = None
                    log_message = f"Async SNMP error for {self._poll.hostname}: {exception_error}"
                    log.log2info(1209, log_message)
                else:
                    log_message = f"Async SNMP error for {self._poll.hostname}: {exception_error}"
                    log.log2die(1003, log_message)
                # Ensure formatted_result is set for exception cases
                formatted_result = {}

            except Exception as exception_error:
                # Handle unexpected errors
                if safe is True:
                    _contactable = None
                    exists = None
                    log_message = f"Unexpected async SNMP error for {self._poll.hostname}: {exception_error}"
                    log.log2info(1210, log_message)
                else:
                    log_message = f"Unexpected async SNMP error for {self._poll.hostname}: {exception_error}"
                    log.log2die(1003, log_message)
                # Ensure formatted_result is set for exception cases
                formatted_result = {}

        # Return
        values = (_contactable, exists, formatted_result)
        return values


class Session:
    """Class to create a SNMP session with a device."""

    def __init__(self, _poll, context_name=""):
        """Initialize the _Session class.

        Args:
            _poll: POLL object containing SNMP configuration
            context_name: String containing SNMPv3 context name.
                Default is empty string.

        Returns:
            session: SNMP session
        """
        # Assign variables
        self.context_name = context_name
        self._poll = _poll
        self._engine = SnmpEngine()

        # Fail if there is no authentication
        if bool(self._poll.authorization) is False:
            log_message = (
                "SNMP parameters provided are blank. None existent host? "
            )
            log.log2die(1046, log_message)

    async def _session(self, walk_operation=False):
        """Create SNMP session parameters based on configuration.

        Returns:
            Tuple of (auth_data, transport_target)
        """

        auth = self._poll.authorization

        # Use shorter timeouts for walk operations to prevent hanging
        if walk_operation:
            timeout = 3
            retries = 1
        else:
            # Normal timeout for GET operations
            timeout = 10
            retries = 3

        # Create transport target
        transport_target = UdpTransportTarget(
            (self._poll.hostname, auth.port), timeout=timeout, retries=retries
        )

        # Create authentication data based on SNMP version
        if auth.version == 3:
            # SNMPv3 with USM
            # If authprotocol/privprotocol is None/False/Empty, leave them as None
            auth_protocol = None
            priv_protocol = None

            # Set auth protocol only if authprotocol is specified
            if auth.authprotocol:
                auth_proto = auth.authprotocol.lower()
                if auth_proto == "md5":
                    auth_protocol = usmHMACMD5AuthProtocol
                elif auth_proto == "sha1" or auth_proto == "sha":
                    auth_protocol = usmHMACSHAAuthProtocol
                elif auth_proto == "sha224":
                    auth_protocol = usmHMAC128SHA224AuthProtocol
                elif auth_proto == "sha256":
                    auth_protocol = usmHMAC192SHA256AuthProtocol
                elif auth_proto == "sha384":
                    auth_protocol = usmHMAC256SHA384AuthProtocol
                elif auth_proto == "sha512":
                    auth_protocol = usmHMAC384SHA512AuthProtocol
                else:
                    # Default to SHA-256 for better security
                    auth_protocol = usmHMAC192SHA256AuthProtocol

            # Set privacy protocol only if privprotocol is specified
            # Also if we have authentication (privacy requires authentication)
            if auth.privprotocol and auth_protocol is not None:
                priv_proto = auth.privprotocol.lower()
                if priv_proto == "des":
                    priv_protocol = usmDESPrivProtocol
                elif priv_proto == "aes128" or priv_proto == "aes":
                    priv_protocol = usmAesCfb128Protocol
                elif priv_proto == "aes192":
                    priv_protocol = usmAesCfb192Protocol
                elif priv_proto == "aes256":
                    priv_protocol = usmAesCfb256Protocol
                else:
                    # Default to AES-256 for best security
                    priv_protocol = usmAesCfb256Protocol

            auth_data = UsmUserData(
                userName=auth.secname,
                authKey=auth.authpassword,
                privKey=auth.privpassword,
                authProtocol=auth_protocol,
                privProtocol=priv_protocol,
            )
        else:
            # SNMPv1/v2c with community
            mp_model = 0 if auth.version == 1 else 1
            auth_data = CommunityData(auth.community, mpModel=mp_model)

        return auth_data, transport_target

    async def _do_async_get(
        self, oid, auth_data, transport_target, context_data
    ):
        """Pure async SNMP GET using pysnmp"""

        error_indication, error_status, error_index, var_binds = await getCmd(
            self._engine,
            auth_data,
            transport_target,
            context_data,
            ObjectType(ObjectIdentity(oid)),
        )

        if error_indication:
            raise PySnmpError(f"SNMP GET error: {error_indication}")
        elif error_status:
            raise PySnmpError(f"SNMP GET error status: {error_status}")

        # Return in object format expected by _format_results
        results = []
        for var_bind in var_binds:
            oid_str = str(var_bind[0])
            value = var_bind[1]
            results.append((oid_str, value))

        return results

    async def _do_async_walk(
        self, oid_prefix, auth_data, transport_target, context_data
    ):
        """Pure async SNMP WALK using pysnmp async capabilities."""

        results = []

        # Use correct walk method based on SNMP version
        if hasattr(auth_data, "mpModel") and auth_data.mpModel == 0:
            # SNMPv1 - use nextCMD
            results = await self._async_walk_v1(
                oid_prefix, auth_data, transport_target, context_data
            )
        else:
            # SNMPv2c/v3 - use bulkCmd

            try:
                results = await asyncio.wait_for(
                    self._async_walk_v2(
                        oid_prefix, auth_data, transport_target, context_data
                    ),
                    timeout=60.0,
                )
            except asyncio.TimeoutError:
                log.log2info(
                    1011, f"bulk walk timeout after 60s for prefix {oid_prefix}"
                )
                # Fallback to SNMPv1 walk which would be more reliable
                results = await self._async_walk_v1(
                    oid_prefix, auth_data, transport_target, context_data
                )

        return results

    async def _async_walk_v1(
        self, oid_prefix, auth_data, transport_target, context_data
    ):
        """Pure async walk for SNMPv1 using nextCmd."""
        results = []

        try:
            async for (
                error_indication,
                error_status,
                error_index,
                var_binds,
            ) in nextCmd(
                self._engine,
                auth_data,
                transport_target,
                context_data,
                ObjectType(ObjectIdentity(oid_prefix)),
                lexicographicMode=False,
            ):
                # Handle errors first
                if error_indication:
                    log.log2warning(
                        1216,
                        f"SNMP v1 walk network error for {oid_prefix}: {error_indication}.",
                    )
                    break

                elif error_status:
                    log.log2info(
                        1217,
                        f"SNMP v1 walk protocol error for {oid_prefix}: {error_status} at index {error_index}",
                    )

                    # Handle specific SNMP errors
                    error_msg = error_status.prettyPrint()
                    if error_msg == "noSuchName":
                        # This OID doesn't exist, try next
                        continue
                    else:
                        # Other errors are usually fatal
                        break

                # Process successful response
                for oid, value in var_binds:
                    oid_str = str(oid)
                    if not oid_str.startswith(oid_prefix):
                        log.log2debug(
                            1220,
                            f"Reached end of OID tree for prefix {oid_prefix}",
                        )
                        return results
                    results.append((oid_str, value))

            # Return results after the loop completes
            return results

        except Exception as e:
            log.log2warning(
                1222, f"Unexpected error in SNMP v1 walk for {oid_prefix}: {e}."
            )
            return results

    async def _async_walk_v2(
        self, oid_prefix, auth_data, transport_target, context_data
    ):
        """Async walk for SNMPv2c/v3 using bulkCmd"""

        results = []
        current_oids = [ObjectType(ObjectIdentity(oid_prefix))]

        try:
            #! checking for 50, 100 would be too long to prevent from hanging
            max_iterations = 50
            iterations = 0
            consecutive_empty_responses = 0
            # Stop after 3 consecutive empty responses
            max_empty_responses = 3

            while current_oids and iterations < max_iterations:
                iterations += 1
                # non-repeaters = 0 , max_repetitions = 25
                error_indication, error_status, error_index, var_bind_table = (
                    await bulkCmd(
                        self._engine,
                        auth_data,
                        transport_target,
                        context_data,
                        0,
                        25,
                        *current_oids,
                    )
                )

                if error_indication:
                    log.log2info(
                        1211, f"BULK error indication: {error_indication}"
                    )
                    break
                elif error_status:
                    log.log2info(
                        1212,
                        f"BULK error status: {error_status.prettyPrint()} at {error_index}",
                    )
                    break

                # Check if we got any response
                if not var_bind_table:
                    consecutive_empty_responses += 1
                    if consecutive_empty_responses >= max_empty_responses:
                        break
                    continue
                else:
                    consecutive_empty_responses = 0

                # Process the response
                next_oids = []
                found_valid_data = False

                for var_bind in var_bind_table:
                    if not var_bind or len(var_bind) == 0:
                        continue

                    # Get the ObjectType from the list
                    obj_type = var_bind[0]

                    # Extract OID and value from ObjectType
                    oid = obj_type[0]
                    value = obj_type[1]

                    # Check for end of MIB
                    if isinstance(value, EndOfMibView):
                        continue

                    # Check if we are still within our desired OID prefix
                    oid_str = str(oid)

                    # Remove leading dot for comparison
                    prefix_normalized = str(oid_prefix).lstrip(".")
                    oid_normalized = oid_str.lstrip(".")

                    if not oid_normalized.startswith(prefix_normalized):
                        continue

                    results.append((oid_str, value))
                    next_oids.append(ObjectType(ObjectIdentity(oid)))
                    found_valid_data = True

                if not found_valid_data:
                    log.log2info(
                        1213,
                        f"BULK walk: No more valid data for prefix {oid_prefix}",
                    )
                    break

                current_oids = next_oids

                # In case, we get too many results
                if len(results) > 10000:
                    log.log2warning(
                        1214,
                        f"Stopping after collecting {len(results)} results (safety limit)",
                    )
                    break

        except Exception as e:
            log.log2warning(1215, f"BULK walk error: {e}")
            return await self._async_walk_v1(
                oid_prefix, auth_data, transport_target, context_data
            )

        return results


def _oid_valid_format(oid):
    """Validate OID string format matching sync version.

    Args:
       oid: String containing OID to validate

    Returns:
       bool: True if OID format is valid, False otherwise
    """

    # oid cannot be numeric
    if isinstance(oid, str) is False:
        return False

    # Make sure that oid is not blank
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
        except ValueError:
            return False

    # Otherwise valid
    return True


def _convert(value):
    """Convert SNMP value from pysnmp object to Python type.

    Args:
        result: pysnmp value object

    Returns:
        converted: Value converted to appropriate Python type (bytes or int),
            or None for null/empty values
    """

    # Handle pysnmp exception values
    if isinstance(value, NoSuchObject):
        return None
    if isinstance(value, NoSuchInstance):
        return None
    if isinstance(value, EndOfMibView):
        return None

    if hasattr(value, "prettyPrint"):
        value_str = value.prettyPrint()

        # Determine type based on pysnmp object type
        value_type = type(value).__name__

        # Handle string-like types - Convert to types for MIB compatibility
        if any(
            t in value_type
            for t in [
                "OctetString",
                "DisplayString",
                "Opaque",
                "Bits",
                "IpAddress",
                "ObjectIdentifier",
            ]
        ):
            # For objectID, convert to string first then to bytes
            if "ObjectIdentifier" in value_type:
                return bytes(str(value_str), "utf-8")
            else:
                return bytes(value_str, "utf-8")

        # Handle integer types
        elif any(
            t in value_type
            for t in ["Integer", "Counter", "Gauge", "TimeTicks", "Unsigned"]
        ):
            try:
                return int(value_str)
            except ValueError:
                # Direct int conversion of the obj if prettyPrint fails
                if hasattr(value, "__int__"):
                    try:
                        return int(value)
                    except (ValueError, TypeError):
                        pass

                # Accessing .value attr directly
                if hasattr(value, "value"):
                    try:
                        return int(value.value)
                    except (ValueError, TypeError):
                        pass

                log_message = f"Failed to convert pysnmp integer valye: {value_type}, prettyPrint'{value_str}"
                log.log2warning(1059, log_message)
                return None

    # Handle direct access to value (for objects without prettyPrint)
    if hasattr(value, "value"):
        try:
            return int(value.value)
        except (ValueError, TypeError):
            return bytes(str(value.value), "utf-8")

    # Default Fallback - convert to string then to bytes
    try:
        return bytes(str(value), "utf-8")
    except Exception:
        return None


def _format_results(results, mock_filter, normalized=False):
    """Normalized and format SNMP results

    Args:
        results: List of (OID, value) tuples from pysnmp
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

    formatted = {}

    for oid_str, value in results:

        # Normalize both OIDs for comparison to handle leading dot mismatch
        if mock_filter:
            # Remove leading dots for comparison
            filter_normalized = mock_filter.lstrip(".")
            oid_normalized = oid_str.lstrip(".")

            if filter_normalized not in oid_normalized:
                continue

        # convert value using proper type conversion
        converted_value = _convert(value=value)

        if normalized is True:
            # use only the last node of the OID
            key = oid_str.split(".")[-1]
        else:
            key = oid_str

        formatted[key] = converted_value

    return formatted


def _update_cache(filename, group):
    """Update SNMP credentials cache file.

    Args:
        filename: String containing path to cache file
        group: String containing SNMP group name to cache

    Returns:
        None
    """
    try:
        with open(filename, "w+") as f_handle:
            f_handle.write(group)
    except Exception as e:
        log_message = f"Failed to update cache file {filename}: {e}"
        log.log2warning(1049, log_message)
