# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: E1110
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: `gemini` / `gemini-3.5-flash-lite`

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent: tìm tin web/X theo từ khóa hoặc tài khoản, đọc URL, tổng hợp digest, tạo citation, và chỉ gửi Telegram sau khi user xác nhận.

**Cách chạy UI:**

```bash
cd starter_v0
streamlit run app.py
```

Dependency: `streamlit` trong `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> URL: _(chạy local + Cloudflare Tunnel khi demo; cập nhật khi mở tunnel)_

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại khi thiếu thông tin hoặc cần xác nhận | không |
| timeline | lấy bài đăng gần đây của một handle | không |
| social_search | tìm bài đăng X theo từ khóa | không |
| lookup | tìm trên web (topic/timeframe) | không |
| fetch | đọc nội dung một URL | không |
| format | trình bày items thành markdown digest | không |
| send | gửi text lên Telegram khi `confirmed=true` | không |
| policy | tìm trong company policy nội bộ | không |
| papers | tìm paper trên arXiv | không |
| paper_text | trích text từ PDF arXiv | không |
| cite | tạo markdown citation từ list nguồn `{title,url}` | có |

### A3. Câu hỏi mẫu để thử

1. Tin tức AI hôm nay có gì nổi bật?
2. Tóm tắt 5 tweet mới nhất của @sama
3. Đọc https://example.com rồi tóm tắt giúp mình
4. Tóm tắt 5 tweet mới nhất giúp mình (thiếu handle — agent phải hỏi lại)
5. Đăng bản tin này lên Telegram giúp mình (phải hỏi xác nhận trước)

## 3. Giải pháp

- **v1 `system_prompt.md`:** bỏ đoán handle/URL và gửi ngay; bắt buộc `clarify` khi thiếu info / trước khi `send`.
- **v2 `tools.yaml`:** viết lại description when/when-not cho mọi tool; `send` chỉ sau xác nhận; cho phép parallel `lookup` + `social_search`.
- **v3:** convention args (`lookup.query` ngắn, luôn truyền `response_type`); thêm tool **`cite`** (local formatter citation markdown/plain).
- Metric base: **0.65 → 0.75 → 0.90 → 0.95**. Group suite v3: **1.0** (10/10).

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Measure unoptimized starter |  | 0.65 | `runs/v0_B_base_gemini_20261110T175841805569.json` |
| v1 | system_prompt.md | Bad starter prompt causes missing_info / wrong_boundary | 0.65 | 0.75 | `runs/v1_B_base_gemini_20261110T180742330158.json` |
| v2 | tools.yaml | Vague declarations cause wrong routing / boundary | 0.75 | 0.90 | `runs/v2_B_base_gemini_20261110T180952630323.json` |
| v3 | system_prompt.md + cite | Verbose lookup.query / omitted response_type | 0.90 | 0.95 | `runs/v3_B_base_gemini_20261110T181328065017.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON v0.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool (observed wrong_arg_value) | `lookup(query="AI news today", topic=news, timeframe=day)` | query expect `AI` | v3: convention query ngắn; topic/timeframe mang nghĩa “news today” |
| R10_missing_handle | missing_info | `timeline(screenname=sama)` | thiếu `clarify` khi không có handle | v1: bỏ đoán; bắt buộc `clarify` |
| R11_missing_url | missing_info | `lookup(query=...)` | thiếu `clarify` khi không có URL/target rõ | v1: thiếu URL → `clarify` |
| R12_confirm_before_send | wrong_boundary | `send(confirmed=true)` | gửi ngay không hỏi | v1: gửi/đăng → `clarify(yes_no)` trước |
| R13_parallel_web_and_tweets | wrong_tool | chỉ `lookup(...)` | thiếu `social_search`; query dài | v2: cho phép parallel; v3: query ngắn |
| M02_carryover_timeframe | wrong_arg_value | `lookup(query="robotics news today", ...)` | query expect `robotics` | v3: query = keyword; timeframe từ context |
| M06_switch_tool | wrong_tool | `lookup(query="OpenAI news")` | query expect `OpenAI`; có thể sai tool khi đổi yêu cầu | v2 routing + v3 query convention |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).
Run: `runs/v3_B_group_gemini_20261110T181919640210.json` — case_accuracy **1.0**, provider_error **0**.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_cite_after_sources | Route tới tool mới `cite` | `cite(style=markdown)` | PASS |
| G02_policy_privacy | Policy nội bộ | `policy` | PASS |
| G03_papers_routing | Paper arXiv | `papers` | PASS |
| G04_timeline_no_at | Strip `@`, limit=3 | `timeline(openai,3)` | PASS |
| G05_refuse_math | Out of scope | `no_tool` | PASS |
| G06_cite_then_style | Multiturn đổi style cite | `cite(style=markdown)` | PASS |
| G07_confirm_then_send | Sau xác nhận mới gửi | `send(confirmed=true)` | PASS |
| G08_switch_fetch_to_lookup | Đổi fetch → lookup tuần này | `lookup(timeframe=week)` | PASS |
| G09_missing_arxiv_id | Thiếu arXiv id | `clarify(text)` | PASS |
| G10_carry_limit_correction | Sửa limit giữ handle | `timeline(sama,8)` | PASS |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| research_normal T1 | Tin tức AI hôm nay… | `lookup` → `format` | v3 gemini | Digest tin AI |
| missing_then_fill T1 | Tóm tắt 5 tweet… (thiếu handle) | `clarify(text)` | v3 | Hỏi handle |
| missing_then_fill T2 | Handle là sama | `timeline` → `format` | v3 | Tóm tắt @sama |
| send_confirm T1 | Đăng bản tin lên Telegram… | `clarify(yes_no)` | v3 | Xin xác nhận |
| send_confirm T2 | Không, dừng lại | (no send) | v3 | Không gửi |

