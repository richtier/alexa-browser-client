from unittest.mock import patch, PropertyMock
import requests_mock
import pytest


def pytest_configure():
    from django.conf import settings
    settings.configure(
        ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID='my-client-id',
        ALEXA_BROWSER_CLIENT_AVS_DEVICE_TYPE_ID='my-device-type-id',
        ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET='my-client-secret',
        ALEXA_BROWSER_CLIENT_AVS_REFRESH_TOKEN='my-refresh-token',
        ALEXA_BROWSER_CLIENT_LIFECYCLE_CLASS='alexa_browser_client.AudioLifecycle',
        ROOT_URLCONF='alexa_browser_client.urls',
        CHANNEL_LAYERS={
            'default': {
                'BACKEND': 'asgiref.inmemory.ChannelLayer',
                'ROUTING': 'tests.config.routing.channel_routing',
            },
        },
        INSTALLED_APPS=['alexa_browser_client']
    )


@pytest.fixture(autouse=True)
def mock_snowboy(request):
    path = (
        'command_lifecycle.wakeword.SnowboyWakewordDetector.'
        'wakeword_library_import_path'
    )
    stub = patch(path, PropertyMock(return_value='unittest.mock.Mock'))
    stub.start()
    yield stub
    stub.stop()


@pytest.fixture
def requests_mocker():
    m = requests_mock.mock()
    m.start()
    yield m
    m.stop()
