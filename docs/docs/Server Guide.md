# API Server 

The **API Server** is the central backend that receives data from pollers, stores it, and serves it to the Dashboard. It interacts with both the **Poller** and the **Dashboard**, as well as a MySQL-compatible database. Its code resides in the `switchmap/server/` package (“server” modules).

## Data Ingestion (Ingester)

- The API server runs an **ingester** process or thread to handle incoming Poller data.  
- When a Poller sends an HTTP POST to the API (e.g., `POST /switchmap/post/poller`), the server **temporarily writes** the JSON payload to a **YAML file** in a cache directory.  
  - This approach lets pollers quickly drop off data.  
- A **separate ingest routine** (running at a configurable interval) watches the cache directory, **parses new YAML**, and **updates the MySQL database**.  
- After successful ingest, the cache file may be removed if `purge_after_ingest` is enabled.  
- This system ensures poller data ultimately reaches the database, either directly or via cached files.

## Database Layer

- The server uses **SQLAlchemy ORM** to access a MySQL-compatible RDBMS, storing network inventory and status.  
- Schema definitions and models (e.g., for devices, interfaces, VLANs) live in `switchmap/server/db/models.py`.  
- Additional database logic:
  - `schemas.py` – Defines GraphQL schema objects.  
  - `attributes.py` – Maps attribute names to schema fields.  
- The **server** initializes a DB connection pool (configurable in `server:` config) and uses these models to **create or update entries** upon SNMP data arrival.

## API Endpoints

The API server exposes data via **web endpoints** (defined in `switchmap/server/api/routes/`). There are two main types:

### 1. Ingestion Endpoints (POST)

- Examples: `/switchmap/post/poller` for poller data or `/switchmap/post/search` for search queries.  
- The Poller POST handler **caches the file** and returns "OK," deferring DB writes to the ingester.  
- The search POST might cache a search term or directly query the DB.

### 2. Query Endpoints (GET/GraphQL)

- Provide **read access** to stored data, typically via a **GraphQL API** (and possibly some REST-like routes).  
- For instance, the Dashboard calls `GET /switchmap/api/devices/<id>` to fetch device details.  
- Internally, this may correspond to a GraphQL query or direct DB query, resolved by **Graphene** in `server/api/routes/graphql.py` and `db/schemas.py`.  
- The server may also offer an **interactive GraphiQL UI** at `/switchmap/api/igraphql` for debugging.  
- Overall, the API can respond with JSON data for devices, interfaces, events, etc., using GraphQL or preset routes.


## Integration with Poller & Dashboard

- The API server acts as a **hub**. Multiple pollers can **post data** to it over HTTP.  
- The Dashboard (and other clients) **query** the API server for the latest information.  
- Only one API server typically writes to the DB at a time, ensuring data consistency.  
- You can run multiple dashboards pointing to the same server, but a single server usually manages data ingestion for one system.


## Structure

- Located in the `switchmap/server` package, split into:
  - **api/**: Flask blueprint routes and request handling.  
  - **db/**: Database models, schema, and ingest logic.  
- Implemented as a **Flask** app (similar to the Dashboard), with blueprints like **API_POST** (for `/post` routes) and others for GraphQL queries.  
- Runs on a configurable host/port (default **7000**) and can be secured by HTTPS/basic auth (per config).  


The **API Server** bridges data collection and data presentation. It ingests raw poller data, manages database updates, and offers structured endpoints for the Dashboard or other clients to retrieve network information.
