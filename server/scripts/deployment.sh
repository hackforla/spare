#!/usr/bin/env bash

echo "Running deployment tasks"

# Run migrations prior to deployment
python manage.py migrate --noinput
