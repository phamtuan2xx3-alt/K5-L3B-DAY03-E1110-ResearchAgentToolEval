# Báo cáo nhóm — Day 03 Research Agent Tool Eval

## 1. Thông tin nhóm

- Tên nhóm: E1110
- Lớp: L3B
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: Gemini / `gemini-3.5-flash-lite`

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent tìm nguồn trên web và mạng xã hội, đọc URL và paper, tra cứu policy nội bộ, rồi tổ chức thông tin thành bản tổng hợp. Bốn tool mới hỗ trợ loại nguồn trùng, đối chiếu mã trích dẫn, so sánh metadata paper và xếp hạng nguồn theo tiêu chí minh bạch.

**Cách chạy UI:**

Chạy từ thư mục gốc repo, chuẩn bị `.env` theo [hướng dẫn Setup](../../README.md#setup):

```bash
cd starter_v0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

UI local: http://127.0.0.1:8501. Giao diện có chat nhiều lượt, xem kết quả tool, tạo cuộc trò chuyện mới và tải transcript JSON của phiên hiện tại. Bản demo sử dụng 13 tool; chức năng gửi Telegram thật được tắt trong UI.

**Link dùng thử (deploy):**

https://personnel-mapping-took-nova.trycloudflare.com

Link được tạo bằng Cloudflare Quick Tunnel và hoạt động khi Streamlit cùng cloudflared còn chạy. Mở terminal thứ hai, sau khi cài `cloudflared` theo [hướng dẫn Cloudflare](https://developers.cloudflare.com/tunnel/downloads/):

```bash
cloudflared tunnel --url http://127.0.0.1:8501 --protocol http2
```

Khởi động tunnel mới sẽ có URL mới. Phiên hiện tại chạy bằng binary tại `/tmp/e1110-cp5-cloudflared/cloudflared`. Local/public HTTP đều trả 200 và public health trả `ok`; kết quả kiểm tra tại [cp5_verification.json](../../starter_v0/analysis/cp5_verification.json).

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại khi thiếu dữ liệu hoặc cần xác nhận | Không |
| timeline | Lấy bài đăng của tài khoản X/Twitter qua handle | Không |
| social_search | Tìm bài đăng X/Twitter theo từ khóa | Không |
| lookup | Tìm web/tin tức qua Tavily | Không |
| fetch | Đọc URL qua Firecrawl | Không |
| format | Tạo digest Markdown từ dữ liệu đã có | Không |
| send | Gửi Telegram sau xác nhận trong CLI; bị chặn trong UI công khai | Không |
| policy | Tìm nội dung policy trong Markdown nội bộ | Không |
| papers | Tìm paper trên arXiv | Không |
| paper_text | Tải PDF arXiv và trích text cục bộ | Không |
| deduplicate_sources | Loại nguồn trùng theo URL chuẩn hóa | Có |
| check_citations | Đối chiếu mã trích dẫn với danh sách nguồn | Có |
| compare_papers | So sánh metadata có sẵn và tạo bảng Markdown | Có |
| rank_sources | Xếp hạng theo từ khóa, độ mới và domain ưu tiên | Có |

### A3. Câu hỏi mẫu để thử

1. Tìm 2 nguồn trên web về robotics trong tuần này, kèm URL.
2. Đọc và tóm tắt trang https://www.python.org/about/ bằng tiếng Việt.
3. Loại nguồn trùng trong danh sách `[{"url":"https://example.org/a?utm_source=feed"},{"url":"https://example.org/a"}]`, giữ bản đầu tiên.
4. So sánh năm và phương pháp của hai paper `[{"title":"Paper A","year":2024,"method":"Survey"},{"title":"Paper B","year":2025,"method":"Experiment"}]`.
5. Kiểm tra mã trích dẫn trong bản nháp `Kết luận [s1], hạn chế [s2].` với nguồn `[{"id":"s1","url":"https://example.org/study"}]`.

## 3. Giải pháp

- v1 sửa `system_prompt.md`: hỏi lại khi thiếu dữ liệu thiết yếu, dùng thông tin từ context và yêu cầu xác nhận nội dung trước khi gửi.
- v2 sửa `tools.yaml`: làm rõ `lookup.query`, tách loại tin và khoảng thời gian qua `topic`, `timeframe`.
- v3 sửa `system_prompt.md`: nhắc lại quy tắc chuẩn hóa query và dùng handle tài khoản thay cho tên hiển thị.
- v4 bỏ ràng buộc một bước/một tool, bổ sung routing theo nguồn và cho phép nhiều tool độc lập; đo đối chứng với cùng 14 tool.
- v5 hoàn thiện description khi dùng/không dùng và quy ước arguments của tất cả tool; send yêu cầu confirmed và chỉ chấp nhận boolean true.
- CP3 thêm bốn tool local, đăng ký registry/schema và viết 46 test. Các tool chỉ xử lý dữ liệu được cung cấp; citation check không xác minh sự thật của nguồn, ranking dùng heuristic.
- UI Streamlit dùng lại `run_model_tool_loop` trong `chat.py` thông qua `web_chat.py`. Mỗi phiên có history và transcript riêng; lượt hỏi lại tiếp tục dùng context. `privacy.py` che credential trong kết quả, file và bản tải xuống.
- UI loại send khỏi schema và chặn tool ngoài allowlist trước khi thực thi. CLI giữ cơ chế xác nhận; phiên đầu kiểm tra hủy gửi, phiên v5 đã gửi thật một tin sau khi user xác nhận đúng nội dung và nhóm nhận.
- Hash prompt/tools được giữ trong mọi run và transcript. Run nhóm/chat sau khi bổ sung tool có tools hash riêng; bảng B1 giữ nguyên v0–v3 và bổ sung đối chứng 14 tool, v4, v5.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Metric là `case_accuracy`. Các run trong bảng đều đo đủ 20 case và không có lỗi provider; hash và giả thuyết được ghi trong [version_log.csv](../../starter_v0/artifacts/version_log.csv).

| Version | Changed Artifact | Hypothesis | Metric Before (case_accuracy) | Metric After (case_accuracy) | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu trước khi sửa prompt và tool declaration |  | 0.65 | [v0_B_base_gemini_20261110T183632505620.json](../../starter_v0/runs/v0_B_base_gemini_20261110T183632505620.json) |
| v1 | system_prompt.md | Quy định hỏi lại khi thiếu dữ liệu và xác nhận nội dung trước khi gửi sẽ giảm lỗi missing_info và wrong_boundary | 0.65 | 0.75 | [v1_B_base_gemini_20261110T192455812815.json](../../starter_v0/runs/v1_B_base_gemini_20261110T192455812815.json) |
| v2 | tools.yaml | Tách chủ đề tìm kiếm khỏi loại tin và thời gian trong khai báo tool sẽ giảm lỗi arguments do tự mở rộng query | 0.75 | 0.85 | [v2_B_base_gemini_20261110T192913379384.json](../../starter_v0/runs/v2_B_base_gemini_20261110T192913379384.json) |
| v3 | system_prompt.md | Nhắc lại quy ước arguments trong prompt sẽ giúp model giữ đúng chủ đề tìm kiếm và dùng handle thay cho tên hiển thị | 0.85 | 0.90 | [v3_B_base_gemini_20261110T193212164707.json](../../starter_v0/runs/v3_B_base_gemini_20261110T193212164707.json) |
| v3-cp3 | baseline 14 tools | Đo routing và arguments trước khi hoàn thiện C2 với cùng danh sách 14 tool |  | 0.85 | [v3-cp3_B_base_gemini_20261111T010319101559.json](../../starter_v0/runs/v3-cp3_B_base_gemini_20261111T010319101559.json) |
| v4 | system_prompt.md | Routing rõ và cho phép nhiều tool sẽ giảm lỗi thiếu nguồn ở yêu cầu web và tweet | 0.85 | 0.95 | [v4_B_base_gemini_20261111T010552889357.json](../../starter_v0/runs/v4_B_base_gemini_20261111T010552889357.json) |
| v5 | tools.yaml | Khai báo rõ mục đích và arguments sẽ giảm nhầm tool và truyền tham số sai | 0.95 | 0.90 | [v5_B_base_gemini_20261111T010040350391.json](../../starter_v0/runs/v5_B_base_gemini_20261111T010040350391.json) |

### B2. Failure Analysis

Phân tích 7 case FAIL của [baseline v0](../../starter_v0/runs/v0_B_base_gemini_20261110T183632505620.json).

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R03_web_news_routing` | `wrong_tool` | `[{"name": "lookup", "args": {"topic": "news", "query": "AI news today artificial intelligence trending", "timeframe": "day"}}]` | Chọn đúng lookup nhưng mở rộng query thành AI news today artificial intelligence trending, khác AI mà eval yêu cầu; khai báo chưa quy định rõ cách giữ từ khóa. | Quy định query giữ chủ đề người dùng; loại tin và thời gian truyền qua topic, timeframe. |
| `R10_missing_handle` | `missing_info` | `[{"name": "timeline", "args": {"limit": 5, "screenname": "sama"}}]` | Tự đoán screenname=sama thay vì hỏi tài khoản; prompt hiện khuyến khích đoán khi thiếu thông tin. | Bỏ chỉ dẫn tự đoán tài khoản; yêu cầu clarify(response_type="text") khi thiếu handle. |
| `R11_missing_url` | `missing_info` | `[{"name": "lookup", "args": {"query": "tin tức mới nhất hôm nay"}}]` | Tự tìm tin tức bằng lookup khi chưa có URL, thay vì hỏi lại; prompt hiện yêu cầu tự đoán khi thiếu thông tin. | Yêu cầu clarify(response_type="text") để lấy URL khi người dùng nhắc bài viết nhưng chưa cung cấp địa chỉ. |
| `R12_confirm_before_send` | `wrong_boundary` | `[{"name": "send", "args": {"confirmed": true, "text": "Bản tin hôm nay: Cập nhật các thông tin mới nhất và quan trọng nhất."}}]` | Gọi send với confirmed=true khi chưa được xác nhận, thay vì clarify; prompt hiện khuyến khích gửi ngay. | Bỏ chỉ dẫn gửi ngay; yêu cầu clarify(response_type="yes_no") xác nhận nội dung trước khi gọi send với confirmed=true. |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `[{"name": "lookup", "args": {"query": "AI news today", "timeframe": "day"}}]` | Thiếu social_search, query lookup khác AI và thiếu topic=news; prompt ép chọn một tool nên không đáp ứng yêu cầu hai nguồn. | Cho phép nhiều tool khi yêu cầu có nhiều nguồn; gọi lookup và social_search, giữ query theo chủ đề và đặt topic=news cho tin tức. |
| `M02_carryover_timeframe` | `wrong_arg_value` | `[{"name": "lookup", "args": {"timeframe": "day", "topic": "news", "query": "robotics news today"}}]` | Giữ đúng timeframe=day và topic=news nhưng query là robotics news today thay vì robotics; chưa tách rõ chủ đề khỏi bộ lọc thời gian. | Giữ query là chủ đề mới; kế thừa topic và timeframe từ ngữ cảnh qua các arguments riêng. |
| `M06_switch_tool` | `wrong_tool` | `[{"name": "lookup", "args": {"timeframe": "week", "query": "OpenAI tin tức mới nhất", "topic": "news"}}]` | Đã chuyển đúng sang lookup nhưng query là OpenAI tin tức mới nhất thay vì OpenAI; chưa quy định rõ cách tách chủ đề và loại tin. | Khi đổi nguồn sang web, giữ query theo chủ đề và biểu diễn yêu cầu tin tức bằng topic=news. |

### B3. Team Eval Cases

[Bộ eval nhóm](../../starter_v0/data/eval_group.json) có 5 single turn và 5 multi turn. Run nhóm đo đủ 10 case, đạt 10/10 PASS và không có lỗi provider.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_deduplicate_collected_sources` | Đã có nguồn thì route tới deduplicate_sources để loại trùng theo URL; chấm lựa chọn tool, không yêu cầu tìm kiếm lại. | `deduplicate_sources()` | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G02_check_existing_citations` | Kiểm tra mã trích dẫn của bản nháp bằng check_citations với draft giữ nguyên; thiếu nguồn được báo trong kết quả tool. | `check_citations(draft="Phương pháp này giảm chi phí tính toán [source_a], nhưng còn giới hạn dữ liệu [source_b].")` | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G03_compare_paper_fields` | Route tới compare_papers và chỉ chọn year, method theo yêu cầu, dựa trên metadata có sẵn. | `compare_papers(fields=["year", "method"])` | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G04_rank_sources_with_explicit_filters` | Xếp hạng nguồn đã có bằng rank_sources; trích đúng chủ đề, ngày mốc, domain ưu tiên và giới hạn. | `rank_sources(query="robotics", reference_date="2026-11-10", preferred_domains=["example.org"], limit=2)` | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G05_explain_ranking_without_execution` | Câu hỏi giải thích nguyên tắc không cần gọi rank_sources hay tool tìm kiếm. | Không gọi tool; giải thích trực tiếp. | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G06_deduplicate_after_user_supplies_items` | Sau khi người dùng cung cấp danh sách còn thiếu, thực hiện deduplicate_sources thay vì hỏi lại hoặc tự tìm nguồn. | `deduplicate_sources()` | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G07_check_revised_draft_in_context` | Dùng bản nháp mới nhất khi kiểm tra citation, không tiếp tục kiểm tra bản nháp cũ trong context. | `check_citations(draft="Kết luận [source_b].")` | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G08_compare_with_revised_columns` | Kế thừa metadata hai paper nhưng thay cột so sánh theo yêu cầu cuối, không dùng lại year/authors. | `compare_papers(fields=["method", "limitations"])` | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G09_rank_with_updated_preferences` | Kế thừa danh sách và ngày mốc; cập nhật chủ đề, domain và limit theo lượt mới nhất. | `rank_sources(query="climate", reference_date="2026-11-10", preferred_domains=["example.org"], limit=1)` | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| `G10_cancel_telegram_delivery` | Người dùng từ chối ở bước xác nhận thì không gọi send hoặc tool khác; chỉ xác nhận đã hủy. | Không gọi tool; xác nhận đã hủy gửi. | [PASS](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |

### B4. Live Chat Evidence

Phiên CLI được chạy bằng `python3 chat.py --provider gemini --version v3 --max-tool-rounds 6`; các câu trả lời và tool results được ghi từ Gemini/API thật. Phiên UI được chạy qua AppTest với Gemini thật.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| CLI 1 | Tìm 2 nguồn trên web về robotics trong tuần này. Trả lời ngắn bằng tiếng Việt và kèm URL của từng nguồn. | `lookup` | `v3+p401da314901c+t7102a4e57de5` · [CLI transcript](../../starter_v0/transcripts/v3_gemini_20261111T000642591554.transcript.json) | Trả 2 nguồn web có URL; lookup không báo lỗi. |
| CLI 2 | Tôi muốn tóm tắt một bài giới thiệu Python khác, chưa cung cấp URL của bài đó. Bạn hãy hỏi tôi URL trước. | Không gọi tool | `v3+p401da314901c+t7102a4e57de5` · [CLI transcript](../../starter_v0/transcripts/v3_gemini_20261111T000642591554.transcript.json) | Hỏi người dùng cung cấp URL bằng câu trả lời văn bản; không tự chọn bài. |
| CLI 3 | URL bài giới thiệu Python là https://www.python.org/about/ . Hãy đọc và tóm tắt ngắn bằng tiếng Việt. | `fetch` | `v3+p401da314901c+t7102a4e57de5` · [CLI transcript](../../starter_v0/transcripts/v3_gemini_20261111T000642591554.transcript.json) | Gọi fetch với URL đã bổ sung và tóm tắt nội dung Python; không báo lỗi tool. |
| CLI 4 | Tôi muốn gửi nguyên văn lên Telegram nội dung: "Bản tin thử nghiệm CP5: nhóm E1110 đã hoàn tất kiểm tra nguồn." Hãy hỏi tôi xác nhận trước khi gửi. | Không gọi tool | `v3+p401da314901c+t7102a4e57de5` · [CLI transcript](../../starter_v0/transcripts/v3_gemini_20261111T000642591554.transcript.json) | Hỏi xác nhận đúng nội dung gửi bằng văn bản; chưa gọi send. |
| CLI 5 | Không, hủy gửi. Không gửi lên Telegram. Chỉ xác nhận đã hủy yêu cầu. | Không gọi tool | `v3+p401da314901c+t7102a4e57de5` · [CLI transcript](../../starter_v0/transcripts/v3_gemini_20261111T000642591554.transcript.json) | Xác nhận đã hủy; không gọi send. |
| UI 1 | Loại nguồn trùng trong danh sách có URL tracking và URL gốc. | `deduplicate_sources` | `v3+p401da314901c+t7102a4e57de5` · [UI transcript](../../starter_v0/transcripts/ui_v3_gemini_20261111T001107859594_68dcd91e.transcript.json) | Hai nguồn được gộp thành một; giao diện hiển thị đủ user và assistant. |
| Telegram 1 | Chuẩn bị gửi nguyên văn bản tin thử nghiệm vào nhóm riêng tư Test_AILabDay3, hỏi xác nhận trước. | `clarify(response_type="yes_no")` | `v5+p3ac1cc7d1507+tc6a268606e07` · [Telegram transcript](../../starter_v0/transcripts/v5_gemini_20261111T011317669763.transcript.json) | Hỏi đúng nội dung cần gửi; waiting_for_user, chưa gửi. |
| Telegram 2 | Xác nhận gửi vào nhóm Test_AILabDay3 | `send(confirmed=true)` | `v5+p3ac1cc7d1507+tc6a268606e07` · [Telegram transcript](../../starter_v0/transcripts/v5_gemini_20261111T011317669763.transcript.json) | status=sent, message_id=5, chat_id=-5534876729; đúng một lần gọi gửi. |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới: deduplicate_sources | `starter_v0/tools/deduplicate_sources/tool.py`, `starter_v0/tools/deduplicate_sources/TOOL.md` | Loại nguồn trùng theo URL chuẩn hóa; giữ nguồn đầu và metadata gốc | Chỉ bỏ fragment và tham số tracking; giữ scheme, path và query có ý nghĩa; URL lỗi trả error dict |
| Tool mới: check_citations | `starter_v0/tools/check_citations/tool.py`, `starter_v0/tools/check_citations/TOOL.md` | Đối chiếu mã trích dẫn với nguồn, liệt kê mã thiếu và nguồn chưa dùng | Không xác minh nội dung nguồn; bỏ qua link và code Markdown; từ chối id trùng hoặc URL lỗi |
| Tool mới: compare_papers | `starter_v0/tools/compare_papers/tool.py`, `starter_v0/tools/compare_papers/TOOL.md` | So sánh metadata đã cung cấp, tạo bảng Markdown | Không suy diễn metadata thiếu; ghi Chưa cung cấp; escape nội dung ô bảng và kiểm tra kiểu dữ liệu |
| Tool mới: rank_sources | `starter_v0/tools/rank_sources/tool.py`, `starter_v0/tools/rank_sources/TOOL.md` | Xếp hạng theo từ khóa, độ mới và domain ưu tiên; trả điểm thành phần | Điểm heuristic không chứng minh độ tin cậy; ngày mốc cho phép tái lập; ngày tương lai không được cộng điểm độ mới |
| Đăng ký 4 tool | `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml` | Cả 4 tool có implementation, khai báo arguments và TOOL.md | Contract test kiểm tra tên tool, signature và schema |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py`; chạy `.venv/bin/python -m pytest` từ `starter_v0/` | 46 test mới pass: deduplicate_sources 12, check_citations 11, compare_papers 10, rank_sources 13. Toàn suite sau khi bổ sung regression test send: 147 passed, 12 skipped, 0 failed | Test offline, không dùng API key; 12 skip là stub của tool có sẵn, các test tool mới không skip |
| UI (lệnh chạy + link dùng thử) | [app.py](../../starter_v0/app.py), [web_chat.py](../../starter_v0/web_chat.py), [kiểm tra CP5](../../starter_v0/analysis/cp5_verification.json) | Streamlit chạy local; link public HTTP 200; AppTest gửi và hiển thị câu trả lời; Gemini thật loại trùng thành công | Transcript riêng cho từng phiên; che API key/token; chặn send ở bước thực thi của bản demo |

Tool unit tests: 46 test mới. Ví dụ `test_deduplicate_sources_preserves_path_case_and_meaningful_query` kiểm tra các URL khác path hoặc query có ý nghĩa không bị gộp nhầm; eval routing/arguments không kiểm tra hành vi này của code tool.

### B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model |  | Không thực hiện |  |
| Hơn 3 tool mới (≥ 4) | Bốn folder tool trong `starter_v0/tools/`, `tests/test_tools_todo.py` | Có 4 tool mới và 46 test đều pass | Không có tác dụng gửi ra ngoài; input lỗi trả error dict |
| send gửi thật lên Telegram sau xác nhận | [Telegram transcript](../../starter_v0/transcripts/v5_gemini_20261111T011317669763.transcript.json), [receipt](../../starter_v0/analysis/telegram_delivery.json) | clarify yes_no → user xác nhận → send confirmed=true → status sent; message_id=5, nhóm Test_AILabDay3 | User chọn nhóm riêng tư có chat.type=group, không phải private channel theo chữ trong rubric; nội dung và đích nhận được duyệt trước, đúng một lần gửi |
| Test challenge | [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py), [send/tool.py](../../starter_v0/tools/send/tool.py), [kết quả kiểm tra C2](../../starter_v0/analysis/c2_verification.json) | Có regression test cho bug tool send có sẵn: chuỗi false/true và số 1 từng vượt qua guard xác nhận; test đã FAIL trước sửa và PASS sau sửa. Toàn suite 147 passed, 12 skipped | Chỉ boolean true được gửi; API phải trả ok=true và message_id hợp lệ mới báo sent |

Test hồi quy của tool mới kiểm tra reference-link Markdown, code nhiều backtick và query URL. Regression test của tool có sẵn send kiểm tra kiểu confirmed và tránh báo sent khi API không xác nhận giao hàng.

### B7. Small Local Model Challenge (bonus)

Không thực hiện.

## 5. Khó khăn và cách xử lý

- Baseline v0 có lỗi HTTP 403 ở tool send; model tự đặt confirmed=true khi chưa được user xác nhận. Bảng B2 phân tích lỗi boundary; v1 bổ sung quy tắc hỏi lại. Token trong URL lỗi đã được che trong run lưu trữ. Kiểm tra sau đó phát hiện chat_id ban đầu trỏ tới chính bot; đã đổi sang nhóm Test_AILabDay3 do user cung cấp và xác nhận, gửi thành công message_id=5.
- Trong run lịch sử v3 còn hai case FAIL: R12 trả clarify dạng text khi chưa có nội dung cụ thể, khác đáp án yes_no; R13 thiếu social_search trong yêu cầu hai nguồn. Chi tiết tại [run base v3](../../starter_v0/runs/v3_B_base_gemini_20261110T193212164707.json).
- Review UI phát hiện lỗi provider ở vòng sau có thể làm mất tool results đã chạy; đã giữ lại rounds/events và thêm regression test `test_provider_failure_keeps_previously_executed_tool_results` trong [test_chat_session.py](../../starter_v0/tests/test_chat_session.py).
- Hai run đầu của giai đoạn C2 gặp 429 do giới hạn 15 request/phút và không được dùng để chấm metric. Các lượt đối chứng được chạy lại tuần tự có giãn cách; log lỗi được giữ trong runs và liệt kê trong [c2_verification.json](../../starter_v0/analysis/c2_verification.json).
- Quick Tunnel là link tạm, không thay thế hosting cố định. Cần giữ hai tiến trình chạy và cập nhật URL nếu khởi động lại tunnel.
- Chưa kiểm thử thao tác trực tiếp bằng Chrome do quyền Computer Use không được cấp. Đã kiểm tra giao diện bằng AppTest, gửi một yêu cầu UI với Gemini thật và kiểm tra HTTP/health của link public.

## 6. Tổng hợp đóng góp

| Thành viên | Phần việc phụ trách | Bằng chứng |
|---|---|---|
| Đỗ Minh Thanh — 2A202603793 | Phụ trách toàn bộ CP1–CP5: setup, baseline, tối ưu prompt/tool declaration, bốn tool mới và test, eval nhóm, UI, chat và báo cáo; có hỗ trợ của Codex/ChatGPT | [Báo cáo cá nhân](2A202603793_DoMinhThanh.md), [TEAM.md](../../TEAM.md), [version log](../../starter_v0/artifacts/version_log.csv) |

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- `system_prompt.md` điều chỉnh hành vi khi thiếu thông tin, cần xác nhận và chuẩn hóa arguments; `tools.yaml` làm rõ ý nghĩa từng trường của lookup. Case accuracy base tăng từ 0.65 lên 0.90, nhưng routing giảm từ 1.00 ở v2 xuống 0.95 ở v3; cần xem cả metric thành phần.
- Eval chấm tool calls và subset arguments, không chấm chất lượng câu trả lời cuối. Một số case nhóm chỉ đo routing vì items/papers/sources là cấu trúc lồng nhau; unit test riêng kiểm tra xử lý dữ liệu của tool. Run nhóm đạt 10/10 không chứng minh agent đúng ở mọi yêu cầu.
- R12 cần review thủ công: thiếu nội dung gửi thì câu hỏi text có thể phù hợp trước khi hỏi yes/no. Cần đánh giá hành vi an toàn thực tế cùng đáp án tự động. V5 vẫn hỏi text khi nội dung gửi chưa được cung cấp.
- Phiên v3 hỏi URL và xác nhận bằng văn bản trực tiếp. Phiên Telegram v5 đã gọi clarify yes_no, chờ câu trả lời xác nhận rồi mới gọi send; transcript và receipt ghi nhận message_id=5. Đích nhận là nhóm riêng tư do user chọn, không ghi nhận đây là private channel.
- Đối chứng 14 tool đạt 85%; v4 thêm routing và cho phép nhiều tool đạt 95%; v5 hoàn thiện khai báo đạt 90%, routing 100%. v5 còn lỗi mở rộng query ở R03 và response_type ở R12; điểm không tăng so với v4 được ghi đúng trong version log. Vòng tiếp theo sẽ kiểm chứng ví dụ few-shot tách chủ đề query khỏi bộ lọc tin/thời gian, không sửa đáp án hoặc metric cũ.
- Citation check chỉ đối chiếu ID và URL; ranking không xác minh độ tin cậy; metadata paper thiếu được ghi rõ. UI hiện chưa có đăng nhập và giữ phiên hội thoại trong tiến trình Streamlit, còn transcript được lưu trên đĩa.

## 8. Tài liệu tham khảo

- [README và quy trình lab](../../README.md), [CHECKPOINTS.md](../../CHECKPOINTS.md), [RUBRIC.md](../../RUBRIC.md).
- [Thiết lập API tool](../../README.md#setup), [contract thư mục tool](../../starter_v0/tools/README.md).
- [Streamlit chat elements](https://docs.streamlit.io/develop/api-reference/chat), [Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).
- [Telegram Bot API — sendMessage](https://core.telegram.org/bots/api#sendmessage).
- [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/), [tải cloudflared](https://developers.cloudflare.com/tunnel/downloads/).
