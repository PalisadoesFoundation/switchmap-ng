"""Class for creating device web pages."""

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap.dashboard.data.system import System


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        """
        Fix the column formatting.
        Args:
            content
        Returns:
            content
        """
        return content


class SystemTable(Table):
    """Declaration of the columns in the Systems table."""

    # Initialize class variables
    parameter = Col("Parameter")
    value = _RawCol("Value")

    # Define the CSS class to use for the header row
    thead_classes = ["tblHead"]
    classes = ["table"]


class SystemRow:
    """Declaration of the rows in the Systems table."""

    def __init__(self, row):
        """Initialize the class.

        Args:
            row: SystemDataRow object

        Returns:
            None

        """
        # Initialize key variables
        [row.parameter, row.value] = row


def table(data):
    """Create summary table for the devie.

    Args:
        None

    Returns:
        html: HTML table string

    """
    # Initialize key variables
    result = None

    # Process the data
    system = System(data)
    rows = system.rows()

    # Populate the result
    if bool(rows) is True:
        result = SystemTable(rows)

    # Return
    return result
