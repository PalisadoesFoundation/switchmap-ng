"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint

# Application imports
from switchmap import Config
from switchmap.dashboard.pages import device

# Define the DASHBOARD_DEVICES global variable
DASHBOARD_DEVICES = Blueprint("DASHBOARD_DEVICES", __name__)


@DASHBOARD_DEVICES.route("/devices/<ip_address>", methods=["GET"])
def fetch_table(ip_address):
    """Return Network Layout tables.

    Args:
        ip_address: Host IP

    Returns:
        HTML string of host table

    """
    # Get HTML
    html = device.create(Config, ip_address)

    # Return
    return html
