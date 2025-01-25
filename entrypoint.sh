#!/bin/bash

set -e

wait_for_mysql() {
    echo "Waiting for MySQL to be ready..."
    for i in {1..30}; do
        if nc -z db 3306; then
            echo "MySQL port is available, waiting for service to be fully ready..."
            sleep 10 
            return 0
        fi
        echo "MySQL is unavailable - attempt $i/30"
        sleep 2
    done
    echo "MySQL failed to become available"
    exit 1
}

cd /opt/switchmap-ng

rm -f var/daemon/pid/*.pid
# Wait for MySQL
wait_for_mysql

if [ "$COMPONENT" = "server" ]; then
    echo "Creating database tables..."
    if ! bin/tools/create_db_tables.py; then
        echo "Failed to create database tables!"
        exit 1
    fi
    echo "Database tables created successfully!"
fi

case "$COMPONENT" in
    "server")
        echo "Starting switchmap server..."
        bin/systemd/switchmap_server --start
        bin/systemd/switchmap_server --status
        ;;
    "dashboard")
        echo "Starting switchmap dashboard..."
        bin/systemd/switchmap_dashboard --start
        bin/systemd/switchmap_dashboard --status
        ;;
    *)
        echo "Error: COMPONENT must be either 'server' or 'dashboard'"
        exit 1
        ;;
esac

exec tail -f /dev/null