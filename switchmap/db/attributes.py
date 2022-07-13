"""ORM attribute classes for SQLAlchemy graphene / GraphQL schemas..

Used for defining GraphQL interaction

Based on the pages at:

    https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

"""
# PIP3 imports
import graphene

###############################################################################
# Define Attribues
###############################################################################


class DeviceAttribute():
    """Descriptive attributes of the Device table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx = graphene.Int(description='Primary key index')
    idx_zone = graphene.Int(description='System zone')
    sys_name = graphene.Int(description='System name')
    hostname = graphene.Int(description='System hostname')
    sys_description = graphene.Int(description='System description')
    sys_objectid = graphene.Int(description='System SNMP sysobjectid')
    sys_uptime = graphene.Int(description='System uptime')
    last_polled = graphene.Int(description='Timestamp of last poll')
    enabled = graphene.Int(description='Enabled')
    ts_modified = graphene.String(description='Row Modification Timestamp')
    ts_created = graphene.String(description='Row Creation Timestamp')


class ZoneAttribute():
    """Descriptive attributes of the Zone table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx = graphene.Int(description='Primary key index')
    name = graphene.String(description='Zone name')
    company_name = graphene.String(description='Company name')
    address_0 = graphene.String(description='Address Line 0')
    address_1 = graphene.String(description='Address Line 1')
    address_2 = graphene.String(description='Address Line 2')
    city = graphene.String(description='City')
    state = graphene.String(description='State')
    country = graphene.String(description='Country')
    postal_code = graphene.String(description='Postal code')
    phone = graphene.String(description='Phone')
    notes = graphene.String(description='Notes')
    enabled = graphene.Int(description='Enabled')
    ts_modified = graphene.String(description='Row Modification Timestamp')
    ts_created = graphene.String(description='Row Creation Timestamp')


class L1InterfaceAttribute():
    """Descriptive attributes of the L1Interface table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx = graphene.Int(description='Primary key index')
    idx_device = graphene.Int(description='Device index foreign key')
    ifindex = graphene.Int(description='Interface IfIndex')
    duplex = graphene.Int(description='Duplex code')
    ethernet = graphene.Int(description='Ethernet port True/False')
    nativevlan = graphene.Int(description='Interface native VLAN')
    trunk = graphene.Int(description='Trunk True/False')
    ifspeed = graphene.String(description='Interface speed')
    ifalias = graphene.String(description='Interface alias')
    ifdescr = graphene.String(description='Interface description')
    ifadminstatus = graphene.Int(description='Interface admin status')
    ifoperstatus = graphene.Int(description='Interface operational status')
    ts_idle = graphene.Int(description='Seconds Idle')
    cdpcachedeviceid = graphene.String(description='CDP device ID')
    cdpcachedeviceport = graphene.String(description='CDP device port')
    cdpcacheplatform = graphene.String(description='CDP platform')
    lldpremportdesc = graphene.String(description='LLDP port description')
    lldpremsyscapenabled = graphene.String(description='Enabled')
    lldpremsysdesc = graphene.String(description='LLDP system description')
    lldpremsysname = graphene.String(description='LLDP system name')
    enabled = graphene.String(description='LLDP enabled capabilities')
    ts_modified = graphene.String(description='Row Modification Timestamp')
    ts_created = graphene.String(description='Row Creation Timestamp')


class MacIpAttribute():
    """Descriptive attributes of the MacIp table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx = graphene.Int(description='Primary key index')
    idx_device = graphene.Int(description='Device index foreign key')
    idx_oui = graphene.Int(description='Oui index foreign key')
    ip_ = graphene.String(description='IP address')
    mac = graphene.String(description='MAC address')
    version = graphene.String(description='IPv4 or IPv6')
    hostname = graphene.String(description='Hostname')
    enabled = graphene.Int(description='Enabled')
    ts_modified = graphene.String(description='Row Modification Timestamp')
    ts_created = graphene.String(description='Row Creation Timestamp')


class OuiAttribute():
    """Descriptive attributes of the Oui table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx = graphene.Int(description='Primary key index')
    oui = graphene.String(description='Organizationally unique identifier')
    manufacturer = graphene.Int(description='Organization')
    enabled = graphene.Int(description='Enabled')
    ts_modified = graphene.String(description='Row Modification Timestamp')
    ts_created = graphene.String(description='Row Creation Timestamp')


class TrunkAttribute():
    """Descriptive attributes of the Trunk table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx = graphene.Int(description='Primary key index')
    idx_l1interface = graphene.Int(
        description='L1 interface index foreign key')
    idx_vlan = graphene.Int(description='VLAN index foreign key')
    enabled = graphene.Int(description='Enabled')
    ts_modified = graphene.String(description='Row Modification Timestamp')
    ts_created = graphene.String(description='Row Creation Timestamp')


class VlanAttribute():
    """Descriptive attributes of the Vlan table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx = graphene.Int(description='Primary key index')
    idx_device = graphene.Int(description='Device index foreign key')
    vlan = graphene.Int(description='VLAN number')
    name = graphene.Int(description='VLAN name')
    state = graphene.Int(description='VLAN state')
    enabled = graphene.Int(description='Enabled')
    ts_modified = graphene.String(description='Row Modification Timestamp')
    ts_created = graphene.String(description='Row Creation Timestamp')
