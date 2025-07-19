"""Asynchronous SNMP Poller module for switchmap-ng. """

import asyncio 

# Switchmap imports 
from switchmap.poller.configuration import ConfigPoller
from switchmap.poller import POLLING_OPTIONS, SNMP, POLL
from . import async_snmp_manager
from . import async_snmp_info
from switchmap.core import log

#!add better description 
class Poll:
    """Switchmap-NG agent that gathers data.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        populate:
        post:
    """

    def __init__(self, hostname):
        """Initialize the class.

        Args:
            hostname: Hostname to poll

        Returns:
            None

        """

        # Initialize key variables 
        self._server_config = ConfigPoller()
        self._hostname = hostname
        self._snmp_object = None 

        print(f"Initialize snmp poller for {hostname}")
     
    #! maybe add a better method name
    async def initialize_snmp(self):
        """Initialize SNMP connection asynchronously.
        
        Returns;
            bool: True if successful, False otherwise
        """
        # Get snmp config information from Switchmap-NG 
        validate = async_snmp_manager.Validate(
            POLLING_OPTIONS(
                hostname=self._hostname,
                authorizations=self._server_config.snmp_auth(),
            )
        )

        # Get credentials asynchronously 
        authorization = await validate.credentials() 

        print(f"check creds for hostname: {self._hostname}, creds: {authorization}")

        # Create an SNMP object for querying
        if _do_poll(authorization) is True:
            self._snmp_object = async_snmp_manager.Interact(
                POLL(
                    hostname=self._hostname,
                    authorization=authorization
                )
            )
            return True
        else:
            print(f"cannot create SNMP object for {self._hostname}")
            log_message = (
                "Uncontactable or disabled host {}, or no valid SNMP "
                "credentials found in it.".format(self._hostname)
            )
            log.log2info(1081, log_message)
            return False
        
    async def query(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            dict: Polled data or None if failed

        """
        # Initialize key variables
        _data = None

        #Only query if the device is contactable
        if bool(self._snmp_object) is False:
            #! may add a log here, for better reading
            print(f"No valid SNMP object for {self._hostname} ")
            return _data 
        
        # Get data 
        log_message = """\
Querying topology data from host: {}.""".format(self._hostname)
        
        log.log2info(1078, log_message)

        status = async_snmp_info.Query(snmp_object=self._snmp_object)

        _data = await status.everything()

        print(f"ALl the data broo: {_data}")

        return _data 
    

def _do_poll(authorization):
    """Determine whether doing a poll is valid.

    Args:
        authorization: SNMP object
    
    Returns:
        poll: True if a poll should be done
    
    """
    # Initialize key variables
    poll = False 

    if bool(authorization) is True:
        if isinstance(authorization, SNMP) is True:
            poll = bool(authorization.enabled)
    
    return poll