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

# Import models
from switchmap.server.db.models import (
    Device as DeviceModel,
    Event as EventModel,
    L1Interface as L1InterfaceModel,
    Zone as ZoneModel,
    MacIp as MacIpModel,
    Oui as OuiModel,
    Vlan as VlanModel,
    Mac as MacModel,
    MacPort as MacPortModel,
    VlanPort as VlanPortModel,
)

# Import attributes
from switchmap.server.db.attributes import (
    DeviceAttribute,
    EventAttribute,
    L1InterfaceAttribute,
    MacAttribute,
    MacIpAttribute,
    MacPortAttribute,
    OuiAttribute,
    VlanAttribute,
    VlanPortAttribute,
    ZoneAttribute,
)

###############################################################################
# Define Schemas
###############################################################################


class Device(SQLAlchemyObjectType, DeviceAttribute):
    """Device node."""

    class Meta:
        """Define the metadata."""

        model = DeviceModel
        interfaces = (graphene.relay.Node,)


class Event(SQLAlchemyObjectType, EventAttribute):
    """Device node."""

    class Meta:
        """Define the metadata."""

        model = EventModel
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
    devices = BatchSQLAlchemyConnectionField(Device.connection, sort=None)

    # Results as a single entry filtered by 'id' and as a list
    event = graphene.relay.Node.Field(Event)
    events = BatchSQLAlchemyConnectionField(Event.connection, sort=None)

    # Results as a single entry filtered by 'id' and as a list
    l1interface = graphene.relay.Node.Field(L1Interface)
    l1interfaces = BatchSQLAlchemyConnectionField(L1Interface.connection)

    # Results as a single entry filtered by 'id' and as a list
    zone = graphene.relay.Node.Field(Zone)
    zones = BatchSQLAlchemyConnectionField(Zone.connection, sort=None)

    # Results as a single entry filtered by 'id' and as a list
    mac = graphene.relay.Node.Field(Mac)
    macs = BatchSQLAlchemyConnectionField(Mac.connection, sort=None)

    # Results as a single entry filtered by 'id' and as a list
    macip = graphene.relay.Node.Field(MacIp)
    macips = BatchSQLAlchemyConnectionField(MacIp.connection, sort=None)

    # Results as a single entry filtered by 'id' and as a list
    macport = graphene.relay.Node.Field(MacPort)
    macports = BatchSQLAlchemyConnectionField(MacPort.connection, sort=None)

    # Results as a single entry filtered by 'id' and as a list
    oui = graphene.relay.Node.Field(Oui)
    ouis = BatchSQLAlchemyConnectionField(Oui.connection, sort=None)

    # Results as a single entry filtered by 'id' and as a list
    vlan = graphene.relay.Node.Field(Vlan)
    vlans = BatchSQLAlchemyConnectionField(Vlan.connection, sort=None)

    # Results as a single entry filtered by 'id' and as a list
    vlanport = graphene.relay.Node.Field(VlanPort)
    vlanports = BatchSQLAlchemyConnectionField(VlanPort.connection, sort=None)


# Make the schema global
SCHEMA = graphene.Schema(query=Query)
