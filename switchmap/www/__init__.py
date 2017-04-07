"""Module of switchmap API routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Pip imports
from flask import Flask, url_for

# Switchmap-NG imports
from switchmap.constants import CONFIG
from switchmap.utils import general

# Do remaining switchmap-ng importations
from switchmap.www.routes.api.devices import API_DEVICES
from switchmap.www.routes.pages.index import INDEX
from switchmap.www.routes.pages.devices import DEVICES
from switchmap.www.routes.pages.search import SEARCH
from switchmap.constants import (
    SITE_PREFIX, API_PREFIX, API_STATIC_FOLDER, API_TEMPLATE_FOLDER
    )

# Initializes the Flask Object.
# Make sure the static URL path is under the SITE_PREFIX.
API = Flask(
    __name__,
    static_url_path='{}/static'.format(SITE_PREFIX),
    static_folder=API_STATIC_FOLDER,
    template_folder=API_TEMPLATE_FOLDER
)

# Register Blueprints
API.register_blueprint(API_DEVICES, url_prefix=API_PREFIX)
API.register_blueprint(INDEX, url_prefix=SITE_PREFIX)
API.register_blueprint(DEVICES, url_prefix=SITE_PREFIX)
API.register_blueprint(SEARCH, url_prefix=SITE_PREFIX)

# Function to easily find your assests
API.jinja_env.globals['static'] = (
    lambda filename: url_for(
        'static', filename=filename)
)

@API.context_processor
def inject():
    """Function for injecting global variables for use by templates.

    Args:
        None

    Returns:
        HTML

    """
    # Get a list of hostnames
    hosts = general.get_hosts()

    # Return
    return dict(
        hosts=hosts,
        url_home=SITE_PREFIX,
        url_static='{}/static'.format(SITE_PREFIX))
