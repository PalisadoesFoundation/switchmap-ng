"""ORM filter classes for SQLAlchemy graphene / GraphQL schemas.

Used for defining GraphQL interaction

Based on the pages at:

    https://pypi.org/project/graphene-sqlalchemy-filter/

"""

# PIP3 imports
from graphene_sqlalchemy_filter import FilterSet

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

_NUMERIC = [
    'eq', 'ne', 'is_null', 'in', 'not_in', 'lt', 'lte', 'gt', 'gte', 'range']
_STRING = [
    'eq', 'ne', 'is_null', 'in', 'not_in', 'lt', 'lte', 'gt', 'gte', 'range',
    'like', 'ilike', 'contains']

###############################################################################
# Define Filters
###############################################################################


class DeviceFilter(FilterSet):
    """Device custom filter."""

    class Meta:
        """Define the metadata."""

        model = DeviceModel
        fields = {
            'idx': _NUMERIC,
            'idx_location': _NUMERIC,
            'sys_name': _STRING,
            'hostname': _STRING,
            'sys_description': _STRING,
            'sys_objectid': _STRING,
            'sys_uptime': _NUMERIC,
            'last_polled': _NUMERIC,
            'enabled': _NUMERIC,
            'ts_modified': _NUMERIC,
            'ts_created': _NUMERIC,
        }


class LocationFilter(FilterSet):
    """Location custom filter."""

    class Meta:
        """Define the metadata."""

        model = LocationModel
        fields = {
            'idx': _NUMERIC,
            'name': _STRING,
            'company_name': _STRING,
            'address_0': _STRING,
            'address_1': _STRING,
            'address_2': _STRING,
            'city': _STRING,
            'state': _STRING,
            'country': _STRING,
            'postal_code': _STRING,
            'phone': _STRING,
            'notes': _STRING,
            'enabled': _NUMERIC,
            'ts_modified': _NUMERIC,
            'ts_created': _NUMERIC,
        }


class L1InterfaceFilter(FilterSet):
    """L1Interface custom filter."""

    class Meta:
        """Define the metadata."""

        model = L1InterfaceModel
        fields = {
            'idx': _NUMERIC,
            'idx_device': _NUMERIC,
            'ifindex': _NUMERIC,
            'duplex': _NUMERIC,
            'ethernet': _NUMERIC,
            'nativevlan': _NUMERIC,
            'trunk': _NUMERIC,
            'ifspeed': _NUMERIC,
            'ifalias': _STRING,
            'ifdescr': _STRING,
            'ifadminstatus': _NUMERIC,
            'ifoperstatus': _NUMERIC,
            'ts_idle': _NUMERIC,
            'cdpcachedeviceid': _STRING,
            'cdpcachedeviceport': _STRING,
            'cdpcacheplatform': _STRING,
            'lldpremportdesc': _STRING,
            'lldpremsyscapenabled': _STRING,
            'lldpremsysdesc': _STRING,
            'lldpremsysname': _STRING,
            'enabled': _NUMERIC,
            'ts_modified': _NUMERIC,
            'ts_created': _NUMERIC,
        }


class MacTableFilter(FilterSet):
    """MacTable custom filter."""

    class Meta:
        """Define the metadata."""

        model = MacTableModel
        fields = {
            'idx': _NUMERIC,
            'idx_device': _NUMERIC,
            'idx_oui': _NUMERIC,
            'ip_': _STRING,
            'mac': _STRING,
            'hostname': _STRING,
            'type': _NUMERIC,
            'enabled': _NUMERIC,
            'ts_modified': _NUMERIC,
            'ts_created': _NUMERIC,
        }


class OUIFilter(FilterSet):
    """OUI custom filter."""

    class Meta:
        """Define the metadata."""

        model = OUIModel
        fields = {
            'idx': _NUMERIC,
            'oui': _STRING,
            'manufacturer': _STRING,
            'enabled': _NUMERIC,
            'ts_modified': _NUMERIC,
            'ts_created': _NUMERIC,
        }


class TrunkFilter(FilterSet):
    """Trunk custom filter."""

    class Meta:
        """Define the metadata."""

        model = TrunkModel
        fields = {
            'idx': _NUMERIC,
            'idx_device': _NUMERIC,
            'ifindex': _NUMERIC,
            'idx_l1interface': _NUMERIC,
            'idx_vlan': _NUMERIC,
            'enabled': _NUMERIC,
            'ts_modified': _NUMERIC,
            'ts_created': _NUMERIC,
        }


class VlanFilter(FilterSet):
    """Vlan custom filter."""

    class Meta:
        """Define the metadata."""

        model = VlanModel
        fields = {
            'idx': _NUMERIC,
            'idx_device': _NUMERIC,
            'vlan': _NUMERIC,
            'name': _STRING,
            'state': _NUMERIC,
            'enabled': _NUMERIC,
            'ts_modified': _NUMERIC,
            'ts_created': _NUMERIC,
        }
