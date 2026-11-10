# CP1 — kiểm tra thực tế ngày 2026-11-10 (GMT+7)

## Cấu hình hiện tại (cập nhật sau CP1)

Theo yêu cầu mới: chỉ dùng Gemini 3.5 Flash Lite, bỏ chia lượt và fallback 3.1.
Request được xếp tuần tự trong cùng tiến trình, cách nhau ít nhất 4,5 giây;
429/lỗi tạm thời chờ 60 giây rồi thử lại tối đa 2 lần cùng model.
Kiểm tra sau thay đổi: preflight PASS với `gemini-3.5-flash-lite`;
pytest `68 passed, 17 skipped in 0.42s`, có test 20 request dùng chung bộ giới hạn
giữa nhiều provider instance (tối đa 14 request/60 giây).
Các kết quả CP1 bên dưới là lịch sử của cấu hình chia hai model.
Cần chạy lại baseline v0 một model trước khi so sánh v1–v3 một model.

## Provider preflight

Lệnh: `python scripts/preflight_provider.py --provider gemini`

```text
OK provider=gemini model=gemini-3.5-flash-lite
tool=timeline
args={'screenname': 'sama'}
```

## Unit test

Lệnh: `python -m pytest -q`

```text
68 passed, 17 skipped in 0.34s
```

17 test skipped là stub CP3 được phép để nguyên tại CP1. Có 6 test mới cho retry:
429 chờ 60 giây; fallback ghi đúng model; 401 không retry; giới hạn số lần retry;
lỗi DNS/kết nối được thử lại; 3.1 cũng có thể fallback sang 3.5.
Các test này mock API và sleep, không gọi mạng.

## Giữ baseline

Không sửa `artifacts/system_prompt.md`, `artifacts/tools.yaml` hoặc `data/eval_base.json`.
Chỉ sửa hạ tầng provider và bổ sung metadata model thực tế trong run eval.
Thông tin nhóm trong `TEAM.md` được tạm bỏ qua theo yêu cầu người dùng.
Eval mặc định chia case luân phiên 3.5/3.1 theo yêu cầu người dùng (10 case/model
trước fallback). Phải giữ nguyên thứ tự case và chính sách chia model khi so sánh v1–v3.

## Các lượt chạy chưa hợp lệ (giữ để truy vết, không dùng làm baseline)

- `../runs/v0_B_base_openrouter_20261110T173034224274.json`: chọn sai provider, thiếu key OpenRouter.
- `../runs/v0_B_base_gemini_20261110T173640521627.json`: 3 case lỗi 429 quota/phút.
- `../runs/v0_B_base_gemini_20261110T174314451521.json`: 1 case lỗi DNS `getaddrinfo failed`.
- `../runs/v0_B_base_gemini_20261110T174352325763.json`: lỗi import `httpx` trong bản sửa trung gian;
  đã bỏ dependency import này và kiểm tra lại toàn suite trước lượt chạy tiếp theo.

Retry áp dụng cho thao tác gọi model, không tự thử lại thao tác tool (đặc biệt tool gửi tin).


## Run CP1 sau khi đổi key

- [Run v0](../runs/v0_B_base_gemini_20261110T175056447101.json).
- Preflight chạy lại với key mới: PASS.
- Đo đủ 20/20, 0 provider_error; 12 PASS, 8 FAIL; accuracy 60%.
- Model thực tế: 10 case 3.5 và 10 case 3.1; không fallback.
- Chọn run này để chốt CP1; version log và bảng B1/B2 ghi từ JSON thật.
