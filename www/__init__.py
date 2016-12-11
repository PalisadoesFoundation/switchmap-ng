"""switchmap-ng Python 3 snmp inventory system.

This package reports and tabulates the status of network connected devices
using snmp queries.

Example:
    TODO add example of using switchmap.here

"""

from flask import Flask, url_for

# Initializes the Flask Object
APP = Flask(__name__)

# Function to easily find your assests
APP.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename=filename)
)
from www import views
