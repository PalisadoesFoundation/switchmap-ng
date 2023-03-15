"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint

# Application imports
# from switchmap.dashboard.net.pages.index import HomePage
from switchmap.dashboard import uri
from switchmap.core import rest
from switchmap.dashboard.configuration import ConfigDashboard

# Define the EVENT global variable
EVENT = Blueprint("EVENT", __name__)


@EVENT.route("/events")
def events():
    """Create the events page.

    Args:
        None

    Returns:
        HTML

    """
    # Get data to display
    config = ConfigDashboard()
    event = rest.get(uri.dashboard(), config, server=False)
    return event
