"""Async module to aggregate query results."""

import time 
from collections import defaultdict
import asyncio 

from . import iana_enterprise
from . import get_queries 

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
        
        # Append data 
        data["misc"] = await self.misc()

        data["system"] = await self.system()

        #! empty for now (will enable as MIBs are converted)
        data["layer1"] = {}

        data["layer2"] = {}

        data["layer3"] = {}

        # Return 
        return data
    
    async def misc(self):
        """Provide miscellaneous information about the device and the poll. """

        # Initialize data
        data = defaultdict(lambda: defaultdict(data))
        data["timestamp"] = int(time.time())
        data["host"] = self.snmp_object.hostname()

        # Get vendor information 
        sysobjectid = await self.snmp_object.sysobjectid()
        vendor = iana_enterprise.Query(sysobjectid=sysobjectid)
        data["IANAEnterpriseNumber"] = vendor.enterprise() 

        print(f"Misc data: for host: {data['host']}, vendor: {data['IANAEnterpriseNumber']}")

        return data
    
    async def system(self):
        """Get all system information from device.
        
        Args: 
            None
        
        Returns: 
            data: Aggregated system data
            
        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        print(f"data to visualize: {data}")

        # Get system information from various MIB classes
        system_queries = get_queries("system")
        print(f"system queries: {system_queries}, len: {len(system_queries)}")

        #! think of async way or something that can reduce polling time
        #Process MIB queries 
        for i, Query in enumerate(system_queries):
            item = Query(self.snmp_object)
            mib_name = item.__class__.__name__ 

            print(f"item: {item}, mib_name: {mib_name}")

            print(f"Testing MIB {i+1}/{len(system_queries)}")

            # Check if supported
            if await item.supported():
                
                processed = True
                old_keys = list(data.keys())

                print(f"oid Keys: {old_keys}")

                data = await _add_system(item,data)

                print(f"data check bro: {data}")

                new_keys = list(data.keys())

                added_keys = set(new_keys) - set(old_keys)
                print(f"added_keys: {added_keys}")
        
        if processed is True:
            return data 
        else:
            return None
        
    async def layer1(self):
        """
        Get all layer 1 information from device.

        Args: 
            None
    
        Returns:
            data: Aggregated layer1 data
        """
         # Initialize key values 
        data = defaultdict(lambda: defaultdict(dict))
        processed = False 
        hostname = self.snmp_object.hostname() 

        layer1_queries = get_queries("layer1")

        # Process MIB queries sequentially
        for i, Query in enumerate(layer1_queries):
            item = Query(self.snmp_object)
            mib_name = item.__class__.__name__ 

                # Check if supported 
            if await item.supported():
                processed = True 
                old_keys = list(data.keys())

                data = await _add_layer1(item, data)

                new_keys = list(data.keys())
                added_keys = set(new_keys) - set(old_keys)
            else:
                print(f" MIB {mib_name} is NOT supported for {hostname}")
        
        # Return 
        if processed:
            print(f"Layer1 data collected successfully for {hostname}")
        else:
            print(f"No layer1 MIBs supported for {hostname}")
    
        return data 
    
    async def layer2(self):
        """
        Args: 
            None 
        
        Returns: 
            data: Aggregated layer2 data

        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        processed = False 
        hostname = self.snmp_object.hostname() 

        # Get layer2 information from MIB classes
        layer2_queries = get_queries("leyer2")
        #! chek layer2 queries how its functions to resolve the issue
        for i,Query in enumerate(layer2_queries):
            item = Query(self.snmp_object)
            mib_name = item.__class__.__name__ 

            # Check if supported 
            if await item.supported():
                processed = True
                old_keys = list(data.keys())

                data = await _add_layer2(item, data)

                new_keys = list(data.keys())
                added_keys = set(new_keys) - set(old_keys)
            else:
                print(f"MIB {mib_name} is not supported for {hostname}")
        
        # Return 
        if processed:
            print(f"layer2 data collected successfully for {hostname}")
        else:
            print(f"No layer2 mibs supported for {hostname}")
        
    async def layer3(self):
        """
        Get all layer3 information from device.

        Args:
            None

        Returns:
           data: Aggregated layer3 data 
        """

        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        processed = False 
        hostname = self.snmp_object.hostname() 

        # Get layer3 information from MIB classes
        layer3_queries = get_queries("layer3")

        for i, Query in enumerate(layer3_queries):
            item = Query(self.snmp_object)
            mib_name = item.__class__.__name__ 

            print(f"Testing MIB {i+1}/{len(layer3_queries)}: {mib_name} for {hostname}")

            # Check if supported 
            if await item.supported():
                print(f"MIB {mib_name} is supported for {hostname}")
                processed = True
                old_keys = list(data.keys())

                data = await _add_layer3(item, data)

                new_keys = list(data.keys())
                added_keys = set(new_keys) - set(old_keys)

                print(f"MIB {mib_name} added: {list(added_keys)}")
            else:
                print(f"MIB {mib_name} is not supported for {hostname}")
        
        # Return 
        if processed:
            print(f"Layer3 data collected successfully for {hostname}")
        else:
            print(f"No layer3 MIBs supported for {hostname}")
            




