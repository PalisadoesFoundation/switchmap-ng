"""Module of switchmap API routes.

Contains all routes that the Flask API uses

"""

# Pip imports
from flask import Flask

# Do remaining switchmap importations
from switchmap.server.api.routes.graphql import API_GRAPHQL
from switchmap.server.api.routes.post import API_POST
from switchmap import API_PREFIX

# Initializes the Flask Object.
# Make sure the static URL path is under the SITE_PREFIX.
API = Flask(
    __name__,
)

# Register Blueprints
API.register_blueprint(API_GRAPHQL, url_prefix=API_PREFIX)
API.register_blueprint(API_POST, url_prefix=API_PREFIX)
