"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint, render_template

# Application imports
from switchmap.dashboard.pages.index import HomePage
from switchmap.dashboard import uri
from switchmap.core import rest
from switchmap.dashboard.configuration import ConfigDashboard

# Define the INDEX global variable
INDEX = Blueprint("INDEX", __name__)


@INDEX.route("/")
def index():
    """Create the dashboard home page.

    Args:
        None

    Returns:
        HTML

    """
    # Get data to display
    config = ConfigDashboard()
    data = rest.get(uri.dashboard(), config, server=False)
    # return jsonify(data)

    # Convert data to HTML and return it to the browser
    homepage = HomePage(data)
    tables = homepage.html()
    return render_template("index.html", device_table=tables)
