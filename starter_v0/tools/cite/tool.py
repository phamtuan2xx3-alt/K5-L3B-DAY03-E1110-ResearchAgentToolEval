from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from tools._shared import domain, err


def cite_sources(sources: list[dict[str, Any]] | None = None, style: str = "markdown") -> dict[str, Any]:
    """Build a citation block from a list of {title, url} sources.

    Local-only formatter: no network. Returns an error dict on bad input.
    """
    try:
        if sources is None:
            raise ValueError("sources is required")
        if not isinstance(sources, list):
            raise TypeError("sources must be a list of objects with title and url")
        if style not in {"markdown", "plain"}:
            raise ValueError("style must be 'markdown' or 'plain'")
        if len(sources) == 0:
            raise ValueError("sources must contain at least one item")

        lines: list[str] = []
        normalized: list[dict[str, str]] = []
        for index, item in enumerate(sources, start=1):
            if not isinstance(item, dict):
                raise TypeError(f"sources[{index - 1}] must be an object")
            title = str(item.get("title") or "").strip()
            url = str(item.get("url") or "").strip()
            if not url:
                raise ValueError(f"sources[{index - 1}].url is required")
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError(f"sources[{index - 1}].url must be an http(s) URL")
            label = title or domain(url) or url
            if style == "markdown":
                lines.append(f"[{index}] [{label}]({url})")
            else:
                lines.append(f"[{index}] {label} — {url}")
            normalized.append({"title": label, "url": url, "source": domain(url)})

        return {
            "tool": "cite_sources",
            "style": style,
            "markdown": "\n".join(lines),
            "citations": normalized,
            "citation_count": len(normalized),
        }
    except Exception as exc:  # noqa: BLE001 — tools must return error dicts
        return err("cite_sources", exc)
