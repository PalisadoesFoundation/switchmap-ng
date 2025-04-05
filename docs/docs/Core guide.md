# Core Services 

The `switchmap/core/` folder houses **foundational utilities and abstractions** used by all other components. This design minimizes code duplication and standardizes behavior across the Poller, Server, and Dashboard.


## Configuration Management

- Provides classes for parsing YAML configuration files.
- `configuration.py` defines `ConfigPoller`, `ConfigServer`, `ConfigDashboard` for each section of the config.
- Methods like `.zones()` (for the Poller) and `.cache_directory()` (for the Server) simplify retrieving specific settings.

## Logging

- `log.py` defines a **standardized logging system** with helper methods (`log2debug`, `log2info`).
- Ensures consistent formatting and a shared log directory (configurable in `core:` settings).
- All modules log to the same files, aiding in unified debugging.

## File & Daemon Utilities

- `files.py` manages file operations (e.g., reading/writing YAML or JSON) and handles “skip” files to stop daemons.
- `daemon.py` may provide logic to run system processes as UNIX daemons (PID files, signal handling).
- Streamlines how the Poller and Server read config and write cache files using PyYAML under the hood.

## Network/REST Helpers

- `rest.py` offers simplified GET/POST methods (e.g., `rest.post(url, data, config)`).
- Used by both Poller and Dashboard to communicate with the API server via HTTP.
- Encapsulates error handling, logging, and authentication in one place.

## GraphQL Schema

- `graphene.py` coordinates the GraphQL schema initialization, possibly containing shared resolvers or object types.
- Primarily supports the API server’s GraphQL layer, but can also provide utilities for the Dashboard if needed.

## General Constants & Variables

- In `variables.py` and `switchmap/__init__.py`, centralized constants exist (e.g., `SITE_PREFIX`, `API_PREFIX`) to standardize paths.
- Defines agent process names (Poller, Ingester, Dashboard, Server) for logs and file references.
- Encourages consistent usage of paths and service identifiers across all modules.

## Process Coordination

- `agent.py` might offer a CLI or scripts to start/stop the Poller, Server, or Dashboard.
- Could handle command-line arguments, environment checks, and call logging routines (`log.check_environment()`).
- Simplifies the user experience of managing multiple microservices.

**Overall**, the **core** module provides **shared infrastructure**—configuration parsing, logging, HTTP utilities, and common definitions—so each microservice (Poller, API Server, Dashboard) can focus on its **specific logic** while relying on `switchmap.core` for foundational services.
