"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint, render_template

# Switchmap-NG imports
from switchmap.utils import general
from switchmap.www.pages.index import HomePage

# Define the INDEX global variable
INDEX = Blueprint('INDEX', __name__)


@INDEX.route('/')
def index():
    """Function for creating host tables.

    Args:
        None

    Returns:
        HTML

    """
    # Get a list of hostnames
    hosts = general.get_hosts()
    homepage = HomePage(hosts)
    device_table = homepage.data()
    return render_template(
        'index.html',
        device_table=device_table)