#! understand this as well
def _add_data(source, target):
    """Add data from source to target dict. Both dicts must have two keys.

    Args:
        source: Source dict
    target: Target dict

    Returns:
        target: Aggregated data

    """
    # Process data
    #! visualize this one 
    for primary in source.keys():
        print(f"primary: {primary}")
        for secondary, value in source[primary].items():
            target[primary][secondary] = value

    # Return
    return target
    
async def _add_system(query, data):
    """Add data from successful system MIB query to original data provided.
        
    Args: 
        query: MIB query object
        data: Three keyed dict of data
        
    Returns:
        data: Aggregated data
        
    """

    try:
        #!Process query - handle both sync and async methods
        mib_name = query.__class__.__name__
        print(f"Processing system data from {mib_name}")

        result = None 
        #! after migrating system level oid to async then we dont have to check for coroutines
        if asyncio.iscoroutinefunction(query.system):
            result = await query.system()
        else:

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, query.system)
            
        if result:

            print(f"for {mib_name}: result: {result.keys()}")
                
            # Add tag
        for primary in result.keys():
            if isinstance(result[primary], dict):
                for secondary in result[primary].keys():
                    if isinstance(result[primary][secondary], dict):
                        for tertiary, value in result[primary][secondary].items():
                            data[primary][secondary][tertiary] = value
                    else:
                        data[primary][secondary] = result[primary][secondary]
            else:
                # Handle case where secondary level is not a dict
                data[primary] = result[primary] 

        return data
    except Exception as e:
        print(f"Error in _add_system: {e}")
        return data

async def _add_layer1(query,data):
    """
    Add data from successful layer1 MIB query to original data provided.
    
    Args: 
       query: MIB query object
       data: dict of data
    
    Returns:
        data: Aggregated data

    """

    try:
        mib_name = query.__class__.__name__
        print(f"Processing layer1 data: {mib_name}")
        #! so, are getting data file wise (like yuo know better understand this better)

        #! so, does are we checking before if the function is async or not
        #! if yes, then have to remove and check if htis works also without this(after laeyr 1 migraiton to async)
        result = None 
        if asyncio.iscoroutinefunction(query.layer1):
            result = await query.layer1()
        else:
            #! what is this, like explain in deatil for this case
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, query.layer1)
        
        if result:
            print(f"{mib_name} returned layer1 data")
            #! what does _add_data do like in detail (is this approach is best)
            data = _add_data(result, data)
            print(f"Successfully added layer1 data for {mib_name}")
        else:
            print(f" No layer1 data returned for {mib_name}")
        
        return data 
    
    except Exception as e:
        print(f" Error in _add_layer1: {e}")

async def _add_layer2(query,data):
    """
    Add data from successful layer2 MIB query to original data provided.
    
    Args: 
       query: MIB query object
       data: dict of data
    
    Returns:
        data: Aggregated data

    """

    try:
        mib_name = query.__class__.__name__ 

        result = None 
        if asyncio.iscoroutinefunction(query.layer2):
            result = await query.layer2() 
        else:
            #! what is this, like explain in deatil for this case
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, query.layer2)
        
        if result:
            print(f"{mib_name} returned layer2 data")
            #! what does _add_data do like in detail (is this approach is best)
            data = _add_data(result, data)
            print(f"Successfully added layer2 data for {mib_name}")
        else:
            print(f" No layer2 data returned for {mib_name}")
        
        return data 
    
    except Exception as e:
        print(f" Error in _add_layer2: {e}")

async def _add_layer3(query,data):
    """
    Add data from successful layer3 MIB query to original data provided.
    
    Args: 
       query: MIB query object
       data: dict of data
    
    Returns:
        data: Aggregated data

    """

    try:
        mib_name = query.__class__.__name__ 

        result = None 
        if asyncio.iscoroutinefunction(query.layer2):
            result = await query.layer3() 
        else:
            #! what is this, like explain in deatil for this case
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, query.layer3)
        
        if result:
            print(f"{mib_name} returned layer2 data")
            #! what does _add_data do like in detail (is this approach is best)
            data = _add_data(result, data)
            print(f"Successfully added layer3 data for {mib_name}")
        else:
            print(f" No layer3 data returned for {mib_name}")
        
        return data 
    
    except Exception as e:
        print(f" Error in _add_layer3: {e}")

