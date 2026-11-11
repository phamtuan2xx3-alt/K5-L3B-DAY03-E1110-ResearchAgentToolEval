from __future__ import annotations

from datetime import date
from typing import Any
from urllib.parse import urlsplit

from tools._research import normalize_url, require_items, require_text
from tools._shared import err, terms


def rank_sources(
    query: str = "",
    items: list[dict[str, Any]] | None = None,
    preferred_domains: list[str] | None = None,
    reference_date: str | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    try:
        keywords = terms(require_text(query, "query"))
        if not keywords:
            raise ValueError("query must contain searchable keywords")
        entries = require_items(items, "items")
        if type(limit) is not int or limit < 1:
            raise ValueError("limit must be a positive integer")
        today = date.today() if reference_date is None else date.fromisoformat(require_text(reference_date, "reference_date"))
        domains = [] if preferred_domains is None else preferred_domains
        if not isinstance(domains, list):
            raise ValueError("preferred_domains must be a list of domain names")
        preferred: list[str] = []
        for value in domains:
            name = require_text(value, "preferred domain").lower()
            if any(character in name for character in "/:@?#[]"):
                raise ValueError("preferred_domains must contain domain names without schemes, paths or ports")
            parsed = urlsplit(normalize_url(f"https://{name}"))
            preferred.append(parsed.hostname or "")
        ranked: list[dict[str, Any]] = []
        for item in entries:
            host = urlsplit(normalize_url(item.get("url"))).hostname or ""
            title = require_text(item.get("title", ""), "item title", allow_empty=True)
            summary = require_text(item.get("summary", ""), "item summary", allow_empty=True)
            relevance = len(keywords & terms(f"{title} {summary}")) / len(keywords)
            freshness = 0.0
            if item.get("published_at") is not None:
                published = date.fromisoformat(require_text(item["published_at"], "published_at"))
                age = (today - published).days
                if age >= 0:
                    freshness = 1 / (1 + age / 30)
            preferred_domain = any(host == name or host.endswith(f".{name}") for name in preferred)
            score = 0.6 * relevance + 0.25 * freshness + 0.15 * preferred_domain
            ranked.append({**item, "ranking": {
                "score": round(score, 6), "relevance": round(relevance, 6),
                "freshness": round(freshness, 6), "preferred_domain": preferred_domain,
            }})
        ranked.sort(key=lambda item: item["ranking"]["score"], reverse=True)
        return {"tool": "rank_sources", "items": ranked[:limit], "total_count": len(entries), "reference_date": today.isoformat()}
    except Exception as exc:
        return err("rank_sources", exc)
