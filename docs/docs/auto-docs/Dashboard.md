<a id="configuration"></a>

# configuration

switchmap classes that manage various configurations.

<a id="configuration.ConfigDashboard"></a>

## ConfigDashboard Objects

```python
class ConfigDashboard(ConfigAPIClient, ConfigAPI)
```

Class gathers all configuration information.

<a id="configuration.ConfigDashboard.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Intialize the class.

**Arguments**:

  None


**Returns**:

  None

<a id="configuration.ConfigDashboard.api_bind_port"></a>

#### api\_bind\_port

```python
def api_bind_port()
```

Get api_bind_port.

**Arguments**:

  None


**Returns**:

- `result` - result

<a id="configuration.ConfigDashboard.username"></a>

#### username

```python
def username()
```

Get username.

**Arguments**:

  None


**Returns**:

- `result` - result

<a id="uri"></a>

# uri

switchmap dashboard URIs.

<a id="uri.dashboard"></a>

#### dashboard

```python
def dashboard()
```

Create the dashboard  page URI.

**Arguments**:

  None


**Returns**:

- `result` - result

<a id="uri.historical_dashboard"></a>

#### historical\_dashboard

```python
def historical_dashboard(idx_root=1)
```

Create the dashboard  page URI.

**Arguments**:

- `idx_root` - Root index


**Returns**:

- `result` - result

<a id="uri.devices"></a>

#### devices

```python
def devices(idx_device)
```

Create the device page URI.

**Arguments**:

- `idx_device` - IDX of the device in the database


**Returns**:

- `result` - result

<a id="uri.events"></a>

#### events

```python
def events()
```

Create the event page URI.

**Arguments**:

  None


**Returns**:

- `result` - result

<a id="uri.events_by_idx_root"></a>

#### events\_by\_idx\_root

```python
def events_by_idx_root(idx_root=1)
```

Create the filtered event page URI.

**Arguments**:

- `idx_root` - Index of the root in the DB


**Returns**:

- `result` - result

<a id="uri.search_dashboard_server"></a>

#### search\_dashboard\_server

```python
def search_dashboard_server()
```

Create the device page URI.

**Arguments**:

  None


**Returns**:

- `result` - result

<a id="uri.search_api_server"></a>

#### search\_api\_server

```python
def search_api_server()
```

Create the device page URI.

**Arguments**:

  None


**Returns**:

- `result` - result

<a id="graphql_filters"></a>

# graphql\_filters

switchmap GraphQL filter operators.

<a id="graphql_filters.or_operator"></a>

#### or\_operator

```python
def or_operator(key, items)
```

Create a GraphQL filter string for OR operations.

**Arguments**:

- `key` - GraphQL key to run the OR operation against
- `items` - List of iitems for filtering


**Returns**:

- `result` - result

<a id="__init__"></a>

# \_\_init\_\_

Module of switchmap DASHBOARD routes.

Contains all routes that switchmap.s Flask webserver uses

<a id="__init__.inject"></a>

#### inject

```python
@DASHBOARD.context_processor
def inject()
```

Inject global variables for use by templates.

**Arguments**:

  None


**Returns**:

- `result` - Dict of url_home and url_static values for Flask to porcess

<a id="data"></a>

# data

Define the switchmap.dashboard.data package.

**Arguments**:

  None


**Returns**:

  None

<a id="data.interface"></a>

# data.interface

Module for parsing interface data from GraphQL JSON.

<a id="data.interface.Interface"></a>

## Interface Objects

```python
class Interface()
```

Class to create an InterfaceDataRow data.

<a id="data.interface.Interface.__init__"></a>

#### \_\_init\_\_

```python
def __init__(interface)
```

Instantiate the class.

**Arguments**:

- `interface` - Interface dict


**Returns**:

  None

<a id="data.interface.Interface.row"></a>

#### row

```python
def row()
```

Get Row data.

**Arguments**:

  None


**Returns**:

- `result` - InterfaceDataRow object

<a id="data.interface.Interface.cdp"></a>

#### cdp

```python
def cdp()
```

Return port CDP HTML string.

**Arguments**:

  None


**Returns**:

