from unittest.mock import call, patch, Mock

import pytest

from alexa_browser_client.alexa_browser_client import consumers, helpers


@pytest.fixture(autouse=True)
def mock_client_connect():
    path = (
        'alexa_browser_client.alexa_browser_client.consumers.'
        'alexa_client.connect'
    )
    stub = patch(path)
    stub.start()
    yield stub
    stub.stop()


def get_lifecycle():
    assert len(consumers.state['audio_lifecycles']) == 1
    return list(consumers.state['audio_lifecycles'].values())[0]


@pytest.fixture(autouse=True)
def clear_state():
    consumers.state = {
        'audio_lifecycles': {},
        'has_connected': False,
    }


def test_ws_add_creates_default_audio_lifecycle(ws_client):
    assert len(consumers.state['audio_lifecycles']) == 0

    ws_client.send_and_consume('websocket.connect', check_accept=False)

    assert len(consumers.state['audio_lifecycles']) == 1
    assert isinstance(get_lifecycle(), helpers.AudioLifecycle)


def test_ws_add_calls_conditional_connect(ws_client):
    ws_client.send_and_consume('websocket.connect', check_accept=False)
    ws_client.send_and_consume('websocket.connect', check_accept=False)
    ws_client.send_and_consume('websocket.connect', check_accept=False)

    assert consumers.alexa_client.connect.call_count == 1


def test_ws_add_creates_custom_audio_lifecycle(ws_client, settings):
    settings.ALEXA_BROWSER_CLIENT_LIFECYCLE_CLASS = 'unittest.mock.Mock'
    assert len(consumers.state['audio_lifecycles']) == 0

    ws_client.send_and_consume('websocket.connect', check_accept=False)

    assert len(consumers.state['audio_lifecycles']) == 1
    assert isinstance(get_lifecycle(), Mock)


def test_ws_add_creates_accecpts_connection(ws_client):
    ws_client.send_and_consume('websocket.connect', check_accept=False)

    assert ws_client.receive() == {'type': 'CONNECTING'}
    assert ws_client.receive() == {'type': 'EXPECTING_WAKEWORD'}
    assert ws_client.receive() == {'accept': True}


def test_ws_receive_extends_lifecycle_audio(ws_client):
    ws_client.send_and_consume('websocket.connect', check_accept=False)

    with patch.object(get_lifecycle(), 'extend_audio') as mock_extend_audio:
        ws_client.send_and_consume(
            'websocket.receive', content={'bytes': [0.3, -0.2]}
        )

    assert mock_extend_audio.call_count == 1
    assert mock_extend_audio.call_args == call([0.3, -0.2])


def test_ws_disconnects_deletes_lifecycle(ws_client):
    assert len(consumers.state['audio_lifecycles']) == 0
    ws_client.send_and_consume('websocket.connect', check_accept=False)
    assert len(consumers.state['audio_lifecycles']) == 1
    ws_client.send_and_consume('websocket.disconnect')
    assert len(consumers.state['audio_lifecycles']) == 0
