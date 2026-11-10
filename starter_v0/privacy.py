from __future__ import annotations

import os
from typing import Any


SECRET_NAMES = (
    "OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY",
    "TAVILY_API_KEY", "FIRECRAWL_API_KEY", "RAPIDAPI_KEY", "TELEGRAM_BOT_TOKEN",
)


def redact_secrets(value: Any) -> Any:
    secrets = sorted({os.getenv(name, "") for name in SECRET_NAMES} - {""}, key=len, reverse=True)

    def clean(item: Any) -> Any:
        if isinstance(item, str):
            for secret in secrets:
                item = item.replace(secret, "[REDACTED]")
            return item
        if isinstance(item, dict):
            return {key: clean(content) for key, content in item.items()}
        if isinstance(item, list):
            return [clean(content) for content in item]
        return item

    return clean(value)
