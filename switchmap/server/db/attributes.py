"""ORM attribute classes for SQLAlchemy graphene / GraphQL schemas..

Used for defining GraphQL interaction

Based on the pages at:

    https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

"""

# PIP3 imports
import graphene
from switchmap.server.db.models import Device


###############################################################################
# Define Resolvers
###############################################################################


def resolve_address(obj, _):
    """Convert 'address' from bytes to string.

    Args:
        obj: Object containing address attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded address string or empty string
    """
    return obj.address.decode() if bool(obj.address) else ""


def resolve_cdpcachedeviceid(obj, _):
    """Convert 'cdpcachedeviceid' from bytes to string.

    Args:
        obj: Object containing cdpcachedeviceid attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded cdpcachedeviceid string or empty string
    """
    return obj.cdpcachedeviceid.decode() if bool(obj.cdpcachedeviceid) else ""


def resolve_cdpcacheplatform(obj, _):
    """Convert 'cdpcacheplatform' from bytes to string.

    Args:
        obj: Object containing cdpcacheplatform attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded cdpcacheplatform string or empty string
    """
    return obj.cdpcacheplatform.decode() if bool(obj.cdpcacheplatform) else ""


def resolve_cdpcachedeviceport(obj, _):
    """Convert 'cdpcachedeviceport' from bytes to string.

    Args:
        obj: Object containing cdpcachedeviceport attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded cdpcachedeviceport string or empty string
    """
    return (
        obj.cdpcachedeviceport.decode() if bool(obj.cdpcachedeviceport) else ""
    )


def resolve_hostname(obj, _):
    """Convert 'hostname' from bytes to string.

    Args:
        obj: Object containing hostname attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded hostname string or empty string
    """
    return obj.hostname.decode() if bool(obj.hostname) else ""


def resolve_ifalias(obj, _):
    """Convert 'ifalias' from bytes to string.

    Args:
        obj: Object containing ifalias attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded ifalias string or empty string
    """
    return obj.ifalias.decode() if bool(obj.ifalias) else ""


def resolve_ifname(obj, _):
    """Convert 'ifname' from bytes to string.

    Args:
        obj: Object containing ifname attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded ifname string or empty string
    """
    return obj.ifname.decode() if bool(obj.ifname) else ""


def resolve_ifdescr(obj, _):
    """Convert 'ifdescr' from bytes to string.

    Args:
        obj: Object containing ifdescr attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded ifdescr string or empty string
    """
    return obj.ifdescr.decode() if bool(obj.ifdescr) else ""


def resolve_lldpremportdesc(obj, _):
    """Convert 'lldpremportdesc' from bytes to string.

    Args:
        obj: Object containing lldpremportdesc attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded lldpremportdesc string or empty string
    """
    return obj.lldpremportdesc.decode() if bool(obj.lldpremportdesc) else ""


def resolve_lldpremsyscapenabled(obj, _):
    """Convert 'lldpremsyscapenabled' from bytes to string.

    Args:
        obj: Object containing lldpremsyscapenabled attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded lldpremsyscapenabled string or empty string
    """
    return (
        obj.lldpremsyscapenabled.decode()
        if bool(obj.lldpremsyscapenabled)
        else ""
    )


def resolve_lldpremsysdesc(obj, _):
    """Convert 'lldpremsysdesc' from bytes to string.

    Args:
        obj: Object containing lldpremsysdesc attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded lldpremsysdesc string or empty string
    """
    return obj.lldpremsysdesc.decode() if bool(obj.lldpremsysdesc) else ""


def resolve_lldpremsysname(obj, _):
    """Convert 'lldpremsysname' from bytes to string.

    Args:
        obj: Object containing lldpremsysname attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded lldpremsysname string or empty string
    """
    return obj.lldpremsysname.decode() if bool(obj.lldpremsysname) else ""


def resolve_mac(obj, _):
    """Convert 'mac' from bytes to string.

    Args:
        obj: Object containing mac attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded mac string or empty string
    """
    return obj.mac.decode() if bool(obj.mac) else ""


def resolve_organization(obj, _):
    """Convert 'organization' from bytes to string.

    Args:
        obj: Object containing organization attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded organization string or empty string
    """
    return obj.organization.decode() if bool(obj.organization) else ""


def resolve_device_by_hostname(obj, info, hostname=None):
    """Resolve device by hostname with proper encoding handling.

    Args:
        hostname: Hostname to search for

    Returns:
        Device: Device object matching hostname
    """
    if not hostname:
        return None

    # Convert hostname to bytes for comparison
    hostname_bytes = hostname.encode("utf-8")
    return Device.query.filter(Device.hostname == hostname_bytes).first()


