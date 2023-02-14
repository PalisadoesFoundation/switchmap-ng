"""Module to handle database table rows."""

from switchmap.server.db.table import RMacPort
from switchmap.server.db.table import RL1Interface
from switchmap.server.db.table import RDevice
from switchmap.server.db.table import RMac
from switchmap.server.db.table import RMacIp
from switchmap.server.db.table import ROui
from switchmap.server.db.table import RVlan
from switchmap.server.db.table import RVlanPort
from switchmap.server.db.table import RZone


def device(row):
    """Convert table row to tuple.

    Args:
        row: Device row

    Returns:
        result: RDevice tuple

    """
    # Initialize key variables
    result = RDevice(
        idx_device=row.idx_device,
        idx_zone=row.idx_zone,
        sys_name=(
            None if bool(row.sys_name) is False else row.sys_name.decode()
        ),
        hostname=(
            None if bool(row.hostname) is False else row.hostname.decode()
        ),
        name=(None if bool(row.name) is False else row.name.decode()),
        sys_description=(
            None
            if bool(row.sys_description) is False
            else row.sys_description.decode()
        ),
        sys_objectid=(
            None
            if bool(row.sys_objectid) is False
            else row.sys_objectid.decode()
        ),
        sys_uptime=row.sys_uptime,
        last_polled=row.last_polled,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result


def l1interface(row):
    """Convert table row to tuple.

    Args:
        row: L1Interface row

    Returns:
        result: RL1Interface tuple

    """
    # Initialize key variables
    result = RL1Interface(
        idx_l1interface=row.idx_l1interface,
        idx_device=row.idx_device,
        ifindex=row.ifindex,
        duplex=row.duplex,
        ethernet=row.ethernet,
        nativevlan=row.nativevlan,
        trunk=row.trunk,
        ifspeed=row.ifspeed,
        ifalias=None if row.ifalias is None else row.ifalias.decode(),
        ifdescr=None if row.ifdescr is None else row.ifdescr.decode(),
        ifadminstatus=row.ifadminstatus,
        ifoperstatus=row.ifoperstatus,
        ts_idle=row.ts_idle,
        cdpcachedeviceid=(
            None
            if row.cdpcachedeviceid is None
            else row.cdpcachedeviceid.decode()
        ),
        cdpcachedeviceport=(
            None
            if row.cdpcachedeviceport is None
            else row.cdpcachedeviceport.decode()
        ),
        cdpcacheplatform=(
            None
            if row.cdpcacheplatform is None
            else row.cdpcacheplatform.decode()
        ),
        lldpremportdesc=(
            None
            if row.lldpremportdesc is None
            else row.lldpremportdesc.decode()
        ),
        lldpremsyscapenabled=(
            None
            if row.lldpremsyscapenabled is None
            else row.lldpremsyscapenabled.decode()
        ),
        lldpremsysdesc=(
            None if row.lldpremsysdesc is None else row.lldpremsysdesc.decode()
        ),
        lldpremsysname=(
            None if row.lldpremsysname is None else row.lldpremsysname.decode()
        ),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result


def mac(row):
    """Convert table row to tuple.

    Args:
        row: Mac row

    Returns:
        result: RMac tuple

    """
    # Initialize key variables
    result = RMac(
        idx_mac=row.idx_mac,
        idx_oui=row.idx_oui,
        idx_zone=row.idx_zone,
        mac=(None if bool(row.mac) is False else row.mac.decode()),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result


def macip(row):
    """Convert table row to tuple.

    Args:
        row: MacIp row

    Returns:
        result: RMacIp tuple

    """
    # Initialize key variables
    result = RMacIp(
        idx_macip=row.idx_macip,
        idx_device=row.idx_device,
        idx_mac=row.idx_mac,
        ip_=None if bool(row.ip_) is False else row.ip_.decode(),
        hostname=(
            None if bool(row.hostname) is False else row.hostname.decode()
        ),
        version=row.version,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result


def macport(row):
    """Convert table row to tuple.

    Args:
        row: MacPort row

    Returns:
        result: RMacPort tuple

    """
    # Initialize key variables
    result = RMacPort(
        idx_macport=row.idx_macport,
        idx_l1interface=row.idx_l1interface,
        idx_mac=row.idx_mac,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result


def oui(row):
    """Convert table row to tuple.

    Args:
        row: Oui row

    Returns:
        result: ROui tuple

    """
    # Initialize key variables
    result = ROui(
        idx_oui=row.idx_oui,
        oui=(None if bool(row.oui) is False else row.oui.decode()),
        organization=(
            None
            if bool(row.organization) is False
            else row.organization.decode()
        ),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result


def vlan(row):
    """Convert table row to tuple.

    Args:
        row: Vlan row

    Returns:
        result: RVlan tuple

    """
    # Initialize key variables
    result = RVlan(
        idx_vlan=row.idx_vlan,
        idx_device=row.idx_device,
        vlan=row.vlan,
        name=None if bool(row.name) is False else row.name.decode(),
        state=row.state,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result


def vlanport(row):
    """Convert table row to tuple.

    Args:
        row: VlanPort row

    Returns:
        result: RVlanPort tuple

    """
    # Initialize key variables
    result = RVlanPort(
        idx_vlanport=row.idx_vlanport,
        idx_l1interface=row.idx_l1interface,
        idx_vlan=row.idx_vlan,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result


def zone(row):
    """Convert table row to tuple.

    Args:
        row: Zone row

    Returns:
        result: RZone tuple

    """
    # Initialize key variables
    result = RZone(
        idx_zone=row.idx_zone,
        name=(None if row.name is None else row.name.decode()),
        company_name=(
            None if row.company_name is None else row.company_name.decode()
        ),
        address_0=(None if row.address_0 is None else row.address_0.decode()),
        address_1=(None if row.address_1 is None else row.address_1.decode()),
        address_2=(None if row.address_2 is None else row.address_2.decode()),
        city=(None if row.city is None else row.city.decode()),
        state=(None if row.state is None else row.state.decode()),
        country=(None if row.country is None else row.country.decode()),
        postal_code=(
            None if row.postal_code is None else row.postal_code.decode()
        ),
        phone=(None if row.phone is None else row.phone.decode()),
        notes=(None if row.notes is None else row.notes.decode()),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified,
    )
    return result
