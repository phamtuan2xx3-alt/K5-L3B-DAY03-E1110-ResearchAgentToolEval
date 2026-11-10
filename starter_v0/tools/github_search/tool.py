from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err


def search_github_repos(
    query: str = "",
    sort: str = "stars",
    limit: int = 5,
) -> dict[str, Any]:
    """Search public GitHub repositories by keyword or topic."""
    try:
        clean_query = (query or "").strip()
        if not clean_query:
            return {
                "tool": "search_github_repos",
                "query": "",
                "repositories": [],
                "total_count": 0,
            }

        clean_limit = 5 if limit is None else max(1, min(int(limit), 30))
        allowed_sorts = {"stars", "forks", "updated"}
        clean_sort = sort if sort in allowed_sorts else "stars"

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Day03-ResearchAgent/1.0",
        }
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        params = {
            "q": clean_query,
            "sort": clean_sort,
            "order": "desc",
            "per_page": clean_limit,
        }

        response = requests.get(
            "https://api.github.com/search/repositories",
            headers=headers,
            params=params,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        items = data.get("items", []) or []
        repos = [
            {
                "name": item.get("name", ""),
                "full_name": item.get("full_name", ""),
                "url": item.get("html_url", ""),
                "description": item.get("description") or "",
                "stars": int(item.get("stargazers_count", 0)),
                "forks": int(item.get("forks_count", 0)),
                "language": item.get("language") or "Unknown",
            }
            for item in items[:clean_limit]
        ]
        return {
            "tool": "search_github_repos",
            "query": clean_query,
            "sort": clean_sort,
            "repositories": repos,
            "total_count": len(repos),
        }
    except Exception as exc:
        return err("search_github_repos", exc)
