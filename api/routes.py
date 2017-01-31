"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Standard imports
import time
from os import path
from os import walk

# Pip imports
from flask import Flask, url_for, render_template

# Switchmap-NG imports
from switchmap.utils.configuration import Config
from switchmap.topology import pages

# Initializes the Flask Object
API = Flask(__name__)

# Function to easily find your assests
API.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename)
)


@API.template_filter('strftime')
def _jinja2_filter_datetime(timestamp):
    timestamp = time.strftime('%H:%M (%d-%m-%Y) ', time.localtime(timestamp))
    return timestamp


@API.route('/')
def tables():
    """Function for creating host tables.

    Args:
        idx_host: Index of host
        idx_agent: Index of agent

    Returns:
        HTML

    """
    hosts = _get_yaml_hosts()
    return render_template('network-topo.html',
                           hostname='Switchmap-NG',
                           hosts=hosts)


@API.route('/fetch/agent/<ip_address>/table', methods=["GET"])
def fetch_table(ip_address):
    """Return Network Layout tables.

    Args:
        ip_address: Host IP

    Returns:
        HTML string of host table

    """
    # Config Object
    config = Config()
    html = pages.create(config, ip_address)

    return html


def _get_yaml_hosts():
    """Get hosts listed in toplogy YAML files.

    Args:
        None

    Returns:
        hosts: List of hostnames

    """
    # Read configuration
    config = Config()
    cache_directory = config.cache_directory()

    hosts = []
    for root, _, files in walk(cache_directory):
        for filename in files:
            filepath = path.join(root, filename)
            if filepath.endswith('.yaml'):
                hostname = filename[:-5]
                hosts.append(hostname)
    return sorted(hosts)
