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
        # Define query object
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

        data["layer1"] = await self.layer1()

        data["layer2"] = await self.layer2()

        data["layer3"] = await self.layer3()

        print(f"Final data: {data}")

        # Return
        return data

    async def misc(self):
        """Provide miscellaneous information about the device and the poll."""

        # Initialize data
        data = defaultdict(lambda: defaultdict(data))
        data["timestamp"] = int(time.time())
        data["host"] = self.snmp_object.hostname()

        # Get vendor information
        sysobjectid = await self.snmp_object.sysobjectid()
        vendor = iana_enterprise.Query(sysobjectid=sysobjectid)
        data["IANAEnterpriseNumber"] = vendor.enterprise()

        print(
            f"Misc data: for host: {data['host']}, vendor: {data['IANAEnterpriseNumber']}"
        )

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

        # Create all query instances
        query_items = [
            (query_class(self.snmp_object), query_class.__name__)
            for query_class in system_queries
        ]

        # Check if supported
        support_results = await asyncio.gather(
            *[item.supported() for item, _ in query_items]
        )

        supported_items = [
            (item, name)
            for (item, name), supported in zip(query_items, support_results)
            if supported
        ]

        if supported_items:
            results = await asyncio.gather(
                *[
                    _add_system(item, defaultdict(lambda: defaultdict(dict)))
                    for item, _ in supported_items
                ]
            )

            # Merge results
            for result in results:
                for key, value in result.items():
                    data[key].update(value)
            processed = True

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

        print(f"layer 1 level MIBs", layer1_queries)

        #! Process MIB queries sequentially
        for i, Query in enumerate(layer1_queries):
            item = Query(self.snmp_object)
            mib_name = item.__class__.__name__
            print(f"polling for MIB_name: {mib_name}")

            # Check if supported
            if await item.supported():
                processed = True
                old_keys = list(data.keys())
                print(f"{mib_name} is supported")

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
        layer2_queries = get_queries("layer2")

        # !Process layer2 MIBs sequentially fn
        for i, Query in enumerate(layer2_queries):
            item = Query(self.snmp_object)
            mib_name = item.__class__.__name__

            # Check if supported
            if await item.supported():
                processed = True
                old_keys = list(data.keys())
                print(f"{mib_name} is supported")

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
        return data

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
        print(f"layer3 level MIBs", layer3_queries)
        
        #! currently polling mibs sequencially
        for i, Query in enumerate(layer3_queries):
            item = Query(self.snmp_object)
            mib_name = item.__class__.__name__

            print(
                f"Testing MIB {i+1}/{len(layer3_queries)}: {mib_name} for {hostname}"
            )

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
        return data


async def _add_data(source, target):
    """Add data from source to target dict. Both dicts must have two keys.

    Args:
        source: Source dict
    target: Target dict

    Returns:
        target: Aggregated data

    """
    # Process data
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
                        for tertiary, value in result[primary][
                            secondary
                        ].items():
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


async def _add_layer1(query, data):
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

        #! after complete async migration remove check for coroutines
        result = None
        if asyncio.iscoroutinefunction(query.layer1):
            print(f"before polling")
            result = await query.layer1()
        else:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, query.layer1)

        if result:
            print(f"Return data before processing {mib_name}: {result}")
            data = await _add_data(result, data)
            print(f"Successfully added layer1 data for {mib_name}")
            print(f"Return data After processing {mib_name}: {data}")
        else:
            print(f" No layer1 data returned for {mib_name}")

        return data

    except Exception as e:
        print(f" Error in _add_layer1: {e}")
        return data


async def _add_layer2(query, data):
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

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, query.layer2)

        if result:
            print(f"{mib_name} returned layer2 data")
            data = await _add_data(result, data)
            print(f"Successfully added layer2 data for {mib_name}")
        else:
            print(f" No layer2 data returned for {mib_name}")

        return data

    except Exception as e:
        print(f" Error in _add_layer2: {e}")


async def _add_layer3(query, data):
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
        if asyncio.iscoroutinefunction(query.layer3):
            result = await query.layer3()
        else:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, query.layer3)

        if result:
            print(f"{mib_name} returned layer3 data")
            data = await _add_data(result, data)
            print(f"Successfully added layer3 data for {mib_name}")
        else:
            print(f" No layer3 data returned for {mib_name}")

        return data

    except Exception as e:
        print(f" Error in _add_layer3: {e}")