- `value` - required string

<a id="data.interface.Interface.duplex"></a>

#### duplex

```python
def duplex()
```

Return port duplex string.

**Arguments**:

  None


**Returns**:

- `duplex` - Duplex string

<a id="data.interface.Interface.lldp"></a>

#### lldp

```python
def lldp()
```

Return port LLDP HTML string.

**Arguments**:

  None


**Returns**:

- `value` - required string

<a id="data.interface.Interface.speed"></a>

#### speed

```python
def speed()
```

Return port speed.

**Arguments**:

  None


**Returns**:

- `result` - Port speed

<a id="data.interface.Interface.state"></a>

#### state

```python
def state()
```

Return InterfaceState object.

**Arguments**:

  None


**Returns**:

- `state` - InterfaceState object

<a id="data.interface.Interface.ts_idle"></a>

#### ts\_idle

```python
def ts_idle()
```

Return idle time.

**Arguments**:

  None


**Returns**:

- `result` - idle time

<a id="data.interface.Interface.vlan"></a>

#### vlan

```python
def vlan()
```

Return VLAN number.

**Arguments**:

  None


**Returns**:

- `result` - VlanState object

<a id="data.mac"></a>

# data.mac

Module for parsing Mac address related data from GraphQL JSON.

<a id="data.mac.Mac"></a>

## Mac Objects

```python
class Mac()
```

Class to create an InterfaceDataRow data.

<a id="data.mac.Mac.__init__"></a>

#### \_\_init\_\_

```python
def __init__(interface)
```

Instantiate the class.

**Arguments**:

- `interface` - Interface dict


**Returns**:

  None

<a id="data.mac.Mac.macs"></a>

#### macs

```python
def macs()
```

Get the MacState of the interface.

**Arguments**:

  None


**Returns**:

- `result` - List of MacState objects

<a id="data.mac.Mac.ips"></a>

#### ips

```python
def ips()
```

Get the IpState of the interface.

**Arguments**:

  None


**Returns**:

- `result` - List of IpState objects

<a id="data.mac.Mac.macips"></a>

#### macips

```python
def macips()
```

Get the MacIpState of the interface.

**Arguments**:

  None


**Returns**:

- `result` - List of MacIpState objects

<a id="data.mac.macips"></a>

#### macips

```python
def macips(interface)
```

Get the MacIpState of the interface.

**Arguments**:

- `interface` - IDX of the interface in the DB


**Returns**:

- `result` - List of MacIpState objects

<a id="data.system"></a>

# data.system

Class for creating device web pages.

<a id="data.system.System"></a>

## System Objects

```python
class System()
```

Class that creates the data to be presented for the device's ports.

<a id="data.system.System.__init__"></a>

#### \_\_init\_\_

```python
def __init__(system_data)
```

Instantiate the class.

**Arguments**:

- `system_data` - Dictionary of system data


**Returns**:

  None

<a id="data.system.System.rows"></a>

#### rows

```python
def rows()
```

Return data for the device's system information.

**Arguments**:

  None


**Returns**:

- `rows` - List of Col objects

<a id="data.system.System.hostname"></a>

#### hostname

```python
def hostname()
```

Return hostname.

**Arguments**:

  None


**Returns**:

- `result` - hostname

<a id="data.system.System.last_polled"></a>

#### last\_polled

```python
def last_polled()
```

Return last_polled.

**Arguments**:

  None


**Returns**:

- `result` - last_polled

<a id="data.system.System.sysdescription"></a>

#### sysdescription

```python
def sysdescription()
```

Return sysdescription.

**Arguments**:

  None


**Returns**:

- `result` - sysdescription

<a id="data.system.System.sysname"></a>

#### sysname

```python
def sysname()
```

Return sysname.

**Arguments**:

  None


**Returns**:

- `result` - sysname

<a id="data.system.System.sysobjectid"></a>

#### sysobjectid

```python
def sysobjectid()
```

Return sysobjectid.

**Arguments**:

  None


**Returns**:

- `result` - sysobjectid

<a id="data.system.System.sysuptime"></a>

#### sysuptime

```python
def sysuptime()
```

