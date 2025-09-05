"""ORM Schema classes.

Used for defining GraphQL interaction

Based on the pages at:

    https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

"""

# PIP3 imports
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import BatchSQLAlchemyConnectionField
from graphene.relay import Connection
from graphene import ConnectionField
from graphene import ObjectType, String  # <- add String here


# Import models
from switchmap.server.db.models import (
    Event as EventModel,
    Root as RootModel,
    Device as DeviceModel,
    DeviceMetricsHistory as DeviceMetricsModel,
    L1Interface as L1InterfaceModel,
    Zone as ZoneModel,
    MacIp as MacIpModel,
    Oui as OuiModel,
    Vlan as VlanModel,
    Mac as MacModel,
    MacPort as MacPortModel,
    VlanPort as VlanPortModel,
    Ip as IpModel,
    IpPort as IpPortModel,
)

# Import attributes
from switchmap.server.db.attributes import (
    EventAttribute,
    RootAttribute,
    DeviceAttribute,
    DeviceMetricsAttribute,
    L1InterfaceAttribute,
    MacAttribute,
    MacIpAttribute,
    MacPortAttribute,
    OuiAttribute,
    VlanAttribute,
    VlanPortAttribute,
    ZoneAttribute,
    IpAttribute,
    IpPortAttribute,
)

###############################################################################
# Define Schemas
###############################################################################


class Event(SQLAlchemyObjectType, EventAttribute):
    """Event node."""

    class Meta:
        """Define the metadata."""

        model = EventModel
        interfaces = (graphene.relay.Node,)


class Root(SQLAlchemyObjectType, RootAttribute):
    """Root node."""

    class Meta:
        """Define the metadata."""

        model = RootModel
        interfaces = (graphene.relay.Node,)


class Device(SQLAlchemyObjectType, DeviceAttribute):
    """Device node."""

    class Meta:
        """Define the metadata."""

        model = DeviceModel
        interfaces = (graphene.relay.Node,)


class DeviceMetrics(SQLAlchemyObjectType, DeviceMetricsAttribute):
    """Device metrics node with decoded hostname."""

    class Meta:
        """Define the metadata."""

        model = DeviceMetricsModel
        interfaces = (graphene.relay.Node,)


class Ip(SQLAlchemyObjectType, IpAttribute):
    """Ip node."""

    class Meta:
        """Define the metadata."""

        model = IpModel
        interfaces = (graphene.relay.Node,)


class IpPort(SQLAlchemyObjectType, IpPortAttribute):
    """IpPort node."""

    class Meta:
        """Define the metadata."""

        model = IpPortModel
        interfaces = (graphene.relay.Node,)


class L1Interface(SQLAlchemyObjectType, L1InterfaceAttribute):
    """L1Interface node."""

    class Meta:
        """Define the metadata."""

        model = L1InterfaceModel
        interfaces = (graphene.relay.Node,)


class Mac(SQLAlchemyObjectType, MacAttribute):
    """Mac node."""

    class Meta:
        """Define the metadata."""

        model = MacModel
        interfaces = (graphene.relay.Node,)


class Zone(SQLAlchemyObjectType, ZoneAttribute):
    """Zone node."""

    class Meta:
        """Define the metadata."""

        model = ZoneModel
        interfaces = (graphene.relay.Node,)


class MacIp(SQLAlchemyObjectType, MacIpAttribute):
    """MacIp node."""

    class Meta:
        """Define the metadata."""

        model = MacIpModel
        interfaces = (graphene.relay.Node,)


class MacPort(SQLAlchemyObjectType, MacPortAttribute):
    """MacPort node."""

    class Meta:
        """Define the metadata."""

        model = MacPortModel
        interfaces = (graphene.relay.Node,)


class Oui(SQLAlchemyObjectType, OuiAttribute):
    """Oui node."""

    class Meta:
        """Define the metadata."""

        model = OuiModel
        interfaces = (graphene.relay.Node,)


class Vlan(SQLAlchemyObjectType, VlanAttribute):
    """Vlan node."""

    class Meta:
        """Define the metadata."""

        model = VlanModel
        interfaces = (graphene.relay.Node,)


class VlanPort(SQLAlchemyObjectType, VlanPortAttribute):
    """VlanPort node."""

    class Meta:
        """Define the metadata."""

        model = VlanPortModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    """Define GraphQL queries."""

    node = relay.Node.Field()

    # Results as a single entry filtered by 'id' and as a list
    device = graphene.relay.Node.Field(Device)
    devices = BatchSQLAlchemyConnectionField(Device.connection)

    deviceMetrics = BatchSQLAlchemyConnectionField(
        DeviceMetrics.connection, hostname=String()
    )

    def resolve_deviceMetrics(self, info, hostname=None, **kwargs):
        """Resolve device metrics with optional hostname filtering.

        Args:
            info: GraphQL info object
            hostname (str, optional): Hostname to filter by. Defaults to None.
            **kwargs: Additional keyword arguments

        Returns:
            QuerySet: Filtered or unfiltered DeviceMetrics query set

        """
        query = DeviceMetrics.get_query(info)
        if hostname:
            query = query.filter(
                DeviceMetricsModel.hostname == hostname.encode()
            )
        return query

    # Results as a single entry filtered by 'id' and as a list
    l1interface = graphene.relay.Node.Field(L1Interface)
    l1interfaces = BatchSQLAlchemyConnectionField(L1Interface.connection)

    # Results as a single entry filtered by 'id' and as a list
    zone = graphene.relay.Node.Field(Zone)
    zones = BatchSQLAlchemyConnectionField(Zone.connection)

    # Results as a single entry filtered by 'id' and as a list
    root = graphene.relay.Node.Field(Root)
    roots = BatchSQLAlchemyConnectionField(Root.connection)

    # Results as a single entry filtered by 'id' and as a list
    event = graphene.relay.Node.Field(Event)
    events = BatchSQLAlchemyConnectionField(Event.connection)

    # Results as a single entry filtered by 'id' and as a list
    ip = graphene.relay.Node.Field(Ip)
    ips = BatchSQLAlchemyConnectionField(Ip.connection)

    # Results as a single entry filtered by 'id' and as a list
    ipport = graphene.relay.Node.Field(IpPort)
    ipports = BatchSQLAlchemyConnectionField(IpPort.connection)

    # Results as a single entry filtered by 'id' and as a list
    mac = graphene.relay.Node.Field(Mac)
    macs = BatchSQLAlchemyConnectionField(Mac.connection)

    # Results as a single entry filtered by 'id' and as a list
    macip = graphene.relay.Node.Field(MacIp)
    macips = BatchSQLAlchemyConnectionField(MacIp.connection)

    # Results as a single entry filtered by 'id' and as a list
    macport = graphene.relay.Node.Field(MacPort)
    macports = BatchSQLAlchemyConnectionField(MacPort.connection)

    # Results as a single entry filtered by 'id' and as a list
    oui = graphene.relay.Node.Field(Oui)
    ouis = BatchSQLAlchemyConnectionField(Oui.connection)

    # Results as a single entry filtered by 'id' and as a list
    vlan = graphene.relay.Node.Field(Vlan)
    vlans = BatchSQLAlchemyConnectionField(Vlan.connection)

    # Results as a single entry filtered by 'id' and as a list
    vlanport = graphene.relay.Node.Field(VlanPort)
    vlanports = BatchSQLAlchemyConnectionField(VlanPort.connection)


# Make the schema global
SCHEMA = graphene.Schema(query=Query)
