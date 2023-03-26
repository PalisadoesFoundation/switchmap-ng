"""Module of switchmap DASHBOARD routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Standard imports
from collections import namedtuple

# Pip imports
from flask import Flask, url_for

# Used in building HTML tables
DeviceMeta = namedtuple("DeviceMeta", "hostname idx_device")
EventMeta = namedtuple("EventMeta", "date idx_root")

# Used in reporting interface state
InterfaceState = namedtuple("InterfaceState", "up string")
VlanState = namedtuple("VlanState", "group string count")
MacState = namedtuple("MacState", "mac organization")
IpState = namedtuple("IpState", "hostname address")
MacIpState = namedtuple("MacIpState", "mac organization hostnames addresses")

InterfaceDataRow = namedtuple(
    "InterfaceDataRow",
    "port vlan state days_inactive speed duplex label "
    "trunk cdp lldp mac_address organization ip_address hostname",
)
SystemDataRow = namedtuple("SystemDataRow", "parameter value")

# Do remaining switchmap-ng importations
from switchmap.dashboard.net.routes.api.api import API
from switchmap.dashboard.net.routes.pages.index import INDEX
from switchmap.dashboard.net.routes.pages.events import EVENT
from switchmap.dashboard.net.routes.pages.devices import DEVICES
from switchmap.dashboard.net.routes.pages.search import SEARCH

# from switchmap.dashboard.net.routes.pages.search import SEARCH
from switchmap import (
    SITE_PREFIX,
    API_PREFIX,
    DASHBOARD_STATIC_FOLDER,
    DASHBOARD_TEMPLATE_FOLDER,
)

# Initializes the Flask Object.
# Make sure the static URL path is under the SITE_PREFIX.
DASHBOARD = Flask(
    __name__,
    static_url_path="{}/static".format(SITE_PREFIX),
    static_folder=DASHBOARD_STATIC_FOLDER,
    template_folder=DASHBOARD_TEMPLATE_FOLDER,
)

# Register Blueprints
DASHBOARD.register_blueprint(API, url_prefix=API_PREFIX)
DASHBOARD.register_blueprint(INDEX, url_prefix=SITE_PREFIX)
DASHBOARD.register_blueprint(EVENT, url_prefix=SITE_PREFIX)
DASHBOARD.register_blueprint(DEVICES, url_prefix=SITE_PREFIX)
DASHBOARD.register_blueprint(SEARCH, url_prefix=SITE_PREFIX)

# Function to easily find your assests
DASHBOARD.jinja_env.globals["static"] = lambda filename: url_for(
    "static", filename="html/{}".format(filename)
)


@DASHBOARD.context_processor
def inject():
    """Inject global variables for use by templates.

    Args:
        None

    Returns:
        HTML

    """
    # Return
    return dict(
        url_home=SITE_PREFIX,
        url_static="{}/static".format(SITE_PREFIX),
    )
