"""Class interacts with devices supporting HOST-RESOURCES-MIB."""

from collections import defaultdict
from switchmap.poller.snmp.base_query import Query
import asyncio 

def get_query():
    """Return this module's Query class."""
    return HostResourcesQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return HostResourcesQuery(snmp_object)

class HostResourcesQuery(Query):
    """Class interacts with devices supporting HOST-RESOURCES-MIB."""

    def __init__(self, snmp_object):
        """Instantiate the class."""
        self.snmp_object = snmp_object

        # Test OID for hrSystem
        test_oid = ".1.3.6.1.2.1.25.1.1.0"

        super().__init__(snmp_object, test_oid, tags=["system"])
    
    async def system(self):
        """Get system resoure data from devices."""
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get CPU and memory data concurrently
        cpu_data = await self.hrprocessorload()
        memory_data = await self.hrstorageused() 

        for key, value in cpu_data.items():
            final[key]["hrProcessorLoad"] = value 
        
        for key,value in memory_data.items():
            final[key]["hrStorageUsed"] = value

        print(f"HostResouces data: {final}")
        print(f"cpu data: {cpu_data}")
        
        return final 
    
    async def hrprocessorload(self, oidonly=False):
        """Return dict of HOST-RESOURCES-MIB hrProcessorLoad for device."""
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID
        oid =  ".1.3.6.1.2.1.25.3.3.1.2"

        # Return OID value for unittests 
        if oidonly is True:
            return oid 

        results = await self.snmp_object.swalk(oid, normalized=True) 
        for key,value in results.items():
            data_dict[int(key)] = value
        
        return data_dict
    
    async def hrstorageused(self, oidonly=False):
        """Return dict of HOST-RESOURCES-MIB hrStorageUsed for device."""
        # Initialize key variables
        data_dict = defaultdict(dict)
        
        # Process OID
        oid = ".1.3.6.1.2.1.25.2.3.1.6"

        # Return OID value for unittests
        if oidonly is True:
            return oid 
        
        results = await self.snmp_object.swalk(oid, normalized=True)

        for key,value in results.items():
            data_dict[int(key)] = value 
        
        return data_dict


       