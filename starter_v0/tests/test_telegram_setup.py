from types import SimpleNamespace

import pytest
import requests

from scripts.preflight_telegram import extract_chats, telegram_call


def test_discovery_only_returns_chat_metadata_and_deduplicates():
    chat = {"id": -100123, "type": "channel", "title": "Team"}
    updates = [{"channel_post": {"chat": chat, "text": "private content"}},
               {"edited_channel_post": {"chat": chat}},
               {"message": {"chat": {"id": 123, "type": "private"}, "text": "secret"}}]
    assert extract_chats(updates) == [chat]


def test_setup_rejects_write_methods_without_network():
    with pytest.raises(ValueError):
        telegram_call("fake-token", "sendMessage", text="no send")


def test_network_failure_does_not_expose_token(monkeypatch):
    token = "fake-token-never-print"
    def fail(*args, **kwargs):
        raise requests.ConnectionError(f"https://api.telegram.org/bot{token}/getMe")
    monkeypatch.setattr(requests, "post", fail)
    with pytest.raises(RuntimeError) as error:
        telegram_call(token, "getMe")
    assert token not in str(error.value)


def test_api_error_redacts_token(monkeypatch):
    token = "fake-token-never-print"
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: SimpleNamespace(ok=False, json=lambda: {"ok": False, "description": f"invalid {token}"}))
    with pytest.raises(RuntimeError) as error:
        telegram_call(token, "getMe")
    assert token not in str(error.value)
    assert "[REDACTED]" in str(error.value)
