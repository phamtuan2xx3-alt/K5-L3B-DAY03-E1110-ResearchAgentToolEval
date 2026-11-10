---
name: send
track: bonus
kind: action
provider: Telegram Bot API
requires_env: [TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]
inputs: [text, confirmed]
outputs: [status, message_id, chat_id]
side_effect: true
requires_confirmation: true
---
# send

Posts text to a Telegram channel. The message is only sent when `confirmed` is true.

Confirmation must be the boolean `true`; strings and numeric values do not authorize delivery. Text must be a non-empty string. A sent result includes the Telegram message ID returned by a successful API response.
