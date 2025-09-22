"""Module for JUNIPER device-specific MIBs (CPU, Memory)."""

from collections import defaultdict
from switchmap.poller.snmp.base_query import Query


def get_query():
    """Return this module's Query class.

    Args:
        None

    Returns:
        JuniperDeviceQuery: Query class for JUNIPER device MIBs

    """
    return JuniperDeviceQuery


def init_query(snmp_object):
    """Initialize and return this module's Query class.

    Args:
        snmp_object (SNMP): SNMP object

    Returns:
        JuniperDeviceQuery: Initialized Query class

    """
    return JuniperDeviceQuery(snmp_object)


class JuniperDeviceQuery(Query):
    """Class interacts with device-level MIBs for Juniper."""

    layer = "device"

    def __init__(self, snmp_object):
        """Instantiate the class.

        Args:
            snmp_object (SNMP): SNMP object

        Returns:
            None

        """
        self.snmp_object = snmp_object
        super().__init__(snmp_object, None, tags=["device"])

    def system(self):
        """Return system info (CPU + memory) in aggregator format.

        Args:
            None

        Returns:
            dict: System info in aggregator format

        """
        data = defaultdict(lambda: defaultdict(dict))

        # CPU
        cpu_oid = ".1.3.6.1.4.1.2636.3.1.13.1.8.0"
        cpu_data = self.snmp_object.swalk(cpu_oid, normalized=True) or {}
        if cpu_data:
            total_cpu = sum(int(v) for v in cpu_data.values() if v is not None)
            data["cpu"]["total"] = {"value": total_cpu}

        # Memory
        mem_oids = {
            "used": ".1.3.6.1.4.1.2636.3.1.13.1.11.0",
            "free": ".1.3.6.1.4.1.2636.3.1.13.1.12.0",
        }
        mem_data = {
            k: self.snmp_object.swalk(v, normalized=True)
            for k, v in mem_oids.items()
        }
        if mem_data.get("used") and mem_data.get("free"):
            used_val = next(iter(mem_data["used"].values()))
            free_val = next(iter(mem_data["free"].values()))
            data["memory"]["used"] = {"value": int(used_val)}
            data["memory"]["free"] = {"value": int(free_val)}

        return data

    def supported(self):
        """Return True if this module can query the device.

        Args:
            None

        Returns:
            bool: True if supported, False otherwise

        """
        # Use a known Juniper CPU OID to check support
        cpu_oid = ".1.3.6.1.4.1.2636.3.1.13.1.8"
        response = self.snmp_object.swalk(cpu_oid, normalized=True)
        return bool(response)