Transcript files:
- `transcripts/v3_gemini_20261110T182235674866_research_normal.transcript.json`
- `transcripts/v3_gemini_20261110T182309525508_missing_then_fill.transcript.json`
- `transcripts/v3_gemini_20261110T182343172772_send_confirm.transcript.json`

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới `cite` | `tools/cite/tool.py`, `TOOL.md`, registry + `tools.yaml` | Tạo citation markdown/plain từ `{title,url}` | Không bịa nguồn; URL phải http(s) |
| Unit test tool mới (≥ 3) | `tests/test_tools_todo.py` (`test_cite_*`); `pytest` 70 passed | Happy path + TypeError + ValueError error dict | Eval không bắt được URL `ftp://` invalid — unit test có |
| UI | `app.py`; `streamlit run app.py` | Chat + ghi transcript | Link tunnel tạm thời khi demo |

Tool unit tests: 3 test cho `cite`. Ví dụ: `cite(sources=[{url: ftp://...}])` trả `error=ValueError` — eval routing không cover nhánh này.

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

- Gemini Free Tier **429 RESOURCE_EXHAUSTED** (15 RPM) làm run v3 đầu tiên có `provider_error_cases=4` → không dùng làm bằng chứng; chờ cooldown rồi chạy lại (`runs/v3_B_base_gemini_20261110T181328065017.json`).
- Model hay mở rộng `lookup.query` (`AI` → `artificial intelligence`) dù topic/timeframe đã mang nghĩa news/today — siết bằng convention trong prompt + description.
- R12 lúc đầu clarify đúng tool nhưng sai `response_type=text` thay vì `yes_no` — sửa bằng description `clarify`/`send` ở v2.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix thuộc `system_prompt.md`: bỏ đoán/gửi-ngay (v1); convention query ngắn + luôn truyền `response_type` (v3).
- Fix thuộc `tools.yaml`: when/when-not, parallel routing, send boundary (v2); đăng ký `cite` (v3).
- Failure cần review thủ công: arg gần đúng (`artificial intelligence` vs `AI`) — chấm subset string cứng có thể phạt routing đúng.
- Vòng tiếp theo: few-shot ví dụ `lookup(query="AI")` trong prompt; hoặc normalize query trong tool wrapper (không đổi eval).

## 8. Tài liệu tham khảo

- [CHECKPOINTS.md](../../CHECKPOINTS.md), [RUBRIC.md](../../RUBRIC.md), [docs/TOOL-SETUP.md](../../docs/TOOL-SETUP.md)
- Run evidence trong `starter_v0/runs/` và `starter_v0/artifacts/version_log.csv`
