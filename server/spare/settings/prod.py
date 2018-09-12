from .base import *  # noqa

import os
import dj_database_url
import os

DEBUG = False

# Recommended settings (Heroku takes care of this for us)
ALLOWED_HOSTS = ['*']

# Set database URL
db = dj_database_url.config(default=os.environ['DATABASE_URL'], conn_max_age=600)
db['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db
}

MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/1.11/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/ja/1.11/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', True)
SECURE_CONTENT_TYPE_NOSNIFF = os.environ.get(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', True)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = os.environ.get('ADMIN_URL','admin/')