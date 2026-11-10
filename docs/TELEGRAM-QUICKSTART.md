# Telegram cho nhóm E1110

## Tạo bot và kênh nhận

1. Trong Telegram, mở [@BotFather chính thức](https://t.me/BotFather), gửi `/newbot`
   và làm theo hướng dẫn để đặt tên/username.
2. Điền token vào `starter_v0/.env`: `TELEGRAM_BOT_TOKEN=...`. Không đưa token vào chat hoặc Git.
3. Tạo **private channel** của nhóm, thêm bot làm admin và cho quyền đăng tin.
4. Tự đăng một tin mới vào channel để bot có update nhận diện chat.

## Lấy chat ID

Từ `starter_v0/`:

```powershell
python scripts/preflight_telegram.py --discover-chats
```

Lệnh chỉ in tên bot và ID/tên của group/channel trong pending updates, không in
token hoặc nội dung tin nhắn. Chọn đúng private channel, lấy ID thường có dạng
`-100...` rồi điền `TELEGRAM_CHAT_ID=-100...` vào `.env`.

Nếu chưa có update, kiểm tra bot đã là admin rồi đăng một tin channel mới và thử
lại. Nếu đang có ứng dụng khác đọc updates, nó có thể đã xác nhận các update đó;
nên tạm dừng ứng dụng đó trước khi đăng tin mới. Nếu bot dùng webhook, script sẽ
báo và không tự xóa webhook; cần dùng thông tin chat từ ứng dụng đang nhận webhook.

## Kiểm tra bot và quyền

```powershell
python scripts/preflight_telegram.py
```

Script gọi các API đọc `getMe`, `getChat`, `getChatMember`, kiểm tra private
channel và quyền đăng. Nó không gửi tin hay thay cấu hình webhook.

## Gửi thử có xác nhận

Sau khi preflight PASS, chạy `python chat.py --provider gemini --version cp3`,
yêu cầu gửi **nội dung cụ thể**. Đọc câu hỏi xác nhận và chỉ xác nhận khi đúng
nội dung, đúng kênh nhóm. Lưu transcript để kiểm chứng `confirmed=true` và kết quả
gửi thật. Chưa tính bonus Telegram nếu chỉ có preflight mà chưa có transcript gửi.

Nguồn: [hướng dẫn BotFather](https://core.telegram.org/bots/tutorial),
[Telegram Bot API](https://core.telegram.org/bots/api#getupdates),
[yêu cầu lab](../RULES.md).
