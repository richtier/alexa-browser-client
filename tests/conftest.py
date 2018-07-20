from unittest.mock import patch, PropertyMock
import requests_mock
import pytest


def pytest_configure():
    from django.conf import settings
    settings.configure(
        ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID='my-client-id',
        ALEXA_BROWSER_CLIENT_AVS_DEVICE_TYPE_ID='my-device-type-id',
        ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET='my-client-secret',
        ROOT_URLCONF='alexa_browser_client.config.urls',
        CHANNEL_LAYERS={
            'default': {
                'BACKEND': 'asgiref.inmemory.ChannelLayer',
                'ROUTING': 'tests.config.routing.channel_routing',
            },
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'channels',
            'alexa_browser_client',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                    ],
                },
            },
        ],
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        },
        SESSION_ENGINE='django.contrib.sessions.backends.cache',
        MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
        ]
    )


@pytest.fixture(autouse=True)
def mock_snowboy(request):
    path = (
        'command_lifecycle.wakeword.SnowboyWakewordDetector.'
        'wakeword_library_import_path'
    )
    stub = patch(path, PropertyMock(return_value='unittest.mock.Mock'))
    yield stub.start()
    stub.stop()


@pytest.fixture
def requests_mocker():
    m = requests_mock.mock()
    m.start()
    yield m
    m.stop()


@pytest.fixture(autouse=True)
def mock_client_connect():
    stub = patch('avs_client.AlexaVoiceServiceClient.connect')
    yield stub.start()
    stub.stop()
