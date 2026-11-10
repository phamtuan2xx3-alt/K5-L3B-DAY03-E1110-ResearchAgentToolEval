from __future__ import annotations

from typing import Any


def deduplicate_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    try:
        if items is None:
            items = []
        if not isinstance(items, list):
            raise TypeError("items must be a list")

        unique: list[dict[str, Any]] = []
        seen_urls: set[str] = set()
        for item in items:
            if not isinstance(item, dict):
                raise TypeError("each item must be an object")
            url = str(item.get("url") or "").strip()
            if url and url in seen_urls:
                continue
            if url:
                seen_urls.add(url)
            unique.append(item)

        return {
            "tool": "source_dedupe",
            "items": unique,
            "removed_count": len(items) - len(unique),
        }
    except Exception as exc:
        return {
            "tool": "source_dedupe",
            "error": type(exc).__name__,
            "message": str(exc),
        }
