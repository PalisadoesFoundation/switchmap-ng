"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Standard imports
from collections import defaultdict

# Flask imports
from flask import Blueprint, request, render_template

# Application imports
from switchmap.dashboard import uri
from switchmap.core import rest
from switchmap.dashboard.configuration import ConfigDashboard
from switchmap.dashboard.net.html.pages.search import SearchPage

# Define the SEARCH global variable
SEARCH = Blueprint("SEARCH", __name__)


@SEARCH.route("/search", methods=["POST"])
def search():
    """Create the search page.

    Args:
        None

    Returns:
        render_template: HTML

    """
    # Initialize key variables
    tables = {}
    idx_root = 1
    date = ""

    # Get data to display
    config = ConfigDashboard()

    # Get search form data
    items = request.form

    # Get the idx_root value for the search
    for key, value in items.items():
        if key == "idx_root":
            idx_root = int(str(value.strip()))
            break

    # Get the event create date
    event_get_response = rest.get(
        uri.events_by_idx_root(idx_root),
        config,
        server=False,
    )
    if bool(event_get_response) is True:
        # event_data = event_get_response.response.json()
        date = event_get_response[0]["event"]["tsCreated"]

    for key, value in items.items():
        # 'search_term' comes from the search form HTML
        if key == "search_term":
            # Post the search term to to the remote API server. The response
            # will be list of idx_l1interfaces that are associated with the
            # search term.
            search_dict = {"idx_root": idx_root, "searchterm": value.strip()}
            idx_post_response = rest.post(
                uri.search_api_server(), search_dict, config, server=True
            )

            # Process the list of idx_l1interfaces if there is
            # a successful response
            if bool(idx_post_response.success) is True:
                # Process data if found
                idx_l1interfaces = idx_post_response.response.json()
                if bool(idx_l1interfaces) is True:
                    # Get data from the API server using GraphQL.
                    # This is the standardized way we get GraphQL data.
                    # This may need to be streamlined later.
                    interfaces_post_response = rest.post(
                        uri.search_dashboard_server(),
                        idx_l1interfaces,
                        config,
                        server=False,
                    )

                    # Get the table HTML by parsing the GraphQL output
                    if bool(interfaces_post_response.success) is True:
                        interfaces = interfaces_post_response.response.json()
                        tables = get_tables(interfaces)

    # Convert data to HTML and return it to the browser
    return render_template(
        "search.html", results_dict=tables, idx_root=idx_root, date=date
    )


def get_tables(_interfaces):
    """Convert interface information to HTML.

    Args:
        _interfaces: List of interface data dicts

    Returns:
        result: HTML

    """
    # Initialize key variables
    device_key = "device"
    result = {}
    default = "<h3>&nbsp;Not Found</h3>"
    zones = defaultdict(lambda: defaultdict(lambda: []))
    result = defaultdict(lambda: "")

    if bool(_interfaces) is True:
        # Populate the device dictionary
        for next_interface in _interfaces:
            # Create a list of devices for port table generation
            next_device = next_interface.get(device_key)
            if bool(next_device) is True:
                # Remove non interface data for the interface dict
                del next_interface[device_key]

                # Extract device information
                next_hostname = next_device.get("hostname", "")
                zone_dict = next_device.get("device", "")
                next_zone = (
                    zone_dict.get("name", "") if bool(zone_dict) else ""
                )

                # Populate the zones dict
                zones[next_zone][next_hostname].append(next_interface)

        # Create the HTML dictionary for tables
        if bool(zones) is True:
            # Iterate over the devices in the zone
            for zone, device in sorted(zones.items()):
                # Iterate over the interfaces on the device
                for hostname, interfaces in sorted(device.items()):
                    # Create a search object for each device in the zone
                    search = SearchPage(interfaces, hostname=hostname)

                    # Append the results for the zone together
                    result[zone] = f"{result[zone]}\n{search.html()}"
        else:
            result[""] = default
    else:
        result[""] = default

    return result
