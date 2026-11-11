# Minh chứng bonus E1110

## Telegram — flow thật sau xác nhận

- [Biên nhận và tham chiếu flow](telegram_send_flow.json).
- [Transcript thật](../../transcripts/cp3_ui_4012b934c2c04647b4dae9c5956ba7a4.transcript.json).
- [Ảnh trước duyệt](telegram-before-confirmation.png), [ảnh sau gửi](telegram-after-send.png).
- [Kiểm tra bot/kênh chỉ đọc](telegram_setup.json).
- [Tin đã gửi trong private channel](https://t.me/c/4338885153/4), chỉ thành viên kênh xem được.

User đã duyệt đúng nội dung/kênh trong chat, sau đó assistant thao tác UI theo
ủy quyền. Research Agent hỏi xác nhận, model gọi send được UI giữ lại ở trạng
thái pending, người vận hành bấm nút duyệt, tool gửi một tin và nhận biên nhận
`message_id=4`, `chat_id=-1004338885153`, `status=sent`. Không tự gửi lại.
Không ghi bot token hoặc API key trong minh chứng.

## Regression test cho tool có sẵn

- [Tóm tắt trước/sau sửa](send_regression_summary.json).
- [Test](../../tests/test_send_receipt.py), [implementation](../../tools/send/tool.py).

Ba test đã FAIL trước sửa vì chuỗi "false", "true" hoặc số 1 qua được guard
truthiness. Sau sửa chỉ boolean true được chấp nhận; 6 test receipt/guard PASS.
Test đều mock HTTP, không gửi tin thật. Biên nhận live ở trên là flow riêng.
Đây là bằng chứng nhánh regression của test challenge, không phải 0 skipped.

## Local model

- [Download/runtime metadata](local_setup.json).
- [Kiểm tra tải và preflight](../local_models_checks.md).
- [Sự cố generation không giới hạn, đã loại khỏi run hợp lệ](llama_unbounded_attempt.json).
- Các run base và hai vòng tối ưu được ghi trong `runs/`, version log và B7 của báo cáo;
  chỉ tính run đủ 20 case, 0 provider_error. Đã chốt bảng tổng hợp ở các link dưới đây.

Hai model: qwen2.5:3b và llama3.2:1b. Sau sự cố vòng lặp, các local run dùng cùng
cap 512 token; các call send trong eval bị chặn thực thi, tool call/args vẫn được
chấm nguyên vẹn. Không dùng preflight thay cho full base eval hoặc bịa điểm.


### Kết quả full flow đã chốt

| Cấu hình | Case accuracy |
|---|---:|
| Gemini v3 tham chiếu | 90% |
| Qwen3B v3, cap512 | 65% |
| Llama1B v3, cap512 | 15% |
| Qwen3B v4-local (rút prompt) | 45% |
| Qwen3B v5-local (rút descriptions) | 40% |
| Gemini kiểm tra ngược v5-local | 85% |

Tất cả 6 dòng đều có đủ 20 case, 0 lỗi provider; dòng đầu dùng run CP2 làm tham
chiếu, 5 dòng sau là các run bonus. Hai giả thuyết rút gọn không cải thiện trong
các run đã đo, vì vậy giữ v3 làm cấu hình tốt hơn; không chỉnh log để tăng điểm.

- [Metric/run/hash](local_metrics.csv), [120 kết quả case để đối chiếu](local_case_results.csv).
- [Phân loại lỗi](local_failure_patterns.csv), [giả thuyết từng vòng](local_experiments.json).
- [Version log](../../artifacts/version_log.csv), [báo cáo B5/B7](../../../report/team/group_report.md).
- [Pytest stdout/stderr](pytest-final.txt), [exit code](pytest-final.json): **103 passed, 14 skipped, 0 failed**.


### Lệnh tái lập (từ starter_v0/)

```powershell
python run_eval.py --provider ollama --model qwen2.5:3b --version v3-qwen3b --suite base --eval-cases data/eval_base.json --system-prompt artifacts/versions/v3/system_prompt.md --tools artifacts/versions/v3/tools.yaml
python run_eval.py --provider ollama --model llama3.2:1b --version v3-llama1b --suite base --eval-cases data/eval_base.json --system-prompt artifacts/versions/v3/system_prompt.md --tools artifacts/versions/v3/tools.yaml
python run_eval.py --provider ollama --model qwen2.5:3b --version v4-local --suite base --eval-cases data/eval_base.json --system-prompt artifacts/versions/v4-local/system_prompt.md --tools artifacts/versions/v4-local/tools.yaml
python run_eval.py --provider ollama --model qwen2.5:3b --version v5-local --suite base --eval-cases data/eval_base.json --system-prompt artifacts/versions/v5-local/system_prompt.md --tools artifacts/versions/v5-local/tools.yaml
python run_eval.py --provider gemini --model gemini-3.5-flash-lite --version v5-local-gemini --suite base --eval-cases data/eval_base.json --system-prompt artifacts/versions/v5-local/system_prompt.md --tools artifacts/versions/v5-local/tools.yaml
```

Giữ OLLAMA_MAX_OUTPUT_TOKENS=512, server/context và cùng bộ base khi so sánh.
Không bấm gửi Telegram lần nữa chỉ để tái lập screenshot; muốn gửi thêm cần
xác nhận nội dung/kênh cho lần gửi mới. Các lệnh eval trên không gửi Telegram.

## Bốn tool tích hợp từ nhánh Đỗ Minh Thanh

- [Commit nguồn và manifest tích hợp](../four_tools_integration.json).
- [46 test cho bốn tool](../../tests/test_thanh_research_tools.py); 10 test source_audit vẫn nằm trong test_tools_todo.py.
- [4 case routing bổ sung](../../data/eval_four_tools.json), [run Gemini 4/4 không lỗi provider](../../runs/main-four-tools_B_group_gemini_20261111T104511986590.json).
- Mỗi tool có TOOL.md, implementation, registry và declaration. Đây là minh chứng để đối chiếu bonus hơn ba tool mới; không tự cộng điểm.
- Bộ tool hiện tại có 15 tool. Chưa chạy lại base/group 10 case hoặc local với snapshot mới; số đo cũ vẫn thuộc snapshot cũ.
