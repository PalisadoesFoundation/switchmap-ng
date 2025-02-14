#!/bin/bash
set -e

mkdir -p /run/secrets

echo "${MYSQL_ROOT_PASSWORD_VALUE}" > /run/secrets/mysql_root_password
echo "${MYSQL_PASSWORD_VALUE}" > /run/secrets/mysql_password

unset MYSQL_ROOT_PASSWORD_VALUE MYSQL_PASSWORD_VALUE

exec /entrypoint.sh "$@"
