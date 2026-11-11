from __future__ import annotations

from html import escape
from typing import Any

from tools._research import normalize_url, require_items, require_text
from tools._shared import err


FIELDS = ("year", "authors", "topic", "method", "limitations", "summary", "url")
DEFAULT_FIELDS = ("year", "authors", "topic", "method", "limitations")


def _cell(value: Any) -> str:
    if value is None or value == "" or value == []:
        return "Chưa cung cấp"
    text = ", ".join(value) if isinstance(value, list) else str(value)
    return escape(text, quote=False).replace("\\", "\\\\").replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def compare_papers(papers: list[dict[str, Any]] | None = None, fields: list[str] | None = None) -> dict[str, Any]:
    try:
        entries = require_items(papers, "papers")
        if len(entries) < 2:
            raise ValueError("papers must contain at least two papers")
        selected = list(DEFAULT_FIELDS) if fields is None else fields
        if not isinstance(selected, list) or not selected or any(not isinstance(field, str) or field not in FIELDS for field in selected):
            raise ValueError(f"fields must be a non-empty list drawn from {', '.join(FIELDS)}")
        if len(selected) != len(set(selected)):
            raise ValueError("fields must not contain duplicates")
        comparison: list[dict[str, Any]] = []
        for paper in entries:
            title = require_text(paper.get("title"), "paper title")
            year = paper.get("year")
            if year is not None and (type(year) is not int or not 1000 <= year <= 9999):
                raise ValueError("paper year must be a four-digit integer")
            authors = paper.get("authors")
            if authors is not None:
                if not isinstance(authors, list):
                    raise ValueError("paper authors must be a list of strings")
                for author in authors:
                    require_text(author, "author")
            for field in FIELDS:
                if field not in {"year", "authors"} and paper.get(field) is not None:
                    require_text(paper[field], f"paper {field}", allow_empty=True)
            if paper.get("url"):
                normalize_url(paper["url"])
            comparison.append({"title": title, **{field: paper.get(field) for field in selected}})
        columns = ["title", *selected]
        table = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
        table.extend("| " + " | ".join(_cell(row[column]) for column in columns) + " |" for row in comparison)
        return {"tool": "compare_papers", "comparison": comparison, "markdown": "\n".join(table), "paper_count": len(entries)}
    except Exception as exc:
        return err("compare_papers", exc)
