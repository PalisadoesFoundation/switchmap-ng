<a id="configuration"></a>

# configuration

switchmap classes that manage various configurations.

<a id="configuration.ConfigServer"></a>

## ConfigServer Objects

```python
class ConfigServer(ConfigAPI)
```

Class gathers all configuration information.

<a id="configuration.ConfigServer.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Intialize the class.

**Arguments**:

  None
  

**Returns**:

  None

<a id="configuration.ConfigServer.api_bind_port"></a>

#### api\_bind\_port

```python
def api_bind_port()
```

Get api_bind_port.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigServer.cache_directory"></a>

#### cache\_directory

```python
def cache_directory()
```

Determine the cache_directory.

**Arguments**:

  None
  

**Returns**:

- `result` - configured cache_directory

<a id="configuration.ConfigServer.db_host"></a>

#### db\_host

```python
def db_host()
```

Return db_host value.

**Arguments**:

  None
  

**Returns**:

- `result` - db_host value

<a id="configuration.ConfigServer.db_name"></a>

#### db\_name

```python
def db_name()
```

Return db_name value.

**Arguments**:

  None
  

**Returns**:

- `result` - db_name value

<a id="configuration.ConfigServer.db_max_overflow"></a>

#### db\_max\_overflow

```python
def db_max_overflow()
```

Get DB connection pool overflow size.

**Arguments**:

  None
  

**Returns**:

- `result` - Configured value

<a id="configuration.ConfigServer.db_pass"></a>

#### db\_pass

```python
def db_pass()
```

Return db_pass value.

**Arguments**:

  None
  

**Returns**:

- `result` - db_pass value

<a id="configuration.ConfigServer.db_pool_size"></a>

#### db\_pool\_size

```python
def db_pool_size()
```

Get DB connection pool size.

**Arguments**:

  None
  

**Returns**:

- `result` - Configured value

<a id="configuration.ConfigServer.db_user"></a>

#### db\_user

```python
def db_user()
```

Return db_user value.

**Arguments**:

  None
  

**Returns**:

- `result` - db_user value

<a id="configuration.ConfigServer.ingest_directory"></a>

#### ingest\_directory

```python
def ingest_directory()
```

Determine the ingest_directory.

**Arguments**:

  None
  

**Returns**:

- `result` - ingest_directory

<a id="configuration.ConfigServer.ingest_interval"></a>

#### ingest\_interval

```python
def ingest_interval()
```

Get ingest_interval.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="configuration.ConfigServer.purge_after_ingest"></a>

#### purge\_after\_ingest

```python
def purge_after_ingest()
```

Return purge_after_ingest value.

**Arguments**:

  None
  

**Returns**:

- `result` - purge_after_ingest value

<a id="configuration.ConfigServer.username"></a>

#### username

```python
def username()
```

Get username.

**Arguments**:

  None
  

**Returns**:

- `result` - result

<a id="__init__"></a>

# \_\_init\_\_

Define the switchmap.server package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db"></a>

# db

Module to manage connection pooling among other things.

<a id="db.main"></a>

#### main

```python
def main()
```

Process agent data.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.ingest"></a>

# db.ingest.ingest

switchmap classes that manage the DB uploading of polled data.

<a id="db.ingest.ingest.Ingest"></a>

## Ingest Objects

```python
class Ingest()
```

Read cache files in the DB.

<a id="db.ingest.ingest.Ingest.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config,
             test=False,
             test_cache_directory=None,
             multiprocessing=False)
