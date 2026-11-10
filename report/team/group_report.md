# Báo cáo nhóm E1110 — Research Agent Tool Eval

## 1. Thông tin nhóm và tiến độ

- **Tên nhóm:** E1110.
- **Nhóm trưởng:** Phạm Quang Tuấn — MSSV **2A202603824**.
- **Repo:** [K5-L3B-DAY03-E1110-ResearchAgentToolEval](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval).
- **Thông tin thành viên:** [TEAM.md](../../TEAM.md).
- **Trạng thái báo cáo:** bản tổng hợp kỹ thuật CP1–CP5; phần cá nhân bổ sung sau; chưa phải báo cáo hoàn tất toàn bộ bài lab.

| Checkpoint                     | Trạng thái                     | Bằng chứng / việc còn lại                                                             |
| ------------------------------ | ------------------------------ | ------------------------------------------------------------------------------------- |
| CP1 — Setup và baseline        | Hoàn thành bằng chứng kỹ thuật | Baseline một model: 13/20 PASS; đủ 20 case, 0 lỗi provider                            |
| Chuẩn hóa cấu hình sau CP1     | Hoàn thành                     | Chỉ Gemini 3.5 Flash Lite, pacing 4,5 giây và retry 60 giây                           |
| CP2 — Tối ưu v1–v3             | Hoàn thành                     | Accuracy 65% → 70% → 75% → 90%; đủ run, hash, snapshot và phân tích                   |
| CP3 — Tool mới và test         | Hoàn thành                     | source_audit, TOOL.md, registry/YAML, 10 unit test cho tool mới                       |
| CP4 — Eval nhóm                | Hoàn thành                     | Đúng 5 single + 5 multi turn; 10/10 PASS, 0 lỗi provider                              |
| CP5 — UI, live chat và báo cáo | UI public và 4 lượt live đã có | Link có mã truy cập đã kiểm tra qua public URL; phần cá nhân bổ sung sau theo yêu cầu |

## 2. Phần A — Giới thiệu agent

### A1. Mục tiêu và cách chạy

Agent hỗ trợ nghiên cứu thông tin bằng cách chọn công cụ phù hợp: tìm trên web và mạng xã hội, đọc URL, tra cứu tài liệu nội bộ hoặc paper, sau đó định dạng kết quả thành bản tin. Mục tiêu thực hành là đo và cải thiện khả năng chọn tool, truyền arguments, hỏi lại khi thiếu thông tin và xác nhận trước khi gửi nội dung.

UI Streamlit của nhóm chạy từ thư mục `starter_v0/`:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Provider mặc định dùng **Gemini 3.5 Flash Lite** và đọc `GEMINI_API_KEY` từ `.env`. Các công cụ gọi dịch vụ bên ngoài cần cấu hình key riêng theo [TOOL-SETUP.md](../../docs/TOOL-SETUP.md).

