"""Class for creating home web pages."""

# Import switchmap.libraries
from switchmap.dashboard.net.html.pages import layouts
from switchmap.dashboard.table import events as events_
from switchmap.dashboard import EventMeta


class EventPage:
    """Class that creates the homepages's various HTML tables."""

    def __init__(self, _events):
        """Initialize the class.

        Args:
            _events: Events to process

        Returns:
            None

        """
        # Initialize key variables
        self._events = _events

    def html(self):
        """Create HTML table for the events.

        Args:
            None

        Returns:
            result: HTML table string

        """
        # Initialize key variables
        events = []
        result = ""

        # Iterate over the events
        for event in self._events:
            # Initialize loop variables
            idx_root = event.get("idxRoot")

            # Extract the event data to create the table rows.
            for _, date in event.get("event").items():
                events.append(
                    EventMeta(
                        date=date,
                        idx_root=idx_root,
                    )
                )

        # Get the table and wrap custom HTML
        table = events_.table(events)
        if bool(table) is True:
            _html = "".join(table.__html__())
            result = layouts.table_wrapper("Polling Event Dates", _html)

        # Return
        return result
