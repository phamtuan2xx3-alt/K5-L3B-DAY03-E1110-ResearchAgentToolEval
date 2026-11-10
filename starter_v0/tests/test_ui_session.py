from pathlib import Path
import shutil

import pytest

from providers.base import ModelResponse, ToolCall
from ui_session import ResearchSession, redact


class FakeProvider:
    def __init__(self, responses):
        self.responses = iter(responses)

    def complete(self, *args, **kwargs):
        return next(self.responses)


@pytest.fixture
def session(tmp_path):
    source = Path(__file__).resolve().parents[1]
    (tmp_path / "artifacts").mkdir()
    for name in ("system_prompt.md", "tools.yaml"):
        shutil.copyfile(source / "artifacts" / name, tmp_path / "artifacts" / name)
    return ResearchSession(root=tmp_path)


def test_model_cannot_send_even_if_it_sets_confirmed_true(session, monkeypatch):
    def unexpected_send(_call):
        raise AssertionError("Model must not send without the UI button")
    monkeypatch.setattr("ui_session.execute_tool_call", unexpected_send)
    provider = FakeProvider([ModelResponse(tool_calls=[ToolCall("send", {"text": "Exact approved draft", "confirmed": True})])])
    turn = session.run("Prepare a draft", provider=provider)
    assert turn["status"] == "waiting_for_user"
    assert session.pending_send == "Exact approved draft"
    assert turn["tool_events"][0]["result"]["status"] == "pending_ui_approval"


def test_ui_approval_sends_exact_text_once_and_records_it(session):
    calls = []
    def send(call):
        calls.append(call)
        return {"tool": call.name, "args": call.args, "result": {"status": "sent"}}
    session.pending_send = "Draft A\nSource: https://example.org/a"
    turn = session.resolve_send(True, executor=send)
    assert calls[0].args == {"text": "Draft A\nSource: https://example.org/a", "confirmed": True}
    assert turn["status"] == "sent" and turn["origin"] == "user_confirmation"
    assert session.path.exists()
    with pytest.raises(ValueError):
        session.resolve_send(True, executor=send)
    assert len(calls) == 1


def test_cancel_never_calls_send(session):
    session.pending_send = "Draft A"
    def unexpected_send(_call):
        raise AssertionError("Cancelled content must not be sent")
    assert session.resolve_send(False, executor=unexpected_send)["status"] == "cancelled"
    assert session.pending_send is None


def test_changed_channel_invalidates_approval(session, monkeypatch):
    session.pending_send = "Draft A"
    session.pending_target = "-100111"
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100222")
    def unexpected_send(_call):
        raise AssertionError("Changed destination requires new approval")
    turn = session.resolve_send(True, executor=unexpected_send)
    assert turn["status"] == "target_changed"
    assert session.pending_send is None


def test_transcript_redacts_known_api_secrets(session, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-secret-must-not-leak")
    provider = FakeProvider([ModelResponse(text="echo: test-secret-must-not-leak")])
    session.run("test-secret-must-not-leak", provider=provider)
    assert "test-secret-must-not-leak" not in session.path.read_text(encoding="utf-8")
    assert "[REDACTED]" in session.path.read_text(encoding="utf-8")
    assert redact({"message": ["test-secret-must-not-leak"]}) == {"message": ["[REDACTED]"]}


def test_tool_error_remains_visible_in_transcript(session):
    provider = FakeProvider([ModelResponse(tool_calls=[ToolCall("not_registered", {})]), ModelResponse(text="Tool failed.")])
    turn = session.run("Check this source", provider=provider)
    assert turn["tool_events"][0]["result"]["error"] == "unknown_tool"
    assert turn["assistant_text"] == "Tool failed."