**UI local:** [http://127.0.0.1:8501](http://127.0.0.1:8501) khi app đang chạy. **Link demo public:** [E1110 Research desk](https://angel-modification-priced-validation.trycloudflare.com). Cần mã DEMO_ACCESS_CODE được nhóm trưởng chia sẻ riêng; mã không ghi trong báo cáo. Link tạm thời chỉ hoạt động khi app/tunnel trên máy này còn chạy; xem [hướng dẫn demo](../../docs/DEMO.md). [Ảnh giao diện](../../starter_v0/analysis/ui-preview.png). Prompt v3 đã bổ sung hỏi lại, xác nhận và routing; bộ base đạt 90%, vẫn cần kiểm tra live trước khi demo.

### A2. Công cụ có trong dự án

Agent có 11 tool: 10 tool từ starter và source_audit do nhóm bổ sung ở CP3.

| Tool                     | Chức năng                                                                  |
| ------------------------ | -------------------------------------------------------------------------- |
| `clarify`                | Hỏi người dùng và tạm dừng để chờ bổ sung thông tin                        |
| `timeline`               | Lấy các bài đăng gần đây của một tài khoản                                 |
| `social_search`          | Tìm bài đăng theo từ khóa, sắp xếp Top hoặc Latest                         |
| `lookup`                 | Tìm trên web theo chủ đề và khoảng thời gian                               |
| `fetch`                  | Đọc nội dung một URL qua Firecrawl                                         |
| `format`                 | Chuyển các item có sẵn thành markdown digest                               |
| `send`                   | Gửi Telegram khi có xác nhận và cấu hình kết nối                           |
| `policy`                 | Tìm trong kho company policy Markdown nội bộ                               |
| `papers`                 | Tìm paper trên arXiv                                                       |
| `paper_text`             | Tải PDF arXiv và trích xuất văn bản                                        |
| `source_audit` **(mới)** | Rà metadata nguồn, URL thiếu/sai/trùng và thiếu tiêu đề/ngày; chạy offline |

Khai báo và registry: [tools.yaml](../../starter_v0/artifacts/tools.yaml), [tools/**init**.py](../../starter_v0/tools/__init__.py).

### A3. Câu hỏi mẫu

1. “Lấy 5 tweet mới nhất của tài khoản sama.”
2. “Tìm tin công nghệ trong tuần này.”
3. “Tóm tắt nội dung tại URL sau: [điền URL cụ thể].”
4. “Tìm paper về retrieval augmented generation trên arXiv.”
5. “Rà URL trùng, không yêu cầu ngày: [{title: A, url: https://example.org/a#one}, {title: B, url: https://example.org/a#two}].”

Đây là câu hỏi để dùng thử; kết quả tìm kiếm thực tế phụ thuộc kết nối và cấu hình từng tool.

## 3. Giải pháp đã triển khai

### 3.1. Tối ưu prompt và tool declaration theo ba giả thuyết

- **v1 — Kiểm tra thông tin và xác nhận:** thay chỉ dẫn đoán account/URL và gửi ngay bằng `clarify`, dùng lịch sử để tránh hỏi lại chi tiết đã có. Giữ nguyên quy tắc một tool để tách ảnh hưởng. Accuracy tăng 65% → 70%; routing tăng 80% → 95%, nhưng còn thiếu/sai `response_type`.
- **v2 — Routing theo ý định:** thay quy tắc một tool bằng chọn tool theo nguồn, cho phép nhiều nguồn độc lập, xử lý lượt sửa mới nhất và không gọi tool cho câu meta/ngoài phạm vi. Accuracy tăng 70% → 75%; routing đạt 100%. Năm case FAIL còn lại đều sai arguments.
- **v3 — Hợp đồng tool rõ ràng:** giữ nguyên prompt v2, viết lại mô tả của cả 10 tool: khi nào dùng/không dùng, handle không có `@`, topic/timeframe, Top/Latest, query ngắn theo chủ đề, `response_type` và điều kiện `confirmed=true`. Accuracy tăng 75% → 90%; multi-turn đạt 100%.

Không sửa tên tool, schema, implementation của tool hoặc nội dung case base/extension trong CP2. Các bản đầu vào được lưu tại [artifacts/versions](../../starter_v0/artifacts/versions/README.md); CP3 sau đó mở rộng v3 với source_audit, lưu riêng ở snapshot cp3; không ghi đè các snapshot CP2.

### 3.2. Ổn định việc gọi Gemini

[Gemini provider](../../starter_v0/providers/gemini_provider.py) hiện chỉ dùng model mặc định `gemini-3.5-flash-lite`, không tự chuyển sang 3.1. Các request trong cùng tiến trình chạy tuần tự, cách thời điểm bắt đầu ít nhất **4,5 giây**, tương ứng tối đa khoảng 14 request trong cửa sổ 60 giây, dưới mức quota 15 RPM được cấu hình cho bài thực hành.

Khi gặp 429, lỗi tạm thời 500/502/503/504 hoặc lỗi kết nối/DNS/timeout, provider chờ **60 giây** và thử lại tối đa hai lần trên cùng model. Lỗi xác thực không được retry. Hàng đợi không điều phối giữa nhiều tiến trình hoặc ứng dụng cùng dùng quota, vì vậy cần chạy từng tác vụ eval/chat lần lượt.

[run_eval.py](../../starter_v0/run_eval.py) lưu model thực tế theo từng case. Những thay đổi trên thuộc hạ tầng chạy, chưa được tính là vòng tối ưu prompt v1–v3.

## 4. Phần B — Kết quả và bằng chứng

### B1. Version Evidence

Mọi run trong bảng dùng **Gemini 3.5 Flash Lite**, cùng bộ base 20 case, temperature 0 và pacing 4,5 giây/request. Cả bốn run đều đo đủ 20/20 case, **0 lỗi provider**. Run hai model trước đó được giữ làm lịch sử, không dùng để tính mức cải thiện CP2.

| Version | Artifact thay đổi | Case accuracy | Routing | Arguments | Multi-turn | Run                                                                       |
| ------- | ----------------- | ------------: | ------: | --------: | ---------: | ------------------------------------------------------------------------- |
| v0      | baseline          |           65% |     80% |       65% |     66,67% | [JSON](../../starter_v0/runs/v0_B_base_gemini_20261110T182510939163.json) |
| v1      | system_prompt.md  |           70% |     95% |       70% |     66,67% | [JSON](../../starter_v0/runs/v1_B_base_gemini_20261110T182726997677.json) |
| v2      | system_prompt.md  |           75% |    100% |       75% |     66,67% | [JSON](../../starter_v0/runs/v2_B_base_gemini_20261110T182947409615.json) |
| v3      | tools.yaml        |           90% |    100% |       90% |       100% | [JSON](../../starter_v0/runs/v3_B_base_gemini_20261110T183254561353.json) |

Kết quả cuối: **18/20 PASS**, tăng **25 điểm phần trăm** so với baseline một model. Mỗi version chỉ đổi một nhóm giả thuyết; v1/v2 thay prompt, v3 chỉ thay descriptions trong YAML. Contract test **55/55** sau mỗi vòng.

Bằng chứng: [version log](../../starter_v0/artifacts/version_log.csv), [bảng metric CSV](../../starter_v0/analysis/cp2_metrics.csv), [chi tiết từng case](../../starter_v0/analysis/cp2_case_results.csv), [giả thuyết và run](../../starter_v0/analysis/cp2_experiments.json). Snapshot hash đã đối chiếu với từng run.

### B2. Failure Analysis

Bảng theo dõi các case từng FAIL qua bốn version. “Loại case” là nhãn dataset, không đồng nghĩa sai lệch thực tế luôn là sai tên tool. Ví dụ R03 mang nhãn wrong_tool nhưng model chọn đúng `lookup`, chỉ sai query.

| Case                        | Loại case       | v0   | v1   | v2   | v3   | Phân tích                                                                                                      |
| --------------------------- | --------------- | ---- | ---- | ---- | ---- | -------------------------------------------------------------------------------------------------------------- |
| R03_web_news_routing        | wrong_tool      | FAIL | FAIL | FAIL | FAIL | Cả bốn bản chọn lookup; v3 vẫn dịch/mở rộng AI thành artificial intelligence news, không khớp query chính xác. |
| R10_missing_handle          | missing_info    | FAIL | PASS | PASS | PASS | v0 tự đoán tài khoản; từ v1 chuyển sang clarify đúng.                                                          |
| R11_missing_url             | missing_info    | FAIL | FAIL | PASS | PASS | v1 đã chọn clarify nhưng thiếu response_type trong call; từ v2 PASS.                                           |
| R12_confirm_before_send     | wrong_boundary  | FAIL | FAIL | FAIL | FAIL | v0 chọn send; v1–v3 đã hỏi lại và không gửi, nhưng response_type=text thay vì yes_no theo expect.              |
| R13_parallel_web_and_tweets | wrong_tool      | FAIL | FAIL | FAIL | PASS | v0/v1 thiếu nguồn social; v2 chọn đủ tool nhưng query không khớp; v3 PASS.                                     |
| M02_carryover_timeframe     | wrong_arg_value | FAIL | FAIL | FAIL | PASS | v0–v2 mở rộng query hoặc giữ chủ đề cũ; v3 dùng đúng chủ đề và timeframe.                                      |
| M06_switch_tool             | wrong_tool      | FAIL | FAIL | FAIL | PASS | Đã đổi sang web nhưng query bị thêm news; v3 dùng đúng query.                                                  |

**Hai case còn FAIL ở v3 cần review thủ công:**

- **R03:** expected query `AI`, actual `artificial intelligence news`. Đây là sai convention arguments theo bộ đo; chưa đủ cơ sở kết luận kết quả tìm kiếm sẽ vô ích.
- **R12:** agent hỏi xin nội dung bản tin bằng `clarify(response_type="text")`; expect yêu cầu `yes_no`. Model không gọi `send`, nên không có bằng chứng gửi khi chưa xác nhận. Cần thêm eval về nội dung cụ thể → xin xác nhận → user đồng ý → gửi để kiểm tra boundary đầy đủ ở CP4/CP5.

Không sửa expect để tăng điểm và không coi việc chỉ đổi response_type là đã chứng minh an toàn khi xuất bản. Kết quả base không thay thế kiểm thử end-to-end các dịch vụ bên ngoài.

### B3. Team Eval Cases

Nguồn: [eval_group.json](../../starter_v0/data/eval_group.json), [run group](../../starter_v0/runs/cp3_B_group_gemini_20261110T185301567314.json). Đúng **10 case: 5 single turn + 5 multi turn**, mọi case có phase, failure_type, expect và what_it_tests.

| Case                                  | Loại   | Nội dung đo                                                                   | Tool mong đợi | Kết quả |
| ------------------------------------- | ------ | ----------------------------------------------------------------------------- | ------------- | ------- |
| G01_audit_duplicate_sources           | Single | Route tới tool mới source_audit với nguồn có sẵn, bỏ yêu cầu ngày theo user.  | source_audit  | PASS    |
| G02_read_exact_report_url             | Single | URL cụ thể phải được giữ nguyên và dùng fetch thay vì lookup.                 | fetch         | PASS    |
| G03_internal_privacy_policy           | Single | Phân biệt kho chính sách nội bộ với tin tức public; truyền đúng policy_area.  | policy        | PASS    |
| G04_recent_scholarly_papers           | Single | Paper discovery khác đọc full text; giữ số lượng và sort enum.                | papers        | PASS    |
| G05_format_existing_items             | Single | Không gọi retrieval/audit thừa khi chỉ được yêu cầu format dữ liệu có sẵn.    | format        | PASS    |
| G06_audit_date_requirement_correction | Multi  | Tool mới nhận correction require_date=false sang true, không bịa ngày thiếu.  | source_audit  | PASS    |
| G07_audit_after_sources_supplied      | Multi  | Khi nguồn đã được bổ sung thì audit, không hỏi lại; giữ tùy chọn bỏ qua ngày. | source_audit  | PASS    |
| G08_correct_article_url               | Multi  | Lượt sửa URL mới nhất thay thế link cũ, không gọi hai nguồn.                  | fetch         | PASS    |
| G09_change_social_order_and_count     | Multi  | Đồng thời cập nhật sort và limit, giữ chủ đề trước đó.                        | social_search | PASS    |
| G10_switch_source_keep_month          | Multi  | Chuyển nguồn và giữ topic/timeframe; không gọi nguồn đã hủy.                  | lookup        | PASS    |

Run đạt 100% case/routing/arguments/multi-turn, đo đủ 10/10 và 0 lỗi provider.
Đây là suite mới, không dùng mức 100% này để kết luận base accuracy tăng từ 90%.
G09 có tool social_search trả HTTPError dù routing/args PASS; cần xử lý kết nối/quota dịch vụ này để hoàn thiện research end-to-end. Ba case G01/G06/G07 route đúng tới tool mới và thực thi audit thật.

### B4. Live Chat Evidence

[Transcript UI thật](../../starter_v0/transcripts/cp3_ui_e1dee9d82ad24b87b2870be3f78073ad.transcript.json), origin=streamlit, Gemini 3.5 Flash Lite. [Ảnh kiểm tra](../../starter_v0/analysis/ui-live-check.png).

| Lượt | Yêu cầu                                             | Tool         | Kết quả thực tế                                                       |
| ---- | --------------------------------------------------- | ------------ | --------------------------------------------------------------------- |
| 1    | Rà nguồn mẫu có hai URL khác fragment               | source_audit | Phát hiện một URL trùng, status needs_review; trả lời từ kết quả thật |
| 2    | Tóm tắt nhưng chưa có URL                           | clarify      | Hỏi URL, status waiting_for_user                                      |
| 3    | Bổ sung URL và chỉ đọc đúng link đó                 | fetch        | Đọc URL, tóm tắt và dẫn nguồn từ tool result                          |
| 4    | Chuẩn bị đăng một nội dung cụ thể, yêu cầu chưa gửi | clarify      | Hỏi xác nhận đúng nội dung; chưa gọi send                             |

UI lưu transcript, cho tải JSON, hiển thị kết quả và lỗi tool. Lớp thực thi UI chặn model tự gửi dù model đặt confirmed=true; cần người dùng bấm duyệt nội dung/kênh. Các hành vi hủy, chống gửi lặp và đổi kênh được test bằng mock. Sau 4 lượt QA ban đầu đã chạy thêm flow gửi Telegram thật; biên nhận/transcript ở B5. Public URL đã trả HTTP 200 và browser hiển thị màn hình nhập mã. AppTest kiểm tra chặn chưa đăng nhập, từ chối mã sai và mở chat với mã đúng. Chưa có xác nhận một người ngoài nhóm trực tiếp dùng thử; cần nhóm khác mở link và nhập mã để kiểm tra cuối.

**Bổ sung kiểm tra CLI theo đúng README:** đã chạy `python chat.py --provider gemini --model gemini-3.5-flash-lite --version cp5-cli` với 3 lượt thật (audit nguồn → hỏi URL → đọc URL được bổ sung), exit code 0, không provider_error. Đây là scripted QA, không phải lời xác nhận của người ngoài nhóm. [Transcript](../../starter_v0/transcripts/cp5-cli_gemini_20261110T195651906996.transcript.json), [log stdout/stderr](../../starter_v0/analysis/cp5_cli_live.log), [metadata](../../starter_v0/analysis/cp5_cli_live.json).

**Mẫu minh chứng dùng thử ngoài nhóm** [Biên bản dùng thử](../../starter_v0/analysis/external_ui_review/review.md)

### B5a. Tool mới, unit test và UI

| Hạng mục               | Kết quả                                                                                            | Bằng chứng                                                                                                     |
| ---------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Tool mới               | source_audit, không gọi mạng và không cần key                                                      | [tool.py](../../starter_v0/tools/source_audit/tool.py), [TOOL.md](../../starter_v0/tools/source_audit/TOOL.md) |
| Đăng ký                | Có trong TOOL_FUNCTIONS và tools.yaml                                                              | [registry](../../starter_v0/tools/__init__.py), [YAML](../../starter_v0/artifacts/tools.yaml)                  |
| Unit test tool mới     | 10 passed: hợp lệ, input xấu, lỗi nội bộ, URL lỗi/trùng, metadata thiếu                            | [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py)                                                |
| Toàn suite hiện tại    | **103 passed, 14 skipped, 0 failed**; skipped là stub tool cũ                                      | [kiểm tra CP3/CP4/UI](../../starter_v0/analysis/cp3_ui_checks.md)                                              |
| UI                     | Streamlit AppTest startup PASS; đã mở browser và chạy 4 lượt thật                                  | [app.py](../../starter_v0/app.py), [ui_session.py](../../starter_v0/ui_session.py)                             |
| Bảo vệ gửi Telegram    | 6 test session: chặn model tự gửi, duyệt đúng text một lần, hủy, đổi kênh, ẩn secret, giữ lỗi tool | [test_ui_session.py](../../starter_v0/tests/test_ui_session.py)                                                |
| Setup Telegram chỉ đọc | 4 test về metadata, whitelist phương thức, ẩn token khi lỗi                                        | [test_telegram_setup.py](../../starter_v0/tests/test_telegram_setup.py)                                        |

Ví dụ lỗi mà unit test kiểm tra ngoài routing: URL trùng qua fragment/port mặc định phải được gộp, nhưng query và chữ hoa/thường của path vẫn phân biệt. Model có thể chọn đúng source_audit nhưng code chuẩn hóa sai; unit test bắt trực tiếp hành vi này.

### B5. Bonus Evidence

| Hạng mục                          | Bằng chứng thực tế                                                                                                                                                                                                                                                                                                          | Trạng thái                                                                            |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Small Local Model                 | 2 model base eval, 2 vòng tối ưu, kiểm tra ngược Gemini, B7 bên dưới                                                                                                                                                                                                                                                        | Đã có đủ run/giả thuyết; kết quả giảm điểm vẫn giữ trung thực                         |
| Telegram gửi thật sau xác nhận    | [Flow JSON](../../starter_v0/analysis/bonus/telegram_send_flow.json), [transcript](../../starter_v0/transcripts/cp3_ui_4012b934c2c04647b4dae9c5956ba7a4.transcript.json), [ảnh trước](../../starter_v0/analysis/bonus/telegram-before-confirmation.png), [ảnh sau](../../starter_v0/analysis/bonus/telegram-after-send.png) | Đã gửi đúng một tin đã được user duyệt; status=sent, message_id=4                     |
| Test challenge — nhánh regression | [Trước/sau sửa](../../starter_v0/analysis/bonus/send_regression_summary.json), [6 test](../../starter_v0/tests/test_send_receipt.py)                                                                                                                                                                                        | 3 test guard FAIL trước sửa; 6 test PASS sau sửa; không gọi mạng thật trong unit test |
| Từ 4 tool mới                     | Hiện chỉ có source_audit là tool nhóm thêm                                                                                                                                                                                                                                                                                  | Chưa thực hiện nhánh bonus này                                                        |

**Flow Telegram thật:** agent hỏi xác nhận → user đồng ý đúng nội dung/kênh → model đề nghị send, UI giữ pending → thao tác bấm duyệt theo ủy quyền của user → `send(confirmed=true)` → Telegram trả **message_id=4, chat_id=-1004338885153, status=sent**. Nội dung duy nhất: “E1110 - kiểm tra quy trình duyệt bản tin.” [Mở tin trong private channel](https://t.me/c/4338885153/4), cần là thành viên kênh. Nguồn ủy quyền được ghi rõ trong flow JSON; không tự giả mạo hành động người dùng.

**Regression:** `if not confirmed` trước đây chấp nhận cả chuỗi "false", "true" và số 1 vì truthiness. Đã sửa chỉ nhận literal boolean true; test xác nhận các input sai không gọi HTTP. Đồng thời kiểm tra Telegram ok=true và biên nhận trước khi trả sent, lưu message_id/chat_id/date, ẩn token khi lỗi và không tự retry gửi.

Đây là bằng chứng cho nhánh regression của test challenge; 14 stub cũ vẫn skipped, không tuyên bố đạt 0 skipped. [Toàn bộ minh chứng bonus](../../starter_v0/analysis/bonus/README.md).

### B7. Small Local Model Challenge

Đã chạy base eval trên **hai model local dưới 8B, khác kích thước**, hai vòng tối ưu trên Qwen3B và kiểm tra ngược bản v5-local trên Gemini. Các run được chọn đều đủ **20/20 case, 0 lỗi provider**; cùng bộ base không sửa và temperature 0.

Các run local dùng **10 tool của snapshot v3**, còn UI live có 11 tool sau CP3; không gán điểm local này cho cấu hình UI chưa đo tương ứng.

Local cap đầu ra **512 token** để tránh sinh vô hạn; cùng cap trong mọi run local được so sánh. Cloud không đặt cap này. Các lệnh send trong eval chỉ bị chặn ở bước thực thi, còn tool call/args vẫn được chấm nguyên vẹn. Không có tin Telegram phát sinh từ eval.

| Version             | Model                 | Case | Routing | Arguments | Multi-turn | Run                                                                                    |
| ------------------- | --------------------- | ---: | ------: | --------: | ---------: | -------------------------------------------------------------------------------------- |
| v3 (tham chiếu CP2) | gemini-3.5-flash-lite |  90% |    100% |       90% |       100% | [JSON](../../starter_v0/runs/v3_B_base_gemini_20261110T183254561353.json)              |
| v3-qwen3b           | qwen2.5:3b            |  65% |     75% |       65% |     66,67% | [JSON](../../starter_v0/runs/v3-qwen3b_B_base_ollama_20261110T193943848724.json)       |
| v3-llama1b          | llama3.2:1b           |  15% |     45% |       15% |         0% | [JSON](../../starter_v0/runs/v3-llama1b_B_base_ollama_20261110T193800881397.json)      |
| v4-local            | qwen2.5:3b            |  45% |     65% |       45% |        50% | [JSON](../../starter_v0/runs/v4-local_B_base_ollama_20261110T194139636388.json)        |
| v5-local            | qwen2.5:3b            |  40% |     50% |       40% |        50% | [JSON](../../starter_v0/runs/v5-local_B_base_ollama_20261110T194346480602.json)        |
| v5-local-gemini     | gemini-3.5-flash-lite |  85% |     95% |       85% |     83,33% | [JSON](../../starter_v0/runs/v5-local-gemini_B_base_gemini_20261110T194607625892.json) |

**Giả thuyết và kết quả:**

1. **v4-local:** chỉ rút prompt từ 399 xuống 220 từ; giữ tools v3. Giả thuyết giảm tải chỉ dẫn cho model nhỏ bị bác bỏ trong run này: Qwen giảm **65% → 45%**.
2. **v5-local:** giữ prompt v4, chỉ rút phần mô tả tool/arguments từ 865 xuống 371 từ; schema và 10 tên tool giữ nguyên. Giả thuyết giảm nhiễu tiếp tục không được ủng hộ: **45% → 40%**.
3. **Kiểm tra ngược:** cùng v5-local trên Gemini đạt **85%**, thấp hơn v3 **90%**. Không thay cấu hình cloud đang dùng bằng bản rút gọn này.

**Kết luận có bằng chứng:** trong các bản đã đo, giữ prompt/mô tả chi tiết của v3 tốt hơn hai bản rút gọn cho Qwen3B. Không thể mặc định prompt ngắn sẽ tốt hơn với model nhỏ. Qwen3B v3 đạt 65%, cao hơn Llama1B v3 15%; đây là so sánh hai model/family/quantization cụ thể, không phải thí nghiệm tách riêng ảnh hưởng số tham số. Mỗi bản mới đo một lần, chưa chứng minh độ ổn định thống kê.

**Lỗi model nhỏ:**

| Run        | Không gọi tool khi cần | Sai args quan sát được | Thiếu tool call | Finish do chạm cap |
| ---------- | ---------------------: | ---------------------: | --------------: | -----------------: |
| v3-qwen3b  |                      1 |                      2 |               4 |                  0 |
| v3-llama1b |                      6 |                      6 |              11 |                  3 |
| v4-local   |                      1 |                      4 |               6 |                  0 |
| v5-local   |                      2 |                      3 |               8 |                  0 |

Các nhóm lỗi có thể trùng nhau; không cộng các cột thành tổng case FAIL. Các run được chọn không có malformed-JSON args hoặc call lặp quan sát được; không bịa các loại lỗi không xuất hiện. Trước khi đặt cap, Llama đã sinh trên 13.000 token và context shift liên tục; lần đó bị dừng, không tính là full run hợp lệ. Qwen uncapped ban đầu đạt 65% và lần capped cũng 65%; giữ cả run cũ để truy vết, chọn capped cho bảng so sánh.

Bằng chứng: [CSV metric](../../starter_v0/analysis/bonus/local_metrics.csv), [case chi tiết](../../starter_v0/analysis/bonus/local_case_results.csv), [phân loại lỗi](../../starter_v0/analysis/bonus/local_failure_patterns.csv), [giả thuyết](../../starter_v0/analysis/bonus/local_experiments.json), [sự cố runtime](../../starter_v0/analysis/bonus/llama_unbounded_attempt.json), [snapshot/lệnh tái lập](../../starter_v0/artifacts/versions/README.md), [version log](../../starter_v0/artifacts/version_log.csv).

## 5. Khó khăn và cách xử lý

- Ban đầu lệnh chọn OpenRouter trong khi chỉ có key Gemini; đã chuyển provider sang Gemini.
- Các lượt chạy đầu gặp lỗi quota 429, lỗi DNS và lỗi import ở bản sửa trung gian. Các run lỗi được giữ để truy vết trong [nhật ký CP1](../../starter_v0/analysis/cp1_checks.md), không dùng làm số đo hợp lệ.
- Đã chạy lại v0 và đủ v1–v3 chỉ dùng 3.5. Có lỗi 503 tạm thời trong quá trình chạy; cơ chế chờ 60 giây và retry đã phục hồi, các JSON cuối cùng đều có 0 lỗi provider.
- Eval chủ yếu đo lựa chọn tool và arguments. Một case PASS không chứng minh dữ liệu bên ngoài được truy xuất thành công; cần xem `tool_results` và kiểm tra cấu hình dịch vụ riêng.

## 6. Tổng hợp đóng góp và phân công

Bản nộp dùng mã và minh chứng main của nhóm trưởng. Chia năm phần có khối lượng dự kiến tương đương (khoảng 20% mỗi người); đây là phân công phụ trách, không xác nhận đóng góp đã hoàn thành.

| Thành viên           | MSSV        | Phụ trách                                                                               | Kiểm tra chéo |
| -------------------- | ----------- | --------------------------------------------------------------------------------------- | ------------- |
| Phạm Quang Tuấn      | 2A202603824 | Nhóm trưởng, provider và đóng gói; Cấu hình, log provider và checklist bản nộp          | Tuấn Đức      |
| Trần Phạm Minh Sơn   | 2A202603802 | Tool và kiểm thử; Tool contract, kết quả test và log API                                | Cường         |
| Huỳnh Văn Cường      | 2A202603866 | Prompt và đánh giá; Bảng metric, phân tích lỗi và eval nhóm                             | Sơn           |
| Nguyễn Phan Tuấn Đức | 2A202603818 | UI và Telegram; Hướng dẫn demo, transcript và receipt Telegram                          | Thanh         |
| Đỗ Minh Thanh        | 2A202603793 | Local model và tài liệu minh chứng; Bảng local metrics, hướng dẫn và chỉ mục minh chứng | Tuấn          |

Chi tiết ba đầu việc mỗi người và liên kết báo cáo cá nhân tại [TEAM.md](../../TEAM.md). Báo cáo nhập từ nhánh thành viên giữ nội dung lịch sử có ghi nguồn; không dùng để thay số đo main. Có Codex hỗ trợ, thành viên cần tự rà soát và giải thích phần phụ trách. Minh chứng dùng thử ngoài nhóm vẫn là MOCK.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Prompt:** v1 cải thiện hỏi lại/xác nhận; v2 giúp routing đạt 100%. **Tool declaration:** v3 cải thiện convention arguments, đặc biệt query và response_type.
- V3 đạt 90%, chưa phải 100%. Hai lỗi còn lại là query không khớp chính xác và loại câu hỏi xác nhận; cần phân tích cả ý nghĩa hành vi lẫn kết quả chấm tự động.
- Chỉ có một run cho mỗi version trên bộ base; chưa đánh giá độ ổn định qua nhiều lần chạy; suite nhóm mới có một run 10 case, không đủ để khẳng định tổng quát. Quy tắc query tối giản có thể ảnh hưởng độ phủ tìm kiếm, cần kiểm tra chất lượng nguồn thực tế.
- CP3/CP4 đã hoàn thành. Bước tiếp theo: nhờ một người ngoài nhóm kiểm tra link/mã truy cập, kiểm chứng dịch vụ social_search, và hoàn thiện phần cá nhân sau theo yêu cầu.
- Đã có đầy đủ flow local và Telegram tương ứng ở B5/B7. Không tự gán điểm; người chấm đối chiếu rubric và bằng chứng thật.

## 8. Tài liệu tham khảo

- [Đề bài và hướng dẫn thực hành](../../README.md).
- [Checkpoints](../../CHECKPOINTS.md), [rubric](../../RUBRIC.md), [quy định](../../RULES.md).
- [Hướng dẫn cấu hình tool](../../docs/TOOL-SETUP.md).
- [Hướng dẫn chạy và giới hạn tốc độ Gemini](../../starter_v0/README.md).
- [Version log](../../starter_v0/artifacts/version_log.csv), [nhật ký kiểm tra CP1](../../starter_v0/analysis/cp1_checks.md).

- [Hướng dẫn Telegram](../../docs/TELEGRAM-QUICKSTART.md), [local models và cleanup](../../docs/LOCAL-MODELS.md).

- [Hướng dẫn demo public](../../docs/DEMO.md), [kiểm tra model local](../../starter_v0/analysis/local_models_checks.md).

- [Log pytest cuối](../../starter_v0/analysis/bonus/pytest-final.txt), [chỉ mục minh chứng bonus](../../starter_v0/analysis/bonus/README.md).

- [Checklist nghiệm thu kỹ thuật README](../../starter_v0/analysis/acceptance_check.json). Phần cá nhân, commit/push và LMS chưa được đánh dấu hoàn tất.

**Lưu ý nghiệm thu hồ sơ:** phần cá nhân/đóng góp để làm sau theo yêu cầu; chưa chốt commit, push và nộp LMS. Chưa có bằng chứng người ngoài nhóm trực tiếp dùng thử. Báo cáo hiện tại hoàn thiện sau mốc 16:30, không ghi nhận như đã hoàn thành Phần A đúng mốc này.

## Cập nhật social_search sau đăng ký API

Đã gọi trực tiếp social_search với query OpenAI, search_type Latest, limit 2 sau khi đăng ký Twitter API45: trả về hai bài có URL, không còn lỗi 403 trong lượt kiểm tra này. [Minh chứng API thật](../../starter_v0/analysis/social_search_after_subscription.json). Lỗi 403 trước đó giữ lại như lịch sử; không còn là việc đang chờ xử lý. Đây là kiểm tra trực tiếp tool, không phải chạy lại toàn bộ eval hoặc flow agent.
