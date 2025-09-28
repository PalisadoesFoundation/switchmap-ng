"Module for JUNIPER-PROCESS-MIB." ""

from collections import defaultdict
from switchmap.poller.snmp.base_query import Query
from switchmap.core import log
import asyncio


def get_query():
    """Return this module's Query class."""
    return JuniperProcessQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return JuniperProcessQuery(snmp_object)


class JuniperProcessQuery(Query):
    """Class interacts with devices supporting JUNIPER-PROCESS_MIB."""

    def __init__(self, snmp_object):
        """Instantiate the class."""
        self.snmp_object = snmp_object

        # Test OID for Juniper CPU monitoring - jnxOperatingCPU
        test_oid = ".1.3.6.1.4.1.2636.3.1.13.1.8"

        super().__init__(snmp_object, test_oid, tags=["system"])

    async def system(self):
        """Get system resource data from Juniper devices."""
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get CPU and memory data concurrently
        try:
            cpu_data, memory_used_data, memory_free_data = await asyncio.gather(
                self.operatingcpu(),
                self.operatingmemoryused(),
                self.operatingmemoryfree(),
                return_exceptions=True,
            )
            # Populate final results
            if cpu_data and not isinstance(cpu_data, Exception):
                final["JUNIPER-MIB"]["jnxOperatingCPU"] = cpu_data

            if memory_used_data and not isinstance(memory_used_data, Exception):
                final["JUNIPER-MIB"][
                    "jnxOperatingMemoryUsed"
                ] = memory_used_data

            if memory_free_data and not isinstance(memory_free_data, Exception):
                final["JUNIPER-MIB"][
                    "jnxOperatingMemoryFree"
                ] = memory_free_data

        except Exception as e:
            log.log2warning(1316, f"Error in Juniper Process MIB: {e}")
            return final

        return final

    async def operatingcpu(self, oidonly=False):
        """Return dict of JUNIPER-MIB jnxOperatingCPU for device."""
        data_dict = defaultdict(dict)
        oid = ".1.3.6.1.4.1.2636.3.1.13.1.8"

        # Return OID value for unittests
        if oidonly is True:
            return oid

        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        return data_dict

    async def operatingmemoryused(self, oidonly=False):
        """Get used memory from JUNIPER-MIB (jnxOperatingMemoryUsed)."""
        oid = ".1.3.6.1.4.1.2636.3.1.13.1.11"

        # Return OID value for unittests
        if oidonly is True:
            return oid

        results = await self.snmp_object.swalk(oid, normalized=True)
        used_memory = sum(results.values())

        return used_memory

    async def operatingmemoryfree(self, oidonly=False):
        """Get free memory from JUNIPER-MIB (jnxOperatingMemoryFree)."""
        oid = ".1.3.6.1.4.1.2636.3.1.13.1.12"

        if oidonly:
            return oid

        results = await self.snmp_object.swalk(oid, normalized=True)
        free_memory = sum(results.values())
        return free_memory
