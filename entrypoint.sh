#!/bin/sh
set -eu
python manage.py migrate --noinput
if [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    python manage.py createsuperuser --noinput
fi
exec "$@"
