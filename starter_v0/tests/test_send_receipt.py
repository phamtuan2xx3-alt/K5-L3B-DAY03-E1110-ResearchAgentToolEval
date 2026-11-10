import pytest

from conftest import FakeResponse
from tools.send.tool import send_telegram


@pytest.mark.parametrize("confirmed", ["false", "true", 1])
def test_send_requires_literal_boolean_confirmation(confirmed, monkeypatch, fake_http):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    calls = fake_http(FakeResponse({"ok": True, "result": {"message_id": 12, "chat": {"id": -100123}}}))
    result = send_telegram(text="Draft", confirmed=confirmed)
    assert result["status"] == "needs_confirmation"
    assert calls == []


def test_send_returns_telegram_receipt(monkeypatch, fake_http):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    calls = fake_http(FakeResponse({"ok": True, "result": {"message_id": 12, "date": 1794300000, "chat": {"id": -100123}}}))
    result = send_telegram(text="Approved draft", confirmed=True)
    assert result["status"] == "sent"
    assert result["message_id"] == 12 and result["chat_id"] == -100123
    assert result["date"] == 1794300000
    assert calls[0]["json"]["text"] == "Approved draft"


def test_http_200_with_telegram_failure_is_not_sent(monkeypatch, fake_http):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    fake_http(FakeResponse({"ok": False, "description": "Chat not found"}))
    result = send_telegram(text="Draft", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert "status" not in result


def test_send_does_not_claim_receipt_when_missing(monkeypatch, fake_http):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    fake_http(FakeResponse({"ok": True, "result": {}}))
    result = send_telegram(text="Draft", confirmed=True)
    assert result["error"] == "RuntimeError"
