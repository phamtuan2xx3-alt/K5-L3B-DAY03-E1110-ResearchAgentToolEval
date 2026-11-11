# Báo cáo cá nhân — Đỗ Minh Thanh — 2A202603793

## 1. Thông tin thành viên

- Họ tên: Đỗ Minh Thanh
- MSSV: 2A202603793
- Email: thd050810@gmail.com
- GitHub: [thd050810](https://github.com/thd050810)
- Nhóm: E1110
- Lớp: L3B

## 2. Phần việc phụ trách

Phụ trách toàn bộ quy trình bài lab từ CP1 đến CP5: thiết lập provider và API tool, đo baseline, tối ưu prompt và tool declaration, bổ sung tool mới cùng unit test, xây dựng eval nhóm, tổ chức chạy thử, hoàn thiện UI và tổng hợp báo cáo. Quá trình thực hiện sử dụng Codex/ChatGPT để hỗ trợ giải thích, đề xuất, triển khai và kiểm tra các sản phẩm theo yêu cầu.

## 3. Đóng góp cụ thể

| Phần | Nội dung phụ trách | Kết quả |
|---|---|---|
| CP1 — Setup và baseline | Cấu hình Gemini và API tool; thực hiện baseline v0; tổ chức ghi version log và phân tích các case FAIL | Run v0 đo đủ 20 case, không lỗi provider; 13/20 PASS; bảng B2 có 7 lỗi |
| CP2 — Tối ưu v1–v5 | Điều chỉnh quy tắc hỏi lại/xác nhận, quy ước query/topic/timeframe và handle tài khoản; so sánh các phiên bản | v0–v3 đạt 0.65, 0.75, 0.85, 0.90; đối chứng 14 tool đạt 0.85, v4 đạt 0.95, v5 đạt 0.90; mỗi version có hash và run JSON |
| CP3 — Tool mới | Bổ sung deduplicate_sources, check_citations, compare_papers, rank_sources; đăng ký registry/schema và TOOL.md | Có 4 tool mới và 46 test mới đều PASS |
| CP4 — Eval nhóm | Xây dựng 5 case single turn và 5 case multi turn; kiểm tra routing tới cả 4 tool mới và hành vi theo context | Run group đo đủ 10 case, đạt 10/10 PASS, không lỗi provider |
| CP5 — UI và chat | Triển khai Streamlit, tạo link dùng thử, tổ chức phiên CLI và UI với Gemini thật; hoàn thiện báo cáo nhóm | Có 5 lượt CLI nghiên cứu, 1 lượt UI kiểm tra và 2 lượt CLI xác nhận/gửi Telegram thật; transcript JSON, receipt và báo cáo có liên kết bằng chứng |
| Kiểm tra và sửa lỗi | Kiểm tra URL/citation, bảo toàn tool results khi provider lỗi, tách phiên chat, che credential và chặn send trong UI công khai | Toàn bộ suite đạt 147 passed, 12 skipped, 0 failed |

## 4. Bằng chứng

### File và kết quả thực hiện

| Nội dung | File bằng chứng |
|---|---|
| Prompt và tool declaration | [system_prompt.md](../../starter_v0/artifacts/system_prompt.md), [tools.yaml](../../starter_v0/artifacts/tools.yaml) |
| Lịch sử giả thuyết, metric và hash | [version_log.csv](../../starter_v0/artifacts/version_log.csv) |
| Baseline v0 — 13/20 | [Run v0](../../starter_v0/runs/v0_B_base_gemini_20261110T183632505620.json) |
| v1 — 15/20 | [Run v1](../../starter_v0/runs/v1_B_base_gemini_20261110T192455812815.json) |
| v2 — 17/20 | [Run v2](../../starter_v0/runs/v2_B_base_gemini_20261110T192913379384.json) |
| v3 — 18/20 | [Run v3](../../starter_v0/runs/v3_B_base_gemini_20261110T193212164707.json) |
| Đối chứng 14 tool — 17/20 | [Run v3-cp3](../../starter_v0/runs/v3-cp3_B_base_gemini_20261111T010319101559.json) |
| v4 — 19/20 | [Run v4](../../starter_v0/runs/v4_B_base_gemini_20261111T010552889357.json) |
| v5 — 18/20 | [Run v5](../../starter_v0/runs/v5_B_base_gemini_20261111T010040350391.json) |
| Hoàn thiện C2 và regression test send | [c2_verification.json](../../starter_v0/analysis/c2_verification.json), [send/tool.py](../../starter_v0/tools/send/tool.py) |
| Tool loại nguồn trùng | [deduplicate_sources/tool.py](../../starter_v0/tools/deduplicate_sources/tool.py), [TOOL.md](../../starter_v0/tools/deduplicate_sources/TOOL.md) |
| Tool kiểm tra mã trích dẫn | [check_citations/tool.py](../../starter_v0/tools/check_citations/tool.py), [TOOL.md](../../starter_v0/tools/check_citations/TOOL.md) |
| Tool so sánh paper | [compare_papers/tool.py](../../starter_v0/tools/compare_papers/tool.py), [TOOL.md](../../starter_v0/tools/compare_papers/TOOL.md) |
| Tool xếp hạng nguồn | [rank_sources/tool.py](../../starter_v0/tools/rank_sources/tool.py), [TOOL.md](../../starter_v0/tools/rank_sources/TOOL.md) |
| Unit test và kiểm tra phiên chat | [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py), [test_chat_session.py](../../starter_v0/tests/test_chat_session.py) |
| Bộ eval nhóm và run 10/10 | [eval_group.json](../../starter_v0/data/eval_group.json), [Run group](../../starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| UI và backend phiên chat | [app.py](../../starter_v0/app.py), [web_chat.py](../../starter_v0/web_chat.py) |
| Chat CLI với Gemini thật | [CLI transcript](../../starter_v0/transcripts/v3_gemini_20261111T000642591554.transcript.json) |
| Phiên UI với Gemini thật | [UI transcript](../../starter_v0/transcripts/ui_v3_gemini_20261111T001107859594_68dcd91e.transcript.json) |
| Kiểm tra UI, public link và toàn suite | [cp5_verification.json](../../starter_v0/analysis/cp5_verification.json) |
| Telegram gửi thật sau xác nhận | [Telegram transcript](../../starter_v0/transcripts/v5_gemini_20261111T011317669763.transcript.json), [receipt message_id=5](../../starter_v0/analysis/telegram_delivery.json) |
| Báo cáo tổng hợp | [group_report.md](group_report.md) |

### AI/công cụ đã dùng và cách kiểm tra kết quả

- Codex/ChatGPT: giải thích cấu trúc code và hướng dẫn lab; hỗ trợ phân tích log, đề xuất và sửa prompt/tool declaration; hỗ trợ viết bốn tool, unit test và eval nhóm; chạy các lệnh kiểm tra và thu thập bằng chứng; thiết kế UI, xử lý phiên chat và định dạng báo cáo Markdown.
- Gemini `gemini-3.5-flash-lite`: model được dùng trong preflight, base eval, group eval và các phiên chat thật.
- pytest và Streamlit AppTest: kiểm tra contract, xử lý dữ liệu tool, phiên chat độc lập, redaction, allowlist và giao diện.
- Streamlit và Cloudflare Tunnel: chạy UI local, tạo link dùng thử và kiểm tra HTTP/health.
- Kết quả được đối chiếu bằng run JSON, transcript, số test thực tế và hash artifacts. Mỗi run dùng làm bằng chứng đều được kiểm tra số case đã đo và lỗi provider; số liệu báo cáo lấy từ log đã lưu.

## 5. Tự đánh giá

Sản phẩm đã có bằng chứng cho chu trình baseline → đặt giả thuyết → sửa → đo lại. Case accuracy base tăng từ 65% lên 90%, tương đương 25 điểm phần trăm. Kết quả routing không tăng đều: v2 đạt 100% nhưng v3 còn 95%; vì vậy cần đối chiếu từng loại lỗi thay vì chỉ nhìn điểm tổng.

Bốn tool mới có test cho đầu vào hợp lệ, input xấu và nhánh trả lỗi. Bộ eval nhóm đạt 10/10 trên dữ liệu đã xây dựng, nhưng chỉ chấm tool calls và subset arguments; chất lượng nội dung và tính đúng của nguồn vẫn cần được kiểm tra riêng. Toàn suite còn 12 test stub bị skip, chưa đạt nhánh 0 skipped; regression test cho lỗi confirmed dạng chuỗi/số trong tool send có sẵn đáp ứng phương án thay thế của test challenge.

v3 còn hai case FAIL: câu hỏi thiếu nội dung gửi có khác biệt giữa kiểu hỏi text và đáp án yes/no; yêu cầu nhiều nguồn còn thiếu social_search. V4 đã bổ sung routing và cho phép nhiều tool. V5 hoàn thiện mô tả và conventions, còn lỗi mở rộng query ở R03 và kiểu câu hỏi ở R12; cần thử ví dụ few-shot cho query và review thủ công đáp án xác nhận khi nội dung chưa có.

UI đã được kiểm tra bằng AppTest và một phiên Gemini thật, link public đã có kiểm tra HTTP/health. Chưa có kiểm thử thao tác trực tiếp bằng Chrome; link Quick Tunnel cần hai tiến trình tiếp tục chạy. Phiên Telegram v5 đã hỏi xác nhận rồi gửi thật một tin vào nhóm riêng tư Test_AILabDay3, message_id=5. User đã chọn đích có chat.type=group; đây không phải private channel theo chữ trong rubric. Chưa thực hiện Small Local Model Challenge.
