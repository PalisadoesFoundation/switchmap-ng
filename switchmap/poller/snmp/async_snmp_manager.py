"""Async SNMP manager class """

import os
import sys
import asyncio


#import project libraries
from switchmap.core import log
from switchmap.core import files
from switchmap.poller import POLL 
from switchmap.poller.configuration import ConfigPoller

from pysnmp.hlapi.asyncio import (
    SnmpEngine, CommunityData, UdpTransportTarget, ContextData, 
    ObjectType, ObjectIdentity, getCmd, nextCmd, bulkCmd, 
    UsmUserData, usmHMACMD5AuthProtocol, usmHMACSHAAuthProtocol,
    usmDESPrivProtocol,usmAesCfb128Protocol, usmAesCfb192Protocol,
    usmAesCfb256Protocol
)

from pysnmp.proto.errind import RequestTimedOut
from pysnmp.error import PySnmpError
from pysnmp.proto.rfc1905 import EndOfMibView, NoSuchInstance, NoSuchObject


class Validate: 
    """Class to validate SNMP data asynchronously. """

    def __init__(self, options):
        """Initialize the Validate class. 
        
        Args: 
            options: POLLING_OPTIONS object containing SNMP configuration.
        
        Returns:
           None
        """

        self._options = options

    async def credentials(self):
        """ Determine valid SNMP credentials for a host.

        Args:
            None
        
        Returns:
            authentication: SNMP authorization object containing valid credentials,
            or None if no valid credentials found
        """

        cache_exists = False

        filename = files.snmp_file(self._options.hostname,ConfigPoller())

        if(os.path.exists(filename)):
            cache_exists= True
        
        if cache_exists is False:
            authentication = self.validation()
    
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
        for authorization in self._options.authorizations():
            #Only process enabled SNMP values
            if bool(authorization.enabled) is False:
                continue
            
            # Setup contact with the remote device
            device = Interact(
                POLL(
                    hostname=self._options.hostname,
                    authorization=authorization
                )
            )
            # Try successive groups



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
                "SNMP parameters provided are either blank or missing." "Non existent host?"
            )
            log.log2die(1045, log_message)
        
    async def contactable(self): 
        """Check if device is reachable via SNMP.
        
        Args: 
            None
        
        Returns:
           bool: True if device responds to SNMP queries, False otherwise
        
        """
        #key variables
        contactable = False
        result = None 

        #Try to reach device
        try:
            # Test if we can poll the SNMP sysObjectID
            # if true, then the device is contactable
            result = await self.sysobjectID(check_reachability=True)
            if bool(result) is True:
                contactable = True
        
        except Exception:
            # Not Contactable
            contactable = False
        
        except:
            # Log the error message
            log_message = "Unexpected SNMP error for device {}" "".format(
                self._poll.hostname
            )
            log.log2die(1008,log_message)
        
        return contactable
    
    async def sysobjectID(self, check_reachability=False):
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
        
        #Get sysObjectID
        results = await self.get(oid, check_reachability)
        # Pysnmp already returns out value as value unlike easysnmp
        if bool(results) is True:
            object_id = results[oid]
        
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
        # Initialize key 
        validity = False

        # Validate OID
        if await self._oid_exists_get(oid_to_get,context_name=context_name) is True:
            validity = True 
        if validity is False:
            if await self._oid_exists_walk(oid_to_get, context_name=context_name) is True:
                validity = True
        
        return validity
    
    async def _oid_exists_get(self, oid_to_get,context_name=""):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exists

        """
        validity = False 
        
        #! check the validity arg in query
        (_,validity,result) = await self.query(
            oid_to_get,
            context_name = context_name,
            get = True,
            check_reachability = True,
            check_existence = True
        )

        # If we get no result, then override validity
        if bool(result) is False:
            validity = False
        elif isinstance(result, dict) is True:
            if result[oid_to_get] is None:
                validity = False
        
        return validity;

    async def _oid_exists_walk(self,oid_to_get, context_name=""):
        """Check OID existence on device using WALK.

         Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exist
        """

        (_,_, results) = await self.query(
            oid_to_get,
            get= False,
            check_reachability = True,
            context_name = context_name,
            check_existence = True
        )

        # If we get no result, then override validity 
        if isinstance(results,dict) is True:
            for value in results.values():
                if value is not None:
                    return True 
        return False

class Session:
    """Class to create a SNMP session with a device. """

    def _init__(self,_poll,context_name=""):
        """Initialize the _Session class.

        Args:
            _poll: POLL object containing SNMP configuration
            context_name: String containing SNMPv3 context name.
                Default is empty string.

        Returns:
            session: SNMP session
        """
        #Assign variables
        self.context_name = context_name
        self._poll = _poll
        self._engine = SnmpEngine()

        
        #! dont hardcore the ratelimit (change it later)
        #Rate limiting 
        self._semaphore = asyncio.Semaphore(10)

        #Fail if there is no authentication
        if bool(self._poll.authorization) is False:
            log_message = (
                "SNMP parameters provided are blank. None existent host? "
            )
            log.log2die(1046, log_message)
        
        #Create SNMP session 
        self.session = self._session

    async def _session(self):
        """ Create SNMP session parameters based on configuration.

        Returns:
            Tuple of (auth_data, transport_target)
        """

        auth = self._poll.authorization

        #Create transport target
        transport_target = UdpTransportTarget(
            (self._poll.hostname, auth.port),
            timeout=10,
            retries= 3
        )

        #Create authentication data based on SNMP version
        if auth.version == 3:
            #SNMPv3 with USM
            #If authprotocol/privprotocol is None/False/Empty, leave them as None 
            auth_protocol = None
            priv_protocol = None 

            #Set auth protocol only if authprotocol is specified
            if auth.authprotocol:
                if auth.authprotocol.lower() == 'md5':
                    auth_protocol = usmHMACMD5AuthProtocol
                else:
                    auth_protocol = usmHMACSHAAuthProtocol
            
            #Set privacy protocol only if privprotocol is specified
            #Also if we have authentication (privacy require authentication)
            if auth.privprotocol and auth_protocol is not None:
                if auth.privprotocol.lower() == 'des':
                    priv_protocol = usmDESPrivProtocol
                else:
                    priv_protocol = usmAesCfb128Protocol
            
            auth_data = UsmUserData(
                userName= auth.secname,
                authKey=auth.authpassword,
                privKey=auth.privpassword,
                authProtocol=auth_protocol,
                privProtocol=priv_protocol
            )
        else:
            #SNMPv1/v2c with community
            mp_model = 0 if auth.version == 1 else 1
            auth_data = CommunityData(auth.community, mpModel=mp_model)

        return auth_data, transport_target
    
    async def _do_async_get(self, oid, auth_data,transport_target, context_data):
        """ Pure async SNMP GET using pysnmp """

        error_indication,error_status,error_index,var_binds = await getCmd(
            self._engine,
            auth_data,
            transport_target,
            context_data,
            ObjectType(ObjectIdentity(oid))
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
            results.append((oid_str,value))
        
        return results
    
    async def _do_async_walk(self,oid_prefix,auth_data,transport_target,context_data):
        """ Pure async SNMP WALK using pysnmp async capabilities. """

        results = []

        #Use correct walk method based on SNMP version
        if hasattr(auth_data, "mpModel") and auth_data.mpModel == 0:
            # SNMPv1 - use nextCMD
            results = await self._async
    
    async def _async_walk_v1(self,oid_prefix, auth_data,transport_target,context_data):
        """Pure async walk for SNMPv1 using nextCmd. """
        results = []
        current_oid = oid_prefix

        async for (error_indication, error_status, error_index, var_binds) in nextCmd(
            self._engine,
            auth_data,
            transport_target,
            context_data,
            ObjectType(ObjectIdentity(oid_prefix)),
            lexicographicMode= False
        ):
            #! better error handling 
            if error_indication or error_status:
                break

            for oid,value in var_binds:
                oid_str = str(oid)
                if not oid_str.startswith(oid_prefix):
                    #! should we just return only till last case or also send a msg that last oid reached
                    return results
                results.append((oid_str,value))
            
        return results
    
    async def _async_walk_v2(self,oid_prefix,auth_data, transport_target,context_data):
        """Async walk for SNMPv2c/v3 using bulkCmd"""

        results = []
        current_oids = ObjectType(ObjectIdentity(oid_prefix))

        try:
            max_iterations = 100
            iterations = 0

            while iterations < max_iterations:
                iterations += 1
                # non-repeaters = 0 , max_repetitions = 25
                error_indication, error_status, error_index, var_bind_table = await bulkCmd(
                    self._engine,
                    auth_data,
                    transport_target,
                    context_data,
                    0, 25,
                    *current_oids
                )
                
                #! adding more speficic logs here
                if error_indication:
                    print(f"BULK error indication: {error_indication}")
                    break
                elif error_status:
                    print(f" BULK error status: {error_status.prettyPrint()} at {error_index}")
                    break
                
                #Check if we got any response
                if not var_bind_table:
                    print(f"No more data")
                    break

                #Process the response
                next_oids= []
                found_valid_data = False

                for var_bind in var_bind_table:
                    for oid,value in var_bind:

                        #Check for end of MIB 
                        if isinstance(value, EndOfMibView):
                            continue 
                        
                        #! little doubt over time complexity 
                        #Check if we are still within our desired OID prefix
                        if not str(oid).startswith(oid_prefix):
                            continue 
                        
                        results.append((str(oid),value))
                        next_oids.append(ObjectType(ObjectIdentity(oid)))
                        found_valid_data = True

                
                if not found_valid_data:
                    print(f"BULK walk: No more valid data for prefix {oid_prefix}")
                    break

                current_oids = [next_oids[-1]] if next_oids else []

        except Exception as e:
            print(f"BULK walk error: {e}")
            return await self._async_walk_v1(oid_prefix, auth_data, transport_target, context_data)

        return results





        






                



    

    
    




       

       
    

    
    
    


    

        