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

# Graphene Filtering
from graphene_sqlalchemy_filter import FilterableConnectionField

# Import models
from switchmap.db.models import (
    Device as DeviceModel,
    L1Interface as L1InterfaceModel,
    Location as LocationModel,
    MacTable as MacTableModel,
    OUI as OUIModel,
    Trunk as TrunkModel,
    Vlan as VlanModel,
)

# Import filters
from switchmap.db.filters import (
    DeviceFilter,
    LocationFilter,
    L1InterfaceFilter,
    MacTableFilter,
    OUIFilter,
    TrunkFilter,
    VlanFilter,
)

# Import attributes
from switchmap.db.attributes import (
    DeviceAttribute,
    LocationAttribute,
    L1InterfaceAttribute,
    MacTableAttribute,
    OUIAttribute,
    TrunkAttribute,
    VlanAttribute,
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


class L1Interface(SQLAlchemyObjectType, L1InterfaceAttribute):
    """L1Interface node."""

    class Meta:
        """Define the metadata."""

        model = L1InterfaceModel
        interfaces = (graphene.relay.Node,)


class Location(SQLAlchemyObjectType, LocationAttribute):
    """Location node."""

    class Meta:
        """Define the metadata."""

        model = LocationModel
        interfaces = (graphene.relay.Node,)


class MacTable(SQLAlchemyObjectType, MacTableAttribute):
    """MacTable node."""

    class Meta:
        """Define the metadata."""

        model = MacTableModel
        interfaces = (graphene.relay.Node,)


class OUI(SQLAlchemyObjectType, OUIAttribute):
    """OUI node."""

    class Meta:
        """Define the metadata."""

        model = OUIModel
        interfaces = (graphene.relay.Node,)


class Trunk(SQLAlchemyObjectType, TrunkAttribute):
    """Trunk node."""

    class Meta:
        """Define the metadata."""

        model = TrunkModel
        interfaces = (graphene.relay.Node,)


class Vlan(SQLAlchemyObjectType, VlanAttribute):
    """Vlan node."""

    class Meta:
        """Define the metadata."""

        model = VlanModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    """Define GraphQL queries."""

    node = relay.Node.Field()

    # Results as a single entry filtered by 'id' and as a list
    device = graphene.relay.Node.Field(Device)
    all_device = FilterableConnectionField(
        connection=Device, sort=None, filters=DeviceFilter())

    # Results as a single entry filtered by 'id' and as a list
    l1interface = graphene.relay.Node.Field(L1Interface)
    all_l1interface = FilterableConnectionField(
        connection=L1Interface, filters=L1InterfaceFilter())

    # Results as a single entry filtered by 'id' and as a list
    location = graphene.relay.Node.Field(Location)
    all_location = FilterableConnectionField(
        connection=Location, sort=None, filters=LocationFilter())

    # Results as a single entry filtered by 'id' and as a list
    mactable = graphene.relay.Node.Field(MacTable)
    all_mactable = FilterableConnectionField(
        connection=MacTable, sort=None, filters=MacTableFilter())

    # Results as a single entry filtered by 'id' and as a list
    oui = graphene.relay.Node.Field(OUI)
    all_oui = FilterableConnectionField(
        connection=OUI, sort=None, filters=OUIFilter())

    # Results as a single entry filtered by 'id' and as a list
    trunk = graphene.relay.Node.Field(Trunk)
    all_trunk = FilterableConnectionField(
        connection=Trunk, sort=None, filters=TrunkFilter())

    # Results as a single entry filtered by 'id' and as a list
    vlan = graphene.relay.Node.Field(Vlan)
    all_vlan = FilterableConnectionField(
        connection=Vlan, sort=None, filters=VlanFilter())


# Make the schema global
SCHEMA = graphene.Schema(query=Query)
