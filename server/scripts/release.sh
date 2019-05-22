#!/usr/bin/env bash

# Check static files
python manage.py collectstatic --no-input --dry-run

# Run database migrations
python manage.py migrate --noinput
