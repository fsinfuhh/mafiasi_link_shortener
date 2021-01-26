#!/usr/bin/env sh
set -e

/app/src/src/manage.py collectstatic --noinput
/app/src/src/manage.py migrate
/app/src/src/manage.py check --deploy
/app/src/src/manage.py "$@"
