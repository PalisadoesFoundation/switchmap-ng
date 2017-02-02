"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""
# Flask imports
from flask import Blueprint, render_template

# Define the INDEX global variable
INDEX = Blueprint('INDEX', __name__)


@INDEX.route('/')
def index():
    """Function for creating host tables.

    Args:
        None

    Returns:
        HTML

    """
    return render_template('index.html')
