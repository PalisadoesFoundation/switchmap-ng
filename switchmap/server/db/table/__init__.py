"""Constants required for DB queries and updates."""

from collections import namedtuple

ROui = namedtuple(
    "ROui", "idx_oui oui organization enabled ts_modified ts_created"
)
IOui = namedtuple("IOui", "oui organization enabled")

RZone = namedtuple(
    "RZone",
    """idx_zone name company_name address_0 address_1 address_2 city \
state country postal_code phone notes enabled ts_modified ts_created""",
)
IZone = namedtuple(
    "IZone",
    """name company_name address_0 address_1 address_2 city state country \
postal_code phone notes enabled""",
)

RDevice = namedtuple(
    "RDevice",
    """idx_device idx_zone  sys_name hostname name \
sys_description sys_objectid sys_uptime last_polled \
enabled ts_modified ts_created""",
)
IDevice = namedtuple(
    "IDevice",
    """idx_zone  sys_name hostname name \
sys_description sys_objectid sys_uptime last_polled enabled""",
)

RL1Interface = namedtuple(
    "RL1Interface",
    """idx_l1interface idx_device ifindex duplex ethernet nativevlan trunk \
ifspeed ifalias ifdescr ifadminstatus ifoperstatus ts_idle cdpcachedeviceid \
cdpcachedeviceport cdpcacheplatform lldpremportdesc lldpremsyscapenabled \
lldpremsysdesc lldpremsysname enabled ts_modified ts_created""",
)
IL1Interface = namedtuple(
    "IL1Interface",
    """idx_device ifindex duplex ethernet nativevlan trunk ifspeed ifalias \
ifdescr ifadminstatus ifoperstatus ts_idle cdpcachedeviceid \
cdpcachedeviceport cdpcacheplatform lldpremportdesc lldpremsyscapenabled \
lldpremsysdesc lldpremsysname enabled""",
)

RVlan = namedtuple(
    "RVlan",
    "idx_vlan idx_device vlan name state enabled ts_modified ts_created",
)
IVlan = namedtuple("IVlan", "idx_device vlan name state enabled")

RTrunk = namedtuple(
    "RTrunk",
    "idx_trunk idx_l1interface idx_vlan enabled ts_modified ts_created",
)
ITrunk = namedtuple("ITrunk", "idx_l1interface idx_vlan enabled")

RMacIp = namedtuple(
    "RMacIp",
    """idx_macip idx_device idx_mac ip_ hostname version enabled \
ts_modified ts_created""",
)
IMacIp = namedtuple(
    "IMacIp", "idx_device idx_mac ip_ hostname version enabled"
)

RMac = namedtuple(
    "RMac",
    """idx_mac idx_oui  idx_zone mac enabled \
ts_modified ts_created""",
)
IMac = namedtuple("IMac", "idx_oui  idx_zone mac enabled")
TopologyMac = namedtuple("TopologyMac", " idx_zone mac enabled")

RMacPort = namedtuple(
    "RMacPort",
    """idx_macport idx_l1interface idx_mac enabled \
ts_modified ts_created""",
)
IMacPort = namedtuple("IMacPort", "idx_l1interface idx_mac enabled")

RVlanPort = namedtuple(
    "RVlanPort",
    """idx_vlanport idx_l1interface idx_vlan enabled \
ts_modified ts_created""",
)
IVlanPort = namedtuple("IVlanPort", "idx_l1interface idx_vlan enabled")

ProcessMacIP = namedtuple("ProcessMacIP", "table idx_device version")

TopologyUpdates = namedtuple("Updates", "idx_macip row")
TopologyResult = namedtuple("Result", "updates adds")
