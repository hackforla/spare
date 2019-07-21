#!/usr/bin/env bash

# Fail on errors
set -e

# Fail if missing migrations
echo "Checking for missing migrations"
python manage.py makemigrations --check

# Style linting checks
echo "Running flake linting tests"
flake8 .

# Import linting checks
echo "Running import linting checks"
isort -rc -c

# Run backend tests
echo "Running backend tests"
pytest
