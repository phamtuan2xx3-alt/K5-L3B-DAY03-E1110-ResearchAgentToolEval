# Source code

## UI của nhóm E1110

Từ `starter_v0/`, sau khi cài `requirements.txt`:

```powershell
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Mở `http://127.0.0.1:8501`. UI hỗ trợ chat nhiều lượt, xem kết quả/lỗi tool,
download transcript JSON và lưu phiên vào `transcripts/`. API key chỉ đọc từ `.env`.
Gửi Telegram được chặn ở tầng UI cho đến khi người dùng bấm **Xác nhận và gửi**
cho đúng nội dung/kênh; hủy hoặc đổi kênh không được gửi. Lỗi gửi không tự retry.

UI mặc định Gemini 3.5; các lựa chọn local chỉ dùng sau khi tải model và start
server theo [LOCAL-MODELS.md](../docs/LOCAL-MODELS.md). Link demo public: https://angel-modification-priced-validation.trycloudflare.com (cần
mã DEMO_ACCESS_CODE trong .env; nhóm trưởng chia sẻ riêng). Link chỉ sống khi app
và tunnel đang chạy. Xem [DEMO.md](../docs/DEMO.md).

Tool mới CP3: [source_audit](tools/source_audit/TOOL.md), rà metadata nguồn có sẵn
hoàn toàn offline. Test: `python -m pytest tests/test_tools_todo.py -k source_audit -v`.

Kiểm tra Telegram (không gửi tin): `python scripts/preflight_telegram.py`;
lấy chat ID: `python scripts/preflight_telegram.py --discover-chats`.
Xem [TELEGRAM-QUICKSTART.md](../docs/TELEGRAM-QUICKSTART.md).

## Gemini: chạy baseline và xử lý lỗi API

Đặt `GEMINI_API_KEY` trong `.env`, rồi chạy từ `starter_v0/`:

```powershell
python scripts/preflight_provider.py --provider gemini
python run_eval.py --provider gemini --version v0 --suite base --eval-cases data/eval_base.json
```

Eval, chat và preflight mặc định chỉ dùng `gemini-3.5-flash-lite`, không fallback sang 3.1.
Provider xếp tuần tự các request trong cùng tiến trình và giữ khoảng cách bắt đầu
ít nhất 4,5 giây/request (tối đa khoảng 14 request trong cửa sổ 60 giây), gồm cả retry.
Với quota 15 RPM, chạy một tiến trình eval/chat tại một thời điểm để không cộng dồn
request từ nhiều tiến trình hoặc ứng dụng dùng chung quota.
Khi API trả 429, 500/502/503/504 hoặc lỗi kết nối mạng/DNS/timeout, provider chờ
60 giây trước mỗi lần thử lại (tối đa 2 lần, vẫn cùng model).
Lỗi khác (ví dụ key không hợp lệ) được trả ngay, không retry.
Eval lưu model thực tế cho từng case ở `results[*].model` và danh sách
`models_used` ở cấp run. Có thể ghi rõ `--model gemini-3.5-flash-lite` trong lệnh.
Run v0 cũ chia hai model được giữ làm lịch sử; trước khi so sánh v1–v3 theo cấu hình
mới, chạy lại v0 chỉ dùng 3.5 để giữ cùng điều kiện đo.


Toàn bộ source code của lab nằm trong folder này. Chạy mọi lệnh từ `starter_v0/`.

- File bắt đầu chạy: `run_eval.py` (chạy eval), `chat.py` (chat live), `scripts/preflight_provider.py` (kiểm tra provider).
- Cách chạy: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`; `python chat.py --provider openrouter --version v3`; `pytest`.
- Input: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, bộ case `data/*.json`, API key trong `.env` (mẫu ở `.env.example`).
- Output: `runs/*.json` (kết quả eval), `transcripts/*.transcript.json` (chat live), `analysis/*.csv` (nếu chạy `scripts/parse_runs.py`).
- File học viên được sửa: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`, `data/eval_group.json`, `tools/` (thêm tool mới và đăng ký trong `tools/__init__.py`), `tests/test_tools_todo.py`, code UI và `requirements.txt`. Không sửa nội dung case trong `data/eval_base.json`.

Chi tiết từng bước xem [README.md](../README.md) ở root; cấu hình API key xem [docs/TOOL-SETUP.md](../docs/TOOL-SETUP.md).
