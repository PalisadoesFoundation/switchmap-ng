"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint, render_template, jsonify

# Application imports
# from switchmap.dashboard.pages.index import HomePage
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
    return jsonify(data)

    # hosts = general.get_hosts()
    # homepage = HomePage(hosts)
    # device_table = homepage.data()
    # return render_template("index.html", device_table=device_table)
