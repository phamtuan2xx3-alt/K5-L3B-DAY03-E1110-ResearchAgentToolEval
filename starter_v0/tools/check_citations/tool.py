from __future__ import annotations

import re
from typing import Any

from tools._research import normalize_url, require_items, require_text
from tools._shared import err


CITATION = re.compile(r"(?<![!\]])\[([A-Za-z0-9_-]+(?:\s*,\s*[A-Za-z0-9_-]+)*)\](?![\[(])")
CODE = re.compile(r"(?<!`)(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)|~~~[\s\S]*?~~~")
REFERENCE_DEFINITION = re.compile(r"(?m)^ {0,3}\[[^\]\n]+\]:[^\n]*")


def check_citations(draft: str = "", sources: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    try:
        text = require_text(draft, "draft")
        source_ids: list[str] = []
        for source in require_items(sources, "sources"):
            source_id = require_text(source.get("id"), "source id")
            if not re.fullmatch(r"[A-Za-z0-9_-]+", source_id):
                raise ValueError("source id must contain only letters, digits, underscores or hyphens")
            if source_id in source_ids:
                raise ValueError(f"Duplicate source id: {source_id}")
            normalize_url(source.get("url"))
            source_ids.append(source_id)
        prose = REFERENCE_DEFINITION.sub(" ", CODE.sub(" ", text))
        citations = list(dict.fromkeys(
            value.strip() for match in CITATION.finditer(prose)
            for value in match.group(1).split(",")
        ))
        missing = [value for value in citations if value not in source_ids]
        return {
            "tool": "check_citations", "citations": citations,
            "missing_sources": missing,
            "unused_sources": [value for value in source_ids if value not in citations],
            "valid": not missing,
        }
    except Exception as exc:
        return err("check_citations", exc)
