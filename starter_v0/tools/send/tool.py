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
    token = None
    try:
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
        payload = response.json()
        if payload.get("ok") is not True:
            raise RuntimeError(f"Telegram rejected message: {payload.get('description', 'unknown API failure')}")
        receipt = payload.get("result", {})
        if not isinstance(receipt.get("message_id"), int) or not receipt.get("chat", {}).get("id"):
            raise RuntimeError("Telegram response lacks message receipt; do not resend automatically")
        return {"tool": "send_telegram", "status": "sent", "message_id": receipt["message_id"],
                "chat_id": receipt["chat"]["id"], "date": receipt.get("date")}
    except Exception as exc:
        result = err("send_telegram", exc)
        if token:
            result["message"] = result["message"].replace(token, "[REDACTED]")
        return result

