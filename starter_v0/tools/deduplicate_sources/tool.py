from __future__ import annotations

from typing import Any

from tools._research import normalize_url, require_items
from tools._shared import err


def deduplicate_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    try:
        sources = require_items(items, "items")
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for item in sources:
            key = normalize_url(item.get("url"))
            if key not in seen:
                seen.add(key)
                unique.append(dict(item))
        return {
            "tool": "deduplicate_sources", "items": unique,
            "original_count": len(sources), "unique_count": len(unique),
            "removed_count": len(sources) - len(unique),
        }
    except Exception as exc:
        return err("deduplicate_sources", exc)
