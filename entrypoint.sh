#!/bin/bash
set -e

source /venv/bin/activate

# Substitute DB_PASSWORD in config.yaml
export DB_PASSWORD=$(cat /run/secrets/mysql_password)
sed -i "s/\${DB_PASSWORD}/$DB_PASSWORD/g" /switchmap-ng/etc/config.yaml

case "$CONTAINER_ROLE" in
  server)
    bin/systemd/switchmap_server --start
    ;;
  poller)
    bin/systemd/switchmap_poller --start
    ;;
  ingester)
    bin/systemd/switchmap_ingester --start
    ;;
  dashboard)
    bin/systemd/switchmap_dashboard --start
    ;;
  apache)
    a2ensite switchmap-ng.conf
    service apache2 start
    tail -f /dev/null
    ;;
  *)
    echo "Unknown role: $CONTAINER_ROLE"
    exit 1
    ;;
esac

# Keep container running
tail -f /dev/null