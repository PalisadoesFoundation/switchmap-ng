"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint, render_template

# Switchmap-NG imports
from switchmap.www.pages.device import Device
from switchmap.topology.ports import Lookup
from switchmap.www import CONFIG

# Define the DEVICES global variable
DEVICES = Blueprint("DEVICES", __name__)


@DEVICES.route("/devices/<hostname>")
def index(hostname):
    """Function for creating device tables.

    Args:
        None

    Returns:
        HTML

    """
    # Get device data
    lookup = Lookup(CONFIG)
    device_object = Device(hostname, CONFIG, lookup)
    port_table = device_object.ports()
    system_table = device_object.system()
    return render_template(
        "device.html",
        hostname=hostname,
        port_table=port_table,
        system_table=system_table,
    )