def resolve_name(obj, _):
    """Convert 'name' from bytes to string.

    Args:
        obj: Object containing name attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded name string or empty string
    """
    return obj.name.decode() if bool(obj.name) else ""


def resolve_notes(obj, _):
    """Convert 'notes' from bytes to string.

    Args:
        obj: Object containing notes attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded notes string or empty string
    """
    return obj.notes.decode() if bool(obj.notes) else ""


def resolve_oui(obj, _):
    """Convert 'oui' from bytes to string.

    Args:
        obj: Object containing oui attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded oui string or empty string
    """
    return obj.oui.decode() if bool(obj.oui) else ""


def resolve_sys_description(obj, _):
    """Convert 'sys_description' from bytes to string.

    Args:
        obj: Object containing sys_description attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded sys_description string or empty string
    """
    return obj.sys_description.decode() if bool(obj.sys_description) else ""


def resolve_sys_name(obj, _):
    """Convert 'sys_name' from bytes to string.

    Args:
        obj: Object containing sys_name attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded sys_name string or empty string
    """
    return obj.sys_name.decode() if bool(obj.sys_name) else ""


def resolve_sys_uptime(obj, _):
    """Convert 'sys_uptime' from Null to zero.

    Args:
        obj: Object containing sys_uptime attribute
        _: Unused GraphQL parameter

    Returns:
        float: System uptime value or 0 if null
    """
    return float(obj.sys_uptime) if bool(obj.sys_uptime) else 0


def resolve_sys_objectid(obj, _):
    """Convert 'sys_objectid' from bytes to string.

    Args:
        obj: Object containing sys_objectid attribute
        _: Unused GraphQL parameter

    Returns:
        str: Decoded sys_objectid string or empty string
    """
    return obj.sys_objectid.decode() if bool(obj.sys_objectid) else ""


###############################################################################
# Define Attribues
###############################################################################


class EventAttribute:
    """Descriptive attributes of the Event table.

    A generic class to mutualize description of attributes for both queries
    and mutations.
    """

    idx_event = graphene.Int(description="Primary key index")
    name = graphene.String(resolver=resolve_name, description="Event name")
    epoch_utc = graphene.Int(description="Epoch UTC timestamp")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.String(description="Row Modification Timestamp")
    ts_created = graphene.String(description="Row Creation Timestamp")


class RootAttribute:
    """Descriptive attributes of the Event table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_root = graphene.Int(description="Primary key index")
    idx_event = graphene.Int(description="Event index foreign key")
    name = graphene.String(resolver=resolve_name, description="Root name")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.String(description="Row Modification Timestamp")
    ts_created = graphene.String(description="Row Creation Timestamp")


class ZoneAttribute:
    """Descriptive attributes of the Zone table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_zone = graphene.Int(description="Primary key index")
    idx_event = graphene.Int(description="Event index foreign key")
    name = graphene.String(resolver=resolve_name, description="Zone name")
    notes = graphene.String(resolver=resolve_notes, description="Notes")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class OuiAttribute:
    """Descriptive attributes of the Oui table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_oui = graphene.Int(description="Primary key index")
    oui = graphene.String(
        resolver=resolve_oui,
        description="Organizationally unique identifier",
    )
    organization = graphene.String(
        resolver=resolve_organization, description="Manufacturing organization"
    )
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class DeviceAttribute:
    """Descriptive attributes of the Device table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_device = graphene.Int(description="Primary key index")
    idx_zone = graphene.Int(description="Zone index foreign key")
    sys_name = graphene.String(
        resolver=resolve_sys_name, description="System name"
    )
    name = graphene.String(resolver=resolve_name, description="Device name")
    hostname = graphene.String(
        resolver=resolve_hostname, description="System hostname"
    )
    sys_description = graphene.String(
        resolver=resolve_sys_description, description="System description"
    )
    sys_objectid = graphene.String(
        resolver=resolve_sys_objectid, description="System SNMP sysobjectid"
    )
    sys_uptime = graphene.Float(
        resolver=resolve_sys_uptime, description="System uptime"
    )
    last_polled = graphene.Int(description="Timestamp of last poll")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class SystemStatAttribute:
    """Descriptive attributes of the SystemStat table.

    A generic class to mutualize description of attributes for both queries
    and mutations.
    """

    idx_systemstat = graphene.Int(description="Primary key index")
    idx_device = graphene.Int(description="Device Index Foreign key ")
    cpu_5min = graphene.Int(description=" Device cpu_5min_usage")
    mem_used = graphene.Float(description="Device memory_used (bytes)")
    mem_free = graphene.Float(description="Device memory_free (bytes)")


