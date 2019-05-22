#!/usr/bin/env bash

# Collect static files
python manage.py collectstatic --no-input
uwsgi uwsgi.ini
