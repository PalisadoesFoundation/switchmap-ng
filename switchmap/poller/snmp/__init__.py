"""Switchmap-NG snmp package."""

from .mib.generic.mib_bridge import BridgeQuery
from .mib.generic.mib_entity import EntityQuery
from .mib.generic.mib_essswitch import EssSwitchQuery
from .mib.generic.mib_etherlike import EtherlikeQuery
from .mib.generic.mib_if import IfQuery
from .mib.generic.mib_if_64 import If64Query
from .mib.generic.mib_ip import IpQuery
from .mib.generic.mib_ipv6 import Ipv6Query
from .mib.generic.mib_lldp import LldpQuery
from .mib.generic.mib_qbridge import QbridgeQuery
from .mib.generic.mib_snmpv2 import Snmpv2Query

from .mib.cisco import CiscoC2900Query
from .mib.cisco import CiscoCdpQuery
from .mib.cisco import CiscoIetfIpQuery
from .mib.cisco import CiscoStackQuery
from .mib.cisco import CiscoVlanMembershipQuery
from .mib.cisco import CiscoVlanIftableRelationshipQuery
from .mib.cisco import CiscoVtpQuery
from .mib.cisco import CiscoProcessQuery

from .mib.juniper import JuniperVlanQuery
from .mib.juniper import JuniperProcessQuery


__all__ = ("cisco", "juniper")

QUERIES = [
    CiscoC2900Query,
    CiscoVtpQuery,
    CiscoIetfIpQuery,
    CiscoCdpQuery,
    CiscoStackQuery,
    CiscoVlanMembershipQuery,
    CiscoVlanIftableRelationshipQuery,
    CiscoProcessQuery,
    Snmpv2Query,
    IfQuery,
    BridgeQuery,
    IpQuery,
    Ipv6Query,
    EtherlikeQuery,
    EntityQuery,
    LldpQuery,
    EssSwitchQuery,
    JuniperVlanQuery,
    JuniperProcessQuery,
    QbridgeQuery,
]


def get_queries(layer):
    """Get mib queries which gather information related to a specific OSI layer.

    Args:
        layer: The layer of queries needed

    Returns:
        queries: List of queries tagged the given layer

    """
    # Return
    queries = [
        class_object for class_object in QUERIES if layer in dir(class_object)
    ]
    return queries
