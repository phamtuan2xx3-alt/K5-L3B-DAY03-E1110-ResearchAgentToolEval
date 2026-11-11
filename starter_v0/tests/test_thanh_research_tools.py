"""Regression tests imported from origin/DoMinhThanh for its four research tools."""
import pytest
from tools import TOOL_FUNCTIONS

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


