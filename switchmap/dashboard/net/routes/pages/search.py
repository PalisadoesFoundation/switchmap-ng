"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint, request, jsonify

# Application imports
from switchmap.dashboard import uri
from switchmap.core import rest
from switchmap.dashboard.configuration import ConfigDashboard

# Define the SEARCH global variable
SEARCH = Blueprint("SEARCH", __name__)


@SEARCH.route("/search", methods=["POST"])
def search():
    """Create the search page.

    Args:
        None

    Returns:
        HTML

    """
    # Initialize key variables
    result = []

    # Get data to display
    config = ConfigDashboard()

    # Get search form data
    items = request.form

    for key, value in items.items():
        # 'search_term' comes from the search form HTML
        if key == "search_term":

            # Post the data to the API server
            seach_dict = {"idx_root": 1, "searchterm": value.strip()}
            post_response = rest.post(uri.search_post(), seach_dict, config)

            # Process a successful response
            if bool(post_response.success) is True:
                # Get data from the API server using GraphQL
                idx_l1interfaces = post_response.json()

                # Process data if found
                if bool(idx_l1interfaces) is True:
                    result = rest.get(
                        uri.search(idx_l1interfaces), config, server=False
                    )

    # Convert data to HTML and return it to the browser
    # eventpage = EventPage(search_)
    # tables = eventpage.html()
    # return render_template("event.html", event_table=tables)
    return jsonify(result)
