"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint, render_template

# Application imports
# from switchmap.dashboard.net.html.pages.index import EventPage
from switchmap.dashboard import uri
from switchmap.core import rest
from switchmap.dashboard.configuration import ConfigDashboard
from switchmap.dashboard.net.html.pages.events import EventPage

# Define the EVENT global variable
EVENT = Blueprint("EVENT", __name__)


@EVENT.route("/events")
def events():
    """Create the events page.

    Args:
        None

    Returns:
        render_template: HTML

    """
    # Get data to display
    config = ConfigDashboard()
    events_ = rest.get(uri.events(), config, server=False)

    # Convert data to HTML and return it to the browser
    eventpage = EventPage(events_)
    tables = eventpage.html()
    return render_template("event.html", event_table=tables, idx_root=1)
