#!/usr/bin/env bash

python manage.py collectstatic --no-input && uwsgi uwsgi.ini
