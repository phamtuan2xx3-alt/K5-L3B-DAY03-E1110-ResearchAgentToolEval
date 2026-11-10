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
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "telegram-test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001234567890")
    calls = fake_http(FakeResponse({"ok": True, "result": {"message_id": 42, "chat": {"id": -1001234567890, "type": "channel"}}}))
    result = TOOL_FUNCTIONS["send"](text="Bản tin đã xác nhận", confirmed=True)
    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert calls[0]["json"]["chat_id"] == "-1001234567890"
    assert calls[0]["json"]["text"] == "Bản tin đã xác nhận"
    assert result["status"] == "sent"
    assert result["message_id"] == 42
    assert result["chat_id"] == -1001234567890


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Bản tin", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert calls == []


@pytest.mark.parametrize("confirmed", ["false", "true", 1])
def test_send_non_boolean_confirmation_never_posts(confirmed, monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "telegram-test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001234567890")
    calls = fake_http(FakeResponse({"ok": True, "result": {"message_id": 42}}))
    result = TOOL_FUNCTIONS["send"](text="Unapproved message", confirmed=confirmed)
    assert calls == []
    assert result["status"] == "needs_confirmation"


@pytest.mark.parametrize("text", ["", "  ", None, 7])
def test_send_invalid_text_returns_error_before_network(text, monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "telegram-test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001234567890")
    calls = fake_http(FakeResponse({"ok": True, "result": {"message_id": 42}}))
    result = TOOL_FUNCTIONS["send"](text=text, confirmed=True)
    assert result["error"] == "ValueError"
    assert calls == []


