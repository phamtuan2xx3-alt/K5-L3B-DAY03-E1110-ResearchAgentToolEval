from types import SimpleNamespace

import pytest

from providers.gemini_provider import GeminiProvider


class ApiFailure(Exception):
    def __init__(self, code):
        self.code = code


def run_fake(monkeypatch, outcomes):
    calls, waits = [], []
    pending = iter(outcomes)

    def generate(**kwargs):
        calls.append(kwargs["model"])
        outcome = next(pending)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    clock = [0.0]
    def sleep(seconds):
        waits.append(seconds)
        clock[0] += seconds
    monkeypatch.setattr("providers.gemini_provider.time.sleep", sleep)
    monkeypatch.setattr("providers.gemini_provider.time.monotonic", lambda: clock[0])
    monkeypatch.setattr(GeminiProvider, "_last_request_at", None)
    provider = GeminiProvider()
    client = SimpleNamespace(models=SimpleNamespace(generate_content=generate))
    return provider, client, calls, waits


def test_quota_waits_one_minute_then_retries_same_model(monkeypatch):
    provider, client, calls, waits = run_fake(monkeypatch, [ApiFailure(429), "ok"])
    assert provider._generate_with_retry(client, model=provider.default_model, contents=[], config=None) == "ok"
    assert calls == [provider.default_model] * 2
    assert waits == [60]
    assert provider.last_model == provider.default_model


def test_exhausted_quota_never_switches_model(monkeypatch):
    provider, client, calls, waits = run_fake(monkeypatch, [ApiFailure(429)] * 3)
    with pytest.raises(ApiFailure):
        provider._generate_with_retry(client, model=provider.default_model, contents=[], config=None)
    assert calls == [provider.default_model] * 3
    assert waits == [60, 60]
    assert provider.last_model is None


def test_invalid_key_is_not_retried(monkeypatch):
    provider, client, calls, waits = run_fake(monkeypatch, [ApiFailure(401)])
    with pytest.raises(ApiFailure):
        provider._generate_with_retry(client, model=provider.default_model, contents=[], config=None)
    assert len(calls) == 1
    assert waits == []


def test_retry_is_bounded_when_service_fails(monkeypatch):
    provider, client, calls, waits = run_fake(monkeypatch, [ApiFailure(503)] * 3)
    with pytest.raises(ApiFailure):
        provider._generate_with_retry(client, model=provider.default_model, contents=[], config=None)
    assert len(calls) == 3
    assert waits == [60] * 2
    assert provider.last_model is None


def test_dns_connection_error_waits_and_retries(monkeypatch):
    ConnectError = type("ConnectError", (Exception,), {"__module__": "httpx"})
    provider, client, calls, waits = run_fake(monkeypatch, [ConnectError("getaddrinfo failed"), "ok"])
    assert provider._generate_with_retry(client, model=provider.default_model, contents=[], config=None) == "ok"
    assert calls == [provider.default_model] * 2
    assert waits == [60]


def test_pacing_is_shared_between_provider_instances(monkeypatch):
    provider, client, calls, waits = run_fake(monkeypatch, ["ok"] * 20)
    for index in range(20):
        current = provider if index % 2 else GeminiProvider()
        assert current._generate_with_retry(client, model=current.default_model, contents=[], config=None) == "ok"
    assert calls == [provider.default_model] * 20
    assert waits == [4.5] * 19
    # 4.5-second spacing allows at most 14 request starts in any 60s window.
    starts = [4.5 * i for i in range(20)]
    assert max(sum(start <= t < start + 60 for t in starts) for start in starts) == 14
