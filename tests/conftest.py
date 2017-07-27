import requests_mock
import pytest


def pytest_configure():
    from django.conf import settings
    settings.configure(
        CLIENT_ID='my-client-id',
        DEVICE_TYPE_ID='my-device-type-id',
        CLIENT_SECRET='my-client-secret',
        REFRESH_TOKEN='my-refresh-token',
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        ROOT_URLCONF='alexa_browser_client.urls',
        CHANNEL_LAYERS={
            'default': {
                'BACKEND': 'asgiref.inmemory.ChannelLayer',
                'ROUTING': 'tests.config.routing.channel_routing',
            },
        },
    )


@pytest.fixture
def requests_mocker():
    m = requests_mock.mock()
    m.start()
    yield m
    m.stop()
