<a id="configuration"></a>

# configuration

switchmap classes that manage various configurations.

<a id="configuration.ConfigPoller"></a>

## ConfigPoller Objects

```python
class ConfigPoller(ConfigAPIClient)
```

Class gathers all configuration information.

<a id="configuration.ConfigPoller.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Intialize the class.

**Arguments**:

  None
  

**Returns**:

  None

<a id="configuration.ConfigPoller.hostnames"></a>

#### hostnames

```python
def hostnames()
```

Get hostnames.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigPoller.polling_interval"></a>

#### polling\_interval

```python
def polling_interval()
```

Get polling_interval.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigPoller.snmp_auth"></a>

#### snmp\_auth

```python
def snmp_auth()
```

Get list of dicts of SNMP information in configuration file.

**Arguments**:

  None
  

**Returns**:

- `snmp_data` - List of SNMP objects.

<a id="configuration.ConfigPoller.username"></a>

#### username

```python
def username()
```

Get username.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigPoller.zones"></a>

#### zones

```python
def zones()
```

Get list of dicts of polling zone information in configuration file.

**Arguments**:

  None
  

**Returns**:

- `result` - List of ZONE objects.

<a id="poll"></a>

# poll

Async Switchmap-NG poll module.

<a id="poll.devices"></a>

#### devices

```python
async def devices(max_concurrent_devices=None)
```

Poll all devices asynchronously.

**Arguments**:

- `max_concurrent_devices` - Maximum number of devices to poll concurrently.
  If None, uses config.agent_subprocesses()
  

**Returns**:

  None

<a id="poll.device"></a>

#### device

```python
async def device(poll_meta, device_semaphore, session, post=True)
```

Poll each device asynchronously.

**Arguments**:

- `poll_meta` - _META object containing zone, hostname, config
- `device_semaphore` - Semaphore to limit concurrent devices
- `session` - aiohttp ClientSession for HTTP requests
- `post` - Post the data if True, else just print it
  

**Returns**:

- `bool` - True if successful, False otherwise

<a id="poll.cli_device"></a>

#### cli\_device

```python
async def cli_device(hostname)
```

Poll single device for data - CLI interface.

**Arguments**:

- `hostname` - Host to poll
  

**Returns**:

  None

<a id="poll.run_devices"></a>

#### run\_devices

```python
def run_devices(max_concurrent_devices=None)
```

Run device polling - main entry point.

**Arguments**:

- `max_concurrent_devices` _int, optional_ - Maximum number of devices to
  poll concurrently. If None, uses config.agent_subprocesses().
  

**Returns**:

  None

<a id="poll.run_cli_device"></a>

#### run\_cli\_device

```python
def run_cli_device(hostname)
```

Run CLI device polling - main entry point.

**Arguments**:

- `hostname` _str_ - The hostname of the device to poll.
  

**Returns**:

  None

<a id="__init__"></a>

# \_\_init\_\_

Define the switchmap.poller package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="snmp"></a>

# snmp

Switchmap-NG snmp package.

<a id="snmp.get_queries"></a>

#### get\_queries

```python
def get_queries(layer)
```

Get mib queries which gather information related to a specific OSI layer.

**Arguments**:

- `layer` - The layer of queries needed
  

**Returns**:

- `queries` - List of queries tagged the given layer

<a id="snmp.iana_enterprise"></a>

# snmp.iana\_enterprise

Vendor queries.

<a id="snmp.iana_enterprise.Query"></a>

## Query Objects

```python
class Query()
```

Class interacts with devices to get vendor information.

**Arguments**:

  None
  

**Returns**:

  None
  

**Methods**:

  All methods rely on this document to determine vendors
  https://www.iana.org/assignments/
  enterprise-numbers/enterprise-numbers

<a id="snmp.iana_enterprise.Query.__init__"></a>

#### \_\_init\_\_

```python
def __init__(enterprise=None, sysobjectid=None)
```

Instantiate the class.

**Arguments**:

- `enterprise` - The enterprise number of the manufacturer
- `sysobjectid` - The sysobjectid of the device
  

**Returns**:

  None

<a id="snmp.iana_enterprise.Query.enterprise"></a>

#### enterprise

```python
def enterprise()
```

Get enterprise number.

**Arguments**:

  None
  

**Returns**:

- `self.enterprise_id` - Enterprise number

<a id="snmp.iana_enterprise.Query.is_cisco"></a>

#### is\_cisco

```python
def is_cisco()
```

Verify whether device is a Cisco device.

**Arguments**:

  None
  

**Returns**:

- `value` - True if matches vendor

<a id="snmp.iana_enterprise.Query.is_juniper"></a>

#### is\_juniper

```python
def is_juniper()
```

Verify whether device is a Juniper device.

**Arguments**:

  None
  

**Returns**:

- `value` - True if matches vendor

<a id="snmp.mib.juniper.mib_junipervlan"></a>

# snmp.mib.juniper.mib\_junipervlan

Module for JUNIPER-VLAN-MIB.

<a id="snmp.mib.juniper.mib_junipervlan.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `JuniperVlanQuery` - Query class for JUNIPER-VLAN-MIB

<a id="snmp.mib.juniper.mib_junipervlan.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMPInteract object
  

**Returns**:

- `JuniperVlanQuery` - Query class for JUNIPER-VLAN-MIB

<a id="snmp.mib.juniper.mib_junipervlan.JuniperVlanQuery"></a>

## JuniperVlanQuery Objects

```python
class JuniperVlanQuery(Query)
```

Class interacts with JUNIPER-VLAN-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.juniper.mib_junipervlan.JuniperVlanQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.juniper.mib_junipervlan.JuniperVlanQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.juniper.mib_junipervlan.JuniperVlanQuery.layer2"></a>

#### layer2

```python
async def layer2()
```

Get layer 2 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.juniper.mib_junipervlan.JuniperVlanQuery.jnxexvlanportaccessmode"></a>

#### jnxexvlanportaccessmode

```python
async def jnxexvlanportaccessmode()
```

Return dict of JUNIPER-VLAN-MIB jnxExVlanPortAccessMode per port.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of jnxExVlanPortAccessMode using ifIndex as key

<a id="snmp.mib.juniper.mib_junipervlan.JuniperVlanQuery.jnxexvlantag"></a>

#### jnxexvlantag

```python
async def jnxexvlantag()
```

Return dict of JUNIPER-VLAN-MIB jnxExVlanTag per port.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of jnxExVlanTag using ifIndex as key

<a id="snmp.mib.juniper.mib_junipervlan.JuniperVlanQuery.jnxexvlanname"></a>

#### jnxexvlanname

```python
async def jnxexvlanname()
```

Return dict of JUNIPER-VLAN-MIB jnxExVlanName for each VLAN tag.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of jnxExVlanName using the VLAN tag as key

<a id="snmp.mib.juniper.mib_juniperprocess"></a>

# snmp.mib.juniper.mib\_juniperprocess

Module for JUNIPER-PROCESS-MIB.

<a id="snmp.mib.juniper.mib_juniperprocess.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `type` - JuniperProcessQuery class

<a id="snmp.mib.juniper.mib_juniperprocess.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP interact class object from snmp_manager.py
  

**Returns**:

- `JuniperProcessQuery` - Initialized query instance

<a id="snmp.mib.juniper.mib_juniperprocess.JuniperProcessQuery"></a>

## JuniperProcessQuery Objects

```python
class JuniperProcessQuery(Query)
```

Class interacts with devices supporting JUNIPER-PROCESS_MIB.

<a id="snmp.mib.juniper.mib_juniperprocess.JuniperProcessQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.juniper.mib_juniperprocess.JuniperProcessQuery.system"></a>

#### system

```python
async def system()
```

Get system resource data from Juniper devices.

<a id="snmp.mib.juniper.mib_juniperprocess.JuniperProcessQuery.operatingcpu"></a>

#### operatingcpu

```python
async def operatingcpu(oidonly=False)
```