Return sysuptime.

**Arguments**:

  None


**Returns**:

- `result` - sysuptime

<a id="net"></a>

# net

Define the switchmap.dashboard.net package.

**Arguments**:

  None


**Returns**:

  None

<a id="net.routes.pages.search"></a>

# net.routes.pages.search

Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

<a id="net.routes.pages.search.search"></a>

#### search

```python
@SEARCH.route("/search", methods=["POST"])
def search()
```

Create the search page.

**Arguments**:

  None


**Returns**:

- `render_template` - HTML

<a id="net.routes.pages.search.get_tables"></a>

#### get\_tables

```python
def get_tables(_interfaces)
```

Convert interface information to HTML.

**Arguments**:

- `_interfaces` - List of interface data dicts


**Returns**:

- `result` - HTML

<a id="net.routes.pages.events"></a>

# net.routes.pages.events

Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

<a id="net.routes.pages.events.events"></a>

#### events

```python
@EVENT.route("/events")
def events()
```

Create the events page.

**Arguments**:

  None


**Returns**:

- `render_template` - HTML

<a id="net.routes.pages.devices"></a>

# net.routes.pages.devices

Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

<a id="net.routes.pages.devices.devices"></a>

#### devices

```python
@DEVICES.route("/devices/<int:idx_device>")
def devices(idx_device)
```

Crerate device tables.

**Arguments**:

- `idx_device` - Device index


**Returns**:

- `render_template` - HTML

<a id="net.routes.pages"></a>

# net.routes.pages

Define the switchmap.dashboard.net.routes.pages package.

**Arguments**:

  None


**Returns**:

  None

<a id="net.routes.pages.index"></a>

# net.routes.pages.index

Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

<a id="net.routes.pages.index.dashboard"></a>

#### dashboard

```python
@INDEX.route("/")
def dashboard()
```

Create the dashboard home page.

**Arguments**:

  None


**Returns**:

- `_dashboard` - HTML via function

<a id="net.routes.pages.index.historical_dashboard"></a>

#### historical\_dashboard

```python
@INDEX.route("/<int:idx_root>")
def historical_dashboard(idx_root)
```

Create the dashboard home page for a specific event index.

**Arguments**:

- `idx_root` - Event index


**Returns**:

- `_dashboard` - HTML via function

<a id="net.routes"></a>

# net.routes

Define the switchmap.dashboard.net.routes package.

**Arguments**:

  None


**Returns**:

  None

<a id="net.routes.api.api"></a>

# net.routes.api.api

Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

<a id="net.routes.api.api.dashboard"></a>

#### dashboard

```python
@API.route("/dashboard", methods=["GET"])
def dashboard()
```

Get dashboard data.

**Arguments**:

  None


**Returns**:

- `html` - Webpage HTML

<a id="net.routes.api.api.historical_dashboard"></a>

#### historical\_dashboard

```python
@API.route("/dashboard/<int:idx_root>", methods=["GET"])
def historical_dashboard(idx_root)
```

Get dashboard data.

**Arguments**:

- `idx_root` - IDX of the root in the DB


**Returns**:

- `html` - Webpage HTML

<a id="net.routes.api.api.event_by_idx_root"></a>

#### event\_by\_idx\_root

```python
@API.route("/events/<int:idx_root>", methods=["GET"])
def event_by_idx_root(idx_root)
```

Get event data.

**Arguments**:

- `idx_root` - IDX of the root in the DB


**Returns**:

- `result` - JSON of zone data

<a id="net.routes.api.api.events"></a>

#### events

```python
@API.route("/events", methods=["GET"])
def events()
```

Get event data.

**Arguments**:

  None


**Returns**:

- `result` - JSON of zone data

<a id="net.routes.api.api.devices"></a>

#### devices

```python
@API.route("/devices/<int:idx_device>", methods=["GET"])
def devices(idx_device)
```

Get device data.

**Arguments**:

- `idx_device` - IDX of the DB device table


**Returns**:

- `result` - JSON of zone data

<a id="net.routes.api.api.search"></a>

#### search

```python
@API.route("/search", methods=["POST"])
def search()
```

Get device data.

**Arguments**:

  None


