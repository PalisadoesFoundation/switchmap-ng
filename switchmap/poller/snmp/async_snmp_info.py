"""Async module to aggregate query results."""

import time 
from collections import defaultdict
import asyncio 

from . import iana_enterprise
from . import get_queries 

#! remove all the prints after debuggign all the issues & implementation

#! ensure proper logging on errs 
#! have to tests it along with snmp_manager, 

#!Phase-1 
#! get misc data && system data (have to convert system queries MIBs to async )

class Query:
    """Async class interacts with devices - use existing MIB classes.

    Args:
        None

    Returns: 
        None 

    """

    def __init__(self, snmp_object):
        """Instantiate the class.
        
        Args:
            snmp_object: SNMP interact class object from async_snmp_manager.py
        
        Returns:
            None 

        """
        #Define query object
        self.snmp_object = snmp_object
        print(f"create Query object for {snmp_object.hostname()}")
    
    async def everything(self):
        """Get all information from device.

        Args:
            None

        Returns:
            data: Aggregated data

        """
        # Initialize key variables
        data = {}
        hostname = self.snmp_object.hostname() 

        print(f"start async everything() for {hostname}")
        
        #! might get error here (check for logs)
        # Create tasks for parallel execution
        tasks = []

        # Append data collection tasks 
        tasks.append(self._gather_misc())

        #! after this move to add for system, layer1, layer2, layer3


        # Execute all tasks concurrently 
        results = await asyncio.gather(*tasks, return_exceptions=True)

        #Process results 
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                #!add log here
                print(f"task: {i} failed for {hostname}: {result}")
            elif result:
                data.update(result)
        
        print(f"everything() completed")
        print(f"data: {list(data.keys())}")

        # Return 
    
    async def _gather_misc(self):
        """Provide miscellaneous information about the device and the poll. """
        try: 
            # Initialize data
            data = defaultdict(lambda: defaultdict(data))
            data["timestamp"] = int(time.time())
            data["host"] = self.snmp_object.hostname()

            # Get vendor information 
            sysobjectid = await self.snmp_object.sysobjectid()
            vendor = iana_enterprise.Query(sysobjectid=sysobjectid)
            data["IANAEnterpriseNumber"] = vendor.enterprise() 

            print(f"Misc data: for host: {data['host']}, vendor: {data['IANAEnterpriseNumber']}")

            return {"misc": data}
        except Exception as e:
            #! add log here
            print(f"Error gathering misc data: {e}")
            return {}
        
    #! testing this to avoid current sequencial MIB query
    async def _process_mib_class(self, Query, layer_type, index, total):
        #!explain each args & return as well
        """Process a single MIB class asynchronously."""
        try:
            hostname = self.snmp_object.hostname()
            item = Query(self.snmp_object)
            mib_name = item.__class__.__name__ 

            print(f"Testing MIB {index}/{total}: {mib_name} for {hostname}")

            if await item.supported():
                print(f"MIB: {mib_name} is supported for {hostname}")

                #! return respected layer type MIBs for poll

                if layer_type == "system":
                    return await item.system()
                elif layer_type == "layer1":
                    return await item.layer1()
                elif layer_type == "layer2":
                    return await item.layer2()
                elif layer_type == "layer3":
                    return await item.layer3()
                
            else:
                print(f"MIB {mib_name} is not supported for hostname: {hostname}")
                return {}
        except Exception as e:
            #! add logs 
            print(f"MIB {mib_name} is not supported for {hostname}")
            return {} 
        

        
    async def _gather_system(self):
        """Get all system information from device using existing MIB classes."""

        try:
            # Initialize data 
            data = defaultdict(lambda: defaultdict(dict))
            processed = False 
            hostname = self.snmp_object.hostname()

            print(f"starting system() queries for {hostname}")

            # Get system information from SNMPv2-MIB, ENTITY-MIB, IF-MIB
            system_queries = get_queries("system")

            print(f"check for system MIB queries {system_queries}")

            #! for now process sequenecially but have to move to concurrent 

            #!check for sys queries (for snmp_obj)
            for i, Query in enumerate(system_queries):
                hostname =  self.snmp_object.hostname()
                item = Query(self.snmp_object)
                mib_name = item.__class__.__name__ 

                print(f"mib: {mib_name}, totalMIBS: {len(system_queries)}")

                # Check if supported
                if await item.supported():
                    print(f"MIB: {mib_name} is supported for {hostname}")

                    processed = True 
                    old_keys = list(data.keys())

                    # For now following sync for data aggregation 
                    # data = await _add_system(item, data)
                    
                    #!usecase just for debugging
                    new_keys = list(data.keys())
                    added_keys = set(new_keys) - set(old_keys)

                    print(f"MIB: {mib_name} added: {list(added_keys)}")
                else:
                    print(f"MIB: {mib_name} is not supported for {hostname}")
            
            # Return (sync one)
            if processed:
                print("ssytem data collected ")
                return {"system": data}
            else: 
                return {}
            
        except Exception as e: 
            #! add err log here
            print(f"error gather system data: {e}")
            return {} 
    





    
