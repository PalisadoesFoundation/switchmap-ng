"""Module for JUNIPER device-specific MIBs (CPU, Memory)."""

from collections import defaultdict
from switchmap.poller.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return JuniperDeviceQuery


def init_query(snmp_object):
    """Initialize and return this module's Query class."""
    return JuniperDeviceQuery(snmp_object)


class JuniperDeviceQuery(Query):
    """Class interacts with device-level MIBs for Juniper."""

    def __init__(self, snmp_object):
        self.snmp_object = snmp_object
        super().__init__(snmp_object, None, tags=["device"])

    def cpu(self):
        """Return CPU usage per device."""
        oid = ".1.3.6.1.4.1.2636.3.1.13.1.8.0"  # example
        results = self.snmp_object.swalk(oid, normalized=True)
        return results

    def memory(self):
        """Return memory usage per device."""
        oids = {
            "used": ".1.3.6.1.4.1.2636.3.1.13.1.11.0",
            "free": ".1.3.6.1.4.1.2636.3.1.13.1.12.0",
        }
        results = {
            k: self.snmp_object.swalk(v, normalized=True)
            for k, v in oids.items()
        }
        return results