**Returns**:

- `result` - JSON of zone data

<a id="net.routes.api.api.roots_filter"></a>

#### roots\_filter

```python
def roots_filter(idx_root=False)
```

Get event data.

**Arguments**:

- `idx_root` - IDX of the DB root


**Returns**:

- `roots` - JSON of zone data

<a id="net.routes.api"></a>

# net.routes.api

Define the switchmap.dashboard.net.routes.api package.

**Arguments**:

  None


**Returns**:

  None

<a id="net.html.pages.device"></a>

# net.html.pages.device

Class for creating device web pages.

<a id="net.html.pages.device.Device"></a>

## Device Objects

```python
class Device()
```

Class that creates the device's various HTML tables.

<a id="net.html.pages.device.Device.__init__"></a>

#### \_\_init\_\_

```python
def __init__(data)
```

Initialize the class.

**Arguments**:

- `data` - Device dictionary


**Returns**:

  None

<a id="net.html.pages.device.Device.hostname"></a>

#### hostname

```python
def hostname()
```

Get the system hostname.

**Arguments**:

  None


**Returns**:

- `result` - The system hostname

<a id="net.html.pages.device.Device.interfaces"></a>

#### interfaces

```python
def interfaces()
```

Create the ports table for the device.

**Arguments**:

  None


**Returns**:

- `html` - HTML table string

<a id="net.html.pages.device.Device.system"></a>

#### system

```python
def system()
```

Create summary table for the devie.

**Arguments**:

  None


**Returns**:

- `html` - HTML table string

<a id="net.html.pages.search"></a>

# net.html.pages.search

Class for creating search web pages.

<a id="net.html.pages.search.SearchPage"></a>

## SearchPage Objects

```python
class SearchPage()
```

Class that creates the search's various HTML tables.

<a id="net.html.pages.search.SearchPage.__init__"></a>

#### \_\_init\_\_

```python
def __init__(data, hostname=None)
```

Initialize the class.

**Arguments**:

- `data` - Search dictionary
- `hostname` - The name of the Device


**Returns**:

  None

<a id="net.html.pages.search.SearchPage.html"></a>

#### html

```python
def html()
```

Create the ports table for the search.

**Arguments**:

  None


**Returns**:

- `html` - HTML table string

<a id="net.html.pages.events"></a>

# net.html.pages.events

Class for creating home web pages.

<a id="net.html.pages.events.EventPage"></a>

## EventPage Objects

```python
class EventPage()
```

Class that creates the homepages's various HTML tables.

<a id="net.html.pages.events.EventPage.__init__"></a>

#### \_\_init\_\_

```python
def __init__(_events)
```

Initialize the class.

**Arguments**:

- `_events` - Events to process


**Returns**:

  None

<a id="net.html.pages.events.EventPage.html"></a>

#### html

```python
def html()
```

Create HTML table for the events.

**Arguments**:

  None


**Returns**:

- `result` - HTML table string

<a id="net.html.pages.layouts"></a>

# net.html.pages.layouts

Module of page layout functions.

<a id="net.html.pages.layouts.table_wrapper"></a>

#### table\_wrapper

```python
def table_wrapper(title, table, strip=True)
```

Wrap the data in HTML stuff.

**Arguments**:

- `title` - title
- `table` - Table HTML
- `strip` - Strip the thead if True


**Returns**:

- `result` - HTML

<a id="net.html.pages.layouts.remove_thead"></a>

#### remove\_thead

```python
def remove_thead(data)
```

Remove line in HTML code containing the 'thead'.

**Arguments**:

- `data` - HTML code


**Returns**:

- `result` - HTML

<a id="net.html.pages"></a>

# net.html.pages

Define the switchmap.dashboard.net.html.pages package.

**Arguments**:

  None


**Returns**:

  None

<a id="net.html.pages.index"></a>

# net.html.pages.index

Class for creating home web pages.

<a id="net.html.pages.index.IndexPage"></a>

## IndexPage Objects

```python
class IndexPage()
```

Class that creates the homepages's various HTML tables.

<a id="net.html.pages.index.IndexPage.__init__"></a>

