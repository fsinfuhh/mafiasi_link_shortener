#!/usr/bin/env sh
set -e

echo "Collecting staticfiles"
/app/src/src/manage.py collectstatic --noinput

echo "Migrating database"
/app/src/src/manage.py migrate

echo "Configuring frontend"
/app/src/src/manage.py configure_frontend

echo "Performing system checks"
/app/src/src/manage.py check --deploy

echo "Starting server"
export PYTHONPATH="$PYTHONPATH:/app/src/src"
exec "$@"
