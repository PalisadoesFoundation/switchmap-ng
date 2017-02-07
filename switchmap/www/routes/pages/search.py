"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint, render_template, request

# Switchmap-NG imports


# Define the SEARCH global variable
SEARCH = Blueprint('SEARCH', __name__)


@SEARCH.route('/search', methods=['POST'])
def index():
    """Function for creating search results.

    Args:
        None

    Returns:
        HTML

    """
    # Initialize key variables
    search_term = ''

    # Get search form data
    items = request.form

    for key, value in items.items():
        print(key, value)
        # (key, value) = item
        if key == 'search_term':
            search_term = value

    # Present results
    return render_template(
        'search.html',
        search_term=search_term)
