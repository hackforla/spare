#!/usr/bin/env bash

echo "Running startup"

python manage.py collectstatic --no-input && uwsgi uwsgi.ini
