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
    Zone as ZoneModel,
    MacIp as MacIpModel,
    Oui as OuiModel,
    Trunk as TrunkModel,
    Vlan as VlanModel,
)

# Import filters
from switchmap.db.filters import (
    DeviceFilter,
    ZoneFilter,
    L1InterfaceFilter,
    MacIpFilter,
    OuiFilter,
    TrunkFilter,
    VlanFilter,
)

# Import attributes
from switchmap.db.attributes import (
    DeviceAttribute,
    ZoneAttribute,
    L1InterfaceAttribute,
    MacIpAttribute,
    OuiAttribute,
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


class Oui(SQLAlchemyObjectType, OuiAttribute):
    """Oui node."""

    class Meta:
        """Define the metadata."""

        model = OuiModel
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
        connection=Device, sort=None, filters=DeviceFilter()
    )

    # Results as a single entry filtered by 'id' and as a list
    l1interface = graphene.relay.Node.Field(L1Interface)
    all_l1interface = FilterableConnectionField(
        connection=L1Interface, filters=L1InterfaceFilter()
    )

    # Results as a single entry filtered by 'id' and as a list
    zone = graphene.relay.Node.Field(Zone)
    all_zone = FilterableConnectionField(
        connection=Zone, sort=None, filters=ZoneFilter()
    )

    # Results as a single entry filtered by 'id' and as a list
    mac = graphene.relay.Node.Field(MacIp)
    all_mac = FilterableConnectionField(
        connection=MacIp, sort=None, filters=MacIpFilter()
    )

    # Results as a single entry filtered by 'id' and as a list
    oui = graphene.relay.Node.Field(Oui)
    all_oui = FilterableConnectionField(
        connection=Oui, sort=None, filters=OuiFilter()
    )

    # Results as a single entry filtered by 'id' and as a list
    trunk = graphene.relay.Node.Field(Trunk)
    all_trunk = FilterableConnectionField(
        connection=Trunk, sort=None, filters=TrunkFilter()
    )

    # Results as a single entry filtered by 'id' and as a list
    vlan = graphene.relay.Node.Field(Vlan)
    all_vlan = FilterableConnectionField(
        connection=Vlan, sort=None, filters=VlanFilter()
    )


# Make the schema global
SCHEMA = graphene.Schema(query=Query)
