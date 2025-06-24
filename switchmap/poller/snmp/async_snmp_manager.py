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


    

        