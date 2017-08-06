from io import StringIO
from unittest.mock import call, patch, Mock

from avs_client.refreshtoken import handlers, http_server

from django.core.management import call_command


@patch.object(http_server, 'AmazonLoginHttpServer')
def test_create_amazon_refresh_token_defaults(mock_http_server, settings):
    settings.ALEXA_VOICE_SERVICE_CLIENT_ID = 'my-client-id'
    settings.ALEXA_VOICE_SERVICE_CLIENT_SECRET = 'my-client-secret'
    settings.ALEXA_VOICE_SERVICE_DEVICE_TYPE_ID = 'my-device-type-id'

    out = StringIO()
    call_command('create_amazon_refresh_token', stdout=out) 

    assert mock_http_server.call_count == 1
    assert mock_http_server.call_args == call(
        server_address=('localhost', 8000),
        RequestHandlerClass=handlers.AmazonAlexaServiceLoginHandler,
        client_id='my-client-id',
        client_secret='my-client-secret',
        device_type_id='my-device-type-id',
    )

    assert 'running server on http://localhost:8000' in out.getvalue()


@patch.object(http_server, 'AmazonLoginHttpServer')
def test_create_amazon_refresh_token_no_defaults(mock_http_server, settings):
    settings.ALEXA_VOICE_SERVICE_CLIENT_ID = 'my-client-id'
    settings.ALEXA_VOICE_SERVICE_CLIENT_SECRET = 'my-client-secret'
    settings.ALEXA_VOICE_SERVICE_DEVICE_TYPE_ID = 'my-device-type-id'

    out = StringIO()
    call_command(
        'create_amazon_refresh_token',
        '--address=127.0.0.1',
        '--port=9000',
        stdout=out
    ) 

    assert mock_http_server.call_count == 1
    assert mock_http_server.call_args == call(
        server_address=('127.0.0.1', 9000),
        RequestHandlerClass=handlers.AmazonAlexaServiceLoginHandler,
        client_id='my-client-id',
        client_secret='my-client-secret',
        device_type_id='my-device-type-id',
    )

    assert 'running server on http://127.0.0.1:9000' in out.getvalue()
