# Do library imports
from switchmap.utils import configuration

# Create global variables used by all applications
CONFIG = configuration.Config()
CONFIG_SNMP = configuration.ConfigSNMP()

# Create global variables for the API
SITE_PREFIX = '/switchmap-ng'
API_PREFIX = '{}/api/v1'.format(SITE_PREFIX)
API_STATIC_FOLDER = 'static/default'
API_TEMPLATE_FOLDER = 'templates/default'
API_EXECUTABLE = 'switchmap-ng-api'
API_GUNICORN_AGENT = 'switchmap-ng-gunicorn'
POLLER_EXECUTABLE = 'switchmap-ng-poller'
