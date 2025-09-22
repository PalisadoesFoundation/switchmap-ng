"""Class interacts with devices supporting SNMPv2-MIB."""

from collections import defaultdict

# Import project libraries
from switchmap.poller.snmp.base_query import Query
from switchmap.core import general


def get_query():
    """Return this module's Query class.

    Args:
        None

    Returns:
        Snmpv2Query: Query class object
    """
    return Snmpv2Query


def init_query(snmp_object):
    """Return initialize and return this module's Query class.

    Args:
        snmp_object: SNMP Interact class object from snmp_manager.py

    Returns:
        Snmpv2Query: Query class object
    """
    return Snmpv2Query(snmp_object)


class Snmpv2Query(Query):
    """Class interacts with devices supporting SNMPv2-MIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        supported: Queries the device to determine whether the MIB is
            supported using a known OID defined in the MIB. Returns True
            if the device returns a response to the OID, False if not.

        system: Returns all relevant system information from the device.
            In some cases a system will have multiple subsystems that are
            covered by an OID. (eg. module / circuit board serial numbers).
            It will therefore be impossible to have a consistent key format
            for data values returned. Data returned by this method will
            therefore be keyed by :
            1) MIB name (primary key)
            2) OID name in the MIB, (secondary key),
            3) Leaf value, or zero (0) if there are no leaves.

    """

    def __init__(self, snmp_object):
        """Instantiate the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

        # Get one OID entry in MIB
        test_oid = ".1.3.6.1.2.1.1.1.0"

        super().__init__(snmp_object, test_oid, tags=["system"])

    async def system(self):
        """Get system data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        data_dict = defaultdict(lambda: defaultdict(dict))
        final = {}
        getvalues = [0]
        key = 0

        # Process
        oidroot = ".1.3.6.1.2.1.1"
        for node in range(1, 7):
            oid = "{}.{}.0".format(oidroot, node)
            results = await self.snmp_object.get(oid, normalized=True)
            for value in results.values():
                getvalues.append(value)

        # Assign values
        data_dict["sysDescr"][key] = general.cleanstring(
            getvalues[1].decode("utf-8")
        )
        data_dict["sysObjectID"][key] = getvalues[2].decode("utf-8")
        data_dict["sysUpTime"][key] = int(getvalues[3])
        data_dict["sysContact"][key] = getvalues[4].decode("utf-8")
        data_dict["sysName"][key] = getvalues[5].decode("utf-8")
        data_dict["sysLocation"][key] = getvalues[6].decode("utf-8")
        # --- generic CPU & memory (HOST-RESOURCES-MIB) ---
        cpu_oid = ".1.3.6.1.2.1.25.3.3.1.2"  # hrProcessorLoad
        mem_used_oid = ".1.3.6.1.2.1.25.2.3.1.6"  # hrStorageUsed
        mem_total_oid = ".1.3.6.1.2.1.25.2.3.1.5"  # hrStorageSize

        cpu_values = self.snmp_object.swalk(cpu_oid) or {}
        if cpu_values:
            vals = [int(v) for v in cpu_values.values()]
            avg = sum(vals) / max(len(vals), 1)
            data_dict["cpu"]["total"] = {"value": round(avg, 2)}

        # Normalize by hrStorageIndex and filter only RAM rows
        mem_used = self.snmp_object.swalk(mem_used_oid, normalized=True) or {}
        mem_total = self.snmp_object.swalk(mem_total_oid, normalized=True) or {}
        mem_units = (
            self.snmp_object.swalk(".1.3.6.1.2.1.25.2.3.1.4", normalized=True)
            or {}
        )
        mem_type = (
            self.snmp_object.swalk(".1.3.6.1.2.1.25.2.3.1.2", normalized=True)
            or {}
        )
        HR_STORAGE_RAM = "1.3.6.1.2.1.25.2.1.2"
        idxs = [
            k
            for k, t in mem_type.items()
            if str(t) == HR_STORAGE_RAM
            and k in mem_total
            and k in mem_used
            and k in mem_units
        ]
        if idxs:
            total_used_bytes = sum(
                int(mem_used[i]) * int(mem_units[i]) for i in idxs
            )
            total_bytes = sum(
                int(mem_total[i]) * int(mem_units[i]) for i in idxs
            )
            total_free_bytes = max(total_bytes - total_used_bytes, 0)
            data_dict["memory"]["used"] = {"value": total_used_bytes}
            data_dict["memory"]["free"] = {"value": total_free_bytes}
        HR_STORAGE_RAM = "1.3.6.1.2.1.25.2.1.2"
        idxs = [
            k
            for k, t in mem_type.items()
            if str(t) == HR_STORAGE_RAM
            and k in mem_total
            and k in mem_used
            and k in mem_units
        ]
        if idxs:
            total_used_bytes = sum(
                int(mem_used[i]) * int(mem_units[i]) for i in idxs
            )
            total_bytes = sum(
                int(mem_total[i]) * int(mem_units[i]) for i in idxs
            )
            total_free_bytes = max(total_bytes - total_used_bytes, 0)
            data_dict["memory"]["used"] = {"value": total_used_bytes}
            data_dict["memory"]["free"] = {"value": total_free_bytes}
        # Return
        final["SNMPv2-MIB"] = data_dict
        return final
