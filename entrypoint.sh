#!/bin/bash
set -e

# Activate the virtual environment
source /venv/bin/activate

# Replace ${DB_PASSWORD} with the actual password
if [ -f /run/secrets/mysql_password ]; then
  export DB_PASSWORD=$(cat /run/secrets/mysql_password)
  sed -i "s/\${DB_PASSWORD}/$DB_PASSWORD/g" /switchmap-ng/etc/config.yaml
else
  echo "Error: MySQL password secret not found!"
  exit 1
fi

# Start SwitchMap server
bin/systemd/switchmap_server --start

bin/systemd/switchmap_dashboard --start

# Start Apache
service apache2 start

# Keep the container running
tail -f /dev/null