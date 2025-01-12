"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint, render_template

# Switchmap-NG imports
from switchmap.dashboard.net.html.pages.device import Device
from switchmap.dashboard.configuration import ConfigDashboard
from switchmap.dashboard import uri
from switchmap.core import rest


# Define the DEVICES global variable
DEVICES = Blueprint("DEVICES", __name__)


@DEVICES.route("/devices/<int:idx_device>")
def devices(idx_device):
    """Crerate device tables.

    Args:
        idx_device: Device index

    Returns:
        render_template: HTML

    """
    # Get data to display
    config = ConfigDashboard()
    data = rest.get(uri.devices(idx_device), config, server=False)

    # Get the idx_root for the device
    idx_roots = data["device"]["event"]["roots"]
    idx_root = min([_.get("idxRoot") for _ in idx_roots])
    date = data["device"]["event"]["tsCreated"]

    # Get device data
    device_ = Device(data)
    interfaces = device_.interfaces()
    system = device_.system()
    hostname = device_.hostname()
    return render_template(
        "device.html",
        hostname=hostname,
        port_table=interfaces,
        system_table=system,
        idx_root=idx_root,
        date=date,
    )
