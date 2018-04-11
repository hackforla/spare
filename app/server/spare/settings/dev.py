import os

import dj_database_url

from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ['*']

db = dj_database_url.config(default=os.environ['DATABASE_URL'], conn_max_age=600)
db['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db
}

INSTALLED_APPS.extend([
    'debug_toolbar',
])

MIDDLEWARE.insert(
    0, 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ['127.0.0.1', '127.0.0.1:8000']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