Return dict of JUNIPER-MIB jnxOperatingCPU for device.

<a id="snmp.mib.juniper.mib_juniperprocess.JuniperProcessQuery.operatingmemoryused"></a>

#### operatingmemoryused

```python
async def operatingmemoryused(oidonly=False)
```

Get used memory from JUNIPER-MIB (jnxOperatingMemoryUsed).

<a id="snmp.mib.juniper.mib_juniperprocess.JuniperProcessQuery.operatingmemoryfree"></a>

#### operatingmemoryfree

```python
async def operatingmemoryfree(oidonly=False)
```

Get free memory from JUNIPER-MIB (jnxOperatingMemoryFree).

<a id="snmp.mib.juniper"></a>

# snmp.mib.juniper

Juniper class imports.

<a id="snmp.mib.generic.mib_entity"></a>

# snmp.mib.generic.mib\_entity

Class interacts with devices supporting ENTITY-MIB.

<a id="snmp.mib.generic.mib_entity.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `EntityQuery` - Query class object

<a id="snmp.mib.generic.mib_entity.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `EntityQuery` - Query class object

<a id="snmp.mib.generic.mib_entity.EntityQuery"></a>

## EntityQuery Objects

```python
class EntityQuery(Query)
```

Class interacts with devices supporting ENTITY-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `system` - Returns all relevant system information from the device.
  In some cases a system will have multiple subsystems that are
  covered by an OID. (eg. module / circuit board serial numbers).
  It will therefore be impossible to have a consistent key format
  for data values returned. Data returned by this method will
  therefore be keyed by :
  1) MIB name (primary key)
  2) OID name in the MIB, (secondary key),
  3) Leaf value, or zero (0) if there are no leaves.

<a id="snmp.mib.generic.mib_entity.EntityQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Intialize the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_entity.EntityQuery.system"></a>

#### system

```python
async def system()
```

Get system data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_entity.EntityQuery.entphysicaldescr"></a>

#### entphysicaldescr

```python
async def entphysicaldescr()
```

Return dict of ENTITY-MIB entPhysicalDescr for device.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of entPhysicalDescr using
  the oid's last node as key

<a id="snmp.mib.generic.mib_entity.EntityQuery.entphysicalclass"></a>

#### entphysicalclass

```python
async def entphysicalclass()
```

Return dict of ENTITY-MIB entPhysicalClass for device.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of entPhysicalClass using
  the oid's last node as key

<a id="snmp.mib.generic.mib_entity.EntityQuery.entphysicalsoftwarerev"></a>

#### entphysicalsoftwarerev

```python
async def entphysicalsoftwarerev()
```

Return dict of ENTITY-MIB entPhysicalSoftwareRev for device.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of entPhysicalSoftwareRev using
  the oid's last node as key

<a id="snmp.mib.generic.mib_entity.EntityQuery.entphysicalserialnum"></a>

#### entphysicalserialnum

```python
async def entphysicalserialnum()
```

Return dict of ENTITY-MIB entPhysicalSerialNum for device.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of entPhysicalSerialNum using
  the oid's last node as key

<a id="snmp.mib.generic.mib_entity.EntityQuery.entphysicalmodelname"></a>

#### entphysicalmodelname

```python
async def entphysicalmodelname()
```

Return dict of ENTITY-MIB entPhysicalModelName for device.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of entPhysicalModelName using
  the oid's last node as key

<a id="snmp.mib.generic.mib_entity.EntityQuery.entphysicalname"></a>

#### entphysicalname

```python
async def entphysicalname()
```

Return dict of ENTITY-MIB entPhysicalName for device.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of entPhysicalName using
  the oid's last node as key

<a id="snmp.mib.generic.mib_entity.EntityQuery.entphysicalhardwarerev"></a>

#### entphysicalhardwarerev

```python
async def entphysicalhardwarerev()
```

Return dict of ENTITY-MIB entPhysicalHardwareRev for device.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of entPhysicalHardwareRev using
  the oid's last node as key

<a id="snmp.mib.generic.mib_entity.EntityQuery.entphysicalfirmwarerev"></a>

#### entphysicalfirmwarerev

```python
async def entphysicalfirmwarerev()
```

Return dict of ENTITY-MIB entPhysicalFirmwareRev for device.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of entPhysicalFirmwareRev using
  the oid's last node as key

<a id="snmp.mib.generic.mib_if"></a>

# snmp.mib.generic.mib\_if

Class interacts with devices supporting IfMIB. (32 Bit Counters).

<a id="snmp.mib.generic.mib_if.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `IfQuery` - Query class object

<a id="snmp.mib.generic.mib_if.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `IfQuery` - Query class object

<a id="snmp.mib.generic.mib_if.IfQuery"></a>

## IfQuery Objects

```python
class IfQuery(Query)
```

Class interacts with devices supporting IfMIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.generic.mib_if.IfQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_if.IfQuery.system"></a>

#### system

```python
async def system()
```

Get system data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_if.IfQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device using Layer 1 OIDs.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_if.IfQuery.iflastchange"></a>

#### iflastchange

```python
async def iflastchange(oidonly=False)
```

Return dict of IFMIB ifLastChange for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifLastChange using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifinoctets"></a>

#### ifinoctets

```python
async def ifinoctets(safe=False, oidonly=False)
```

Return dict of IFMIB ifInOctets for each ifIndex for device.

**Arguments**:

- `safe` - Do a failsafe walk if True
- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifInOctets using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifoutoctets"></a>

#### ifoutoctets

```python
async def ifoutoctets(safe=False, oidonly=False)
```

Return dict of IFMIB ifOutOctets for each ifIndex for device.

**Arguments**:

- `safe` - Do a failsafe walk if True
- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifOutOctets using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifdescr"></a>

#### ifdescr

```python
async def ifdescr(safe=False, oidonly=False)
```

Return dict of IFMIB ifDescr for each ifIndex for device.

**Arguments**:

- `safe` - Do a failsafe walk if True
- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifDescr using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.iftype"></a>

#### iftype

```python
async def iftype(oidonly=False)
```

Return dict of IFMIB ifType for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifType using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifspeed"></a>

#### ifspeed

```python
async def ifspeed(oidonly=False)
```

Return dict of IFMIB ifSpeed for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifSpeed using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifadminstatus"></a>

#### ifadminstatus

```python
async def ifadminstatus(oidonly=False)
```

Return dict of IFMIB ifAdminStatus for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifAdminStatus using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifoperstatus"></a>

#### ifoperstatus

```python
async def ifoperstatus(oidonly=False)
```

Return dict of IFMIB ifOperStatus for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifOperStatus using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifalias"></a>

#### ifalias

```python
async def ifalias(oidonly=False)
```

Return dict of IFMIB ifAlias for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifAlias using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifname"></a>

#### ifname

```python
async def ifname(oidonly=False)
```

Return dict of IFMIB ifName for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifName using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifindex"></a>

#### ifindex

```python
async def ifindex(oidonly=False)
```

Return dict of IFMIB ifindex for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifindex using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifphysaddress"></a>

#### ifphysaddress

```python
async def ifphysaddress(oidonly=False)
```

Return dict of IFMIB ifPhysAddress for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifPhysAddress using the oid's last node as key

<a id="snmp.mib.generic.mib_if.IfQuery.ifinmulticastpkts"></a>

#### ifinmulticastpkts

```python
async def ifinmulticastpkts(oidonly=False)
```

Return dict of IFMIB ifInMulticastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifInMulticastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifoutmulticastpkts"></a>

#### ifoutmulticastpkts

```python
async def ifoutmulticastpkts(oidonly=False)
```

Return dict of IFMIB ifOutMulticastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifOutMulticastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifinbroadcastpkts"></a>

#### ifinbroadcastpkts

```python
async def ifinbroadcastpkts(oidonly=False)
```

Return dict of IFMIB ifInBroadcastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifInBroadcastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifoutbroadcastpkts"></a>

