# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

INSTALLED_APPS = [
    # Early dependencies
    'grappelli',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project-specific apps
    'api',
    'core',
    'donations',

    # Dependencies
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'django_rq',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spare.wsgi.application'


# Default site id
SITE_ID = 1


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/public')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/dist')
]


# Django Custom User model
AUTH_USER_MODEL = 'core.User'


# Django Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# Auth/Login Settings
LOGIN_REDIRECT_URL = 'api-root'
LOGIN_URL = 'login'

# Email Settings
if os.environ.get('EMAIL_BACKEND') == 'mailgun':
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    ANYMAIL = {
        'MAILGUN_API_KEY': os.environ['MAILGUN_API_KEY'],
        'MAILGUN_SENDER_DOMAIN': 'whatcanyouspare.org'
    }
elif os.environ.get('EMAIL_BACKEND', 'console') == 'console':
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Email Addresses
DEFAULT_FROM_EMAIL = "team@whatcanyouspare.org"
ADMINS = [('Team', DEFAULT_FROM_EMAIL)]

# RQ Settings
RQ_QUEUES = {
    'default': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    }
}
if os.environ.get('ENQUEUE_TASKS', 'false') not in ('false', 'true'):
    raise ValueError("ENQUEUE_TASKS must be set to either 'true' or 'false'")

ENQUEUE_TASKS = os.environ.get('ENQUEUE_TASKS', 'false') == 'true'

# SMS Settings
if os.environ.get('SMS_BACKEND') == 'twilio':
    SMS_BACKEND = 'core.sms.backends.twilio.SMSBackend'
    TWILIO_ACCOUNT_ID = os.environ.get('TWILIO_ACCOUNT_ID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
elif os.environ.get('SMS_BACKEND') == 'locmem':
    SMS_BACKEND = 'core.sms.backends.locmem.SMSBackend'
elif os.environ.get('SMS_BACKEND', 'console') == 'console':
    SMS_BACKEND = 'core.sms.backends.console.SMSBackend'
else:
    raise ValueError("SMS_BACKEND must be set to either 'twilio', 'locmem', or 'console'")

SMS_FROM_NUMBER = os.environ.get('SMS_FROM_NUMBER')
