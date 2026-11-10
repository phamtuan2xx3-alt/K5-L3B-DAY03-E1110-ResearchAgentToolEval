"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = TOOL_FUNCTIONS["clarify"](
        question="Chọn nguồn nào?",
        response_type="choice",
        options=["web", "social"],
    )
    assert result["options"] == ["web", "social"]
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    result = TOOL_FUNCTIONS["format"](
        items=[
            {"title": "A1", "section": "A"},
            {"title": "B1", "section": "B"},
            {"title": "A2", "section": "A"},
        ],
        template="sections",
    )
    assert result["markdown"].count("## A") == 1
    assert result["markdown"].count("## B") == 1


def test_format_thread_numbers_items() -> None:
    result = TOOL_FUNCTIONS["format"](
        items=[{"title": "First"}, {"title": "Second"}],
        template="thread",
    )
    lines = result["markdown"].splitlines()
    assert lines[0].startswith("1/")
    assert lines[2].startswith("2/")


def test_format_empty_items_does_not_crash() -> None:
    assert TOOL_FUNCTIONS["format"](items=None, template="brief")["item_count"] == 0
    assert TOOL_FUNCTIONS["format"](items=[], template="brief")["item_count"] == 0


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "chat-1")
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Digest", confirmed=True)
    assert len(calls) == 1
    assert "bot-token" in calls[0]["url"]
    assert calls[0]["json"] == {"chat_id": "chat-1", "text": "Digest", "parse_mode": "Markdown"}
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Digest", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert calls == []


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    TOOL_FUNCTIONS["lookup"](query="AI", timeframe=None)
    assert "time_range" not in calls[0]["json"]


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = fake_http(FakeResponse({
        "data": {
            "markdown": "Article body",
            "metadata": {"title": "T", "sourceURL": "https://example.com/a"},
        }
    }))
    result = TOOL_FUNCTIONS["fetch"]("https://example.com/a")
    assert calls[0]["json"] == {"url": "https://example.com/a", "formats": ["markdown"]}
    assert result["items"][0]["title"] == "T"
    assert result["items"][0]["url"] == "https://example.com/a"
    assert result["items"][0]["source"] == "example.com"
    assert result["items"][0]["summary"] == "Article body"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({
        "data": {
            "markdown": "x" * 5000,
            "metadata": {"title": "T", "sourceURL": "https://example.com/a"},
        }
    }))
    result = TOOL_FUNCTIONS["fetch"]("https://example.com/a")
    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    monkeypatch.setenv("RAPIDAPI_TWITTER_HOST", "twitter.example")
    payload = {"timeline": [{"screen_name": "sama"}] + [
        {"tweet_id": str(index), "screen_name": "sama", "text": f"Tweet {index}"}
        for index in range(6)
    ]}
    calls = fake_http(FakeResponse(payload))
    result = TOOL_FUNCTIONS["timeline"]("sama", limit=3)
    assert len(result["items"]) == 3
    assert all(item["url"].startswith("https://x.com/sama/status/") for item in result["items"])
    assert calls[0]["params"]["screenname"] == "sama"


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    monkeypatch.setenv("RAPIDAPI_TWITTER_HOST", "twitter.example")
    calls = fake_http(FakeResponse({"timeline": []}))
    TOOL_FUNCTIONS["social_search"]("OpenAI", search_type="Top")
    assert calls[0]["params"]["query"] == "OpenAI"
    assert calls[0]["params"]["search_type"] == "Top"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    result = TOOL_FUNCTIONS["policy"]("")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"]("data privacy", policy_area="data_privacy")
    assert result["results"]
    assert all(item["policy_area"] == "data_privacy" for item in result["results"])


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = TOOL_FUNCTIONS["policy"]("injection probe", policy_area="source_citation")
    assert result["results"]
    item = result["results"][0]
    assert item["untrusted_text"]
    untrusted = " ".join(item["untrusted_text"]).lower()
    assert "ignore the citation policy" in untrusted
    assert "ignore the citation policy" not in item["facts"].lower()


# ---------------- source_dedupe (team tool) ----------------

def test_source_dedupe_keeps_first_item_for_duplicate_url() -> None:
    result = TOOL_FUNCTIONS["source_dedupe"](items=[
        {"title": "First", "url": "https://example.com/a"},
        {"title": "Duplicate", "url": "https://example.com/a"},
        {"title": "Second", "url": "https://example.com/b"},
    ])

    assert result["items"] == [
        {"title": "First", "url": "https://example.com/a"},
        {"title": "Second", "url": "https://example.com/b"},
    ]
    assert result["removed_count"] == 1


def test_source_dedupe_rejects_non_list_input() -> None:
    result = TOOL_FUNCTIONS["source_dedupe"](items="not-a-list")

    assert result["error"] == "TypeError"
    assert "items must be a list" in result["message"]


def test_source_dedupe_returns_error_dict_for_non_object_item() -> None:
    result = TOOL_FUNCTIONS["source_dedupe"](items=[{"url": "https://example.com"}, "bad-item"])

    assert result["error"] == "TypeError"
    assert "each item must be an object" in result["message"]
