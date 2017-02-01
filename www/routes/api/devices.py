"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint

# Infoset-ng imports
from www import CONFIG
from www.pages import device

# Define the DEVICES global variable
DEVICES = Blueprint('DEVICES', __name__)


@DEVICES.route('/devices/<ip_address>', methods=["GET"])
def fetch_table(ip_address):
    """Return Network Layout tables.

    Args:
        ip_address: Host IP

    Returns:
        HTML string of host table

    """
    # Get HTML
    html = device.create(CONFIG, ip_address)

    # Return
    return html
