"""Constants required for DB queries and updates."""

from collections import namedtuple

ROui = namedtuple(
    "ROui", "idx_oui oui organization enabled ts_modified ts_created"
)
IOui = namedtuple("IOui", "oui organization enabled")

RZone = namedtuple(
    "RZone",
    """idx_zone idx_event name notes enabled ts_modified ts_created""",
)
IZone = namedtuple(
    "IZone",
    """idx_event name notes enabled""",
)

RRoot = namedtuple(
    "RRoot",
    "idx_root idx_event name enabled ts_modified ts_created",
)

IRoot = namedtuple(
    "IRoot",
    "idx_event name enabled",
)

REvent = namedtuple(
    "REvent", "idx_event name epoch_utc enabled ts_modified ts_created"
)
IEvent = namedtuple("IEvent", "name epoch_utc enabled")

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

SystemStat = namedtuple(
    "SystemStat", "idx_systemstat idx_device cpu_5min mem_used mem_free"
)

ISystemStat = namedtuple("ISystemStat", "idx_device cpu_5min mem_used mem_free")

RL1Interface = namedtuple(
    "RL1Interface",
    """idx_l1interface idx_device ifindex duplex ethernet nativevlan trunk \
ifspeed iftype ifalias ifdescr ifname ifadminstatus ifoperstatus \
ifin_ucast_pkts ifout_ucast_pkts ifin_errors ifin_discards ts_idle \
cdpcachedeviceid cdpcachedeviceport cdpcacheplatform lldpremportdesc \
lldpremsyscapenabled lldpremsysdesc lldpremsysname enabled ts_modified \
ts_created""",
)
IL1Interface = namedtuple(
    "IL1Interface",
    """idx_device ifindex duplex ethernet nativevlan trunk ifspeed iftype \
ifalias ifdescr ifname ifadminstatus ifoperstatus ifin_ucast_pkts \
ifout_ucast_pkts ifin_errors ifin_discards ts_idle cdpcachedeviceid \
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
    """idx_macip idx_ip idx_mac enabled ts_modified ts_created""",
)
IMacIp = namedtuple("IMacIp", "idx_ip idx_mac enabled")

RMac = namedtuple(
    "RMac",
    """idx_mac idx_oui  idx_zone mac enabled \
ts_modified ts_created""",
)
IMac = namedtuple("IMac", "idx_oui  idx_zone mac enabled")

RIp = namedtuple(
    "RIp",
    """idx_ip idx_zone address version hostname enabled \
ts_modified ts_created""",
)
IIp = namedtuple("IIp", "idx_zone address version hostname enabled")

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

RIpPort = namedtuple(
    "RIpPort",
    """idx_ipport idx_l1interface idx_ip enabled \
ts_modified ts_created""",
)
IIpPort = namedtuple("IIpPort", "idx_l1interface idx_ip enabled")

ProcessMacIP = namedtuple("ProcessMacIP", "table idx_device idx_zone version")
