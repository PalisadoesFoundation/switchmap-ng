"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint, render_template

# Application imports
from switchmap.dashboard.net.html.pages.index import IndexPage
from switchmap.dashboard import uri
from switchmap.core import rest
from switchmap.dashboard.configuration import ConfigDashboard

# Define the INDEX global variable
INDEX = Blueprint("INDEX", __name__)


@INDEX.route("/")
def dashboard():
    """Create the dashboard home page.

    Args:
        None

    Returns:
        HTML

    """
    # Get data to display
    config = ConfigDashboard()
    event = rest.get(uri.dashboard(), config, server=False)
    return _dashboard(event)


@INDEX.route("/<int:idx_root>")
def historical_dashboard(idx_root):
    """Create the dashboard home page for a specific event index.

    Args:
        idx_root: Event index

    Returns:
        HTML

    """
    # Get data to display
    config = ConfigDashboard()
    event = rest.get(uri.historical_dashboard(idx_root), config, server=False)
    return _dashboard(event, idx_root=idx_root)


def _dashboard(event, idx_root=1):
    """Create the dashboard home page for a specific event index.

    Args:
        event: Event dict
        idx_root: Root db table primary key

    Returns:
        HTML

    """
    # Convert data to HTML and return it to the browser
    zones = event.get("zones")
    date = event.get("tsCreated", "")

    homepage = IndexPage(zones)
    tables = homepage.html()
    return render_template(
        "index.html", device_table=tables, date=date, idx_root=idx_root
    )