#### ifoutbroadcastpkts

```python
async def ifoutbroadcastpkts(oidonly=False)
```

Return dict of IFMIB ifOutBroadcastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifOutBroadcastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifstackstatus"></a>

#### ifstackstatus

```python
async def ifstackstatus(oidonly=False)
```

Return dict of IFMIB ifStackStatus for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `final` - Dict of ifStackStatus keyed by the ifIndex of the
  ifstacklowerlayer as primary, and ifstackhigherlayer as
  secondary.
  
  Summary:
  According to the official IF-MIB file. ifStackStatus is a
  "table containing information on the relationships
  between the multiple sub-layers of network interfaces.  In
  particular, it contains information on which sub-layers run
  'on top of' which other sub-layers, where each sub-layer
  corresponds to a conceptual row in the ifTable.  For
  example, when the sub-layer with ifIndex value x runs over
  the sub-layer with ifIndex value y, then this table
  contains:
  
  ifStackStatus.x.y=active
  
  For each ifIndex value, I, which identifies an active
  interface, there are always at least two instantiated rows
  in this table associated with I.  For one of these rows, I
  is the value of ifStackHigherLayer; for the other, I is the
  value of ifStackLowerLayer.  (If I is not involved in
  multiplexing, then these are the only two rows associated
  with I.)
  
  For example, two rows exist even for an interface which has
  no others stacked on top or below it:
  
  ifStackStatus.0.x=active
  ifStackStatus.x.0=active"
  
  In the case of Juniper equipment, VLAN information is only
  visible on subinterfaces of the main interface. For example
  interface ge-0/0/0 won't have VLAN information assigned to it
  directly.
  
  When a VLAN is assigned to this interface, a subinterface
  ge-0/0/0.0 is automatically created with a non-Ethernet ifType.
  VLAN related OIDs are only maintained for this new subinterface
  only. This makes determining an interface's VLAN based on
  Ethernet ifType more difficult. ifStackStatus maps the ifIndex of
  the primary interface (ge-0/0/0) to the ifIndex of the secondary
  interface (ge-0/0/0.0) which manages higher level protocols and
  data structures such as VLANs and LLDP.
  
  The primary interface is referred to as the
  ifStackLowerLayer and the secondary subinterface is referred to
  as the ifStackHigherLayer.

<a id="snmp.mib.generic.mib_if.IfQuery.ifInUcastPkts"></a>

#### ifInUcastPkts

```python
async def ifInUcastPkts(oidonly=False)
```

Get inbound unicast packet counters for each interface.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True

**Returns**:

- `dict` - Mapping of ifIndex → packet count.

<a id="snmp.mib.generic.mib_if.IfQuery.ifOutUcastPkts"></a>

#### ifOutUcastPkts

```python
async def ifOutUcastPkts(oidonly=False)
```

Get Outbound unicast packet counters for each interface.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True

**Returns**:

- `data_dict` - Dict of ifOutUcastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifInErrors"></a>

#### ifInErrors

```python
async def ifInErrors(oidonly=False)
```

Return dict of IFMIB ifInErrors for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True

**Returns**:

- `data_dict` - Dict of ifInErrors. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifOutErrors"></a>

#### ifOutErrors

```python
async def ifOutErrors(oidonly=False)
```

Return dict of IFMIB ifOutErrors for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True

**Returns**:

- `data_dict` - Dict of ifOutErrors. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifInDiscards"></a>

#### ifInDiscards

```python
async def ifInDiscards(oidonly=False)
```

Return dict of IFMIB ifInDiscards for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True

**Returns**:

- `data_dict` - Dict of ifInDiscards. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifOutDiscards"></a>

#### ifOutDiscards

```python
async def ifOutDiscards(oidonly=False)
```

Return dict of IFMIB ifOutDiscards for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True

**Returns**:

- `data_dict` - Dict of ifOutDiscards. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifInNUcastPkts"></a>

#### ifInNUcastPkts

```python
async def ifInNUcastPkts(oidonly=False)
```

Return dict of IFMIB ifInNUcastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True

**Returns**:

- `data_dict` - Dict of ifInNUcastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if.IfQuery.ifOutNUcastPkts"></a>

#### ifOutNUcastPkts

```python
async def ifOutNUcastPkts(oidonly=False)
```

Return dict of IFMIB ifOutNUcastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True

**Returns**:

- `data_dict` - Dict of ifOutNUcastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_etherlike"></a>

# snmp.mib.generic.mib\_etherlike

Module for ETHERLIKE-MIB.

<a id="snmp.mib.generic.mib_etherlike.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `EtherlikeQuery` - Query class object

<a id="snmp.mib.generic.mib_etherlike.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `EtherlikeQuery` - Query class object

<a id="snmp.mib.generic.mib_etherlike.EtherlikeQuery"></a>

## EtherlikeQuery Objects

```python
class EtherlikeQuery(Query)
```

Class interacts with ETHERLIKE-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.generic.mib_etherlike.EtherlikeQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_etherlike.EtherlikeQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_etherlike.EtherlikeQuery.dot3statsduplexstatus"></a>

#### dot3statsduplexstatus

```python
async def dot3statsduplexstatus(oidonly=False)
```

Return dict of ETHERLIKE-MIB dot3StatsDuplexStatus for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of dot3StatsDuplexStatus using ifIndex as key

<a id="snmp.mib.generic.mib_ip"></a>

# snmp.mib.generic.mib\_ip

Class interacts with devices supporting IP-MIB.

<a id="snmp.mib.generic.mib_ip.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `IpQuery` - Query class object

<a id="snmp.mib.generic.mib_ip.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `IpQuery` - Query class object

<a id="snmp.mib.generic.mib_ip.IpQuery"></a>

## IpQuery Objects

```python
class IpQuery(Query)
```

