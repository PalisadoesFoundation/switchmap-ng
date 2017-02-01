"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint, render_template

# Switchmap-NG imports
from switchmap.utils import general
from switchmap.constants import API_PREFIX, SITE_PREFIX

# Define the HOMEPAGE global variable
HOMEPAGE = Blueprint('HOMEPAGE', __name__, static_url_path=SITE_PREFIX)


@HOMEPAGE.route('/')
def index():
    """Function for creating host tables.

    Args:
        None

    Returns:
        HTML

    """
    hosts = general.get_hosts()
    defaulthost = hosts[0]
    return render_template(
        'network-topo.html',
        defaulthost=defaulthost, hosts=hosts, prefix=API_PREFIX)
