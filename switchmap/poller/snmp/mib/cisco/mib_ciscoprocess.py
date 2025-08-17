"""Class interacts with devices supporting CISCO-PROCESS-MIB."""

from collections import defaultdict
from switchmap.poller.snmp.base_query import Query
import asyncio

def get_query():
    """Return this module's Query class."""
    return CiscoProcessQuery

def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return CiscoProcessQuery(snmp_object)

class CiscoProcessQuery(Query):
    """Class interacts with devices supporting CISCO-PROCESS-MIB."""

    def __init__(self, snmp_object):
        """Instantiate the class."""
        self.snmp_object = snmp_object

        # Test OID for Cisco CPU monitoring - cpmCPUTotalTable
        test_oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.8.1"

        super().__init__(snmp_object, test_oid, tags=["system"])
    
    async def system(self):
        """Get system resource data from Cisco devices."""
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get CPU and memory data concurrently
        try:
            cpu_data, memory_used_data, memory_free_data = await asyncio.gather(
                self.cpmcputotal5minrev(),
                self.cempmempoolhcused(),
                self.cempmempoolhcfree(),
                return_exceptions=True
            )

            # Populate final results with better structure
            if cpu_data and not isinstance(cpu_data, Exception):
                final["CISCO-PROCESS-MIB"]["cpmCPUTotal5minRev"] = cpu_data
            
            if memory_used_data and not isinstance(memory_used_data, Exception):
                final["CISCO-ENHANCED-MEMPOOL-MIB"]["cempMemPoolHCUsed"] = memory_used_data
            
            if memory_free_data and not isinstance(memory_free_data, Exception):
                final["CISCO-ENHANCED-MEMPOOL-MIB"]["cempMemPoolHCFree"] = memory_free_data

        except Exception as e:
            print(f"Error in Cisco system queries: {e}")

        print(f"Cisco Process data: {final}")
        
        return final 
    
    async def cpmcputotal5minrev(self, oidonly=False):
        """Return dict of CISCO-PROCESS-MIB cpmCPUTotal5minRev for device."""
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID - 5 minute average CPU utilization
        oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.8"

        # Return OID value for unittests 
        if oidonly is True:
            return oid 

        try:
            results = await self.snmp_object.swalk(oid, normalized=True) 
            for key, value in results.items():
                data_dict[int(key)] = value
        except Exception as e:
            print(f"Error querying Cisco CPU: {e}")
        
        return data_dict
    
    async def cempmempoolhcused(self, oidonly=False):
        """Return dict of CISCO-ENHANCED-MEMPOOL-MIB cempMemPoolHCUsed for device."""
        # Initialize key variables
        data_dict = defaultdict(dict)
        
        # Process OID - Enhanced memory pool used (high capacity)
        oid = ".1.3.6.1.4.1.9.9.221.1.1.1.1.18"

        # Return OID value for unittests
        if oidonly is True:
            return oid 
        
        try:
            results = await self.snmp_object.swalk(oid, normalized=True)
            for key, value in results.items():
                data_dict[int(key)] = value
        except Exception as e:
            print(f"Error querying Cisco Memory: {e}")
        
        return data_dict

    async def cempmempoolhcfree(self, oidonly=False):
        """Return dict of CISCO-ENHANCED-MEMPOOL-MIB cempMemPoolHCFree for device."""
        # Initialize key variables
        data_dict = defaultdict(dict)
        
        # Process OID - Enhanced memory pool free (high capacity)
        oid = ".1.3.6.1.4.1.9.9.221.1.1.1.1.20"

        # Return OID value for unittests
        if oidonly is True:
            return oid 
        
        try:
            results = await self.snmp_object.swalk(oid, normalized=True)
            for key, value in results.items():
                data_dict[int(key)] = value
        except Exception as e:
            print(f"Error querying Cisco Memory Free: {e}")
        
        return data_dict
