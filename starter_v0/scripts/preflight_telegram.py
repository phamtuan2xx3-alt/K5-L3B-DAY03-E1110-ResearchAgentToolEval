"""Read-only Telegram setup checks. Never sends messages or changes webhooks."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from env_loader import load_lab_env


def telegram_call(token: str, method: str, **params: Any) -> Any:
    if method not in {"getMe", "getChat", "getChatMember", "getUpdates", "getWebhookInfo"}:
        raise ValueError("Only read-only setup methods are allowed")
    try:
        response = requests.post(f"https://api.telegram.org/bot{token}/{method}", json=params, timeout=30)
        payload = response.json()
    except (requests.RequestException, ValueError):
        raise RuntimeError("Telegram connection/response error; token and request URL omitted") from None
    if not response.ok or not payload.get("ok"):
        description = str(payload.get("description", "API request failed")).replace(token, "[REDACTED]")
        raise RuntimeError(f"Telegram {method}: {description}")
    return payload["result"]


def extract_chats(updates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chats: dict[int, dict[str, Any]] = {}
    for update in updates:
        for key in ("channel_post", "edited_channel_post", "message", "my_chat_member"):
            chat = update.get(key, {}).get("chat", {})
            if chat.get("type") in {"channel", "group", "supergroup"} and "id" in chat:
                chats[chat["id"]] = {name: chat.get(name) for name in ("id", "type", "title")}
    return list(chats.values())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover-chats", action="store_true", help="Read pending updates and print channel/group IDs only")
    parser.add_argument("--chat-id", help="Check a specific chat without changing .env")
    args = parser.parse_args()
    load_lab_env(ROOT)
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token or token.startswith("<"):
        raise SystemExit("Missing TELEGRAM_BOT_TOKEN in starter_v0/.env")
    try:
        bot = telegram_call(token, "getMe")
        print(f"Bot OK: @{bot.get('username', '(no username)')}")
        if args.discover_chats:
            if telegram_call(token, "getWebhookInfo").get("url"):
                raise RuntimeError("Bot uses a webhook; getUpdates unavailable. Webhook was not changed.")
            chats = extract_chats(telegram_call(token, "getUpdates", timeout=0, limit=100))
            for chat in chats:
                print(f"chat_id={chat['id']} type={chat['type']} title={chat['title']}")
            if not chats:
                print("No channel/group updates. Add the bot as channel admin, post a new channel message, then retry.")
            return
        chat_id = (args.chat_id or os.getenv("TELEGRAM_CHAT_ID", "")).strip()
        if not chat_id or chat_id.startswith("<"):
            raise RuntimeError("Missing TELEGRAM_CHAT_ID. Run with --discover-chats after posting in the channel.")
        chat = telegram_call(token, "getChat", chat_id=chat_id)
        member = telegram_call(token, "getChatMember", chat_id=chat_id, user_id=bot["id"])
        print(f"Chat: id={chat['id']} type={chat['type']} title={chat.get('title', '')}")
        if chat.get("type") != "channel" or chat.get("username"):
            raise RuntimeError("Lab delivery target must be the team's private channel")
        if member.get("status") != "administrator" or not member.get("can_post_messages"):
            raise RuntimeError("Grant the bot channel administrator permission to post messages")
        print("OK: private channel accessible; bot has posting permission. No message sent.")
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from None


if __name__ == "__main__":
    main()
