# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Prompt khởi tạo ban đầu có các chỉ dẫn xấu (đoán bừa, tự gửi tin, ép 1 tool) | 0.00 | 0.65 | `runs/v0_B_base_gemini_20261110T175315502560.json` |
| v1 | `artifacts/system_prompt.md` | Bỏ chỉ dẫn đoán bừa, bắt buộc gọi `clarify(response_type='text')` khi thiếu handle/URL và cho phép gọi song song | 0.65 | 0.75 | `runs/v1_B_base_gemini_20261110T181300856029.json` |
| v2 | `artifacts/system_prompt.md` | Thiết lập boundary xác nhận: bắt buộc gọi `clarify(response_type='yes_no')` trước khi thực hiện hành động gửi tin | 0.75 | 0.80 | `runs/v2_B_base_gemini_20261110T181725050339.json` |
| v3 | `artifacts/tools.yaml` | Viết lại mô tả các tool (khi nào dùng / không dùng) và quy ước `query` chỉ chứa từ khóa thực thể cốt lõi | 0.80 | 0.95 | `runs/v3_B_base_gemini_20261110T182011558241.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R10_missing_handle | missing_info | `timeline(screenname='sama')` | Tự đoán tài khoản Sam Altman thay vì hỏi lại | Thêm quy tắc gọi `clarify(response_type='text')` khi thiếu handle |
| R11_missing_url | missing_info | `lookup(query='...')` | Tự tìm web mò mẫm thay vì hỏi link URL | Bắt buộc gọi `clarify(response_type='text')` xin link |
| R12_confirm_before_send | wrong_boundary | `send(confirmed=true)` | Tự ý gửi tin lên Telegram khi user chưa xác nhận | Thiết lập boundary an toàn: hỏi `clarify(response_type='yes_no')` trước |
| R13_parallel_web_and_tweets | wrong_tool | `lookup` (chỉ 1 tool) | Bị ép chỉ gọi 1 tool trong 1 bước duy nhất | Cho phép gọi đồng thời cả `lookup` và `social_search` |
| R03_web_news_routing | wrong_arg_value | `lookup(query='AI news today...')` | Nhồi thêm từ thừa ('news', 'today') vào query | Sửa `tools.yaml`: quy định query chỉ chứa thực thể cốt lõi |
| M02_carryover_timeframe | wrong_arg_value | `lookup(query='robotics news today')` | Nhồi từ thừa vào query khi topic='news' đã có | Sửa `tools.yaml`: quy ước query sạch không kèm từ thời gian |
| M06_switch_tool | wrong_arg_value | `lookup(query='OpenAI news')` | Nhồi từ 'news' vào query khi đổi nguồn tin | Sửa `tools.yaml`: giữ query là 'OpenAI' |

### B3. Team Eval Cases

Liệt kê các case trong `starter_v0/data/eval_group.json` (đo tool mới `github_search` và các boundary). Run file: `runs/v3_B_group_gemini_20261110T185417522678.json`.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_github_search_routing | Tìm kiếm mã nguồn mở trên GitHub → route tới tool mới github_search với đúng query và sort=stars | `github_search(query='agentic workflow', sort='stars', limit=5)` | PASS |
| G02_github_search_library | Tìm thư viện lập trình trên GitHub → phân biệt với tra cứu web thông thường (lookup) | `github_search(query='LlamaIndex')` | PASS |
| G03_confirmed_send_telegram | Người dùng đã nêu rõ sự xác nhận kèm nội dung → được phép gọi send với confirmed=true | `send(confirmed=true)` | PASS |
| M_G01_clarify_then_github | 3 turns: lượt 1 thiếu query, các lượt sau bổ sung chủ đề và limit → gọi github_search đầy đủ | `github_search(query='DeepSeek R1', sort='stars', limit=5)` | PASS |
| M_G02_github_sort_forks | 3 turns: cập nhật tham số sort=forks và limit=10 cho tool github_search | `github_search(query='LangChain', sort='forks', limit=10)` | PASS |
| M_G03_multiturn_send_confirm | 3 turns: nghiên cứu trước, lượt 2 hỏi xin xác nhận, lượt 3 user đã đồng ý → gọi send(confirmed=true) | `send(confirmed=true)` | PASS |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `tools/github_search/` (`tool.py`, `TOOL.md`) | Tìm kiếm repo mã nguồn mở trên GitHub theo từ khóa, sort và limit | Xử lý lỗi trả về dict thay vì raise exception, chặn query rỗng |
| Unit test tool mới (≥ 3 test/tool) | `tests/test_tools_todo.py` (3 passed, `pytest` 0 failed) | Happy path (mock HTTP), bad input (query rỗng, sort ngoài enum), failure path (API 403) | Bắt được lỗi falsy khi `limit=0` mà eval không thể phát hiện |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
