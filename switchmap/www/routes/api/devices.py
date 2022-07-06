"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint

# Application imports
from switchmap import Config
from switchmap.www.pages import device

# Define the API_DEVICES global variable
API_DEVICES = Blueprint('API_DEVICES', __name__)


@API_DEVICES.route('/devices/<ip_address>', methods=["GET"])
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
