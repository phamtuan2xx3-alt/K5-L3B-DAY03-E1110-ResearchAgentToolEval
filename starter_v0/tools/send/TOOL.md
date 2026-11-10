---
name: send
track: bonus
kind: action
provider: Telegram Bot API
requires_env: [TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]
inputs: [text, confirmed]
outputs: [status, message_id, chat_id, date]
side_effect: true
---
# send

Posts text to a Telegram channel. The message is only sent when `confirmed` is true.

Confirmation must be the literal boolean `true`; strings and numbers are not
accepted. Before confirmation no network call is made. A successful call also
requires Telegram `ok=true` and a message receipt; return `message_id`, `chat_id`
and Telegram's Unix `date` for evidence. API errors do not include the bot token.
Never retry a failed/ambiguous send automatically.
