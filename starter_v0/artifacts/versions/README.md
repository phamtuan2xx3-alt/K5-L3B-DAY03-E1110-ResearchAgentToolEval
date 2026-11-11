# Các bản prompt và tool declaration dùng trong CP2

Mỗi thư mục chứa đúng hai file đầu vào đã dùng cho version tương ứng. Các bản
v0/v1 giữ một số chỉ dẫn chưa tốt để đo ảnh hưởng từng thay đổi, không phải bản
khuyến nghị để dùng tiếp. Sau CP2, `artifacts/` được mở rộng từ v3 với tool
source_audit; snapshot cấu hình mới ở `cp3/`. Không ghi đè v0–v3 để giữ bằng chứng.

| Version | Thay đổi so với version trước | Giả thuyết |
|---|---|---|
| v0 | Không đổi prompt/tools của starter | Đo baseline chỉ dùng Gemini 3.5 Flash Lite |
| v1 | Chỉ đổi prompt: hỏi lại và xác nhận | Bỏ chỉ dẫn đoán và gửi ngay sẽ giảm lỗi thiếu thông tin/boundary |
| v2 | Chỉ đổi prompt: routing, nhiều nguồn, phạm vi và lịch sử hiện tại | Bỏ ép một tool sẽ giảm thiếu nguồn và chọn sai tool |
| v3 | Giữ prompt v2, chỉ đổi mô tả tool và tham số | Quy ước arguments rõ sẽ giảm query mở rộng và response_type không nhất quán |

Chạy từ `starter_v0/`, thay `v3` bằng version cần tái lập:

```powershell
python run_eval.py --provider gemini --model gemini-3.5-flash-lite --version v3 --suite base --eval-cases data/eval_base.json --system-prompt artifacts/versions/v3/system_prompt.md --tools artifacts/versions/v3/tools.yaml
```

Mọi version dùng cùng model, bộ base không đổi và pacing tối thiểu 4,5 giây giữa
các request. Kiểm tra `provider_error_cases == 0` và `measured_cases == total_cases`
trước khi so sánh. Hash trong run JSON phải khớp file của version; tên version
không thay thế việc kiểm tra hash. Kết quả có thể biến động giữa những lần chạy API.

Kết quả và phân tích: [báo cáo nhóm](../../../report/team/group_report.md),
[version log](../version_log.csv). Snapshot v0 cũng khớp các run cũ dùng hai model;
chỉ dùng run v0 một model được chỉ rõ trong báo cáo để so với v1–v3.


## Các vòng local sau CP2

- `v4-local/`: prompt 220 từ thay prompt v3 399 từ; tools v3 giữ nguyên.
- `v5-local/`: prompt v4 giữ nguyên; descriptions giảm 865 → 371 từ, schema giữ nguyên.
- Local eval dùng cap512 và chặn thực thi send (vẫn chấm calls/args). Thay provider/model bằng
  `--provider ollama --model qwen2.5:3b` trong lệnh tái lập tương ứng; dùng Gemini
  để kiểm tra ngược cùng v5-local. Không thay bản cloud/live đang dùng bằng các
  bản rút gọn vì kết quả đo giảm điểm. [Minh chứng](../../analysis/bonus/README.md).

## Tích hợp bốn tool sau CP3

main-four-tools/ giữ prompt và declaration sau khi tích hợp deduplicate_sources, check_citations, compare_papers, rank_sources từ DoMinhThanh cùng source_audit có sẵn. Dùng hai file trong thư mục này với --system-prompt và --tools để tái lập supplemental run main-four-tools. Bộ eval_four_tools.json có 4 single-turn case bổ sung, không thay bộ group 10 case. Không gán metric base/local cũ cho snapshot mới.
