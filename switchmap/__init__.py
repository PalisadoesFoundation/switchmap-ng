#!/usr/bin/env python3
"""Switchmap-NG setup.

Manages parameters required by all classes in the module.

"""

# Do library imports
from .core import log
from .poll.update import TrunkInterface
from .core.configuration import Config, ConfigSNMP

# Create global variables for the API
SITE_PREFIX = '/switchmap-ng'
API_PREFIX = '{}/api/v1'.format(SITE_PREFIX)
API_STATIC_FOLDER = 'static/default'
API_TEMPLATE_FOLDER = 'templates/default'
AGENT_API_CHILD = 'switchmap-ng-gunicorn'
AGENT_POLLER = 'Poller'
AGENT_API = 'API'


def main():
    """Process data.

    Args:
        None

    Returns:
        None

    """
    # Check the environment
    log.check_environment()


if __name__ == 'switchmap':
    main()
