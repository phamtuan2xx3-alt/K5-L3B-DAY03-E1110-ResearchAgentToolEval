# Model local của E1110

Model, Ollama portable, file tải tạm và log đều nằm trong **`.local-models/`** ở
root repo, đã được Git bỏ qua. Không cài Ollama toàn hệ thống và không đổi PATH.

## Model đang chuẩn bị

- `qwen2.5:3b`: khoảng 1,9 GB weights.
- `llama3.2:1b`: khoảng 1,3 GB weights.

Hai model khác kích thước, đều dưới 8B, để chuẩn bị phần Small Local Model.
Tải xong chưa đồng nghĩa hoàn thành bonus: vẫn cần eval hai model, hai vòng tối ưu
local và so sánh cloud/local theo README.

Downloader dùng public Ollama registry, kiểm SHA256 từng blob trước khi ghi
manifest. Nếu bị ngắt, chạy lại `python starter_v0/scripts/download_local_weights.py`
từ root; các blob hợp lệ được giữ, file `.part` được thử tiếp tục nếu server hỗ trợ.

## Kiểm tra / khởi động / dừng

Từ root repo, PowerShell:

```powershell
.\starter_v0\scripts\local_models.ps1 status
.\starter_v0\scripts\local_models.ps1 start
.\starter_v0\scripts\local_models.ps1 stop
```

Server riêng chỉ nghe `127.0.0.1:11435`, dùng model store trong dự án, cloud tắt,
tối đa một model/luồng xử lý. Không ảnh hưởng Ollama khác ở cổng 11434. Log ở
`.local-models/logs/`. Không khởi chạy inference cho tới khi cả hai manifest đã sẵn sàng.

Đặt trong `starter_v0/.env`:

```dotenv
OLLAMA_BASE_URL=http://127.0.0.1:11435/v1
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_MAX_OUTPUT_TOKENS=512
```

Sau khi tải xong và start server, từ `starter_v0/`:

```powershell
python scripts/preflight_provider.py --provider ollama --model qwen2.5:3b
python scripts/preflight_provider.py --provider ollama --model llama3.2:1b
```

UI có sẵn lựa chọn hai model local. Khả năng tool calling của model nhỏ cần được
đo thực tế, không coi việc download thành công là đã đạt chất lượng của Gemini.
Local giới hạn đầu ra mặc định 512 token để tránh vòng lặp sinh không dừng;
run eval lưu `max_output_tokens`, `finish_reason` và usage khi provider cung cấp.
Các lệnh send bị chặn thực thi trong eval nhưng vẫn chấm nguyên tool call/args;
gửi thật chỉ thực hiện qua flow chat/UI sau khi người dùng duyệt.

## Dọn khi không dùng nữa

Chạy lệnh này khi bạn muốn xóa runtime, weights, cache tải và log local:

```powershell
.\starter_v0\scripts\local_models.ps1 clean
```

Script kiểm tra đường dẫn tuyệt đối và ownership marker trước khi xóa, chỉ dừng
server/worker thuộc dự án. Nếu runtime vẫn đang tải, đợi tải xong trước khi clean.
Code, `.env`, báo cáo, run eval và transcript không nằm trong thư mục bị dọn.
Các key/config nhỏ mà Ollama tự tạo theo chuẩn trong hồ sơ người dùng (nếu có)
không thuộc thư mục weights của dự án và không bị script xóa.

Nguồn: [Ollama Windows portable](https://docs.ollama.com/windows),
[model location và server config](https://docs.ollama.com/faq),
[Qwen2.5](https://ollama.com/library/qwen2.5), [Llama3.2](https://ollama.com/library/llama3.2).
