# CP3, CP4 và UI local — kiểm tra thực tế 2026-11-10 (GMT+7)

## CP3: tool mới source_audit

- [Implementation](../tools/source_audit/tool.py), [TOOL.md](../tools/source_audit/TOOL.md).
- Đăng ký trong registry và tools.yaml; thêm routing cho trường hợp user yêu cầu rà metadata.
- Chạy offline, không API key, không sửa input và không tự xóa nguồn.
- `python -m pytest tests/test_tools_todo.py -k source_audit -q`:
  **10 passed, 14 deselected in 0.19s**.
- Test gồm happy path, 5 input xấu, nhánh lỗi nội bộ trả error dict, chuẩn hóa URL
  trùng mà giữ query/path case, metadata/URL lỗi và boolean sai kiểu.

## CP4: eval nhóm

- [10 case](../data/eval_group.json): **5 single turn + 5 multi turn**,
  có failure_type, expect và metadata.what_it_tests, không sửa bộ base/extension.
- [Run thật](../runs/cp3_B_group_gemini_20261110T185301567314.json),
  artifact `cp3+p47845cc8cfe7+t85b8cb34de42`.
- Gemini 3.5 Flash Lite; **10/10 PASS**, measured=10, provider_errors=0;
  routing/arguments/multi-turn=100%.
- G01/G06/G07 gọi tool mới đúng lúc. Kết quả audit thật lần lượt needs_review,
  needs_review, ok. G09 routing/args PASS nhưng social_search trả HTTPError;
  không coi điểm eval là bằng chứng API social hoạt động end-to-end.
- Snapshot đầu vào: [cp3](../artifacts/versions/cp3/system_prompt.md),
  [tools](../artifacts/versions/cp3/tools.yaml). Có dòng cp3 trong version log;
  không so trực tiếp group 100% với base v3 90%.

## UI Streamlit

- [app.py](../app.py) dùng lại loop chat với executor riêng để chặn send trước duyệt.
- Streamlit AppTest startup PASS, 0 exception.
- Đã mở `http://127.0.0.1:8501` bằng browser automation, kiểm tra giao diện thực,
  chạy 4 lượt thật và đọc transcript đã lưu.
- [Transcript](../transcripts/cp3_ui_e1dee9d82ad24b87b2870be3f78073ad.transcript.json):
  audit mẫu → hỏi URL → nhận URL và fetch → yêu cầu chuẩn bị Telegram và clarify.
- **Không có send thành công hoặc gửi tin Telegram trong các lượt QA.**
- [Ảnh giao diện](ui-preview.png), [ảnh live](ui-live-check.png).
- UI hiển thị tool errors, cho xem kết quả và tải transcript; có lựa chọn model
  local nhưng chặn nhập khi weights chưa tải/checksum xong.

## Test sau toàn bộ thay đổi

`python -m pytest -q`: **94 passed, 14 skipped in 3.11s**, 0 failed.

Trong đó 6 test session UI kiểm tra: chặn model tự gửi dù confirmed=true;
duyệt exact text chỉ gửi một lần; hủy không gửi; thay kênh hủy hiệu lực duyệt;
ẩn secret trong transcript; giữ lỗi tool. 4 test Telegram setup xác nhận API
đọc, không nhận phương thức gửi và không lộ token khi lỗi. Các test gửi dùng mock
và transcript tạm trong thư mục pytest, không được tính là gửi thật.

14 skipped là stub tool cũ, chưa hoàn thành bonus test challenge 0 skipped.

## Telegram và model local

- Preflight thật đã xác nhận bot `@ai20kvine1110bot` truy cập private channel
  `AI20K VIN E1110 CHANNEL` và có quyền đăng. Chưa thực hiện send thật.
- Ollama portable đã tải, checksum và chữ ký executable hợp lệ; API version
  ở `127.0.0.1:11435` trả `0.40.16`. Không cài toàn hệ thống.
- Weights Qwen2.5 3B / Llama3.2 1B đã tải đủ và xác minh SHA256 trong `.local-models/`;
  server nhận đủ hai model. Cả hai trả structured call khi preflight, nhưng còn sai
  routing/args; xem [kiểm tra local](local_models_checks.md). Chưa chạy full eval local.
- [Hướng dẫn local/cleanup](../../docs/LOCAL-MODELS.md),
  [hướng dẫn Telegram](../../docs/TELEGRAM-QUICKSTART.md).

## Còn lại

Đã có [link public có mã truy cập](https://angel-modification-priced-validation.trycloudflare.com),
HTTP 200 và browser thấy màn hình đăng nhập. Test UI có thêm 1 test auth gate
(chặn chưa đăng nhập, mã sai và cho vào với mã đúng), không gọi model trong test.
[Ảnh public](ui-public-access.png), [cách chạy/dừng demo](../../docs/DEMO.md).
Còn xác nhận người ngoài nhóm trực tiếp mở UI và thử câu hỏi, Telegram
gửi thật sau duyệt (bonus), local eval và tối ưu local (bonus).
Đóng góp/báo cáo cá nhân để làm sau theo yêu cầu người dùng.


## Cập nhật sau khi chạy bonus thật

Đã có full flow local (hai model base, hai vòng tối ưu, kiểm tra ngược cloud) và Telegram gửi sau xác nhận. Xem [minh chứng bonus](bonus/README.md). Test cuối: **103 passed, 14 skipped, 0 failed**; [stdout/stderr](bonus/pytest-final.txt). Các dòng “chưa gửi” và test count phía trên là mốc QA ban đầu, không thay thế bản cập nhật này. [Checklist nghiệm thu kỹ thuật](acceptance_check.json).
