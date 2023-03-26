"""Class for creating home web pages."""
# Standard imports
from operator import attrgetter

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap import SITE_PREFIX
from switchmap.core import general


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


class EventTable(Table):
    """Declaration of the columns in the Events table."""

    # Initialize class variables
    col0 = _RawCol("")
    col1 = _RawCol("")
    col2 = _RawCol("")
    col3 = _RawCol("")
    col4 = _RawCol("")
    col5 = _RawCol("")

    # Define the CSS class to use for the header row
    classes = ["table"]


class EventsRow:
    """Declaration of the rows in the Events table."""

    def __init__(self, row_data):
        """Initialize the class.

        Args:
            row_data: Row data

        Returns:
            None

        """
        # Initialize key variables
        self.col0 = row_data[0]
        self.col1 = row_data[1]
        self.col2 = row_data[2]
        self.col3 = row_data[3]
        self.col4 = row_data[4]
        self.col5 = row_data[5]


def table(events):
    """Return data for the event's information.

    Args:
        events: List of EventMeta objects

    Returns:
        result: EventTable object

    """
    # Initialize key variables
    rows = []
    links = []
    width = 6
    result = False

    # The idx_root=0 element always points to the most recent poll.
    # We can remove this
    if len(events) > 1:
        events.pop(0)

    # Create list of links for table
    for event in sorted(events, key=attrgetter("date"), reverse=True):
        # Get URL link for event page
        url = "{}/{}".format(SITE_PREFIX, event.idx_root)
        link = '<a href="{}">{}</a>'.format(url, event.date)
        links.append(link)

    # Convert the rows to table rows
    list_of_lists = general.padded_list_of_lists(links, pad="", width=width)
    for item in list_of_lists:
        rows.append(EventsRow(item))

    # Append the result to create a table object
    if bool(rows) is True:
        # Append the result to create a table object
        result = EventTable(rows)

    # Return
    return result
