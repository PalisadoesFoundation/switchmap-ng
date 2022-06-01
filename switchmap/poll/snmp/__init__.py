"""Switchmap-NG snmp package."""

from switchmap.poll.snmp.base_query import Query

from switchmap.poll.snmp import iana_enterprise

from switchmap.poll.snmp.mib_bridge import BridgeQuery
from switchmap.poll.snmp.mib_entity import EntityQuery
from switchmap.poll.snmp.mib_essswitch import EssSwitchQuery
from switchmap.poll.snmp.mib_etherlike import EtherlikeQuery
from switchmap.poll.snmp.mib_if import IfQuery
from switchmap.poll.snmp.mib_if_64 import If64Query
from switchmap.poll.snmp.mib_ip import IpQuery
from switchmap.poll.snmp.mib_ipv6 import Ipv6Query
from switchmap.poll.snmp.mib_lldp import LldpQuery
from switchmap.poll.snmp.mib_qbridge import QbridgeQuery
from switchmap.poll.snmp.mib_snmpv2 import Snmpv2Query

from switchmap.poll.snmp.cisco import CiscoC2900Query
from switchmap.poll.snmp.cisco import CiscoCdpQuery
from switchmap.poll.snmp.cisco import CiscoIetfIpQuery
from switchmap.poll.snmp.cisco import CiscoStackQuery
from switchmap.poll.snmp.cisco import CiscoVlanMembershipQuery
from switchmap.poll.snmp.cisco import CiscoVlanIftableRelationshipQuery
from switchmap.poll.snmp.cisco import CiscoVtpQuery

from switchmap.poll.snmp.juniper import JuniperVlanQuery


__all__ = ('cisco', 'juniper')

QUERIES = [CiscoC2900Query, CiscoVtpQuery, CiscoIetfIpQuery,
           CiscoCdpQuery, CiscoStackQuery, CiscoVlanMembershipQuery,
           CiscoVlanIftableRelationshipQuery,
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
