#!/usr/bin/env bash

echo "Running deployment tasks"

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate --noinput
