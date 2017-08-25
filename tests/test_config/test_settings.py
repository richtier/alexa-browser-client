from alexa_browser_client.config import settings


def test_get_settings_default():
    key = 'ALEXA_BROWSER_CLIENT_LIFECYCLE_CLASS'

    assert settings.get_setting(key) == 'alexa_browser_client.AudioLifecycle'


def test_get_settings_user_defined():
    key = 'ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID'

    assert settings.get_setting(key) == 'my-client-id'
