"""Async SNMP manager class """

import os
import sys


#import project libraries
from switchmap.core import log
from switchmap.core import files
from switchmap.poller import POLL 
from switchmap.poller.configuration import ConfigPoller


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
        

       

       
    

    
    
    


    

        