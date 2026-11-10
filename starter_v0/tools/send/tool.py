from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err


def send_telegram(text: str = "", confirmed: bool = False) -> dict[str, Any]:
    if confirmed is not True:
        return {
            "tool": "send_telegram",
            "status": "needs_confirmation",
            "message": "Only send after the user explicitly confirms.",
        }
    try:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            raise RuntimeError("Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID env var")
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        message = data.get("result") or {}
        if data.get("ok") is not True or not isinstance(message, dict):
            raise RuntimeError("Telegram did not confirm delivery")
        message_id = message.get("message_id")
        if type(message_id) is not int or message_id < 1:
            raise RuntimeError("Telegram response is missing a valid message_id")
        return {
            "tool": "send_telegram", "status": "sent", "message_id": message_id,
            "chat_id": (message.get("chat") or {}).get("id"),
        }
    except Exception as exc:
        return err("send_telegram", exc)