#### \_\_init\_\_

```python
def __init__(zones)
```

Initialize the class.

**Arguments**:

- `zones` - List of zones


**Returns**:

  None

<a id="net.html.pages.index.IndexPage.html"></a>

#### html

```python
def html()
```

Create HTML table for the devices.

**Arguments**:

  None


**Returns**:

- `result` - HTML table string

<a id="net.html"></a>

# net.html

Define the switchmap.dashboard.net.html package.

**Arguments**:

  None


**Returns**:

  None

<a id="table"></a>

# table

Define the switchmap.dashboard.table package.

**Arguments**:

  None


**Returns**:

  None

<a id="table.device"></a>

# table.device

Class for creating device web pages.

<a id="table.device.Device"></a>

## Device Objects

```python
class Device()
```

Class that creates the device's various HTML tables.

<a id="table.device.Device.__init__"></a>

#### \_\_init\_\_

```python
def __init__(data)
```

Initialize the class.

**Arguments**:

- `data` - Device dictionary


**Returns**:

  None

<a id="table.device.Device.interfaces"></a>

#### interfaces

```python
def interfaces()
```

Create the ports table for the device.

**Arguments**:

  None


**Returns**:

- `table` - Interface table

<a id="table.device.Device.system"></a>

#### system

```python
def system()
```

Create summary table for the devie.

**Arguments**:

  None


**Returns**:

- `table` - System table

<a id="table.search"></a>

# table.search

Class for creating search web pages.

<a id="table.search.Search"></a>

## Search Objects

```python
class Search()
```

Class that creates the search's various HTML tables.

<a id="table.search.Search.__init__"></a>

#### \_\_init\_\_

```python
def __init__(data)
```

Initialize the class.

**Arguments**:

- `data` - Search dictionary


**Returns**:

  None

<a id="table.search.Search.interfaces"></a>

#### interfaces

```python
def interfaces()
```

Create the ports table for the search.

**Arguments**:

  None


**Returns**:

- `table` - Interface table

<a id="table.interfaces"></a>

# table.interfaces

Class for creating device web pages.

<a id="table.interfaces._RawCol"></a>

## \_RawCol Objects

```python
class _RawCol(Col)
```

Class outputs whatever it is given and will not escape it.

<a id="table.interfaces._RawCol.td_format"></a>

#### td\_format

```python
def td_format(content)
```

Format the column content without escaping.

**Arguments**:

- `content` - The content to be displayed in the column


**Returns**:

- `content` - The unmodified content

<a id="table.interfaces.InterfaceTable"></a>

## InterfaceTable Objects

```python
class InterfaceTable(Table)
```

Declaration of the columns in the Ports table.

<a id="table.interfaces.InterfaceTable.get_tr_attrs"></a>

#### get\_tr\_attrs

```python
def get_tr_attrs(item)
```

Apply CSS class attributes to regular table row.

**Arguments**:

- `item` - Row data object containing interface information


**Returns**:

- `dict` - CSS class mapping based on interface state

<a id="table.interfaces.InterfaceRow"></a>

## InterfaceRow Objects

```python
class InterfaceRow()
```

Declaration of the rows in the Interfaces table.

