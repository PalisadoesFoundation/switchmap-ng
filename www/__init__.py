"""Module of switchmap API routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Pip imports
from flask import Flask, url_for

# Switchmap-NG imports
from switchmap.utils import configuration
CONFIG = configuration.Config()

# Do remaining switchmap-ng importations
from www.routes.api.devices import DEVICES
from www.routes.pages.homepage import HOMEPAGE
from switchmap.constants import SITE_PREFIX, API_PREFIX

# Initializes the Flask Object.
# Make sure the static URL path is under the SITE_PREFIX.
API = Flask(__name__, static_url_path='{}/static'.format(SITE_PREFIX))

# Register Blueprints
API.register_blueprint(DEVICES, url_prefix=API_PREFIX)
API.register_blueprint(HOMEPAGE, url_prefix=SITE_PREFIX)

# Function to easily find your assests
API.jinja_env.globals['static'] = (
    lambda filename: url_for(
        'static', filename=filename)
)
