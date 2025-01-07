"""Class for creating device system information table web pages.

Provides table formatting and data organization for displaying system-related
information in the web interface. Includes classes for column formatting,
table structure, and row data management.
"""

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap.dashboard.data.system import System


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it.

    Extends the Col class to provide raw HTML output without escaping.
    """

    def td_format(self, content):
        """Format the column content without escaping.

        Args:
            content: The content to be displayed in the column

        Returns:
            content: The unmodified content
        """
        return content


class SystemTable(Table):
    """Declaration of the columns in the Systems table.

    Defines the structure and styling of the system information display table.
    """

    # Initialize class variables
    parameter = Col("Parameter")
    value = _RawCol("Value")

    # Define the CSS class to use for the header row
    thead_classes = ["tblHead"]
    classes = ["table"]


class SystemRow:
    """Declaration of the rows in the Systems table.

    Handles individual row data storage and formatting for system information.
    """

    def __init__(self, row):
        """Initialize the class.

        Args:
            row: SystemDataRow object containing parameter and value

        Returns:
            None
        """
        # Initialize key variables
        [row.parameter, row.value] = row


def table(data):
    """Create summary table for the device system information.

    Args:
        data: Dictionary containing system information data

    Returns:
        html: HTML table string or None if no rows are present
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
