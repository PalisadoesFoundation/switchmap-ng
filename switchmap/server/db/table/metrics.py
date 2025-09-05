"""Database table operations for metrics."""

from switchmap.server.db import db
from switchmap.server.db.models import (
    DeviceMetricsHistory as _DeviceMetricsHistory,
)
import datetime
from collections.abc import Iterable


def _to_epoch(value):
    """Normalize int/float/datetime/ISO-8601 string to epoch seconds (int).

    Args:
        value (int, float, datetime, str, None): Input value to normalize.
            - If None, returns current UTC epoch time.
            - If int or float, returns int(value).
            - If datetime, returns int(value.timestamp()).
            - If str, attempts to parse as ISO-8601 datetime and returns
              int(parsed_datetime.timestamp()).

    Returns:
        int: Epoch time in seconds.

    """
    if value is None:
        return int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, datetime.datetime):
        dt = value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return int(dt.timestamp())
    if isinstance(value, str):
        try:
            s = value.strip()
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"
            dt = datetime.datetime.fromisoformat(s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            return int(dt.timestamp())
        except ValueError as exc:
            raise TypeError("Invalid last_polled ISO-8601 string") from exc
    raise TypeError("Invalid type for last_polled")


def insert_row(rows):
    """Insert rows into smap_device_metrics_history (historical metrics).

    Args:
        rows (list or object): Single row or list of rows to insert. Each row is
            expected to have the following attributes:
                - hostname (str or None): Device hostname
                - last_polled (int, float, datetime, str, or None):
                  Timestamp of last poll
                - uptime (int or None): Device uptime in seconds
                - cpu_utilization (float or None): CPU utilization percentage
                - memory_utilization (float or None): Memory utilization in %

    Returns:
        None

    """
    if isinstance(rows, Iterable) and not isinstance(
        rows, (str, bytes, bytearray, dict)
    ):
        rows = list(rows)
    else:
        rows = [rows]

    inserts = []
    for row in rows:

        # Validate/encode hostname (VARBINARY NOT NULL)
        if getattr(row, "hostname", None) is None:
            raise ValueError("hostname is required for DeviceMetricsHistory")
        _host = (
            row.hostname.encode("utf-8")
            if isinstance(row.hostname, str)
            else (
                bytes(row.hostname)
                if isinstance(row.hostname, (bytes, bytearray))
                else None
            )
        )
        if _host is None:
            raise TypeError("hostname must be str or bytes")
        if len(_host) > 256:
            raise ValueError("hostname exceeds 256 bytes")
        inserts.append(
            {
                "hostname": _host,
                "last_polled": _to_epoch(row.last_polled),
                "uptime": (
                    0
                    if (row.uptime is not None and row.uptime < 0)
                    else row.uptime
                ),
                "cpu_utilization": (
                    min(100.0, max(0.0, float(row.cpu_utilization)))
                    if row.cpu_utilization is not None
                    else None
                ),
                "memory_utilization": (
                    min(100.0, max(0.0, float(row.memory_utilization)))
                    if row.memory_utilization is not None
                    else None
                ),
            }
        )

    if inserts:
        db.db_insert_row(2000, _DeviceMetricsHistory, inserts)
