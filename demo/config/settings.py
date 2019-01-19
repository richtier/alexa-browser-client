import os

import environ

env = environ.Env()
env.read_env()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Application definition
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'channels',
    'alexa_browser_client',
    'demo',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
]

ROOT_URLCONF = 'demo.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.config.wsgi.application'

ASGI_APPLICATION = 'alexa_browser_client.config.routing.application'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    },
    'rooms': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    },
}


# Alexa client
ALEXA_BROWSER_CLIENT_AVS_DEVICE_TYPE_ID = env.str(
    'ALEXA_BROWSER_CLIENT_AVS_DEVICE_TYPE_ID'
)
ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID = env.str(
    'ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID'
)
ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET = env.str(
    'ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET'
)

ALEXA_BROWSER_CLIENT_AVS_REFRESH_TOKEN = env.str(
    'ALEXA_BROWSER_CLIENT_AVS_REFRESH_TOKEN'
)

# static files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