```

Initialize class.

**Arguments**:

- `config` - ConfigServer object
- `test` - True if testing
- `test_cache_directory` - Ingest directory. Only used when testing.
- `multiprocessing` - True if multiprocessing is enabled
  

**Returns**:

  None

<a id="db.ingest.ingest.Ingest.process"></a>

#### process

```python
def process()
```

Process files in the cache.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.ingest.Ingest.zone"></a>

#### zone

```python
def zone(arguments)
```

Ingest the files' zone data.

**Arguments**:

- `arguments` - List of Argument objects
  

**Returns**:

- `success` - True if successful

<a id="db.ingest.ingest.Ingest.device"></a>

#### device

```python
def device(arguments)
```

Ingest the files' device data.

**Arguments**:

- `arguments` - List of arguments for the processing the zone
  [[item.idx_zone, item.data, item.filepath, item.config]]
  

**Returns**:

- `success` - True if successful

<a id="db.ingest.ingest.Ingest.cleanup"></a>

#### cleanup

```python
def cleanup(event)
```

Ingest the files' device data.

**Arguments**:

- `event` - Name of event
  

**Returns**:

  None

<a id="db.ingest.ingest.process_zone"></a>

#### process\_zone

```python
def process_zone(argument)
```

Ingest a single file for device updates.

**Arguments**:

- `argument` - Argument object
  

**Returns**:

- `rows` - ZoneObjects object

<a id="db.ingest.ingest.process_device"></a>

#### process\_device

```python
def process_device(argument)
```

Ingest a single file for device updates.

**Arguments**:

- `argument` - Argument object
  

**Returns**:

  None

<a id="db.ingest.ingest.setup"></a>

#### setup

```python
def setup(src, config)
```

Ingest the files in parallel.

**Arguments**:

- `src` - Directory where device YAML files are located
- `config` - Configuration object
  

**Returns**:

- `result` - EventObjects object

<a id="db.ingest.ingest.insert_arptable"></a>

#### insert\_arptable

```python
def insert_arptable(data, test=False)
```

Insert values from ARP tables.

**Arguments**:

- `data` - List of lists of ZoneObjects, one per device
  OR a single ZoneObjects from testing
- `test` - Sequentially insert values into the database if True.
  Bulk inserts don't insert data with predictable primary keys.
  

**Returns**:

- `pairmacips` - List of PairMacIp objects

<a id="db.ingest.ingest.insert_macips"></a>

#### insert\_macips

```python
def insert_macips(items, test=False)
```

Update the mac DB table.

**Arguments**:

- `items` - List of PairMacIp objects
- `test` - Sequentially insert values into the database if True.
  Bulk inserts don't insert data with predictable primary keys.
  

**Returns**:

  None

<a id="db.ingest.query.device"></a>

# db.ingest.query.device

Module to check the Device table when updating the DB with polled data.

<a id="db.ingest.query.device.Device"></a>

## Device Objects

```python
class Device()
```

Get all Device data.

<a id="db.ingest.query.device.Device.__init__"></a>

#### \_\_init\_\_

```python
def __init__(idx_zone, hostname)
```

Initialize class.

**Arguments**:

- `idx_zone` - Zone index to which the data belongs
- `hostname` - Hostname to process
  

**Returns**:

  None

<a id="db.ingest.query.device.Device.data"></a>

#### data

```python
def data()
```

Return complete device.

**Arguments**:

  None
  

**Returns**:

- `Result` - DeviceDetail object

<a id="db.ingest.query.device.Device.device"></a>

#### device

```python
def device()
```

Return system summary data.

**Arguments**:

  None
  

**Returns**:

- `Result` - RDevice object

<a id="db.ingest.query.device.Device.interfaces"></a>

#### interfaces

```python
def interfaces()
```

Return L1 data for Ethernet ports only.

**Arguments**:

  None
  

**Returns**:

- `self._ports` - L1 data for Ethernet ports

<a id="db.ingest.query.device.vlanports"></a>

#### vlanports

```python
def vlanports(idx_device)
```

Get all the VlanPorts for a device.

**Arguments**:

- `idx_device` - Idx_device of the device being processed
  

**Returns**:

- `result` - List of RVlanPort tuple

<a id="db.ingest.query.mac"></a>

# db.ingest.query.mac

Module for getting interface specific mac data.

<a id="db.ingest.query.mac.by_idx_mac"></a>

#### by\_idx\_mac

```python
def by_idx_mac(idx_mac)
```

Search for MAC addresses.

**Arguments**:

- `idx_mac` - idx_mac
  

**Returns**:

- `result` - List of MacDetail objects

<a id="db.ingest.query.vlan"></a>

# db.ingest.query.vlan

Module for getting interface specific VLAN data.

<a id="db.ingest.query.vlan.by_idx_l1interface"></a>

#### by\_idx\_l1interface

```python
def by_idx_l1interface(idx_l1interface)
```

Search for VLANs tied to interface.

**Arguments**:

- `idx_l1interface` - idx_l1interface
  

**Returns**:

- `result` - List of RVlan objects

<a id="db.ingest.query"></a>

# db.ingest.query

Define the switchmap.server.db.ingest.query package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest"></a>

# db.ingest

Define the switchmap.server.db.ingest package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.device"></a>

# db.ingest.update.device

Module for updating the database with topology data.

<a id="db.ingest.update.device.process"></a>

#### process

```python
def process(data, idx_zone, dns=True)
```

Process data received from a device.

**Arguments**:

- `data` - Device data (dict)
- `idx_zone` - Zone index to which the data belongs
- `dns` - Do DNS lookups if True
  

**Returns**:

  None

<a id="db.ingest.update.device.device"></a>

#### device

```python
def device(idx_zone, data)
```

Update the Device DB table.

**Arguments**:

- `idx_zone` - Zone index to which the data belongs
- `data` - Device data (dict)
  

**Returns**:

  None

<a id="db.ingest.update.device.Status"></a>

## Status Objects

```python
class Status()
```

Tracks the status of various Topology methods.

<a id="db.ingest.update.device.Status.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Instantiate the class.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.device.Status.l1interface"></a>

#### l1interface

```python
@property
def l1interface()
```

Provide the value of the 'l1interface' property.

<a id="db.ingest.update.device.Status.l1interface"></a>

#### l1interface

```python
@l1interface.setter
def l1interface(value)
```

Set the 'l1interface' property.

<a id="db.ingest.update.device.Status.systemstat"></a>

#### systemstat

```python
@property
def systemstat()
```

Provide the value of the 'systemstat' property.

<a id="db.ingest.update.device.Status.systemstat"></a>

#### systemstat

```python
@systemstat.setter
def systemstat(value)
```

Set the 'systemstat' property.

<a id="db.ingest.update.device.Status.ipport"></a>

#### ipport

```python
@property
def ipport()
```

Provide the value of  the 'ipport' property.

<a id="db.ingest.update.device.Status.ipport"></a>

#### ipport

```python
@ipport.setter
def ipport(value)
```

Set the 'ipport' property.

<a id="db.ingest.update.device.Status.macport"></a>

#### macport

```python
@property
def macport()
```

Provide the value of  the 'macport' property.

<a id="db.ingest.update.device.Status.macport"></a>

#### macport

```python
@macport.setter
def macport(value)
```

Set the 'macport' property.

<a id="db.ingest.update.device.Status.vlanport"></a>

#### vlanport

```python
@property
def vlanport()
```

Provide the value of  the 'vlanport' property.

<a id="db.ingest.update.device.Status.vlanport"></a>

#### vlanport

```python
@vlanport.setter
def vlanport(value)
```

Set the 'vlanport' property.

<a id="db.ingest.update.device.Status.vlan"></a>

#### vlan

```python
@property
def vlan()
```

Provide the value of  the 'vlan' property.

<a id="db.ingest.update.device.Status.vlan"></a>

#### vlan

```python
@vlan.setter
def vlan(value)
```

Set the 'vlan' property.

<a id="db.ingest.update.device.Topology"></a>

## Topology Objects

```python
class Topology()
```

Update Device data in the database.

<a id="db.ingest.update.device.Topology.__init__"></a>

#### \_\_init\_\_

```python
def __init__(exists, data, dns=True)
```

Initialize class.

**Arguments**:

- `exists` - RDevice object
- `data` - Dict of device data
- `dns` - Do DNS lookups if True
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.process"></a>

#### process

```python
def process()
```

Process data received from a device.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.l1interface"></a>

#### l1interface

```python
def l1interface(test=False)
```

Update the L1interface DB table.

**Arguments**:

- `test` - Sequentially insert values into the database if True.
  Bulk inserts don't insert data with predictable primary keys.
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.vlan"></a>

#### vlan

```python
def vlan(test=False)
```

Update the Vlan DB table.

**Arguments**:

- `test` - Sequentially insert values into the database if True.
  Bulk inserts don't insert data with predictable primary keys.
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.vlanport"></a>

#### vlanport

```python
def vlanport(test=False)
```

Update the VlanPort DB table.

**Arguments**:

- `test` - Sequentially insert values into the database if True.
  Bulk inserts don't insert data with predictable primary keys.
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.macport"></a>

#### macport

```python
def macport(test=False)
```

Update the MacPort DB table.

**Arguments**:

- `test` - Sequentially insert values into the database if True.
  Bulk inserts don't insert data with predictable primary keys.
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.ipport"></a>

#### ipport

```python
def ipport(test=False)
```

Update the IpPort DB table.

**Arguments**:

- `test` - Sequentially insert values into the database if True.
  Bulk inserts don't insert data with predictable primary keys.
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.systemstat"></a>

#### systemstat

```python
def systemstat(test=False)
```

Update the SystemStat DB table.

**Arguments**:

- `test` - Test mode if True
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.log"></a>

#### log

```python
def log(table, updated=False)
```

Create standardized log messaging.

**Arguments**:

- `table` - Name of table being updated
- `updated` - True if the table has been updated
  

**Returns**:

  None

<a id="db.ingest.update.device.Topology.log_invalid"></a>

#### log\_invalid

```python
def log_invalid(table)
```

Create standardized log messaging for invalid states.

**Arguments**:

- `table` - Name of table being updated
  

**Returns**:

  None

<a id="db.ingest.update"></a>

# db.ingest.update

Define the switchmap.server.db.ingest.update package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.zone"></a>

# db.ingest.update.zone

Module for updating the database with topology data.

<a id="db.ingest.update.zone.process"></a>

#### process

```python
def process(data, idx_zone, dns=True)
```

Process data received from a device.

**Arguments**:

- `data` - Device data (dict)
- `idx_zone` - Zone index to which the data belongs
- `dns` - Do DNS lookups if True
  

**Returns**:

- `results` - ZoneObjects object

<a id="db.ingest.update.zone.Status"></a>

## Status Objects

```python
class Status()
```

Tracks the status of various Topology methods.

<a id="db.ingest.update.zone.Status.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Instantiate the class.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.zone.Status.ip"></a>

#### ip

```python
@property
def ip()
```

Provide the value of the 'ip' property.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.zone.Status.ip"></a>

#### ip

```python
@ip.setter
def ip(value)
```

Set the 'ip' property.

**Arguments**:

- `value` - Value to set
  

**Returns**:

  None

<a id="db.ingest.update.zone.Status.mac"></a>

#### mac

```python
@property
def mac()
```

Provide the value of the 'mac' property.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.zone.Status.mac"></a>

#### mac

```python
@mac.setter
def mac(value)
```

Set the 'mac' property.

**Arguments**:

- `value` - Value to set
  

**Returns**:

  None

<a id="db.ingest.update.zone.Status.macip"></a>

#### macip

```python
@property
def macip()
```

Provide the value of the 'macip' property.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.zone.Status.macip"></a>

#### macip

```python
@macip.setter
def macip(value)
```

Set the 'macip' property.

**Arguments**:

- `value` - Value to set
  

**Returns**:

  None

<a id="db.ingest.update.zone.Topology"></a>

## Topology Objects

```python
class Topology()
```

Update Device data in the database.

<a id="db.ingest.update.zone.Topology.__init__"></a>

#### \_\_init\_\_

```python
def __init__(data, idx_zone, dns=True)
```

Initialize class.

**Arguments**:

- `data` - Dict of device data
- `idx_zone` - idx_zone of the Zone being processed
- `dns` - Do DNS lookups if True
  

**Returns**:

  None

<a id="db.ingest.update.zone.Topology.process"></a>

#### process

```python
def process()
```

Process data received from a device.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.zone.Topology.mac"></a>

#### mac

```python
def mac()
```

Update the Mac DB table.

**Arguments**:

  None
  

**Returns**:

- `rows` - List of unique IMac objects

<a id="db.ingest.update.zone.Topology.ip"></a>

#### ip

```python
def ip()
```

Update the Ip DB table.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.ingest.update.zone.Topology.macip"></a>

#### macip

```python
def macip()
```

Update the MacIp DB table.

**Arguments**:

  None
  

**Returns**:

- `rows` - List of PairMacIp objects

<a id="db.ingest.update.zone.Topology.log"></a>

#### log

```python
def log(table, updated=False)
```

Create standardized log messaging.

**Arguments**:

- `table` - Name of table being updated
- `updated` - True if the table has been updated
  

**Returns**:

  None

<a id="db.ingest.update.zone.Topology.log_invalid"></a>

#### log\_invalid

```python
def log_invalid(table)
```

Create standardized log messaging for invalid states.

**Arguments**:

- `table` - Name of table being updated
  

**Returns**:

  None

<a id="db.models"></a>

# db.models

Define SQLalchemy database table models.

<a id="db.models.Oui"></a>

## Oui Objects

```python
class Oui(BASE)
```

Database table definition.

<a id="db.models.Event"></a>

## Event Objects

```python
class Event(BASE)
```

Database table definition.

<a id="db.models.Root"></a>

## Root Objects

```python
class Root(BASE)
```

Database table definition.

<a id="db.models.Zone"></a>

## Zone Objects

```python
class Zone(BASE)
```

Database table definition.

<a id="db.models.Device"></a>

## Device Objects

```python
class Device(BASE)
```

Database table definition.

<a id="db.models.SystemStat"></a>

## SystemStat Objects

```python
class SystemStat(BASE)
```

Database table definition.

<a id="db.models.L1Interface"></a>

## L1Interface Objects

```python
class L1Interface(BASE)
```

Database table definition.

<a id="db.models.Vlan"></a>

## Vlan Objects

```python
class Vlan(BASE)
```

Database table definition.

<a id="db.models.VlanPort"></a>

## VlanPort Objects

```python
class VlanPort(BASE)
```

Database table definition.

<a id="db.models.Mac"></a>

## Mac Objects

```python
class Mac(BASE)
```

Database table definition.

<a id="db.models.MacPort"></a>

## MacPort Objects

```python
class MacPort(BASE)
```

Database table definition.

<a id="db.models.Ip"></a>

## Ip Objects

```python
class Ip(BASE)
```

Database table definition.

<a id="db.models.IpPort"></a>

## IpPort Objects

```python
class IpPort(BASE)
```

Database table definition.

<a id="db.models.MacIp"></a>

## MacIp Objects

```python
class MacIp(BASE)
```

Database table definition.

<a id="db.models.create_all_tables"></a>

#### create\_all\_tables

```python
def create_all_tables()
```

Ensure all tables are created.

**Arguments**:

  None

**Returns**:

  None

<a id="db.db"></a>

# db.db

Class to process connection.

<a id="db.db.db_select_row"></a>

#### db\_select\_row

```python
def db_select_row(error_code, statement)
```

Support 'Select' actions for __ENTIRE__ row.

**Arguments**:

- `error_code` - Error code to use in messages
- `statement` - SqlALchemy statement to execute. This must only reference
  an ORM Row object.
  

**Returns**:

- `result` - List of objects resulting from Select
  
  https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session

<a id="db.db.db_select"></a>

#### db\_select

```python
def db_select(error_code, statement)
```

Provide a transactional support for Select actions.

**Arguments**:

- `error_code` - Error code to use in messages
- `statement` - SqlALchemy statement to execute
  

**Returns**:

- `result` - List of objects resulting from Select
  
  https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session

<a id="db.db.db_update"></a>

#### db\_update

```python
def db_update(error_code, statement, values=None)
```

Provide a transactional support for Update actions.

**Arguments**:

- `error_code` - Error code to use in messages
- `statement` - SqlALchemy statement to execute
- `values` - List of values to insert if required
  

**Returns**:

- `result` - True if the transaction is successful
  
  https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session

<a id="db.db.db_delete_row"></a>

#### db\_delete\_row

```python
def db_delete_row(error_code, statement)
```

Support 'Delete' actions for __ENTIRE__ row.

**Arguments**:

- `error_code` - Error code to use in messages
- `statement` - SqlALchemy statement to execute. This must only reference
  an ORM Row object.
  

**Returns**:

- `result` - List of objects resulting from Delete
  
  https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session

<a id="db.db.db_delete"></a>

#### db\_delete

```python
def db_delete(error_code, statement)
```

Provide a transactional support for Delete actions.

**Arguments**:

- `error_code` - Error code to use in messages
- `statement` - SqlALchemy statement to execute
  

**Returns**:

- `result` - Number of affected rows

<a id="db.db.db_insert_row"></a>

#### db\_insert\_row

```python
def db_insert_row(error_code, model, mappings, die=True)
```

Perform bulk insert for ORM objects with enhanced logging.

**Arguments**:

- `error_code` - Error code to use in messages
- `model` - SQLAlchemy model to insert into
- `mappings` - List of dictionaries with data to insert
- `die` - Die if True
  

**Returns**:

- `result` - True if successful

<a id="db.schemas"></a>

# db.schemas

ORM Schema classes.

Used for defining GraphQL interaction

Based on the pages at:

    https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

<a id="db.schemas.Event"></a>

## Event Objects

```python
class Event(SQLAlchemyObjectType, EventAttribute)
```

Event node.

<a id="db.schemas.Event.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.Root"></a>

## Root Objects

```python
class Root(SQLAlchemyObjectType, RootAttribute)
```

Root node.

<a id="db.schemas.Root.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.Device"></a>

## Device Objects

```python
class Device(SQLAlchemyObjectType, DeviceAttribute)
```

Device node.

<a id="db.schemas.Device.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.SystemStat"></a>

## SystemStat Objects

```python
class SystemStat(SQLAlchemyObjectType, SystemStatAttribute)
```

SystemStat node.

<a id="db.schemas.SystemStat.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.Ip"></a>

## Ip Objects

```python
class Ip(SQLAlchemyObjectType, IpAttribute)
```

Ip node.

<a id="db.schemas.Ip.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.IpPort"></a>

## IpPort Objects

```python
class IpPort(SQLAlchemyObjectType, IpPortAttribute)
```

IpPort node.

<a id="db.schemas.IpPort.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.L1Interface"></a>

## L1Interface Objects

```python
class L1Interface(SQLAlchemyObjectType, L1InterfaceAttribute)
```

L1Interface node.

<a id="db.schemas.L1Interface.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.Mac"></a>

## Mac Objects

```python
class Mac(SQLAlchemyObjectType, MacAttribute)
```

Mac node.

<a id="db.schemas.Mac.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.Zone"></a>

## Zone Objects

```python
class Zone(SQLAlchemyObjectType, ZoneAttribute)
```

Zone node.

<a id="db.schemas.Zone.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.MacIp"></a>

## MacIp Objects

```python
class MacIp(SQLAlchemyObjectType, MacIpAttribute)
```

MacIp node.

<a id="db.schemas.MacIp.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.MacPort"></a>

## MacPort Objects

```python
class MacPort(SQLAlchemyObjectType, MacPortAttribute)
```

MacPort node.

<a id="db.schemas.MacPort.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.Oui"></a>

## Oui Objects

```python
class Oui(SQLAlchemyObjectType, OuiAttribute)
```

Oui node.

<a id="db.schemas.Oui.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.Vlan"></a>

## Vlan Objects

```python
class Vlan(SQLAlchemyObjectType, VlanAttribute)
```

Vlan node.

<a id="db.schemas.Vlan.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.VlanPort"></a>

## VlanPort Objects

```python
class VlanPort(SQLAlchemyObjectType, VlanPortAttribute)
```

VlanPort node.

<a id="db.schemas.VlanPort.Meta"></a>

## Meta Objects

```python
class Meta()
```

Define the metadata.

<a id="db.schemas.Query"></a>

## Query Objects

```python
class Query(graphene.ObjectType)
```

Define GraphQL queries.

<a id="db.schemas.Query.resolve_devices"></a>

#### resolve\_devices

```python
def resolve_devices(root, info, hostname=None, **kwargs)
```

Resolve and return devices from the database.

**Arguments**:

- `root` - The root object (not used here).
- `info` - GraphQL resolver info, used to get the query context.
- `hostname` _str, optional_ - If provided, filters by this hostname.
- `**kwargs` - Additional arguments (ignored).
  

**Returns**:

- `sqlalchemy.orm.Query` - A query object for the matching Device.

<a id="db.table.ipport"></a>

# db.table.ipport

Module for querying the IpPort table.

<a id="db.table.ipport.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_ipport
  

**Returns**:

- `result` - True if exists

<a id="db.table.ipport.exists"></a>

#### exists

```python
def exists(idx_l1interface, idx_ip)
```

Determine whether entry exists in the IpPort table.

**Arguments**:

- `idx_l1interface` - Device.idx_l1interface
- `idx_ip` - Ip.idx_ip
  

**Returns**:

- `result` - RIpPort tuple

<a id="db.table.ipport.find_idx_ip"></a>

#### find\_idx\_ip

```python
def find_idx_ip(idx_ip)
```

Find all ports on which MAC address has been found.

**Arguments**:

- `idx_ip` - Ip.idx_ip
  

**Returns**:

- `result` - RIpPort tuple

<a id="db.table.ipport.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a IpPort table entry.

**Arguments**:

- `rows` - IIpPort objects
  

**Returns**:

  None

<a id="db.table.ipport.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a IpPort table entry.

**Arguments**:

- `idx` - idx_ipport value
- `row` - IIpPort object
  

**Returns**:

  None

<a id="db.table.device"></a>

# db.table.device

Module for querying the Device table.

<a id="db.table.device.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_device
  

**Returns**:

- `result` - RDevice object

<a id="db.table.device.exists"></a>

#### exists

```python
def exists(idx_zone, hostname)
```

Determine whether hostname exists in the Device table.

**Arguments**:

- `idx_zone` - Zone index
- `hostname` - Device
  

**Returns**:

- `result` - RDevice tuple

<a id="db.table.device.devices"></a>

#### devices

```python
def devices(idx_zone)
```

Get all Devices for a zone.

**Arguments**:

- `idx_zone` - Zone index
  

**Returns**:

- `result` - list of RDevice tuples

<a id="db.table.device.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a Device table entry.

**Arguments**:

- `rows` - IDevice objects
  

**Returns**:

  None

<a id="db.table.device.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a Device table entry.

**Arguments**:

- `idx` - idx_device value
- `row` - IDevice object
  

**Returns**:

  None

<a id="db.table.metrics"></a>

# db.table.metrics

Database table operations for metrics.

<a id="db.table.metrics.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Insert rows into smap_device_metrics_history (historical metrics).

**Arguments**:

- `rows` _list or object_ - Single row or list of rows to insert. Each row is
  expected to have the following attributes:
  - hostname (str | bytes): Device hostname (required; UTF-8
  encoded to VARBINARY, ≤256 bytes)
  - last_polled (int, float, datetime, str, or None):
  Timestamp of last poll
  - uptime (int or None): Device uptime in seconds
  - cpu_utilization (float or None): CPU utilization percentage
  - memory_utilization (float or None): Memory utilization in %

**Returns**:

  None

<a id="db.table.systemstat"></a>

# db.table.systemstat

Module for querying the SystemStat table.

<a id="db.table.systemstat.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_systemstat

**Returns**:

- `results` - SystemStat object

<a id="db.table.systemstat.device_exists"></a>

#### device\_exists

```python
def device_exists(idx_device)
```

Determine whether SystemStat record exists for a device.

**Arguments**:

- `idx_device` - Device index

**Returns**:

- `result` - SystemStat object or False if not found

<a id="db.table.systemstat.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a SystemStat table entry.

**Arguments**:

- `rows` - SystemStat objects

**Returns**:

  None

<a id="db.table.systemstat.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Update a systemstat table entry.

**Arguments**:

- `idx` - idx_systemstat value
- `row` - SystemStat object

**Returns**:

  None

<a id="db.table.l1interface"></a>

# db.table.l1interface

Module for querying the L1Interface table.

<a id="db.table.l1interface.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_l1interface
  

**Returns**:

- `result` - RL1Interface object

<a id="db.table.l1interface.exists"></a>

#### exists

```python
def exists(idx_device, ifindex)
```

Determine whether hostname exists in the L1Interface table.

**Arguments**:

- `idx_device` - Device.idx_device
- `ifindex` - SNMP IfIndex number
  

**Returns**:

- `result` - RL1Interface tuple

<a id="db.table.l1interface.ifindexes"></a>

#### ifindexes

```python
def ifindexes(idx_device)
```

Get all the L1Interface table records for a device.

**Arguments**:

- `idx_device` - Device.idx_device
  

**Returns**:

- `result` - RL1Interface tuple

<a id="db.table.l1interface.findifalias"></a>

#### findifalias

```python
def findifalias(idx_device, ifalias)
```

Find ifalias.

**Arguments**:

- `idx_device` - Device.idx_device
- `ifalias` - Hostname
  

**Returns**:

- `idx_device` - Device.idx_device
- `result` - list of L1Interface tuples

<a id="db.table.l1interface.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a L1Interface table entry.

**Arguments**:

- `rows` - IL1Interface objects
  

**Returns**:

  None

<a id="db.table.l1interface.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Update a L1Interface table entry.

**Arguments**:

- `idx` - idx_l1interface value
- `row` - IL1Interface object
  

**Returns**:

  None

<a id="db.table.vlanport"></a>

# db.table.vlanport

Module for querying the VlanPort table.

<a id="db.table.vlanport.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_vlanport
  

**Returns**:

- `result` - True if exists

<a id="db.table.vlanport.exists"></a>

#### exists

```python
def exists(idx_l1interface, idx_vlan)
```

Determine whether entry exists in the VlanPort table.

**Arguments**:

- `idx_l1interface` - Device.idx_l1interface
- `idx_vlan` - Vlan.idx_vlan
  

**Returns**:

- `result` - RVlanPort tuple

<a id="db.table.vlanport.find_idx_vlan"></a>

#### find\_idx\_vlan

```python
def find_idx_vlan(idx_vlan)
```

Find all ports on which MAC address has been found.

**Arguments**:

- `idx_vlan` - Vlan.idx_vlan
  

**Returns**:

- `result` - RVlanPort tuple

<a id="db.table.vlanport.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a VlanPort table entry.

**Arguments**:

- `rows` - IVlanPort objects
  

**Returns**:

  None

<a id="db.table.vlanport.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a VlanPort table entry.

**Arguments**:

- `idx` - idx_vlanport value
- `row` - IVlanPort object
  

**Returns**:

  None

<a id="db.table.macport"></a>

# db.table.macport

Module for querying the MacPort table.

<a id="db.table.macport.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_macport
  

**Returns**:

- `result` - True if exists

<a id="db.table.macport.exists"></a>

#### exists

```python
def exists(idx_l1interface, idx_mac)
```

Determine whether entry exists in the MacPort table.

**Arguments**:

- `idx_l1interface` - Device.idx_l1interface
- `idx_mac` - Mac.idx_mac
  

**Returns**:

- `result` - RMacPort tuple

<a id="db.table.macport.find_idx_mac"></a>

#### find\_idx\_mac

```python
def find_idx_mac(idx_mac)
```

Find all ports on which MAC address has been found.

**Arguments**:

- `idx_mac` - Mac.idx_mac
  

**Returns**:

- `result` - RMacPort tuple

<a id="db.table.macport.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a MacPort table entry.

**Arguments**:

- `rows` - IMacPort objects
  

**Returns**:

  None

<a id="db.table.macport.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a MacPort table entry.

**Arguments**:

- `idx` - idx_macport value
- `row` - IMacPort object
  

**Returns**:

  None

<a id="db.table.mac"></a>

# db.table.mac

Module for querying the Mac table.

<a id="db.table.mac.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_mac
  

**Returns**:

- `result` - RMac object

<a id="db.table.mac.exists"></a>

#### exists

```python
def exists(idx_zone, _mac)
```

Determine whether MAC exists in the Mac table.

**Arguments**:

- `idx_zone` - Zone index
- `_mac` - Mac address
  

**Returns**:

- `result` - RMac tuple

<a id="db.table.mac.findmac"></a>

#### findmac

```python
def findmac(idx_zone, macs)
```

Determine whether MAC exists in the Mac table.

**Arguments**:

- `idx_zone` - Zone index
- `macs` - List or single MAC address
  

**Returns**:

- `result` - list of RMac tuples

<a id="db.table.mac.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a Mac table entry.

**Arguments**:

- `rows` - TopologyMac objects
  

**Returns**:

  None

<a id="db.table.mac.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a Mac table entry.

**Arguments**:

- `idx` - idx_mac value
- `row` - IMac object
  

**Returns**:

  None

<a id="db.table.ip"></a>

# db.table.ip

Module for querying the Ip table.

<a id="db.table.ip.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_ip
  

**Returns**:

- `result` - RIp object

<a id="db.table.ip.exists"></a>

#### exists

```python
def exists(idx_zone, _ip)
```

Determine whether MAC exists in the Ip table.

**Arguments**:

- `idx_zone` - Zone index
- `_ip` - Ip address
  

**Returns**:

- `result` - RIp tuple

<a id="db.table.ip.findhostname"></a>

#### findhostname

```python
def findhostname(idx_zone, hostname)
```

Determine whether hostname exists in the Ip table.

**Arguments**:

- `idx_zone` - Zone index
- `hostname` - hostname
  

**Returns**:

- `results` - RIp list

<a id="db.table.ip.findip"></a>

#### findip

```python
def findip(idx_zone, ips)
```

Determine whether MAC exists in the Ip table.

**Arguments**:

- `idx_zone` - Zone index
- `ips` - one or more IP addresses
  

**Returns**:

- `result` - list of RIp tuples

<a id="db.table.ip.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Perform bulk insert for the Mac table.

**Arguments**:

- `rows` - List of IMac objects to be inserted into the database.
  

**Returns**:

- `None` - This function does not return any value.

<a id="db.table.ip.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a Ip table entry.

**Arguments**:

- `idx` - idx_ip value
- `row` - IIp object
  

**Returns**:

  None

<a id="db.table.vlan"></a>

# db.table.vlan

Module for querying the Vlan table.

<a id="db.table.vlan.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_vlan
  

**Returns**:

- `result` - RVlan object

<a id="db.table.vlan.exists"></a>

#### exists

```python
def exists(idx_device, vlan)
```

Determine whether vlan exists in the Vlan table.

**Arguments**:

- `idx_device` - DB idx for the device
- `vlan` - Vlan
  

**Returns**:

- `result` - RVlan tuple

<a id="db.table.vlan.vlans"></a>

#### vlans

```python
def vlans(idx_device)
```

Get all VLANs for a device.

**Arguments**:

- `idx_device` - Device index
  

**Returns**:

- `result` - list of RVlan tuples

<a id="db.table.vlan.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a Vlan table entry.

**Arguments**:

- `rows` - IVlan objects
  

**Returns**:

  None

<a id="db.table.vlan.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a Vlan table entry.

**Arguments**:

- `idx` - idx_vlan value
- `row` - IVlan object
  

**Returns**:

  None

<a id="db.table.root"></a>

# db.table.root

Module for querying the Root table.

<a id="db.table.root.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_root
  

**Returns**:

- `result` - RRoot record

<a id="db.table.root.exists"></a>

#### exists

```python
def exists(root)
```

Determine whether root exists in the Root table.

**Arguments**:

- `root` - Root
  

**Returns**:

- `result` - RRoot tuple

<a id="db.table.root.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a Root table entry.

**Arguments**:

- `rows` - IRoot objects
  

**Returns**:

  None

<a id="db.table.root.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a Root table entry.

**Arguments**:

- `idx` - idx_root value
- `row` - IRoot object
  

**Returns**:

  None

<a id="db.table.root.roots"></a>

#### roots

```python
def roots()
```

Get list of Roots.

**Arguments**:

  None
  

**Returns**:

- `result` - RRoot object

<a id="db.table"></a>

# db.table

Constants required for DB queries and updates.

<a id="db.table.event"></a>

# db.table.event

Module for querying the Event table.

<a id="db.table.event.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_event
  

**Returns**:

- `result` - REvent object

<a id="db.table.event.exists"></a>

#### exists

```python
def exists(event)
```

Determine whether event exists in the Event table.

**Arguments**:

- `event` - Event
  

**Returns**:

- `result` - REvent tuple

<a id="db.table.event.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a Event table entry.

**Arguments**:

- `rows` - IEvent objects
  

**Returns**:

  None

<a id="db.table.event.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a Event table entry.

**Arguments**:

- `idx` - idx_event value
- `row` - IEvent object
  

**Returns**:

  None

<a id="db.table.event.events"></a>

#### events

```python
def events()
```

Get list of Events.

**Arguments**:

  None
  

**Returns**:

- `result` - REvent object

<a id="db.table.event.delete"></a>

#### delete

```python
def delete(idx)
```

Delete event.

**Arguments**:

- `idx` - idx_event
  

**Returns**:

  None

<a id="db.table.event.create"></a>

#### create

```python
def create(name=None)
```

Create an event.

**Arguments**:

- `name` - Alternative name
  

**Returns**:

- `result` - Event object for row that doesn't already exist

<a id="db.table.event.purge"></a>

#### purge

```python
def purge()
```

Purge all events except the most recent two.

**Arguments**:

  None
  

**Returns**:

- `result` - None

<a id="db.table.zone"></a>

# db.table.zone

Module for querying the Zone table.

<a id="db.table.zone.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_zone
  

**Returns**:

- `result` - RZone record

<a id="db.table.zone.exists"></a>

#### exists

```python
def exists(idx_event, name)
```

Determine whether name exists in the Zone table.

**Arguments**:

- `idx_event` - Event index
- `name` - Zone
  

**Returns**:

- `result` - RZone tuple

<a id="db.table.zone.zones"></a>

#### zones

```python
def zones(idx_event)
```

Get all Zones for a event.

**Arguments**:

- `idx_event` - Event index
  

**Returns**:

- `result` - list of RZone tuples

<a id="db.table.zone.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a Zone table entry.

**Arguments**:

- `rows` - IZone objects
  

**Returns**:

  None

<a id="db.table.zone.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a Zone table entry.

**Arguments**:

- `idx` - idx_zone value
- `row` - IZone object
  

**Returns**:

  None

<a id="db.table.macip"></a>

# db.table.macip

Module for querying the MacIp table.

<a id="db.table.macip.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_macip
  

**Returns**:

- `result` - RMacIp object

<a id="db.table.macip.exists"></a>

#### exists

```python
def exists(idx_mac, idx_ip)
```

Determine whether mac exists in the MacIp table.

**Arguments**:

- `idx_mac` - Mac.idx_mac
- `idx_ip` - Ip.idx_ip
  

**Returns**:

- `result` - RMacIp tuple

<a id="db.table.macip.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a MacIp table entry.

**Arguments**:

- `rows` - IMacIp objects
  

**Returns**:

  None

<a id="db.table.macip.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a MacIp table entry.

**Arguments**:

- `idx` - idx_macip value
- `row` - IMacIp object
  

**Returns**:

  None

<a id="db.table.macip.idx_ips_exist"></a>

#### idx\_ips\_exist

```python
def idx_ips_exist(idx_mac)
```

Get a list of idx_ip values matching idx_mac from the MacIp table.

**Arguments**:

- `idx_mac` - Mac.idx_mac
  

**Returns**:

- `result` - List of RMacIp tuples

<a id="db.table.oui"></a>

# db.table.oui

Module for querying the Oui table.

<a id="db.table.oui.idx_oui"></a>

#### idx\_oui

```python
def idx_oui(mac)
```

Get the idx_oui value.

**Arguments**:

- `mac` - MAC address
  

**Returns**:

- `result` - idx_oui value

<a id="db.table.oui.idx_exists"></a>

#### idx\_exists

```python
def idx_exists(idx)
```

Determine whether primary key exists.

**Arguments**:

- `idx` - idx_oui
  

**Returns**:

- `result` - ROui record

<a id="db.table.oui.exists"></a>

#### exists

```python
def exists(oui)
```

Determine whether oui exists in the Oui table.

**Arguments**:

- `oui` - Oui
  

**Returns**:

- `result` - ROui tuple

<a id="db.table.oui.insert_row"></a>

#### insert\_row

```python
def insert_row(rows)
```

Create a Oui table entry.

**Arguments**:

- `rows` - IOui objects
  

**Returns**:

  None

<a id="db.table.oui.update_row"></a>

#### update\_row

```python
def update_row(idx, row)
```

Upadate a Oui table entry.

**Arguments**:

- `idx` - idx_oui value
- `row` - IOui object
  

**Returns**:

  None

<a id="db.table.oui.ouis"></a>

#### ouis

```python
def ouis()
```

Get all the OUIs.

**Arguments**:

  None
  

**Returns**:

- `result` - ROui record

<a id="db.misc.rows"></a>

# db.misc.rows

Module to handle database table rows.

<a id="db.misc.rows.device"></a>

#### device

```python
def device(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - Device row
  

**Returns**:

- `result` - RDevice tuple

<a id="db.misc.rows.root"></a>

#### root

```python
def root(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - Root row
  

**Returns**:

- `result` - RRoot tuple

<a id="db.misc.rows.event"></a>

#### event

```python
def event(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - Event row
  

**Returns**:

- `result` - REvent tuple

<a id="db.misc.rows.systemstat"></a>

#### systemstat

```python
def systemstat(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - SystemStat row

**Returns**:

- `results` - SystemStat tuple

<a id="db.misc.rows.l1interface"></a>

#### l1interface

```python
def l1interface(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - L1Interface row
  

**Returns**:

- `result` - RL1Interface tuple

<a id="db.misc.rows.mac"></a>

#### mac

```python
def mac(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - Mac row
  

**Returns**:

- `result` - RMac tuple

<a id="db.misc.rows.macip"></a>

#### macip

```python
def macip(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - MacIp row
  

**Returns**:

- `result` - RMacIp tuple

<a id="db.misc.rows.macport"></a>

#### macport

```python
def macport(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - MacPort row
  

**Returns**:

- `result` - RMacPort tuple

<a id="db.misc.rows.oui"></a>

#### oui

```python
def oui(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - Oui row
  

**Returns**:

- `result` - ROui tuple

<a id="db.misc.rows.vlan"></a>

#### vlan

```python
def vlan(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - Vlan row
  

**Returns**:

- `result` - RVlan tuple

<a id="db.misc.rows.vlanport"></a>

#### vlanport

```python
def vlanport(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - VlanPort row
  

**Returns**:

- `result` - RVlanPort tuple

<a id="db.misc.rows.zone"></a>

#### zone

```python
def zone(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - Zone row
  

**Returns**:

- `result` - RZone tuple

<a id="db.misc.rows.ip"></a>

#### ip

```python
def ip(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - Ip row
  

**Returns**:

- `result` - RIp tuple

<a id="db.misc.rows.ipport"></a>

#### ipport

```python
def ipport(row)
```

Convert table row to tuple.

**Arguments**:

- `row` - IpPort row
  

**Returns**:

- `result` - RIpPort tuple

<a id="db.misc.interface"></a>

# db.misc.interface

Switchmap Interface library.

<a id="db.misc.interface.interfaces"></a>

#### interfaces

```python
def interfaces(rdevice)
```

Get an Rl1interface list for the device during the previous event.

**Arguments**:

- `rdevice` - RDevice object
  

**Returns**:

- `result` - List of matching Rl1interface objects

<a id="db.misc.search"></a>

# db.misc.search

switchmap.Search class.

Description:

    This files has classes that process searches for:
        1) IP and MAC address
        2) Port names
        3) Hostnames

<a id="db.misc.search.Search"></a>

## Search Objects

```python
class Search()
```

Class that manages searches.

Methods return lists of Found objects for the idx_l1interface table entries
where there are matches.

<a id="db.misc.search.Search.__init__"></a>

#### \_\_init\_\_

```python
def __init__(idx_event, searchstring)
```

Initialize the class.

**Arguments**:

- `idx_event` - Event index
- `searchstring` - search string to look for
  

**Returns**:

  None

<a id="db.misc.search.Search.find"></a>

#### find

```python
def find()
```

Find search string.

**Arguments**:

  None
  

**Returns**:

- `result` - List of Found objects of interfaces that have data matching
  the search string

<a id="db.misc.search.Search.macaddress"></a>

#### macaddress

```python
def macaddress()
```

Search for macaddress.

**Arguments**:

  None
  

**Returns**:

- `result` - List of Found objects of interfaces that have data matching
  the search string

<a id="db.misc.search.Search.ifalias"></a>

#### ifalias

```python
def ifalias()
```

Search for string in ifalias names.

**Arguments**:

  None
  

**Returns**:

- `result` - List of Found objects of interfaces that have data matching
  the search string

<a id="db.misc.search.Search.ipaddress"></a>

#### ipaddress

```python
def ipaddress()
```

Search for ipaddress.

**Arguments**:

  None
  

**Returns**:

- `result` - List of Found objects of interfaces that have data matching
  the search string

<a id="db.misc.search.Search.hostname"></a>

#### hostname

```python
def hostname()
```

Search for string hostnames.

**Arguments**:

  None
  

**Returns**:

- `result` - List of Found objects of interfaces that have data matching
  the search string

<a id="db.misc.search.find_ip_interface"></a>

#### find\_ip\_interface

```python
def find_ip_interface(idx_ip)
```

Find all ports on which an specfic IP address has been found.

**Arguments**:

- `idx_ip` - Ip.idx_ip
  

**Returns**:

- `result` - RIpPort tuple

<a id="db.misc.search.search"></a>

#### search

```python
def search(idx_root, searchstring)
```

Search based on idx_root values.

**Arguments**:

- `idx_root` - Root index
- `searchstring` - search string to look for
  

**Returns**:

- `result` - List of idx_l1interface values

<a id="db.misc.search.trunk"></a>

#### trunk

```python
def trunk(idx_l1interface)
```

Determine whether the interface is a trunk.

**Arguments**:

- `idx_l1interface` - L1interface table primary key
  

**Returns**:

- `result` - True / False status

<a id="db.misc"></a>

# db.misc

Define the switchmap.server.db.misc package.

**Arguments**:

  None
  

**Returns**:

  None

<a id="db.misc.oui"></a>

# db.misc.oui

Switchmap OUI library.

<a id="db.misc.oui.update_db_oui"></a>

#### update\_db\_oui

```python
def update_db_oui(filepath, new=False)
```

Update the database with Oui data.

**Arguments**:

- `filepath` - File to process
- `new` - If True, skip existing entry checks for new installations
  

**Returns**:

  None
  

**Raises**:

- `FileNotFoundError` - If the file cannot be found
- `ValueError` - If the CSV is improperly formatted

<a id="db.attributes"></a>

# db.attributes

ORM attribute classes for SQLAlchemy graphene / GraphQL schemas..

Used for defining GraphQL interaction

Based on the pages at:

    https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

<a id="db.attributes.resolve_address"></a>

#### resolve\_address

```python
def resolve_address(obj, _)
```

Convert 'address' from bytes to string.

**Arguments**:

- `obj` - Object containing address attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded address string or empty string

<a id="db.attributes.resolve_cdpcachedeviceid"></a>

#### resolve\_cdpcachedeviceid

```python
def resolve_cdpcachedeviceid(obj, _)
```

Convert 'cdpcachedeviceid' from bytes to string.

**Arguments**:

- `obj` - Object containing cdpcachedeviceid attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded cdpcachedeviceid string or empty string

<a id="db.attributes.resolve_cdpcacheplatform"></a>

#### resolve\_cdpcacheplatform

```python
def resolve_cdpcacheplatform(obj, _)
```

Convert 'cdpcacheplatform' from bytes to string.

**Arguments**:

- `obj` - Object containing cdpcacheplatform attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded cdpcacheplatform string or empty string

<a id="db.attributes.resolve_cdpcachedeviceport"></a>

#### resolve\_cdpcachedeviceport

```python
def resolve_cdpcachedeviceport(obj, _)
```

Convert 'cdpcachedeviceport' from bytes to string.

**Arguments**:

- `obj` - Object containing cdpcachedeviceport attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded cdpcachedeviceport string or empty string

<a id="db.attributes.resolve_hostname"></a>

#### resolve\_hostname

```python
def resolve_hostname(obj, _)
```

Convert 'hostname' from bytes to string.

**Arguments**:

- `obj` - Object containing hostname attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded hostname string or empty string

<a id="db.attributes.resolve_ifalias"></a>

#### resolve\_ifalias

```python
def resolve_ifalias(obj, _)
```

Convert 'ifalias' from bytes to string.

**Arguments**:

- `obj` - Object containing ifalias attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded ifalias string or empty string

<a id="db.attributes.resolve_ifname"></a>

#### resolve\_ifname

```python
def resolve_ifname(obj, _)
```

Convert 'ifname' from bytes to string.

**Arguments**:

- `obj` - Object containing ifname attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded ifname string or empty string

<a id="db.attributes.resolve_ifdescr"></a>

#### resolve\_ifdescr

```python
def resolve_ifdescr(obj, _)
```

Convert 'ifdescr' from bytes to string.

**Arguments**:

- `obj` - Object containing ifdescr attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded ifdescr string or empty string

<a id="db.attributes.resolve_lldpremportdesc"></a>

#### resolve\_lldpremportdesc

```python
def resolve_lldpremportdesc(obj, _)
```

Convert 'lldpremportdesc' from bytes to string.

**Arguments**:

- `obj` - Object containing lldpremportdesc attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded lldpremportdesc string or empty string

<a id="db.attributes.resolve_lldpremsyscapenabled"></a>

#### resolve\_lldpremsyscapenabled

```python
def resolve_lldpremsyscapenabled(obj, _)
```

Convert 'lldpremsyscapenabled' from bytes to string.

**Arguments**:

- `obj` - Object containing lldpremsyscapenabled attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded lldpremsyscapenabled string or empty string

<a id="db.attributes.resolve_lldpremsysdesc"></a>

#### resolve\_lldpremsysdesc

```python
def resolve_lldpremsysdesc(obj, _)
```

Convert 'lldpremsysdesc' from bytes to string.

**Arguments**:

- `obj` - Object containing lldpremsysdesc attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded lldpremsysdesc string or empty string

<a id="db.attributes.resolve_lldpremsysname"></a>

#### resolve\_lldpremsysname

```python
def resolve_lldpremsysname(obj, _)
```

Convert 'lldpremsysname' from bytes to string.

**Arguments**:

- `obj` - Object containing lldpremsysname attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded lldpremsysname string or empty string

<a id="db.attributes.resolve_mac"></a>

#### resolve\_mac

```python
def resolve_mac(obj, _)
```

Convert 'mac' from bytes to string.

**Arguments**:

- `obj` - Object containing mac attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded mac string or empty string

<a id="db.attributes.resolve_organization"></a>

#### resolve\_organization

```python
def resolve_organization(obj, _)
```

Convert 'organization' from bytes to string.

**Arguments**:

- `obj` - Object containing organization attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded organization string or empty string

<a id="db.attributes.resolve_device_by_hostname"></a>

#### resolve\_device\_by\_hostname

```python
def resolve_device_by_hostname(self, info, hostname=None, **kwargs)
```

Resolve all devices by hostname for historical data.

<a id="db.attributes.resolve_name"></a>

#### resolve\_name

```python
def resolve_name(obj, _)
```

Convert 'name' from bytes to string.

**Arguments**:

- `obj` - Object containing name attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded name string or empty string

<a id="db.attributes.resolve_notes"></a>

#### resolve\_notes

```python
def resolve_notes(obj, _)
```

Convert 'notes' from bytes to string.

**Arguments**:

- `obj` - Object containing notes attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded notes string or empty string

<a id="db.attributes.resolve_oui"></a>

#### resolve\_oui

```python
def resolve_oui(obj, _)
```

Convert 'oui' from bytes to string.

**Arguments**:

- `obj` - Object containing oui attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded oui string or empty string

<a id="db.attributes.resolve_sys_description"></a>

#### resolve\_sys\_description

```python
def resolve_sys_description(obj, _)
```

Convert 'sys_description' from bytes to string.

**Arguments**:

- `obj` - Object containing sys_description attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded sys_description string or empty string

<a id="db.attributes.resolve_sys_name"></a>

#### resolve\_sys\_name

```python
def resolve_sys_name(obj, _)
```

Convert 'sys_name' from bytes to string.

**Arguments**:

- `obj` - Object containing sys_name attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded sys_name string or empty string

<a id="db.attributes.resolve_sys_uptime"></a>

#### resolve\_sys\_uptime

```python
def resolve_sys_uptime(obj, _)
```

Convert 'sys_uptime' from Null to zero.

**Arguments**:

- `obj` - Object containing sys_uptime attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `float` - System uptime value or 0 if null

<a id="db.attributes.resolve_sys_objectid"></a>

#### resolve\_sys\_objectid

```python
def resolve_sys_objectid(obj, _)
```

Convert 'sys_objectid' from bytes to string.

**Arguments**:

- `obj` - Object containing sys_objectid attribute
- `_` - Unused GraphQL parameter
  

**Returns**:

- `str` - Decoded sys_objectid string or empty string

<a id="db.attributes.EventAttribute"></a>

## EventAttribute Objects

```python
class EventAttribute()
```

Descriptive attributes of the Event table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.RootAttribute"></a>

## RootAttribute Objects

```python
class RootAttribute()
```

Descriptive attributes of the Event table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.ZoneAttribute"></a>

## ZoneAttribute Objects

```python
class ZoneAttribute()
```

Descriptive attributes of the Zone table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.OuiAttribute"></a>

## OuiAttribute Objects

```python
class OuiAttribute()
```

Descriptive attributes of the Oui table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.DeviceAttribute"></a>

## DeviceAttribute Objects

```python
class DeviceAttribute()
```

Descriptive attributes of the Device table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.SystemStatAttribute"></a>

## SystemStatAttribute Objects

```python
class SystemStatAttribute()
```

Descriptive attributes of the SystemStat table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.L1InterfaceAttribute"></a>

## L1InterfaceAttribute Objects

```python
class L1InterfaceAttribute()
```

Descriptive attributes of the L1Interface table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.VlanAttribute"></a>

## VlanAttribute Objects

```python
class VlanAttribute()
```

Descriptive attributes of the Vlan table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.VlanPortAttribute"></a>

## VlanPortAttribute Objects

```python
class VlanPortAttribute()
```

Descriptive attributes of the VlanPort table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.MacAttribute"></a>

## MacAttribute Objects

```python
class MacAttribute()
```

Descriptive attributes of the Mac table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.MacIpAttribute"></a>

## MacIpAttribute Objects

```python
class MacIpAttribute()
```

Descriptive attributes of the MacIp table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.MacPortAttribute"></a>

## MacPortAttribute Objects

```python
class MacPortAttribute()
```

Descriptive attributes of the MacPort table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.IpAttribute"></a>

## IpAttribute Objects

```python
class IpAttribute()
```

Descriptive attributes of the MacPort table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="db.attributes.IpPortAttribute"></a>

## IpPortAttribute Objects

```python
class IpPortAttribute()
```

Descriptive attributes of the MacPort table.

A generic class to mutualize description of attributes for both queries
and mutations.

<a id="api"></a>

# api

Module of switchmap API routes.

Contains all routes that the Flask API uses

<a id="api.routes.config"></a>

# api.routes.config

Config API routes for Switchmap.

<a id="api.routes.config.merge_preserving_secrets"></a>

#### merge\_preserving\_secrets

```python
def merge_preserving_secrets(current, incoming)
```

Merge two configuration objects while preserving secret values.

**Arguments**:

- `current` _dict | Any_ - Existing configuration or value.
- `incoming` _dict | Any_ - New configuration or value to merge.
  

**Returns**:

- `result` - Merged configuration where secrets are preserved.

<a id="api.routes.config.read_config"></a>

#### read\_config

```python
def read_config()
```

Read the configuration file from disk.

**Arguments**:

  None
  

**Returns**:

- `dict` - The loaded configuration data. Returns an empty dictionary if
  the configuration file does not exist or is empty.

<a id="api.routes.config.write_config"></a>

#### write\_config

```python
def write_config(data)
```

Write the configuration data to disk.

**Arguments**:

- `data` _dict_ - The configuration data to write.
  

**Returns**:

  None

<a id="api.routes.config.get_config"></a>

#### get\_config

```python
@API_CONFIG.route("/config", methods=["GET"])
def get_config()
```

Return the current configuration as JSON.

**Arguments**:

  None
  

**Returns**:

- `Response` - A Flask JSON response containing the current config
  loaded from config.yaml.

<a id="api.routes.config.mask_secrets"></a>

#### mask\_secrets

```python
def mask_secrets(config: dict) -> dict
```

Recursively masks sensitive values in a configuration dictionary.

Specifically, replaces the value of "db_pass" with a masked string,
while preserving the structure of nested dictionaries.

**Arguments**:

- `config` _dict_ - The configuration dictionary to process.
  

**Returns**:

- `dict` - A new dictionary with secrets masked.

<a id="api.routes.config.post_config"></a>

#### post\_config

```python
@API_CONFIG.route("/config", methods=["POST"])
def post_config()
```

Update the config.yaml with new JSON data from the request.

**Arguments**:

  None
  
  

**Returns**:

- `Response` - A Flask JSON response indicating success or failure.
  Returns 400 if the JSON data is invalid, otherwise returns
  a success message.

<a id="api.routes.config.deep_merge"></a>

#### deep\_merge

```python
def deep_merge(dst, src)
```

Recursively merge two dictionaries or values.

**Arguments**:

- `dst` _dict | Any_ - Destination dictionary or value.
- `src` _dict | Any_ - Source dictionary or value to merge into dst.
  

**Returns**:

- `result` - Result of merging src into dst.

<a id="api.routes.config.patch_config"></a>

#### patch\_config

```python
@API_CONFIG.route("/config", methods=["PATCH"])
def patch_config()
```

Partially update the SwitchMap configuration.

Handles the db_pass secret:
- Expects {"new": "..."}.
- Updates db_pass directly.
- Other non-secret fields are merged directly.

**Arguments**:

  None
  
  The request JSON body can contain:
  - "db_pass" (dict, optional): {"new": "<new_password>"}
  - Other configuration keys to update.
  

**Returns**:

- `Response` - JSON response indicating success or failure:
  - 400 if the request JSON is invalid or db_pass format is incorrect.
  - 200 with {"status": "success"} on successful update.

<a id="api.routes.post"></a>

# api.routes.post

Database server API. HTTP POST routes.

<a id="api.routes.post.post_device_data"></a>

#### post\_device\_data

```python
@API_POST.route(API_POLLER_POST_URI, methods=["POST"])
def post_device_data()
```

Accept posts of network device data from pollers.

**Arguments**:

  None
  

**Returns**:

- `_response` - OK message when successful

<a id="api.routes.post.post_searchterm"></a>

#### post\_searchterm

```python
@API_POST.route(API_POLLER_SEARCH_URI, methods=["POST"])
def post_searchterm()
```

Accept posts searches.

**Arguments**:

  None
  

**Returns**:

- `_response` - OK message when successful

<a id="api.routes.graphql"></a>

# api.routes.graphql

GraphQL routes.

<a id="api.routes"></a>

# api.routes

Define the switchmap.server.api.routes package.

**Arguments**:

  None
  

**Returns**:

  None