Class interacts with devices supporting IP-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer3` - Returns all needed layer 3 MIB information from the device.
  Keyed by OID's MIB name (primary key), IP address (secondary key).

<a id="snmp.mib.generic.mib_ip.IpQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_ip.IpQuery.supported"></a>

#### supported

```python
async def supported()
```

Return device's support for the MIB.

**Arguments**:

  None
  

**Returns**:

- `validity` - True if supported

<a id="snmp.mib.generic.mib_ip.IpQuery.layer3"></a>

#### layer3

```python
async def layer3()
```

Get layer 3 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_ip.IpQuery.ipnettomediatable"></a>

#### ipnettomediatable

```python
async def ipnettomediatable(oidonly=False)
```

Return dict of ipNetToMediaTable, the device's ARP table.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of MAC addresses keyed by IPv4 address

<a id="snmp.mib.generic.mib_ip.IpQuery.ipnettophysicalphysaddress"></a>

#### ipnettophysicalphysaddress

```python
async def ipnettophysicalphysaddress(oidonly=False)
```

Return dict of the device's ipNetToPhysicalPhysAddress ARP table.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of MAC addresses keyed by IPv6 Address

<a id="snmp.mib.generic.mib_bridge"></a>

# snmp.mib.generic.mib\_bridge

Class interacts with devices supporting BRIDGE-MIB.

<a id="snmp.mib.generic.mib_bridge.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `BridgeQuery` - Query class object

<a id="snmp.mib.generic.mib_bridge.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py

**Returns**:

- `BridgeQuery` - Query class object

<a id="snmp.mib.generic.mib_bridge.BridgeQuery"></a>

## BridgeQuery Objects

```python
class BridgeQuery(Query)
```

Class interacts with devices supporting BRIDGE-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.generic.mib_bridge.BridgeQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_bridge.BridgeQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_bridge.BridgeQuery.dot1dbaseport_2_ifindex"></a>

#### dot1dbaseport\_2\_ifindex

```python
async def dot1dbaseport_2_ifindex(context_names=None)
```

Return dict of BRIDGE-MIB dot1dBasePortIfIndex data.

**Arguments**:

- `context_names` - List of context names
  

**Returns**:

- `data_dict` - Dict of dot1dBasePortIfIndex with dot1dBasePort as key.

<a id="snmp.mib.generic.mib_snmpv2"></a>

# snmp.mib.generic.mib\_snmpv2

Class interacts with devices supporting SNMPv2-MIB.

<a id="snmp.mib.generic.mib_snmpv2.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `Snmpv2Query` - Query class object

<a id="snmp.mib.generic.mib_snmpv2.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `Snmpv2Query` - Query class object

<a id="snmp.mib.generic.mib_snmpv2.Snmpv2Query"></a>

## Snmpv2Query Objects

```python
class Snmpv2Query(Query)
```

Class interacts with devices supporting SNMPv2-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `system` - Returns all relevant system information from the device.
  In some cases a system will have multiple subsystems that are
  covered by an OID. (eg. module / circuit board serial numbers).
  It will therefore be impossible to have a consistent key format
  for data values returned. Data returned by this method will
  therefore be keyed by :
  1) MIB name (primary key)
  2) OID name in the MIB, (secondary key),
  3) Leaf value, or zero (0) if there are no leaves.

<a id="snmp.mib.generic.mib_snmpv2.Snmpv2Query.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_snmpv2.Snmpv2Query.system"></a>

#### system

```python
async def system()
```

Get system data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_essswitch"></a>

# snmp.mib.generic.mib\_essswitch

Module for MIB-ESSWITCH.

<a id="snmp.mib.generic.mib_essswitch.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `EssSwitchQuery` - Query class object

<a id="snmp.mib.generic.mib_essswitch.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `EssSwitchQuery` - Query class object

<a id="snmp.mib.generic.mib_essswitch.EssSwitchQuery"></a>

## EssSwitchQuery Objects

```python
class EssSwitchQuery(Query)
```

Class interacts with MIB-ESSWITCH.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.generic.mib_essswitch.EssSwitchQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_essswitch.EssSwitchQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_essswitch.EssSwitchQuery.swportduplexstatus"></a>

#### swportduplexstatus

```python
async def swportduplexstatus(oidonly=False)
```

Return dict of MIB-ESSWITCH swPortDuplexStatus for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of swPortDuplexStatus using ifIndex as key

<a id="snmp.mib.generic.mib_lldp"></a>

# snmp.mib.generic.mib\_lldp

Module for LLDP-MIB.

<a id="snmp.mib.generic.mib_lldp.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `LldpQuery` - Query class object

<a id="snmp.mib.generic.mib_lldp.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `LldpQuery` - Query class object

<a id="snmp.mib.generic.mib_lldp.LldpQuery"></a>

## LldpQuery Objects

```python
class LldpQuery(Query)
```

Class interacts with LLDP-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.generic.mib_lldp.LldpQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_lldp.LldpQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_lldp.LldpQuery.lldpremsysname"></a>

#### lldpremsysname

```python
async def lldpremsysname(oidonly=False)
```

Return dict of LLDP-MIB lldpRemSysName for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of lldpRemSysName using ifIndex as key

<a id="snmp.mib.generic.mib_lldp.LldpQuery.lldpremsyscapenabled"></a>

#### lldpremsyscapenabled

```python
async def lldpremsyscapenabled(oidonly=False)
```

Return dict of LLDP-MIB lldpRemSysCapEnabled for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of lldpRemSysCapEnabled using ifIndex as key

<a id="snmp.mib.generic.mib_lldp.LldpQuery.lldpremsysdesc"></a>

#### lldpremsysdesc

```python
async def lldpremsysdesc(oidonly=False)
```

Return dict of LLDP-MIB lldpRemSysDesc for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of lldpRemSysDesc using ifIndex as key

<a id="snmp.mib.generic.mib_lldp.LldpQuery.lldpremportdesc"></a>

#### lldpremportdesc

```python
async def lldpremportdesc(oidonly=False)
```

Return dict of LLDP-MIB lldpRemPortDesc for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of lldpRemPortDesc using ifIndex as key

<a id="snmp.mib.generic.mib_lldp.LldpQuery.lldplocportdesc"></a>

#### lldplocportdesc

```python
async def lldplocportdesc(oidonly=False)
```

Return dict of LLDP-MIB lldpLocPortDesc for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of lldpLocPortDesc using ifIndex as key

<a id="snmp.mib.generic.mib_ipv6"></a>

# snmp.mib.generic.mib\_ipv6

Class interacts with CISCO-IETF-IP-MIB.

<a id="snmp.mib.generic.mib_ipv6.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `Ipv6Query` - Query class object

<a id="snmp.mib.generic.mib_ipv6.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `Ipv6Query` - Query class object

<a id="snmp.mib.generic.mib_ipv6.Ipv6Query"></a>

## Ipv6Query Objects

```python
class Ipv6Query(Query)
```

Class interacts with CISCO-IETF-IP-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer3` - Returns all needed layer 3 MIB information from the device.
  Keyed by OID's MIB name (primary key), IP address (secondary key).

<a id="snmp.mib.generic.mib_ipv6.Ipv6Query.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_ipv6.Ipv6Query.layer3"></a>

#### layer3

```python
async def layer3()
```

Get layer 3 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_ipv6.Ipv6Query.ipv6nettomediaphysaddress"></a>

#### ipv6nettomediaphysaddress

```python
async def ipv6nettomediaphysaddress()
```

Return dict of the device's ipv6NetToMediaPhysAddress ARP table.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of MAC addresses keyed by IPv6 Address

<a id="snmp.mib.generic.mib_if_64"></a>

# snmp.mib.generic.mib\_if\_64

Class interacts with devices supporting IfMIB. (64 Bit Counters).

<a id="snmp.mib.generic.mib_if_64.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `If64Query` - Query class object

<a id="snmp.mib.generic.mib_if_64.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `If64Query` - Query class object

<a id="snmp.mib.generic.mib_if_64.If64Query"></a>

## If64Query Objects

```python
class If64Query(Query)
```

Class interacts with devices supporting IfMIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.generic.mib_if_64.If64Query.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_if_64.If64Query.system"></a>

#### system

```python
async def system()
```

Get system data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_if_64.If64Query.layer1"></a>

#### layer1

```python
def layer1()
```

Get layer 1 data from device using Layer 1 OIDs.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhighspeed"></a>

#### ifhighspeed

```python
def ifhighspeed(oidonly=False)
```

Return dict of IFMIB ifHighSpeed for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHighSpeed using the oid's last node as key

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhcinucastpkts"></a>

#### ifhcinucastpkts

```python
def ifhcinucastpkts(oidonly=False)
```

Return dict of IFMIB ifHCInUcastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHCInUcastPkts using the oid's last node as key

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhcoutucastpkts"></a>

#### ifhcoutucastpkts

```python
def ifhcoutucastpkts(oidonly=False)
```

Return dict of IFMIB ifHCOutUcastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHCOutUcastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhcinmulticastpkts"></a>

#### ifhcinmulticastpkts

```python
def ifhcinmulticastpkts(oidonly=False)
```

Return dict of IFMIB ifHCInMulticastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHCInMulticastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhcoutmulticastpkts"></a>

#### ifhcoutmulticastpkts

```python
def ifhcoutmulticastpkts(oidonly=False)
```

Return dict of IFMIB ifHCOutMulticastPkts.

Keyed by ifIndex for the device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHCOutMulticastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhcinbroadcastpkts"></a>

#### ifhcinbroadcastpkts

```python
def ifhcinbroadcastpkts(oidonly=False)
```

Return dict of IFMIB ifHCInBroadcastPkts for each ifIndex for device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHCInBroadcastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhcoutbroadcastpkts"></a>

#### ifhcoutbroadcastpkts

```python
def ifhcoutbroadcastpkts(oidonly=False)
```

Return dict of IFMIB ifHCOutBroadcastPkts.

Keyed by ifIndex for the device.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHCOutBroadcastPkts. Key = OID's last node.

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhcinoctets"></a>

#### ifhcinoctets

```python
def ifhcinoctets(safe=False, oidonly=False)
```

