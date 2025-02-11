#!/bin/bash

set -e

# Activate virtual environment
source venv/bin/activate

# Function to wait for MySQL
wait_for_mysql() {
    echo "Waiting for MySQL to be ready..."
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if mysqladmin ping -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; then
            echo "MySQL is up and running!"
            return 0
        fi
        echo "Attempt $attempt of $max_attempts: MySQL is unavailable - sleeping"
        sleep 5
        attempt=$((attempt + 1))
    done
    
    echo "Failed to connect to MySQL after $max_attempts attempts"
    return 1
}

# Wait for MySQL to be ready
wait_for_mysql

# Ensure database exists
mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Run database initialization
echo "Initializing database..."
bin/tools/create_db_tables.py

# Start the appropriate service based on SERVICE_TYPE
case "$SERVICE_TYPE" in
    "api")
        echo "Starting API Server..."
        exec bin/systemd/switchmap_server --start
        ;;
    "dashboard")
        echo "Starting Web Dashboard..."
        exec bin/systemd/switchmap_dashboard --start
        ;;
    "poller")
        echo "Starting Poller..."
        exec bin/systemd/switchmap_poller --start
        ;;
    *)
        echo "No valid service type specified. Exiting."
        exit 1
        ;;
esac