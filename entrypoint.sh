#!/bin/bash
set -e

source /venv/bin/activate

export DB_PASSWORD=$(cat /run/secrets/mysql_password)
sed -i "s/\${DB_PASSWORD}/$DB_PASSWORD/g" /switchmap-ng/etc/config.yaml

python bin/systemd/switchmap_server --start

tail -f /dev/null