Return dict of IFMIB ifHCInOctets for each ifIndex for device.

**Arguments**:

- `safe` - Do a failsafe walk if True
- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHCInOctets. Key = OID's last node.

<a id="snmp.mib.generic.mib_if_64.If64Query.ifhcoutoctets"></a>

#### ifhcoutoctets

```python
def ifhcoutoctets(safe=False, oidonly=False)
```

Return dict of IFMIB ifHCOutOctets for each ifIndex for device.

**Arguments**:

- `safe` - Do a failsafe walk if True
- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of ifHCOutOctets. Key = OID's last node.

<a id="snmp.mib.generic"></a>

# snmp.mib.generic

Define the switchmap.poller.snmp.mib.generic package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_qbridge"></a>

# snmp.mib.generic.mib\_qbridge

Module for Q-BRIDGE-MIB.

<a id="snmp.mib.generic.mib_qbridge.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `QbridgeQuery` - Query class object

<a id="snmp.mib.generic.mib_qbridge.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `QbridgeQuery` - Query class object

<a id="snmp.mib.generic.mib_qbridge.QbridgeQuery"></a>

## QbridgeQuery Objects

```python
class QbridgeQuery(Query)
```

Class interacts with Q-BRIDGE-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.generic.mib_qbridge.QbridgeQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.generic.mib_qbridge.QbridgeQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_qbridge.QbridgeQuery.layer2"></a>

#### layer2

```python
async def layer2()
```

Get layer 2 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.generic.mib_qbridge.QbridgeQuery.dot1qpvid"></a>

#### dot1qpvid

```python
async def dot1qpvid(oidonly=False)
```

Return dict of Q-BRIDGE-MIB dot1qPvid per port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of dot1qPvid using ifIndex as key

<a id="snmp.mib.generic.mib_qbridge.QbridgeQuery.dot1qvlanstaticname"></a>

#### dot1qvlanstaticname

```python
async def dot1qvlanstaticname(oidonly=False)
```

Return dict of Q-BRIDGE-MIB dot1qVlanStaticName per port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of dot1qVlanStaticName using ifIndex as key

<a id="snmp.mib.cisco.mib_ciscovlaniftablerelationship"></a>

# snmp.mib.cisco.mib\_ciscovlaniftablerelationship

Module for CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB.

<a id="snmp.mib.cisco.mib_ciscovlaniftablerelationship.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `CiscoVlanIftableRelationshipQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscovlaniftablerelationship.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `CiscoVlanIftableRelationshipQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscovlaniftablerelationship.CiscoVlanIftableRelationshipQuery"></a>

## CiscoVlanIftableRelationshipQuery Objects

```python
class CiscoVlanIftableRelationshipQuery(Query)
```

Class interacts with CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.cisco.mib_ciscovlaniftablerelationship.CiscoVlanIftableRelationshipQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.cisco.mib_ciscovlaniftablerelationship.CiscoVlanIftableRelationshipQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.cisco.mib_ciscovlaniftablerelationship.CiscoVlanIftableRelationshipQuery.cviroutedvlanifindex"></a>

#### cviroutedvlanifindex

```python
async def cviroutedvlanifindex(oidonly=False)
```

Return dictionary of CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB.

Keyed by OID cviRoutedVlanIfIndex for each VLAN.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of cviRoutedVlanIfIndex using the oid's last node
  as key

<a id="snmp.mib.cisco.mib_ciscovlanmembership"></a>

# snmp.mib.cisco.mib\_ciscovlanmembership

Module for CISCO-VLAN-MEMBERSHIP-MIB.

<a id="snmp.mib.cisco.mib_ciscovlanmembership.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `CiscoVlanMembershipQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscovlanmembership.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `CiscoVlanMembershipQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscovlanmembership.CiscoVlanMembershipQuery"></a>

## CiscoVlanMembershipQuery Objects

```python
class CiscoVlanMembershipQuery(Query)
```

Class interacts with CISCO-VLAN-MEMBERSHIP-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.cisco.mib_ciscovlanmembership.CiscoVlanMembershipQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.cisco.mib_ciscovlanmembership.CiscoVlanMembershipQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.cisco.mib_ciscovlanmembership.CiscoVlanMembershipQuery.vmvlan"></a>

#### vmvlan

```python
async def vmvlan(oidonly=False)
```

Return dict of CISCO-VLAN-MEMBERSHIP-MIB vmVlan for each VLAN.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vmVlan using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovlanmembership.CiscoVlanMembershipQuery.vmportstatus"></a>

#### vmportstatus

```python
async def vmportstatus(oidonly=False)
```

Return dict of CISCO-VLAN-MEMBERSHIP-MIB vmPortStatus for each VLAN.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vmPortStatus using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovtp"></a>

# snmp.mib.cisco.mib\_ciscovtp

Class interacts with CISCO-VTP-MIB.

<a id="snmp.mib.cisco.mib_ciscovtp.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `CiscoVtpQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscovtp.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `CiscoVtpQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery"></a>

## CiscoVtpQuery Objects

```python
class CiscoVtpQuery(Query)
```

Class interacts with CISCO-VTP-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)
  
- `layer2` - Returns all needed layer 2 MIB information from the device.
  Keyed by OID's MIB name (primary key), VLAN number (secondary key)

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.layer2"></a>

#### layer2

```python
async def layer2()
```

Get layer 2 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.vlantrunkportencapsulationtype"></a>

#### vlantrunkportencapsulationtype

```python
async def vlantrunkportencapsulationtype(oidonly=False)
```

Return CISCO-VTP-MIB vlanTrunkPortEncapsulationType per ifIndex.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vlanTrunkPortEncapsulationType
  using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.vlantrunkportnativevlan"></a>

#### vlantrunkportnativevlan

```python
async def vlantrunkportnativevlan(oidonly=False)
```

Return dict of CISCO-VTP-MIB vlanTrunkPortNativeVlan per ifIndex.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vlanTrunkPortNativeVlan
  using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.vlantrunkportdynamicstatus"></a>

#### vlantrunkportdynamicstatus

```python
async def vlantrunkportdynamicstatus(oidonly=False)
```

Return dict of CISCO-VTP-MIB vlanTrunkPortDynamicStatus per ifIndex.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vlanTrunkPortDynamicStatus
  using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.vlantrunkportdynamicstate"></a>

#### vlantrunkportdynamicstate

```python
async def vlantrunkportdynamicstate(oidonly=False)
```

Return dict of CISCO-VTP-MIB vlanTrunkPortDynamicState per ifIndex.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vlanTrunkPortDynamicState
  using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.vtpvlanname"></a>

#### vtpvlanname

```python
async def vtpvlanname(oidonly=False)
```

Return dict of CISCO-VTP-MIB vtpVlanName for each VLAN.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vtpVlanName using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.vtpvlantype"></a>

#### vtpvlantype

```python
async def vtpvlantype(oidonly=False)
```

Return dict of CISCO-VTP-MIB vtpVlanType for each VLAN.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vtpVlanType using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.vtpvlanstate"></a>

#### vtpvlanstate

```python
async def vtpvlanstate(oidonly=False)
```

Return dict of CISCO-VTP-MIB vtpVlanState for each VLAN.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vtpVlanState using the oid's last node as key

<a id="snmp.mib.cisco.mib_ciscovtp.CiscoVtpQuery.vlantrunkportvlansenabled"></a>

#### vlantrunkportvlansenabled

```python
async def vlantrunkportvlansenabled(oidonly=False)
```

Return CISCO-VTP-MIB vlanTrunkPortVlansEnabled data per ifIndex.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of vlanTrunkPortVlansEnabled keyed by ifIndex
  with values being lists of enabled VLAN tags.

<a id="snmp.mib.cisco.mib_ciscoprocess"></a>

# snmp.mib.cisco.mib\_ciscoprocess

Class interacts with devices supporting CISCO-PROCESS-MIB.

