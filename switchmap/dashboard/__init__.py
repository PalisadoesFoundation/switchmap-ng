"""Module of switchmap DASHBOARD routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Pip imports
from flask import Flask, url_for

# Switchmap-NG imports
# from switchmap.utils import general

# Do remaining switchmap-ng importations
from switchmap.dashboard.routes.api.api import API
from switchmap.dashboard.routes.pages.index import INDEX

# from switchmap.dashboard.routes.pages.devices import DEVICES
# from switchmap.dashboard.routes.pages.search import SEARCH
from switchmap import (
    SITE_PREFIX,
    API_PREFIX,
    # DASHBOARD_PREFIX,
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
# DASHBOARD.register_blueprint(DEVICES, url_prefix=SITE_PREFIX)
# DASHBOARD.register_blueprint(SEARCH, url_prefix=SITE_PREFIX)

# Function to easily find your assests
DASHBOARD.jinja_env.globals["static"] = lambda filename: url_for(
    "static", filename=filename
)


@DASHBOARD.context_processor
def inject():
    """Inject global variables for use by templates.

    Args:
        None

    Returns:
        HTML

    """
    # Get a list of hostnames
    # hosts = general.get_hosts()

    # Return
    return dict(
        # hosts=hosts,
        url_home=SITE_PREFIX,
        url_static="{}/static".format(SITE_PREFIX),
    )
