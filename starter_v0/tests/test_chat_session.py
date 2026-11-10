from __future__ import annotations

import json
from pathlib import Path

from chat import run_model_tool_loop, write_transcript
from providers.base import ModelResponse, ToolCall


class ScriptedProvider:
    default_model = "test-model"

    def __init__(self, responses):
        self.responses = iter(responses)
        self.messages = []

    def complete(self, messages, tools=None, **kwargs):
        self.messages.append(list(messages))
        return next(self.responses)


def test_ui_allowlist_blocks_generated_send_before_execution(monkeypatch) -> None:
    provider = ScriptedProvider([
        ModelResponse(tool_calls=[ToolCall("send", {"text": "Do not deliver", "confirmed": True})]),
        ModelResponse(text="Delivery is unavailable."),
    ])
    def forbidden(call):
        raise AssertionError("Disallowed tool reached executor")
    monkeypatch.setattr("chat.execute_tool_call", forbidden)
    result = run_model_tool_loop(provider=provider, messages=[], tools=[], model=None, max_tool_rounds=2, allowed_tools={"clarify"})
    assert result["status"] == "answered"
    assert result["tool_events"][0]["result"]["error"] == "tool_not_allowed"


def test_transcript_write_redacts_credentials_without_mutating_memory(tmp_path, monkeypatch) -> None:
    token = "1234567890:private-test-token"
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", token)
    path = tmp_path / "session.json"
    transcript = {"error": f"HTTP 403 https://api.telegram.org/bot{token}/sendMessage"}
    write_transcript(path, transcript)
    assert token not in path.read_text()
    assert "[REDACTED]" in path.read_text()
    assert token in transcript["error"]


def test_session_retains_context_and_writes_rounds(tmp_path, monkeypatch) -> None:
    from web_chat import ChatSession
    provider = ScriptedProvider([
        ModelResponse(tool_calls=[ToolCall("clarify", {"question": "Which URL?", "response_type": "text"})]),
        ModelResponse(text="Received URL."),
    ])
    monkeypatch.setattr("web_chat.make_provider", lambda name: provider)
    session = ChatSession(transcripts_dir=tmp_path)
    first = session.submit("Summarize this article")
    second = session.submit("https://example.org")
    assert first["status"] == "waiting_for_user"
    assert second["status"] == "answered"
    assert {"role": "assistant", "content": "Which URL?"} in provider.messages[1]
    transcript = json.loads(session.path.read_text())
    assert len(transcript["turns"]) == 2
    assert transcript["turns"][0]["tool_events"][0]["tool"] == "clarify"
    assert transcript["model"] == "test-model"


def test_new_sessions_have_independent_history_and_paths(tmp_path, monkeypatch) -> None:
    from web_chat import ChatSession
    monkeypatch.setattr("web_chat.make_provider", lambda name: ScriptedProvider([ModelResponse(text="Answer")]))
    first = ChatSession(transcripts_dir=tmp_path)
    second = ChatSession(transcripts_dir=tmp_path)
    first.submit("My private question")
    assert first.path != second.path
    assert second.history == []
    assert json.loads(second.export())["turns"] == []


def test_session_download_redacts_provider_error(tmp_path, monkeypatch) -> None:
    from web_chat import ChatSession
    token = "private-gemini-api-key-for-test"
    monkeypatch.setenv("GEMINI_API_KEY", token)
    class FailingProvider:
        default_model = "test-model"
        def complete(self, *args, **kwargs):
            raise RuntimeError("Request failed with " + token)
    monkeypatch.setattr("web_chat.make_provider", lambda name: FailingProvider())
    session = ChatSession(transcripts_dir=tmp_path)
    result = session.submit("Question")
    assert result["status"] == "provider_error"
    assert token not in session.export()
    assert token not in session.path.read_text()
    assert token not in result["assistant_text"]
    assert len(json.loads(session.export())["turns"]) == 1


def test_ui_excludes_send_from_model_declarations(tmp_path, monkeypatch) -> None:
    from web_chat import ChatSession
    monkeypatch.setattr("web_chat.make_provider", lambda name: ScriptedProvider([]))
    session = ChatSession(transcripts_dir=tmp_path)
    names = {tool["function"]["name"] for tool in session.tools}
    assert "send" not in names
    assert {"clarify", "lookup", "deduplicate_sources", "rank_sources"} <= names


def test_ui_renders_and_submits_a_chat_message(tmp_path, monkeypatch) -> None:
    from streamlit.testing.v1 import AppTest
    from web_chat import ChatSession
    provider = ScriptedProvider([ModelResponse(text="A useful answer")])
    monkeypatch.setattr("web_chat.make_provider", lambda name: provider)
    at = AppTest.from_file(str(Path(__file__).parents[1] / "app.py"))
    at.session_state["conversation"] = ChatSession(transcripts_dir=tmp_path)
    at.run()
    assert not at.exception
    at.chat_input[0].set_value("My research question").run()
    assert not at.exception
    assert len(at.chat_message) == 2
    assert "A useful answer" in [item.value for item in at.markdown]
    assert json.loads(at.session_state["conversation"].export())["turns"][0]["user"] == "My research question"


def test_ui_new_chat_does_not_reuse_previous_history(tmp_path, monkeypatch) -> None:
    from streamlit.testing.v1 import AppTest
    from web_chat import ChatSession
    monkeypatch.setattr("web_chat.make_provider", lambda name: ScriptedProvider([ModelResponse(text="First answer")]))
    initial = ChatSession(transcripts_dir=tmp_path)
    initial.submit("Private first-session question")
    at = AppTest.from_file(str(Path(__file__).parents[1] / "app.py"))
    at.session_state["conversation"] = initial
    at.run()
    next(button for button in at.button if button.label == "Cuộc trò chuyện mới").click().run()
    assert not at.exception
    assert at.session_state["conversation"].path != initial.path
    assert at.session_state["conversation"].history == []
    assert len(at.chat_message) == 0
    assert initial.path.exists()


def test_provider_failure_keeps_previously_executed_tool_results(tmp_path, monkeypatch) -> None:
    from web_chat import ChatSession
    class FailsAfterTool:
        default_model = "test-model"
        def __init__(self):
            self.calls = 0
        def complete(self, *args, **kwargs):
            self.calls += 1
            if self.calls == 1:
                return ModelResponse(tool_calls=[ToolCall("format", {"items": [], "template": "bullets"})])
            raise RuntimeError("Provider unavailable after tool execution")
    monkeypatch.setattr("web_chat.make_provider", lambda name: FailsAfterTool())
    session = ChatSession(transcripts_dir=tmp_path)
    result = session.submit("Format the supplied items")
    assert result["status"] == "provider_error"
    assert [event["tool"] for event in result["tool_events"]] == ["format"]
    saved = json.loads(session.path.read_text())["turns"][0]
    assert saved["rounds"][0]["tool_results"][0]["result"]["item_count"] == 0
    assert saved["rounds"][1]["status"] == "provider_error"
    assert session.history == []