def test_send_api_rejection_is_not_reported_as_sent(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "telegram-test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001234567890")
    fake_http(FakeResponse({"ok": False, "description": "Delivery refused"}))
    result = TOOL_FUNCTIONS["send"](text="Approved message", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert "status" not in result


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


def test_deduplicate_sources_removes_tracking_and_keeps_first_item() -> None:
    items = [
        {"title": "First", "url": "https://EXAMPLE.com:443/paper?id=7&utm_source=feed#abstract"},
        {"title": "Duplicate", "url": "https://example.com/paper?id=7"},
        {"title": "Other paper", "url": "https://example.com/paper?id=8"},
    ]
    result = TOOL_FUNCTIONS["deduplicate_sources"](items=items)
    assert result["items"] == [items[0], items[2]]
    assert result["original_count"] == 3
    assert result["unique_count"] == 2
    assert result["removed_count"] == 1
    assert items[0]["url"].endswith("#abstract")


def test_deduplicate_sources_preserves_path_case_and_meaningful_query() -> None:
    items = [{"url": url} for url in [
        "https://example.com/Paper?q=A", "https://example.com/paper?q=A",
        "https://example.com/Paper?q=a", "http://example.com/Paper?q=A",
    ]]
    assert TOOL_FUNCTIONS["deduplicate_sources"](items=items)["unique_count"] == 4


def test_deduplicate_sources_accepts_empty_list() -> None:
    assert TOOL_FUNCTIONS["deduplicate_sources"](items=[])["items"] == []


@pytest.mark.parametrize("items", [None, "bad", [{}], [None], [{"url": ""}], [{"url": "ftp://example.com/a"}], [{"url": "https://example.com:bad/a"}], [{"url": "https://user:pass@example.com/a"}]])
def test_deduplicate_sources_bad_input_returns_error(items) -> None:
    result = TOOL_FUNCTIONS["deduplicate_sources"](items=items)
    assert result["error"] == "ValueError"
    assert result["message"]


def test_check_citations_reports_missing_and_unused_ids() -> None:
    result = TOOL_FUNCTIONS["check_citations"](
        draft="Evidence [1, 2], repeated [1], other [study-a].",
        sources=[{"id": "1", "url": "https://example.com/a"}, {"id": "unused", "url": "https://example.com/b"}],
    )
    assert result["citations"] == ["1", "2", "study-a"]
    assert result["missing_sources"] == ["2", "study-a"]
    assert result["unused_sources"] == ["unused"]
    assert result["valid"] is False


def test_check_citations_ignores_markdown_links_images_and_code() -> None:
    result = TOOL_FUNCTIONS["check_citations"](
        draft="[link](https://example.com) ![image](x) [label][ref] `code [4]`\n```text\n[5]\n```\nEvidence [1].",
        sources=[{"id": "1", "url": "https://example.com"}],
    )
    assert result["citations"] == ["1"]
    assert result["missing_sources"] == []
    assert result["valid"] is True


def test_check_citations_empty_sources_reports_unresolved_references() -> None:
    result = TOOL_FUNCTIONS["check_citations"](draft="Evidence [1].", sources=[])
    assert result["missing_sources"] == ["1"]
    assert result["valid"] is False


@pytest.mark.parametrize("draft,sources", [
    (None, []), ("", []), ("Text", None),
    ("Text", [{"id": "1"}]),
    ("Text", [{"id": "1", "url": "https://example.com"}, {"id": "1", "url": "https://example.org"}]),
    ("Text", [{"id": "bad id", "url": "https://example.com"}]),
])
def test_check_citations_bad_input_returns_error(draft, sources) -> None:
    result = TOOL_FUNCTIONS["check_citations"](draft=draft, sources=sources)
    assert result["error"] == "ValueError"
    assert result["message"]


def test_compare_papers_preserves_metadata_and_marks_missing_fields() -> None:
    papers = [{"title": "A", "year": 2025, "authors": ["An", "Binh"], "method": "Survey"}, {"title": "B", "year": 2026}]
    result = TOOL_FUNCTIONS["compare_papers"](papers=papers, fields=["year", "authors", "method"])
    assert result["comparison"] == [
        {"title": "A", "year": 2025, "authors": ["An", "Binh"], "method": "Survey"},
        {"title": "B", "year": 2026, "authors": None, "method": None},
    ]
    assert "An, Binh" in result["markdown"]
    assert "Chưa cung cấp" in result["markdown"]
    assert result["paper_count"] == 2
    assert "method" not in papers[1]


def test_compare_papers_escapes_table_cells() -> None:
    result = TOOL_FUNCTIONS["compare_papers"](
        papers=[{"title": "A|B", "method": "Line 1\nLine 2 <script>"}, {"title": "C"}], fields=["method"],
    )
    assert "A\\|B" in result["markdown"]
    assert "Line 1<br>Line 2 &lt;script&gt;" in result["markdown"]
    assert len(result["markdown"].splitlines()) == 4


@pytest.mark.parametrize("papers,fields", [
    (None, None), ([], None), ([{"title": "A"}], None),
    ([{"title": "A"}, {}], None),
    ([{"title": "A", "year": True}, {"title": "B"}], None),
    ([{"title": "A", "authors": "An"}, {"title": "B"}], None),
    ([{"title": "A"}, {"title": "B"}], ["invented"]),
    ([{"title": "A"}, {"title": "B"}], []),
])
def test_compare_papers_bad_input_returns_error(papers, fields) -> None:
    result = TOOL_FUNCTIONS["compare_papers"](papers=papers, fields=fields)
    assert result["error"] == "ValueError"
    assert result["message"]


def test_rank_sources_scores_relevance_freshness_and_domain() -> None:
    items = [
        {"title": "Robotics", "url": "https://other.org/a", "published_at": "2025-12-02"},
        {"title": "Robotics", "url": "https://lab.example.org/a", "published_at": "2026-01-01"},
        {"title": "Cooking", "url": "https://example.org/b", "published_at": "2026-01-01"},
    ]
    result = TOOL_FUNCTIONS["rank_sources"](query="robotics", items=items, preferred_domains=["example.org"], reference_date="2026-01-01", limit=2)
    assert [item["url"] for item in result["items"]] == ["https://lab.example.org/a", "https://other.org/a"]
    assert result["items"][0]["ranking"] == {"score": 1.0, "relevance": 1.0, "freshness": 1.0, "preferred_domain": True}
    assert result["items"][1]["ranking"]["score"] == 0.725
    assert result["total_count"] == 3
    assert result["reference_date"] == "2026-01-01"
    assert all("ranking" not in item for item in items)


def test_rank_sources_matches_vietnamese_accents() -> None:
    result = TOOL_FUNCTIONS["rank_sources"](query="trí tuệ", items=[{"title": "Tri tue", "url": "https://example.com"}], reference_date="2026-01-01")
    assert result["items"][0]["ranking"]["relevance"] == 1.0


def test_rank_sources_preserves_ties_and_rejects_lookalike_domain_bonus() -> None:
    result = TOOL_FUNCTIONS["rank_sources"](
        query="robotics", preferred_domains=["example.org"], reference_date="2026-01-01",
        items=[{"title": "robotics", "url": "https://evil-example.org/a"}, {"title": "robotics", "url": "https://other.org/b", "published_at": "2026-01-02"}],
    )
    assert [item["url"] for item in result["items"]] == ["https://evil-example.org/a", "https://other.org/b"]
    assert all(item["ranking"]["score"] == 0.6 for item in result["items"])


@pytest.mark.parametrize("kwargs", [
    {"query": ""}, {"query": 1}, {"items": "bad"}, {"limit": 0}, {"limit": True},
    {"preferred_domains": "example.org"}, {"preferred_domains": ["https://example.org"]},
    {"reference_date": "not-a-date"},
    {"items": [{"url": "https://example.com", "published_at": "2026-02-30"}]},
    {"items": [{"url": "https://example.com", "title": []}]},
])
def test_rank_sources_bad_input_returns_error(kwargs) -> None:
    arguments = {"query": "robotics", "items": [{"title": "robotics", "url": "https://example.com"}], "reference_date": "2026-01-01"}
    arguments.update(kwargs)
    result = TOOL_FUNCTIONS["rank_sources"](**arguments)
    assert result["error"] == "ValueError"
    assert result["message"]


def test_check_citations_ignores_reference_link_definitions() -> None:
    result = TOOL_FUNCTIONS["check_citations"](draft="[label][ref]\n\n[ref]: https://example.org", sources=[])
    assert result["citations"] == []
    assert result["valid"] is True


def test_check_citations_ignores_matching_backtick_runs() -> None:
    result = TOOL_FUNCTIONS["check_citations"](draft="Use `` [missing] `inner` `` as literal. Evidence [1].", sources=[{"id": "1", "url": "https://example.org"}])
    assert result["citations"] == ["1"]
    assert result["valid"] is True


def test_deduplicate_sources_preserves_distinct_encoded_query_bytes() -> None:
    result = TOOL_FUNCTIONS["deduplicate_sources"](items=[
        {"url": "https://example.org/?q=%FF&utm_source=feed"},
        {"url": "https://example.org/?q=%FE"},
        {"url": "https://example.org/?q=%FF"},
    ])
    assert result["unique_count"] == 2
    assert [item["url"] for item in result["items"]] == ["https://example.org/?q=%FF&utm_source=feed", "https://example.org/?q=%FE"]
