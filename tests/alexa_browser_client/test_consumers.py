from unittest.mock import call, patch

import pytest

from alexa_browser_client.alexa_browser_client import consumers, helpers


def get_lifecycle():
    assert len(consumers.audio_lifecycles) == 1
    return list(consumers.audio_lifecycles.values())[0]


@pytest.fixture(autouse=True)
def clear_connections():
    consumers.audio_lifecycles = {}


def test_ws_add_creates_audio_lifecycle(ws_client):
    assert len(consumers.audio_lifecycles) == 0

    ws_client.send_and_consume('websocket.connect', check_accept=False)

    assert len(consumers.audio_lifecycles) == 1
    assert isinstance(get_lifecycle(), helpers.AudioLifecycle)


def test_ws_add_creates_accecpts_connection(ws_client):
    ws_client.send_and_consume('websocket.connect', check_accept=False)

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
    assert len(consumers.audio_lifecycles) == 0
    ws_client.send_and_consume('websocket.connect', check_accept=False)
    assert len(consumers.audio_lifecycles) == 1
    ws_client.send_and_consume('websocket.disconnect')
    assert len(consumers.audio_lifecycles) == 0