<a id="snmp.mib.cisco.mib_ciscoprocess.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `type` - CiscoProcessQuery class

<a id="snmp.mib.cisco.mib_ciscoprocess.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP interact class object from snmp_manager.py
  

**Returns**:

- `CiscoProcessQuery` - Initialized query instance

<a id="snmp.mib.cisco.mib_ciscoprocess.CiscoProcessQuery"></a>

## CiscoProcessQuery Objects

```python
class CiscoProcessQuery(Query)
```

Class interacts with devices supporting CISCO-PROCESS-MIB.

<a id="snmp.mib.cisco.mib_ciscoprocess.CiscoProcessQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.cisco.mib_ciscoprocess.CiscoProcessQuery.system"></a>

#### system

```python
async def system()
```

Get system resource data from Cisco devices.

<a id="snmp.mib.cisco.mib_ciscoprocess.CiscoProcessQuery.cpmcputotal5minrev"></a>

#### cpmcputotal5minrev

```python
async def cpmcputotal5minrev(oidonly=False)
```

Return dict of CISCO-PROCESS-MIB cpmCPUTotal5minRev for device.

<a id="snmp.mib.cisco.mib_ciscoprocess.CiscoProcessQuery.memorypoolused"></a>

#### memorypoolused

```python
async def memorypoolused(oidonly=False)
```

Get total used memory from CISCO-MEMORY-POOL-MIB.

**Arguments**:

- `oidonly` _bool_ - If True, return the OID string instead of querying.
  

**Returns**:

  int | str | None: Sum of used memory in bytes,
  OID string if oidonly=True,
  or None on error.

<a id="snmp.mib.cisco.mib_ciscoprocess.CiscoProcessQuery.memorypoolfree"></a>

#### memorypoolfree

```python
async def memorypoolfree(oidonly=False)
```

Get total free memory from CISCO-MEMORY-POOL-MIB.

**Arguments**:

- `oidonly` _bool_ - If True, return the OID string instead of querying.
  

**Returns**:

  int | str | None: Sum of free memory in bytes,
  OID string if oidonly=True,
  or None on error.

<a id="snmp.mib.cisco.mib_ciscostack"></a>

# snmp.mib.cisco.mib\_ciscostack

Module for CISCO-STACK-MIB.

<a id="snmp.mib.cisco.mib_ciscostack.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `CiscoStackQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscostack.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `CiscoStackQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscostack.CiscoStackQuery"></a>

## CiscoStackQuery Objects

```python
class CiscoStackQuery(Query)
```

Class interacts with CISCO-STACK-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.cisco.mib_ciscostack.CiscoStackQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.cisco.mib_ciscostack.CiscoStackQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.cisco.mib_ciscostack.CiscoStackQuery.portduplex"></a>

#### portduplex

```python
async def portduplex(oidonly=False)
```

Return dict of CISCO-STACK-MIB portDuplex for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of portDuplex using ifIndex as key

<a id="snmp.mib.cisco.mib_ciscoietfip"></a>

# snmp.mib.cisco.mib\_ciscoietfip

Class interacts with CISCO-IETF-IP-MIB.

<a id="snmp.mib.cisco.mib_ciscoietfip.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `CiscoIetfIpQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscoietfip.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `CiscoIetfIpQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscoietfip.CiscoIetfIpQuery"></a>

## CiscoIetfIpQuery Objects

```python
class CiscoIetfIpQuery(Query)
```

Class interacts with CISCO-IETF-IP-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer3` - Returns all needed layer 3 MIB information from the device.
  Keyed by OID's MIB name (primary key), IP address (secondary key).

<a id="snmp.mib.cisco.mib_ciscoietfip.CiscoIetfIpQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.cisco.mib_ciscoietfip.CiscoIetfIpQuery.layer3"></a>

#### layer3

```python
async def layer3()
```

Get layer 3 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.cisco.mib_ciscoietfip.CiscoIetfIpQuery.cinetnettomediaphysaddress"></a>

#### cinetnettomediaphysaddress

```python
async def cinetnettomediaphysaddress()
```

Return dict of the device's ARP table.

**Arguments**:

  None
  

**Returns**:

- `data_dict` - Dict of MAC addresses keyed by IPv6 Address

<a id="snmp.mib.cisco.mib_ciscocdp"></a>

# snmp.mib.cisco.mib\_ciscocdp

Module for CISCO-CDP-MIB.

<a id="snmp.mib.cisco.mib_ciscocdp.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `CiscoCdpQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscocdp.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `CiscoCdpQuery` - Query class object

<a id="snmp.mib.cisco.mib_ciscocdp.CiscoCdpQuery"></a>

## CiscoCdpQuery Objects

```python
class CiscoCdpQuery(Query)
```

Class interacts with CISCO-CDP-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.cisco.mib_ciscocdp.CiscoCdpQuery.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.cisco.mib_ciscocdp.CiscoCdpQuery.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.cisco.mib_ciscocdp.CiscoCdpQuery.cdpcachedeviceid"></a>

#### cdpcachedeviceid

```python
async def cdpcachedeviceid(oidonly=False)
```

Return dict of CISCO-CDP-MIB cdpCacheDeviceId for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of cdpCacheDeviceId using ifIndex as key

<a id="snmp.mib.cisco.mib_ciscocdp.CiscoCdpQuery.cdpcacheplatform"></a>

#### cdpcacheplatform

```python
async def cdpcacheplatform(oidonly=False)
```

Return dict of CISCO-CDP-MIB cdpCachePlatform for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of cdpCachePlatform using ifIndex as key

<a id="snmp.mib.cisco.mib_ciscocdp.CiscoCdpQuery.cdpcachedeviceport"></a>

#### cdpcachedeviceport

```python
async def cdpcachedeviceport(oidonly=False)
```

Return dict of CISCO-CDP-MIB cdpCacheDevicePort for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of cdpCacheDevicePort using ifIndex as key

<a id="snmp.mib.cisco"></a>

# snmp.mib.cisco

Cisco class imports.

<a id="snmp.mib.cisco.mib_ciscoc2900"></a>

# snmp.mib.cisco.mib\_ciscoc2900

Module for CISCO-C2900-MIB.

<a id="snmp.mib.cisco.mib_ciscoc2900.get_query"></a>

#### get\_query

```python
def get_query()
```

Return this module's Query class.

**Arguments**:

  None
  

**Returns**:

- `CiscoC2900Query` - Query class object

<a id="snmp.mib.cisco.mib_ciscoc2900.init_query"></a>

#### init\_query

```python
def init_query(snmp_object)
```

Return initialize and return this module's Query class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

- `CiscoC2900Query` - Query class object

<a id="snmp.mib.cisco.mib_ciscoc2900.CiscoC2900Query"></a>

## CiscoC2900Query Objects

```python
class CiscoC2900Query(Query)
```

Class interacts with CISCO-C2900-MIB.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.mib.cisco.mib_ciscoc2900.CiscoC2900Query.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.mib.cisco.mib_ciscoc2900.CiscoC2900Query.layer1"></a>

#### layer1

```python
async def layer1()
```

Get layer 1 data from device.

**Arguments**:

  None
  

**Returns**:

- `final` - Final results

<a id="snmp.mib.cisco.mib_ciscoc2900.CiscoC2900Query.c2900portlinkbeatstatus"></a>

#### c2900portlinkbeatstatus

```python
async def c2900portlinkbeatstatus(oidonly=False)
```

Return dict of CISCO-C2900-MIB c2900PortLinkbeatStatus per port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of c2900PortLinkbeatStatus using ifIndex as key

<a id="snmp.mib.cisco.mib_ciscoc2900.CiscoC2900Query.c2900portduplexstatus"></a>

#### c2900portduplexstatus

```python
async def c2900portduplexstatus(oidonly=False)
```

Return dict of CISCO-C2900-MIB c2900PortDuplexStatus for each port.

**Arguments**:

- `oidonly` - Return OID's value, not results, if True
  

**Returns**:

