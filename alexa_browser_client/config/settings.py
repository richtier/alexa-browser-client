from django.conf import settings


default_settings = {
    'ALEXA_BROWSER_CLIENT_LIFECYCLE_CLASS': (
        'alexa_browser_client.AudioLifecycle'
    ),
}


def get_setting(key):
    if hasattr(settings, key):
        return getattr(settings, key)
    return default_settings[key]
