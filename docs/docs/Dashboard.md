# Dashboard

The **Dashboard** is a Flask-based web server that **renders HTML pages** using data from the API Server. Its code resides in the `switchmap/dashboard/` folder, containing route definitions, data formatting logic, and Jinja2 templates.

## Web Framework

- Uses **Flask** as the primary web framework.
- Organized into **Flask Blueprints** for different pages (e.g., devices, events, search).
- Modules like `index.py`, `devices.py`, `events.py` define routes under `switchmap/dashboard/net/routes/pages/`.
- Each route calls the backend API to fetch fresh data, then populates a Jinja2 template.

## Data Fetching

- The Dashboard does **not** query the database directly.
- It calls the **API Server** via HTTP, using a core REST client helper (`rest.get`, etc.).
- Example: `rest.get(uri.devices(idx_device), config, server=False)` retrieves JSON data for a specific device ID.
- Raw JSON responses are processed by data classes (under `switchmap/dashboard/data/`) to form tables or contexts suitable for templates.

## Templating and UI

- Uses **Jinja2** templates in `switchmap/dashboard/net/html/templates/default/` (e.g., `index.html`, `device.html`).
- A base layout (`base.html`) provides site-wide structure (navigation, header, footer).
- The UI is styled with a **Bootstrap-based admin theme**, offering a responsive interface.
- Static assets (CSS, JS, images) are located in `dashboard/net/html/static/`.

## Routes and Pages

- The main Dashboard page is typically at `/switchmap/dashboard` (configured by `DASHBOARD_PREFIX`).
- Clicking a device link (e.g., `/switchmap/dashboard/devices/<id>`) shows detailed interface info for that device.
- Additional pages include **events** (logs/changes) and **search** (to find devices or interfaces).
- Each page’s route transforms API responses into HTML tables and calls `render_template(...)` with the relevant data.

## Frameworks and Libraries

- Primarily **Flask** + **Bootstrap** (the SB Admin theme).
- May also use some **JavaScript** or jQuery plugins for interactive elements.
- Renders most data server-side, always requesting fresh information from the API when a page loads.

## Configuration

- Reads settings (like API server host/port, dashboard port) from the `dashboard:` section of the config.
- Often runs on **port 7001** while the API server runs on **port 7000**.
- Can be deployed behind an existing web server for SSL or load balancing if needed.

## Summary

The **Dashboard** is a Flask application that provides the **user-facing HTML**. By **pulling data** from the API Server whenever a page loads, it ensures the interface reflects the **latest polled network info**. This **separation of concerns** lets the dashboard scale or be hosted separately from the polling and ingestion processes, functioning like the **View** in a classic MVC pattern, with the API server acting as the **Model**.
