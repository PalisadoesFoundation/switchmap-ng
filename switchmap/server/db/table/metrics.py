# switchmap/server/db/table/metrics.py

from switchmap.server.db import db
from switchmap.server.db.models import (
    DeviceMetricsHistory as _DeviceMetricsHistory,
)
import datetime


def insert_row(rows):
    """Insert rows into smap_device_metrics_history (historical metrics)."""

    if not isinstance(rows, list):
        rows = [rows]

    inserts = []
    for row in rows:
        inserts.append(
            {
                "hostname": (
                    None if row.hostname is None else row.hostname.encode()
                ),
                "timestamp": row.timestamp or datetime.datetime.utcnow(),
                "uptime": row.uptime,
                "cpu_utilization": row.cpu_utilization,
                "memory_utilization": row.memory_utilization,
            }
        )

    if inserts:
        db.db_insert_row(2000, _DeviceMetricsHistory, inserts)
