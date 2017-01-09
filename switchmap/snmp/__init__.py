"""Switchmap-NG snmp package."""

from switchmap.snmp.base_query import Query

from switchmap.snmp import iana_enterprise

from switchmap.snmp.mib_bridge import BridgeQuery
from switchmap.snmp.mib_entity import EntityQuery
from switchmap.snmp.mib_essswitch import EssSwitchQuery
from switchmap.snmp.mib_etherlike import EtherlikeQuery
from switchmap.snmp.mib_if import IfQuery
from switchmap.snmp.mib_if_64 import If64Query
from switchmap.snmp.mib_ip import IpQuery
from switchmap.snmp.mib_ipv6 import Ipv6Query
from switchmap.snmp.mib_lldp import LldpQuery
from switchmap.snmp.mib_qbridge import QbridgeQuery
from switchmap.snmp.mib_snmpv2 import Snmpv2Query

from switchmap.snmp.cisco import CiscoC2900Query
from switchmap.snmp.cisco import CiscoCdpQuery
from switchmap.snmp.cisco import CiscoIetfIpQuery
from switchmap.snmp.cisco import CiscoStackQuery
from switchmap.snmp.cisco import CiscoVlanMembershipQuery
from switchmap.snmp.cisco import CiscoVtpQuery

from switchmap.snmp.juniper import JuniperVlanQuery


__all__ = ('cisco', 'juniper')

QUERIES = [CiscoC2900Query, CiscoVtpQuery, CiscoIetfIpQuery,
           CiscoCdpQuery, CiscoStackQuery, CiscoVlanMembershipQuery,
           Snmpv2Query, IfQuery, BridgeQuery, IpQuery,
           Ipv6Query, EtherlikeQuery, EntityQuery, LldpQuery,
           EssSwitchQuery, JuniperVlanQuery, QbridgeQuery]


def get_queries(layer):
    """Get mib queries which gather information related to a specific OSI layer.

    Args:
        tag: The layer of queries needed

    Returns:
        queries: List of queries tagged the given layer

    """
    return [
        class_object for class_object in QUERIES if layer in dir(
            class_object)]
