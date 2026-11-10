import requests

from tools.social_search.tool import search_tweets


def test_subscription_error_explains_required_action_without_leaking_key(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "private-test-key")
    response = requests.Response()
    response.status_code = 403
    response._content = b'{"message":"You are not subscribed to this API. private-test-key"}'
    monkeypatch.setattr(requests, "get", lambda *a, **kw: response)
    result = search_tweets("OpenAI")
    assert result["error"] == "RuntimeError"
    assert "subscribe" in result["message"].lower()
    assert "RAPIDAPI_KEY" in result["message"]
    assert "private-test-key" not in str(result)
    assert "items" not in result


def test_other_forbidden_error_is_not_misdiagnosed_as_subscription(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "private-test-key")
    response = requests.Response()
    response.status_code = 403
    response._content = b'{"message":"Forbidden"}'
    monkeypatch.setattr(requests, "get", lambda *a, **kw: response)
    assert search_tweets("OpenAI")["error"] == "HTTPError"