- `data_dict` - Dict of c2900PortDuplexStatus using ifIndex as key

<a id="snmp.mib"></a>

# snmp.mib

Define the switchmap.poller.snmp.mib package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="snmp.poller"></a>

# snmp.poller

Asynchronous SNMP Poller module for switchmap-ng.

<a id="snmp.poller.Poll"></a>

## Poll Objects

```python
class Poll()
```

Asynchronous SNMP poller for switchmap-ng that gathers network data.

This class manages SNMP credential validation and data querying for
network devices using asynchronous operations for improved
performance and scalability.

**Arguments**:

- `hostname` _str_ - The hostname or IP address of the device to poll
  

**Methods**:

- `initialize_snmp()` - Validates SNMP credentials and
  initializes SNMP interaction
- `query()` - Queries the device for topology data asynchronously

<a id="snmp.poller.Poll.__init__"></a>

#### \_\_init\_\_

```python
def __init__(hostname)
```

Initialize the class.

**Arguments**:

- `hostname` - Hostname to poll
  

**Returns**:

  None

<a id="snmp.poller.Poll.initialize_snmp"></a>

#### initialize\_snmp

```python
async def initialize_snmp()
```

Initialize SNMP connection asynchronously.

**Returns**:

- `bool` - True if successful, False otherwise

<a id="snmp.poller.Poll.close"></a>

#### close

```python
def close()
```

Clean up SNMP resources.

This method should be called when the Poll object is no longer needed
to ensure proper cleanup of SNMP engine resources.

**Arguments**:

  None
  

**Returns**:

  None

<a id="snmp.poller.Poll.query"></a>

#### query

```python
async def query()
```

Query all remote hosts for data.

**Arguments**:

  None
  

**Returns**:

- `dict` - Polled data or None if failed

<a id="snmp.snmp_manager"></a>

# snmp.snmp\_manager

Async SNMP manager class.

<a id="snmp.snmp_manager.Validate"></a>

## Validate Objects

```python
class Validate()
```

Class to validate SNMP data asynchronously.

<a id="snmp.snmp_manager.Validate.__init__"></a>

#### \_\_init\_\_

```python
def __init__(options)
```

Initialize the Validate class.

**Arguments**:

- `options` - POLLING_OPTIONS object containing SNMP configuration.
  

**Returns**:

  None

<a id="snmp.snmp_manager.Validate.credentials"></a>

#### credentials

```python
async def credentials()
```

Determine valid SNMP credentials for a host.

**Arguments**:

  None
  

**Returns**:

- `authentication` - SNMP authorization object containing valid
  credentials, or None if no valid credentials found

<a id="snmp.snmp_manager.Validate.validation"></a>

#### validation

```python
async def validation(group=None)
```

Determine valid SNMP authorization for a host.

**Arguments**:

- `group` - String containing SNMP group name to try, or None to try all
  groups
  

**Returns**:

- `result` - SNMP authorization object if valid credentials found,
  None otherwise

<a id="snmp.snmp_manager.Interact"></a>

## Interact Objects

```python
class Interact()
```

Class Gets SNMP data.

<a id="snmp.snmp_manager.Interact.__init__"></a>

#### \_\_init\_\_

```python
def __init__(_poll)
```

Initialize the Interact class.

**Arguments**:

- `_poll` - POLL object containing SNMP configuration and target info
  

**Returns**:

  None

<a id="snmp.snmp_manager.Interact.enterprise_number"></a>

#### enterprise\_number

```python
async def enterprise_number()
```

Get SNMP enterprise number for the device.

**Arguments**:

  None
  

**Returns**:

- `int` - SNMP enterprise number identifying the device vendor

<a id="snmp.snmp_manager.Interact.hostname"></a>

#### hostname

```python
def hostname()
```

Get SNMP hostname for the interaction.

**Arguments**:

  None
  

**Returns**:

- `str` - Hostname of the target device

<a id="snmp.snmp_manager.Interact.close"></a>

#### close

```python
def close()
```

Clean up SNMP engine resources.

This method should be called when the Interact object is no longer
needed to ensure proper cleanup of SNMP engine resources.

**Arguments**:

  None
  

**Returns**:

  None

<a id="snmp.snmp_manager.Interact.contactable"></a>

#### contactable

```python
async def contactable()
```

Check if device is reachable via SNMP.

**Arguments**:

  None
  

**Returns**:

- `bool` - True if device responds to SNMP queries, False otherwise

<a id="snmp.snmp_manager.Interact.sysobjectid"></a>

#### sysobjectid

```python
async def sysobjectid(check_reachability=False)
```

Get the sysObjectID of the device.

**Arguments**:

- `check_reachability` - Boolean indicating whether to test connectivity.
  Some session errors are ignored to return null result.
  

**Returns**:

- `str` - sysObjectID value as string, or None if not available

<a id="snmp.snmp_manager.Interact.oid_exists"></a>

#### oid\_exists

```python
async def oid_exists(oid_to_get, context_name="")
```

Determine if an OID exists on the device.

**Arguments**:

- `oid_to_get` - String containing OID to check
- `context_name` - String containing SNMPv3 context name.
  Default is empty string.
  

**Returns**:

- `bool` - True if OID exists, False otherwise

<a id="snmp.snmp_manager.Interact.get"></a>

#### get

```python
async def get(oid_to_get,
              check_reachability=False,
              check_existence=False,
              normalized=False,
              context_name="")
```

Do an SNMPget.

**Arguments**:

- `oid_to_get` - OID to get
- `check_reachability` - Set if testing for connectivity. Some session
  errors are ignored so that a null result is returned
- `check_existence` - Set if checking for the existence of the OID
- `normalized` - If True, then return results as a dict keyed by
  only the last node of an OID, otherwise return results
  keyed by the entire OID string. Normalization is useful
  when trying to create multidimensional dicts where the
  primary key is a universal value such as IF-MIB::ifIndex
  or BRIDGE-MIB::dot1dBasePort
- `context_name` - Set the contextName used for SNMPv3 messages.
  The default contextName is the empty string "".  Overrides the
  defContext token in the snmp.conf file.
  

**Returns**:

- `result` - Dictionary of {OID: value} pairs

<a id="snmp.snmp_manager.Interact.walk"></a>

#### walk

```python
async def walk(oid_to_get,
               normalized=False,
               check_reachability=False,
               check_existence=False,
               context_name="",
               safe=False)
```

Do an async SNMPwalk.

**Arguments**:

- `oid_to_get` - OID to walk
- `normalized` - If True, then return results as a dict keyed by
  only the last node of an OID, otherwise return results
  keyed by the entire OID string. Normalization is useful
  when trying to create multidimensional dicts where the
  primary key is a universal value such as IF-MIB::ifIndex
  or BRIDGE-MIB::dot1dBasePort
  check_reachability:
  Set if testing for connectivity. Some session
  errors are ignored so that a null result is returned
  check_existence:
  Set if checking for the existence of the OID
- `context_name` - Set the contextName used for SNMPv3 messages.
  The default contextName is the empty string "".  Overrides the
  defContext token in the snmp.conf file.
- `safe` - Safe query if true. If there is an exception, then return                 blank values.
  

**Returns**:

- `result` - Dictionary of {OID: value} pairs

<a id="snmp.snmp_manager.Interact.swalk"></a>

#### swalk

```python
async def swalk(oid_to_get, normalized=False, context_name="")
```

Perform a safe async SNMPwalk that handles errors gracefully.

**Arguments**:

- `oid_to_get` - OID to get
- `normalized` - If True, then return results as a dict keyed by
  only the last node of an OID, otherwise return results
  keyed by the entire OID string. Normalization is useful
  when trying to create multidimensional dicts where the
  primary key is a universal value such as IF-MIB::ifIndex
  or BRIDGE-MIB::dot1dBasePort
- `context_name` - Set the contextName used for SNMPv3 messages.
  The default contextName is the empty string "".  Overrides the
  defContext token in the snmp.conf file.
  

**Returns**:

- `dict` - Results of SNMP walk as OID-value pairs

