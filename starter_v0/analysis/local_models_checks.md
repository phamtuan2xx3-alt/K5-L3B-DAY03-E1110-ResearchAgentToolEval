# Chuẩn bị model local — 2026-11-10 (GMT+7)

## Download và server

- Ollama Windows portable **0.40.16**, tải từ release chính thức, archive SHA256:
  `50fcf5ad54277f2fa5d173ebfc93bcb017adbc0c9ef2314daabc96ca9e6aa64e`.
- Chữ ký `ollama.exe`: hợp lệ, signer Ollama Inc.
- Đã giải nén vào `.local-models/runtime/`; đã bỏ ZIP tạm sau khi kiểm tra chạy
  để tiết kiệm khoảng 1,5 GB. Metadata xác minh vẫn ở `.local-models/runtime-verified.json`.
- Tải Qwen2.5 3B và Llama3.2 1B từ public Ollama registry; SHA256 của **mọi blob**
  đã khớp digest manifest trước khi xuất bản manifest cho Ollama.
- `GET http://127.0.0.1:11435/api/tags` nhận diện đủ hai model.
- Server riêng, cloud tắt, GPU nhận diện NVIDIA GeForce GTX 1650; không cài Ollama
  toàn hệ thống và không đổi PATH/model store của các Ollama khác.

## Preflight thật

Lệnh chạy từ root repo:

```powershell
.\starter_v0\.venv\Scripts\python.exe starter_v0/scripts/preflight_provider.py --provider ollama --model qwen2.5:3b
.\starter_v0\.venv\Scripts\python.exe starter_v0/scripts/preflight_provider.py --provider ollama --model llama3.2:1b
```

| Model | Structured tool call nhận được | Đánh giá đúng phạm vi preflight |
|---|---|---|
| qwen2.5:3b | timeline, screenname=samaltman | Server/model chạy và có tool call; handle chưa đúng (`sama` mới là handle cần dùng cho câu hỏi này) |
| llama3.2:1b | clarify, response_type=text | Server/model chạy và có tool call; chưa route đúng timeline cho câu hỏi đã nêu rõ người |

Preflight chỉ kiểm tra có structured call, không chấm routing/arguments. Không
coi các dòng OK là bằng chứng local đạt chất lượng của Gemini. Lần in kết quả
Llama đầu bị lỗi encoding cp1252 ở console; đã đổi in args sang JSON ASCII và
chạy lại thành công. Đây là sửa output CLI, không thay kết quả model.

Tại thời điểm preflight ban đầu chưa có full eval. Sau đó đã chạy đủ hai model,
hai vòng tối ưu và kiểm tra ngược Gemini; xem [minh chứng full flow](bonus/README.md)
và bảng B7 báo cáo. Các kết quả preflight ở trên được giữ nguyên như lịch sử chuẩn bị.

## Chạy và dọn

Xem [LOCAL-MODELS.md](../../docs/LOCAL-MODELS.md). Từ root:

```powershell
.\starter_v0\scripts\local_models.ps1 status
.\starter_v0\scripts\local_models.ps1 start
.\starter_v0\scripts\local_models.ps1 stop
# Chỉ chạy khi muốn xóa runtime/weights/cache/log của model local:
.\starter_v0\scripts\local_models.ps1 clean
```

Cleanup kiểm tra đường dẫn tuyệt đối và marker sở hữu của repo. Không chạy lệnh
clean trong quá trình chuẩn bị này. `.local-models/` đã được Git bỏ qua.