class L1InterfaceAttribute:
    """Descriptive attributes of the L1Interface table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_l1interface = graphene.Int(description="Primary key index")
    idx_device = graphene.Int(description="Device index foreign key")
    ifindex = graphene.Int(description="Interface IfIndex")
    duplex = graphene.Int(description="Duplex code")
    ethernet = graphene.Int(description="Ethernet port True/False")
    nativevlan = graphene.Int(description="Interface native VLAN")
    trunk = graphene.Int(description="Trunk True/False")
    ifspeed = graphene.Int(description="Interface speed")
    iftype = graphene.Int(description="Interface type")
    ifalias = graphene.String(
        resolver=resolve_ifalias, description="Interface alias"
    )
    ifname = graphene.String(
        resolver=resolve_ifname, description="Interface name"
    )
    ifdescr = graphene.String(
        resolver=resolve_ifdescr, description="Interface description"
    )
    ifadminstatus = graphene.Int(description="Interface admin status")
    ifoperstatus = graphene.Int(description="Interface operational status")
    ts_idle = graphene.Int(description="Seconds Idle")
    cdpcachedeviceid = graphene.String(
        resolver=resolve_cdpcachedeviceid, description="CDP device ID"
    )
    cdpcachedeviceport = graphene.String(
        resolver=resolve_cdpcachedeviceport, description="CDP device port"
    )
    cdpcacheplatform = graphene.String(
        resolver=resolve_cdpcacheplatform, description="CDP platform"
    )
    lldpremportdesc = graphene.String(
        resolver=resolve_lldpremportdesc, description="LLDP port description"
    )
    lldpremsyscapenabled = graphene.String(
        resolver=resolve_lldpremsyscapenabled,
        description="LLDP capabilities enabled",
    )
    lldpremsysdesc = graphene.String(
        resolver=resolve_lldpremsysdesc, description="LLDP system description"
    )
    lldpremsysname = graphene.String(
        resolver=resolve_lldpremsysname, description="LLDP system name"
    )
    ifin_ucast_pkts = graphene.Float(
        description="Interface inbound unicast packets"
    )
    ifout_ucast_pkts = graphene.Float(
        description="Interface outbound unicast packets"
    )
    ifin_errors = graphene.Float(description="Interface inbound errors")
    ifin_discards = graphene.Float(description="Interface inbound discards")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class VlanAttribute:
    """Descriptive attributes of the Vlan table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_vlan = graphene.Int(description="Primary key index")
    idx_device = graphene.Int(description="Device index foreign key")
    vlan = graphene.Int(description="VLAN number")
    name = graphene.Int(description="VLAN name")
    state = graphene.Int(description="VLAN state")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class VlanPortAttribute:
    """Descriptive attributes of the VlanPort table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_vlanport = graphene.Int(description="Primary key index")
    idx_device = graphene.Int(description="Device index foreign key")
    idx_l1interface = graphene.Int(description="L1Interface index foreign key")
    idx_vlan = graphene.Int(description="Vlan index foreign key")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class MacAttribute:
    """Descriptive attributes of the Mac table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_mac = graphene.Int(description="Primary key index")
    idx_oui = graphene.Int(description="OUI index foreign key")
    idx_zone = graphene.Int(description="Zone index foreign key")
    mac = graphene.String(resolver=resolve_mac, description="MAC address")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class MacIpAttribute:
    """Descriptive attributes of the MacIp table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_macip = graphene.Int(description="Primary key index")
    idx_ip = graphene.Int(description="IP index foreign key")
    idx_mac = graphene.Int(description="MAC address index foreign key")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class MacPortAttribute:
    """Descriptive attributes of the MacPort table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_macport = graphene.Int(description="Primary key index")
    idx_mac = graphene.Int(description="MAC address index foreign key")
    idx_l1interface = graphene.Int(description="L1Interface index foreign key")
    enabled = graphene.Boolean(description="Enabled")
    ts_modified = graphene.DateTime(description="Row Modification Timestamp")
    ts_created = graphene.DateTime(description="Row Creation Timestamp")


class IpAttribute:
    """Descriptive attributes of the MacPort table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_ip = graphene.Int(description="IP index foreign key")
    idx_zone = graphene.Int(description="Zone index foreign key")
    address = graphene.String(
        resolver=resolve_address, description="IP address"
    )
    version = graphene.Int(description="IPv4 or IPv6")
    hostname = graphene.String(
        resolver=resolve_hostname, description="Hostname"
    )


class IpPortAttribute:
    """Descriptive attributes of the MacPort table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_ipport = graphene.Int(description="IpPort index foreign key")
    idx_ip = graphene.Int(description="Ip index foreign key")
    idx_l1interface = graphene.Int(description="L1interface index foreign key")