<a id="snmp.snmp_manager.Interact.query"></a>

#### query

```python
async def query(oid_to_get,
                get=False,
                check_reachability=False,
                check_existence=False,
                normalized=False,
                context_name="",
                safe=False)
```

Do an SNMP query.

**Arguments**:

- `oid_to_get` - OID to walk
- `get` - Flag determining whether to do a GET or WALK
- `check_reachability` - Set if testing for connectivity. Some session
  errors are ignored so that a null result is returned
- `check_existence` - Set if checking for the existence of the OID
- `normalized` - If True, then return results as a dict keyed by
  only the last node of an OID, otherwise return results
  keyed by the entire OID string. Normalization is useful
  when trying to create multidimensional dicts where the
  primary key is a universal value such as IF-MIB::ifIndex
  or BRIDGE-MIB::dot1dBasePort
- `context_name` - Set the contextName used for SNMPv3 messages.
  The default contextName is the empty string "".  Overrides the
  defContext token in the snmp.conf file.
- `safe` - Safe query if true. If there is an exception, then return                blank values.
  

**Returns**:

- `return_value` - Tuple of (_contactable, exists, values)

<a id="snmp.snmp_manager.Session"></a>

## Session Objects

```python
class Session()
```

Class to create a SNMP session with a device.

<a id="snmp.snmp_manager.Session.__init__"></a>

#### \_\_init\_\_

```python
def __init__(_poll, engine, context_name="")
```

Initialize the _Session class.

**Arguments**:

- `_poll` - POLL object containing SNMP configuration
- `engine` - SNMP engine object
- `context_name` - String containing SNMPv3 context name.
  Default is empty string.
  

**Returns**:

- `session` - SNMP session

<a id="snmp.base_query"></a>

# snmp.base\_query

Base Query Class for interacting with devices.

<a id="snmp.base_query.Query"></a>

## Query Objects

```python
class Query()
```

Base snmp query object.

**Arguments**:

  None
  

**Returns**:

  None
  
  Key Methods:
  
- `supported` - Queries the device to determine whether the MIB is
  supported using a known OID defined in the MIB. Returns True
  if the device returns a response to the OID, False if not.
  
- `layer1` - Returns all needed layer 1 MIB information from the device.
  Keyed by OID's MIB name (primary key), ifIndex (secondary key)

<a id="snmp.base_query.Query.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object, test_oid, tags)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP Interact class object from snmp_manager.py
- `test_oid` - Oid that is used to check if the mib is supported
- `tags` - List of the layers for which this query gathers information
  

**Returns**:

  None

<a id="snmp.base_query.Query.supported"></a>

#### supported

```python
async def supported()
```

Return device's support for the MIB.

**Arguments**:

  None
  

**Returns**:

- `validity` - True if supported

<a id="snmp.snmp_info"></a>

# snmp.snmp\_info

Async module to aggregate query results.

<a id="snmp.snmp_info.Query"></a>

## Query Objects

```python
class Query()
```

Async class interacts with devices - use existing MIB classes.

**Arguments**:

  None
  

**Returns**:

  None

<a id="snmp.snmp_info.Query.__init__"></a>

#### \_\_init\_\_

```python
def __init__(snmp_object)
```

Instantiate the class.

**Arguments**:

- `snmp_object` - SNMP interact class object from snmp_manager.py
  

**Returns**:

  None

<a id="snmp.snmp_info.Query.everything"></a>

#### everything

```python
async def everything()
```

Get all information from device.

**Arguments**:

  None
  

**Returns**:

- `data` - Aggregated data

<a id="snmp.snmp_info.Query.misc"></a>

#### misc

```python
async def misc()
```

Provide miscellaneous information about the device and the poll.

<a id="snmp.snmp_info.Query.system"></a>

#### system

```python
async def system()
```

Get all system information from device.

**Arguments**:

  None
  

**Returns**:

- `data` - Aggregated system data

<a id="snmp.snmp_info.Query.layer1"></a>

#### layer1

```python
async def layer1()
```

Get all layer 1 information from device.

**Arguments**:

  None
  

**Returns**:

- `data` - Aggregated layer1 data

<a id="snmp.snmp_info.Query.layer2"></a>

#### layer2

```python
async def layer2()
```

Get all layer 2 information from device.

**Arguments**:

  None
  

**Returns**:

- `data` - Aggregated layer2 data

<a id="snmp.snmp_info.Query.layer3"></a>

#### layer3

```python
async def layer3()
```

Get all layer3 information from device.

**Arguments**:

  None
  

**Returns**:

- `data` - Aggregated layer3 data

<a id="update"></a>

# update

Define the switchmap.poller.update package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="update.device"></a>

# update.device

Module for preparing polled device data for the database.

<a id="update.device.Device"></a>

## Device Objects

```python
class Device()
```

Process data for a device.

The aim of this class is to process the YAML file consistently
across multiple manufacturers and present it to other classes
consistently. That way manufacturer specific code for processing YAML
data is in one place.

For example, there isn't a standard way of reporting ethernet duplex
values with different manufacturers exposing this data to different MIBs.
This class file attempts to determine the true duplex value of the
device by testing the presence of one or more OID values in the data.
It adds a 'duplex' data key to self.ports to act as the canonical key for
duplex across all devices.

<a id="update.device.Device.__init__"></a>

#### \_\_init\_\_

```python
def __init__(data)
```

Initialize class.

**Arguments**:

- `data` - Dict of device data
  

**Returns**:

  None

<a id="update.device.Device.process"></a>

#### process

```python
def process()
```

Initialize class.

**Arguments**:

  None
  

**Returns**:

  None
  
  Summary:
  
  IF-MIB
  
  A significant portion of this code relies on ifIndex
  IF-MIB::ifStackStatus information. This is stored under the
  'system' key of the device YAML files.
  
  According to the official IF-MIB file. ifStackStatus is a
  "table containing information on the relationships
  between the multiple sub-layers of network interfaces.  In
  particular, it contains information on which sub-layers run
  'on top of' which other sub-layers, where each sub-layer
  corresponds to a conceptual row in the ifTable.  For
  example, when the sub-layer with ifIndex value x runs over
  the sub-layer with ifIndex value y, then this table
  contains:
  
  ifStackStatus.x.y=active
  
  For each ifIndex value, I, which identifies an active
  interface, there are always at least two instantiated rows
  in this table associated with I.  For one of these rows, I
  is the value of ifStackHigherLayer; for the other, I is the
  value of ifStackLowerLayer.  (If I is not involved in
  multiplexing, then these are the only two rows associated
  with I.)
  
  For example, two rows exist even for an interface which has
  no others stacked on top or below it:
  
  ifStackStatus.0.x=active
  ifStackStatus.x.0=active"
  
  In the case of Juniper equipment, VLAN information is only
  visible on subinterfaces of the main interface. For example
  interface ge-0/0/0 won't have VLAN information assigned to it
  directly.
  
  When a VLAN is assigned to this interface, a subinterface
  ge-0/0/0.0 is automatically created with a non-Ethernet ifType.
  VLAN related OIDs are only maintained for this new subinterface
  only. This makes determining an interface's VLAN based on
  Ethernet ifType more difficult. ifStackStatus maps the ifIndex of
  the primary interface (ge-0/0/0) to the ifIndex of the secondary
  interface (ge-0/0/0.0) which manages higher level protocols and
  data structures such as VLANs and LLDP.
  
  The primary interface is referred to as the
  ifStackLowerLayer and the secondary subinterface is referred to
  as the ifStackHigherLayer.
  
  =================================================================
  
  Layer1 Keys
  
  The following Layer1 keys are presented by the ethernet_data
  method due to this instantiation:
  
- `l1_nativevlan` - A vendor agnostic Native VLAN
- `l1_vlans` - A list of vendor agnostic VLANs
- `l1_trunk` - A vendor agnostic flag of "True" if the port is a Trunk
- `l1_duplex` - A vendor agnostic status code for the duplex setting

