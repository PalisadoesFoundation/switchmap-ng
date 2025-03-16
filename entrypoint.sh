#!/bin/bash
set -e

# Ensure proper ownership of the var directory
chown -R switchmap:switchmap /opt/switchmap-ng/var 2>/dev/null || true

# Activate the virtual environment
source /opt/switchmap-ng/venv/bin/activate

# Function: Wait for MySQL to be ready
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

# Function: Verify database and required tables exist
verify_database() {
    echo "Verifying database setup..."
    if mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "USE $MYSQL_DATABASE"; then
        echo "Database $MYSQL_DATABASE exists."
        tables=("smap_oui")
        for table in "${tables[@]}"; do
            if mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -e "DESC $table" >/dev/null 2>&1; then
                echo "Table $table exists and is accessible."
            else
                echo "Table $table does not exist or is not accessible."
                return 1
            fi
        done
        return 0
    else
        echo "Database $MYSQL_DATABASE does not exist or is not accessible."
        return 1
    fi
}

# Wait for MySQL to become available
wait_for_mysql

# Remove stale daemon pid files (if any)
rm -f /opt/switchmap-ng/var/daemon/pid/*.pid

if [ "$SERVICE_TYPE" = "api" ]; then
    echo "Initializing database..."
    if ! bin/tools/create_db_tables.py; then
        echo "Database initialization failed"
        exit 1
    fi
    if ! verify_database; then
        echo "Database verification failed"
        exit 1
    fi
    echo "Database initialization and verification completed successfully"
else
    echo "Waiting for API service to initialize database..."
    max_attempts=30
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        if verify_database; then
            echo "Database is ready"
            break
        fi
        echo "Attempt $attempt of $max_attempts: Waiting for database initialization..."
        sleep 5
        attempt=$((attempt + 1))
    done
    if [ $attempt -gt $max_attempts ]; then
        echo "Database was not initialized properly after maximum attempts"
        exit 1
    fi
fi

# Start the service based on SERVICE_TYPE
case "$SERVICE_TYPE" in
    "api")
        echo "Starting API Server..."
        bin/systemd/switchmap_server --start
        ;;
    "dashboard")
        echo "Starting Web Dashboard..."
        bin/systemd/switchmap_dashboard --start
        ;;
    "poller")
        echo "Starting Poller..."
        su -c '/opt/switchmap-ng/bin/systemd/switchmap_poller --start' switchmap
        ;;
    *)
        echo "No valid service type specified. Exiting."
        exit 1
        ;;
esac

echo "Service started successfully, keeping container alive..."
tail -f /dev/null