<a id="table.interfaces.InterfaceRow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(row)
```

Initialize the class.

**Arguments**:

- `row` - List of row values
- `port` - Interface name string
- `vlan` - VLAN of port string
- `state` - State of port string
- `days_inactive` - Number of days the port's inactive string
- `speed` - Speed of port string
- `duplex` - Duplex of port string
- `label` - Label given to the port by the network manager
- `trunk` - Whether a trunk or not
- `cdp` - CDP data string
- `lldp` - LLDP data string
- `mac_address` - MAC Address
- `organization` - Name of the organization


**Returns**:

  None

<a id="table.interfaces.InterfaceRow.active"></a>

#### active

```python
def active()
```

Determine if the interface is active.

**Arguments**:

  None


**Returns**:

- `bool` - True if interface state is 'Active', False otherwise

<a id="table.interfaces.InterfaceRow.enabled"></a>

#### enabled

```python
def enabled()
```

Determine if the interface is enabled.

**Arguments**:

  None


**Returns**:

- `bool` - True if interface state is not 'Disabled', False otherwise
  boolean value of state if is not Disabled.

<a id="table.interfaces.table"></a>

#### table

```python
def table(_interfaces)
```

Get Interface data from the device.

**Arguments**:

- `_interfaces` - Interface dict


**Returns**:

- `table` - InterfaceTable object

<a id="table.events"></a>

# table.events

Class for creating home web pages.

<a id="table.events._RawCol"></a>

## \_RawCol Objects

```python
class _RawCol(Col)
```

Class outputs whatever it is given and will not escape it.

Extends the Col class to provide raw HTML output without escaping.

<a id="table.events._RawCol.td_format"></a>

#### td\_format

```python
def td_format(content)
```

Format the column content without escaping.

**Arguments**:

- `content` - The content to be displayed in the column


**Returns**:

- `content` - The unmodified content

<a id="table.events.EventTable"></a>

## EventTable Objects

```python
class EventTable(Table)
```

Declaration of the columns in the Events table.

<a id="table.events.EventsRow"></a>

## EventsRow Objects

```python
class EventsRow()
```

Declaration of the rows in the Events table.

<a id="table.events.EventsRow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(row_data)
```

Initialize the class.

**Arguments**:

- `row_data` - List containing the data for each column in the row


**Returns**:

  None

<a id="table.events.table"></a>

#### table

```python
def table(events)
```

Return data for the event's information.

Creates a formatted table object from a list of events.

**Arguments**:

- `events` - List of EventMeta objects


**Returns**:

- `result` - EventTable object or False if no valid rows

<a id="table.system"></a>

# table.system

Class for creating device web pages.

<a id="table.system._RawCol"></a>

## \_RawCol Objects

```python
class _RawCol(Col)
```

Class outputs whatever it is given and will not escape it.

<a id="table.system._RawCol.td_format"></a>

#### td\_format

```python
def td_format(content)
```

Format the column content without escaping.

**Arguments**:

- `content` - The content to be displayed in the column


**Returns**:

- `content` - The unmodified content

<a id="table.system.SystemTable"></a>

## SystemTable Objects

```python
class SystemTable(Table)
```

Declaration of the columns in the Systems table.

<a id="table.system.SystemRow"></a>

## SystemRow Objects

```python
class SystemRow()
```

Declaration of the rows in the Systems table.

<a id="table.system.SystemRow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(row)
```

Initialize the class.

**Arguments**:

- `row` - SystemDataRow object containing parameter and value


**Returns**:

  None

<a id="table.system.table"></a>

#### table

```python
def table(data)
```

Create summary table for the devie.

**Arguments**:

- `data` - Dictionary containing system information data


**Returns**:

- `html` - HTML table string or None if no rows are present

<a id="table.index"></a>

# table.index

Class for creating home web pages.

<a id="table.index._RawCol"></a>

## \_RawCol Objects

```python
class _RawCol(Col)
```

Class outputs whatever it is given and will not escape it.

<a id="table.index._RawCol.td_format"></a>

#### td\_format

```python
def td_format(content)
```

Fix the column formatting.

**Arguments**:

- `content` - Content to parse


**Returns**:

- `content` - Content to parse

<a id="table.index.tables"></a>

#### tables

```python
def tables(zones)
```

Create HTML table for the devices.

**Arguments**:

- `zones` - List of Zones


**Returns**:

- `results` - List of ZoneTable objects

<a id="table.index.ZoneTable"></a>

## ZoneTable Objects

```python
class ZoneTable(Table)
```

Declaration of the columns in the Devices table.

<a id="table.index.ZoneRow"></a>

## ZoneRow Objects

```python
class ZoneRow()
```

Declaration of the rows in the Devices table.

<a id="table.index.ZoneRow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(row_data)
```

Initialize the class.

**Arguments**:

- `row_data` - Row data


**Returns**:

  None

<a id="table.index.rows"></a>

#### rows

```python
def rows(devices)
```

Return data for the device's system information.

**Arguments**:

- `devices` - List of DeviceMeta objects


**Returns**:

- `rows` - List of Col objects
