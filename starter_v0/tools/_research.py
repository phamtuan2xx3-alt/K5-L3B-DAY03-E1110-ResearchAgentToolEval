from __future__ import annotations

import re
from typing import Any
from urllib.parse import unquote, urlsplit, urlunsplit


def require_text(value: Any, name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ValueError(f"{name} must be {'a string' if allow_empty else 'a non-empty string'}")
    return value.strip()


def require_items(value: Any, name: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{name} must be a list of objects")
    return value


def normalize_url(value: Any) -> str:
    url = require_text(value, "url")
    if re.search(r"\s", url):
        raise ValueError("url must not contain whitespace")
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("url must be an absolute HTTP or HTTPS URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("url must not contain credentials")
    hostname = parsed.hostname.lower()
    port = parsed.port
    host = f"[{hostname}]" if ":" in hostname else hostname
    if port is not None and (parsed.scheme, port) not in {("http", 80), ("https", 443)}:
        host += f":{port}"
    query_parts = []
    for part in parsed.query.split("&"):
        key = unquote(part.split("=", 1)[0]).lower()
        if not key.startswith("utm_") and key not in {"fbclid", "gclid"}:
            query_parts.append(part)
    return urlunsplit((parsed.scheme, host, parsed.path or "/", "&".join(query_parts), ""))
