"""
Simple script to test our async manager for misc data collections
also credentials validation && 
checking for device connection 
"""

import sys
import time
import asyncio


sys.path.insert(0,"/Users/imexyyyyy/files/gsoc/switchmap-ng")

from switchmap.poller.snmp import async_snmp_manager 
from switchmap.poller.snmp import iana_enterprise 
from switchmap.poller.configuration import ConfigPoller 
from switchmap.poller import POLLING_OPTIONS, POLL 

async def test_misc_data_collection():
    print("Testing async misc data collection")


    #testing for single device for now only
    hostname = "162.249.37.218"

    try:
        config = ConfigPoller()

        validate = async_snmp_manager.Validate(
            POLLING_OPTIONS(
                hostname=hostname,
                authorizations=config.snmp_auth()
            )
        )
        print(f"Testing async misc data for hostname {hostname}")
        
      
        # getting the connection credentials 
        authorization = await validate.credentials()

        #!checking we no err in validation
        if not authorization:
            print(f"Failed to get valid snmp creds for hostname: {hostname}")
            return False
        
        #checking creds 
        print(f"Group: {authorization.group}")
        print(f"SNMP version: {authorization.version}")

        print(f"Secname: {authorization.secname}")

        print("Testing snmp connectivity with the device ")

        device = async_snmp_manager.Interact(
            POLL(
                hostname=hostname,
                authorization=authorization
            )
        )

        is_contactable = await device.contactable() 

        if not is_contactable:
            print(f"device {hostname} is not contactable via SNMP")
            return False
        
        print(f"Device {hostname} is contactable")

        #polling for systemID from our hostname
        sysID = await device.sysobjectid()

        if not sysID:
            print(f"Failed to get sysObjID from {hostname}")

        
        # testing enterprise number 

        enterprise_no = await device.enterprise_number() 

        if enterprise_no is None:
            print("Failed to get enterprise no")
            return False
        
        print(f"Enterprise no: {enterprise_no}")

        #just for showing (simulating the misc data collection)
        misc_data = {
            "timestamp": int(time.time()),
            "host": hostname,
            "Enterprise_no": enterprise_no,
            "sysObjID": sysID,
        }
        
        print(f"Misc data collected: {misc_data}")
        return True
    
    except Exception as e:
        print(f"Exception err during async misc data test: {e}")
        return False


async def main():
    print("starting async misc data tests")

    check_success = await test_misc_data_collection()

    if check_success:
        print("Single device test passed")
    else:
        print("Single device test failed")


if __name__ == "__main__":
    asyncio.run(main())





