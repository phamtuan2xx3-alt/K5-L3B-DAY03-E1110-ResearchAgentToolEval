from types import SimpleNamespace

from providers.ollama_provider import OllamaProvider
from providers.openai_provider import OpenAIProvider


def fake_sdk(monkeypatch):
    calls = []
    def create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="ok", tool_calls=[]), finish_reason="length")],
                               usage=SimpleNamespace(prompt_tokens=8, completion_tokens=2, total_tokens=10))
    import openai
    monkeypatch.setattr(openai, "OpenAI", lambda **kwargs: SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create))))
    return calls


def test_local_requests_are_bounded_and_report_finish_reason(monkeypatch):
    monkeypatch.delenv("OLLAMA_MAX_OUTPUT_TOKENS", raising=False)
    calls = fake_sdk(monkeypatch)
    provider = OllamaProvider()
    provider.complete([{"role": "user", "content": "test"}])
    assert calls[0]["max_tokens"] == 512
    assert provider.last_finish_reason == "length"
    assert provider.last_usage == {"prompt_tokens": 8, "completion_tokens": 2, "total_tokens": 10}


def test_cloud_openai_request_not_changed_by_local_limit(monkeypatch):
    calls = fake_sdk(monkeypatch)
    OpenAIProvider(api_key_default="fake-key").complete([{"role": "user", "content": "test"}])
    assert "max_tokens" not in calls[0]
