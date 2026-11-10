from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit, urlunsplit

from tools._shared import err


def _canonical_url(value: Any) -> tuple[str | None, str | None]:
    if not isinstance(value, str) or not value.strip():
        return None, None
    value = value.strip()
    if any(char.isspace() for char in value):
        return None, None
    try:
        parts = urlsplit(value)
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
            return None, None
        host = parts.hostname.lower()
        netloc = f"[{host}]" if ":" in host else host
        port = parts.port
        if port is not None and (parts.scheme.lower(), port) not in {("http", 80), ("https", 443)}:
            netloc += f":{port}"
        canonical = urlunsplit((parts.scheme.lower(), netloc, parts.path or "/", parts.query, ""))
        return canonical, host
    except ValueError:
        return None, None


def audit_sources(items: list[dict[str, Any]] | None = None, require_date: bool = True) -> dict[str, Any]:
    """Inspect supplied source metadata without fetching URLs or changing input."""
    try:
        if not isinstance(items, list) or not items:
            raise ValueError("items must be a non-empty list of source objects")
        if not isinstance(require_date, bool):
            raise TypeError("require_date must be a boolean")
        if any(not isinstance(item, dict) for item in items):
            raise TypeError("every source item must be an object")

        seen: dict[str, int] = {}
        results: list[dict[str, Any]] = []
        issues: list[dict[str, Any]] = []
        for index, item in enumerate(items):
            item_issues: list[dict[str, Any]] = []

            def flag(code: str, **details: Any) -> None:
                issue = {"index": index, "code": code, **details}
                item_issues.append(issue)
                issues.append(issue)

            url = item.get("url")
            canonical, host = _canonical_url(url)
            if url is None or (isinstance(url, str) and not url.strip()):
                flag("missing_url")
            elif canonical is None:
                flag("invalid_url")
            if canonical:
                if canonical in seen:
                    flag("duplicate_url", duplicate_of=seen[canonical])
                else:
                    seen[canonical] = index
            if not isinstance(item.get("title"), str) or not item["title"].strip():
                flag("missing_title")
            dates = [item.get(key) for key in ("published_at", "published_date", "date")]
            if require_date and not any(isinstance(date, str) and date.strip() for date in dates):
                flag("missing_date")
            results.append({"index": index, "canonical_url": canonical, "source_domain": host, "issues": item_issues})
        return {
            "tool": "source_audit",
            "status": "needs_review" if issues else "ok",
            "summary": {"item_count": len(items), "unique_url_count": len(seen), "issue_count": len(issues),
                        "duplicate_count": sum(issue["code"] == "duplicate_url" for issue in issues)},
            "results": results,
            "issues": issues,
            "limitations": "Metadata only: no network requests, fact checking, credibility scoring, date validation, or freshness guarantee.",
        }
    except Exception as exc:
        return err("source_audit", exc)
