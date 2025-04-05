---
title: Architecture
sidebar_label: Architecture
sidebar_position: 9
---

# Architecture

This page outlines the architecture and components of `switchmap-ng`

## Poller

This section explains how polling operates.

### How Devices are Polled

- The following refers to files in the `switchmap.poller.snmp` folder:
  - 1. Modules supporting all MIBs are imported from `__init__.py`.
  - 2. The `iana_enterprise.py` module to determine the manufacturer which is then used in collating the data.
  - 3. For each device OIDs in the MIBs are polled using `snmp_info.py`. OIDs not supported by the app are ignored.
    - 1. Some Layer 1 and Layer 2 data may be found using the `ifIndex` id (some Cisco devices), or that of the spanning tree port index. The `switchmap/poller/snmp/mib/generic/mib_bridge.py` determines which methodology is used by the device and returns values keyed by `ifIndex` for consistency.
  - 4. This results in a `dict` with keys for Layer 1, Layer 2 and Layer 3 information in the [OSI model](https://en.wikipedia.org/wiki/OSI_model).
    - 1. The Layer 1 and Layer 2 information are keyed by `ifIndex`.

### Processing Polled OSI Model Data

- The following refers to files in the `switchmap.poller.update` folder.
- Different manufacturers use different MIBs to do the same thing. The `device.py` module attempts to update the `dict` obtained from polled data to create a uniform format suitable for updating the database.
  - 1. Iterates through each Layer 1 interface by `ifIndex` number.
  - 2. Extracts data to be more suitable for updating the database. This includes:
    - 1. VLAN (Some manufacturers assign them to the physical interface, others to a virtual subinterface.)
    - 2. Duplex
    - 3. Speed
    - 4. Trunk status
  - 3. This data is then posted to the API in JSON format.

## Ingester

This section explains how database updates operate.

- The posted polled data is stored on disk on the API server in YAML format for ease of human readability.
- The ingester reads the datafiles and processes them like this:
  - 1. Network devices in the same routing or VLAN domain will often observe the same information such as IP and MAC addresses.
  - 2. The ingester processes these and deduplicates the information before adding it to the database. This information is often needed before processing the interface information to help cross referencing.
    - 1. All IP address, MAC address and VLAN data in a particular Zone in the configuration file are processed first.
    - 2. The remaining information is then processed linking to the IP address, MAC address and VLAN database foreign keys previously created.
  - 3. The update is done using the Python multiprocessing module for speed.



## Overview of Microservices and Data Flow

**Switchmap-NG is structured as four cooperative microservices – Poller, Server (API), and Dashboard** – which together form a pipeline for collecting, processing, and displaying network device data. The Poller gathers raw SNMP data,and sends it to the Server, After processing it the Server provides API access via `REST/GraphQL` to that data, and the Dashboard Renders it.

### Step-by-Step Data Flow (Poller → Dashboard):

#### SNMP Polling (Poller):
- The Poller service periodically collects SNMP data from configured network devices (switches, routers, etc.) using multiple threads for efficiency.  
- It leverages vendor-specific MIB modules to retrieve Layer1/2/3 information (port status, VLANs, ARP tables, etc.) via SNMP OIDs.
- For example, the module in `switchmap/poller/snmp/iana_enterprise.py` identifies each device’s vendor to pick the correct MIB set, and modules like `snmp_info.py` perform the low-level SNMP GETs for supported OIDs (unsupported OIDs are ignored).
- A generic bridge logic in `mib_bridge.py` normalizes differences in interface indexing (e.g. mapping spanning-tree indices to ifIndex) so that data keys are consistent by ifIndex.

#### Data Formatting (Poller):
- The raw SNMP results are assembled into a Python dictionary categorized by OSI layer (Layer1 interfaces, Layer2 VLAN/trunk info, Layer3 IP/MAC info).
- The Poller then refines this data into a uniform schema suitable for the database.
- The `switchmap/poller/update/device.py` module iterates through each interface (by ifIndex) and enriches/extracts fields like VLAN assignments, duplex mode, link speed, and trunk status in a consistent format.
- This yields a standardized JSON-like structure representing the device’s state.

#### Publishing to API Server:
- Once a device’s data is prepared, the Poller posts it to the Switchmap-NG API server.
- The data is transmitted in JSON format over HTTP.
- In the current code, this happens via an HTTP POST to an API endpoint on the Server, with each Poller (there can be multiple instances in different zones) configured with the central Server’s address and credentials.
- This decouples polling from database writes and allows distributed pollers to feed a central system.

#### Caching on API Server:
- The Server (API service) receives the Poller’s JSON payload and temporarily stores it on disk as a cache file in YAML format for readability.
- This cached file resides on the API server’s filesystem (typically under a cache/ directory) and contains the polled device data just received.
- Staging the data in cache files ensures that the next step (database ingestion) can occur asynchronously, without blocking the Poller or API request.

#### Data Ingestion and Deduplication (Core Ingester):
- The Core service (also called the Ingester daemon) continuously watches for new cache files on the API server.
- At a configured interval (`ingest_interval`), it reads any new polled data files.
- The Core’s logic then deduplicates and processes the data before inserting it into the MySQL database.
- Deduplication is crucial for information that might appear on multiple devices – for example, the same MAC address or IP may be seen in the ARP tables of two switches in the same network.
- The Ingester first consolidates all IP address, MAC address, and VLAN records for the site (zone) across devices, storing each unique entry only once.
- Next, it processes the interface-specific data, linking ports to those unified IP/MAC/VLAN records via foreign keys in the DB.
- This two-phase ingest ensures cross-device references are resolved before port records are stored.
- The Core uses SQLAlchemy models to map these records into the MySQL database, performing inserts/updates.
- Notably, the ingestion uses Python’s multiprocessing to speed up bulk database operations by parallelizing work across CPU cores.
- If `purge_after_ingest` is true, the cache file is deleted once its data is committed, so the system only keeps the latest snapshot per device.

#### API Server – Database Access:
- With the fresh data now in the database, the API Server can fulfill data queries.
- The Server microservice runs a Flask-based web API (by default on port 7000) and exposes both a RESTful interface and a GraphQL endpoint for clients.
- Under the hood, Switchmap-NG defines SQLAlchemy ORM models (for devices, interfaces, IPs, VLANs, etc.) in its core modules, and uses Graphene (GraphQL for Python) to map these models to a GraphQL schema.
- The `switchmap/server/api/routes/graphql.py` module sets up GraphQL query and mutation routes. This allows flexible retrieval of network inventory data in a single query.
- The API server may also provide predefined REST endpoints returning JSON data.
- When the Dashboard or any client requests data, the Server reads from the MySQL database (using the ORM) to gather the latest information.
- In essence, the Server is stateless regarding data – the authoritative state lives in the DB, and the server queries it on demand.

#### Dashboard (Front-End):
- The Dashboard is a single-page application that provides a user interface for viewing network data.
- It runs as a separate service (by default, a web server on port 7001).
- When a user visits the dashboard, the app communicates with the Server’s API (typically via AJAX calls or GraphQL queries) to retrieve the device and interface data.
- For example, the dashboard’s main view might call the API to list all monitored devices, and clicking on a device issues another API request to get detailed interface information.
- The API responds with JSON data, which the front-end uses to render tables and charts. The Dashboard is dynamic – it periodically or on-demand fetches updates.


# End-to-End Data Flow

Putting it all together, here’s how data flows through Switchmap-NG from the network devices to the user interface:

## SNMP Polling
- The **Poller** daemon periodically connects to each configured network device using SNMP (v2c/v3) as specified in the config.
- It collects interface statuses, MAC tables, VLAN info, ARP entries, etc., using OIDs defined in SNMP modules.
- The polled data for each device is assembled into a Python dictionary, later serialized into YAML/JSON.

## Sending to Server
- After collecting data for a device, the Poller sends it to the central **API Server**.
- By default, this occurs via an HTTP `POST` to `/post/poller`.
- The request includes a “misc” section with the device hostname and zone to identify the data.

## Caching and Ingestion
- The API Server receives the POST and writes the JSON payload into a **YAML file** in a configured `cache_directory`.
- An ingest worker (part of the API Server or a separate “Ingester” daemon) periodically scans for new cache files.
- It reads each file, parses the data, and uses ORM models to **insert or update** records in the MySQL database.
- If `purge_after_ingest` is enabled, the cache file is removed upon successful DB update.

## Database Storage
- The MySQL database holds the latest snapshot of the network state.
- Each poll refreshes the database with up-to-date device, interface, and VLAN info.
- Depending on configuration, historical data may be retained or only current info stored.

## User Requests Dashboard
- A user accesses the Dashboard (e.g., `http://<server>:7001/switchmap/dashboard`).
- The Dashboard Flask app calls the **API Server** to obtain device lists, statuses, etc.
- The API Server queries the MySQL database (via SQLAlchemy) for the requested data.

## Data to Dashboard
- The **API Server** returns JSON (or responds to GraphQL queries) with the necessary information.
- The Dashboard processes this data, converting it into tables or other UI elements.
- For device details, the Dashboard might call `/switchmap/api/devices/<id>` to retrieve interface info, system details, etc.

## Rendering HTML
- The Dashboard uses data classes (in `dashboard/data/`) to structure the JSON into an HTML-friendly format.
- Flask templates (Jinja2) then render the pages, inserting the data into tables and sections.
- The user’s browser receives fully rendered HTML pages with the latest polled information.

## User Interaction
- The user can navigate between devices, perform searches, or view event logs.
- Each action triggers a new API call from the Dashboard to the Server, fetching fresh data from the database.
- For example, a search page might POST a query to `/post/search`, and the API returns matching results, which the Dashboard displays.

By separating roles—Poller for SNMP collection, API Server for ingestion/data access, and Dashboard for presentation—**Switchmap-NG** remains modular and scalable. Its microservice-like layout (`switchmap/poller`, `switchmap/server`, `switchmap/dashboard`, `switchmap/core`) keeps each layer focused on its specific tasks.
