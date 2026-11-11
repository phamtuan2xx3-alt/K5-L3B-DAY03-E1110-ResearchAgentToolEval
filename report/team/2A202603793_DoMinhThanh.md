# Báo cáo cá nhân — Đỗ Minh Thanh — 2A202603793

## 1. Thông tin thành viên

- Họ tên: Đỗ Minh Thanh
- MSSV: 2A202603793
- Email: thd050810@gmail.com
- GitHub: [thd050810](https://github.com/thd050810)
- Nhóm: E1110
- Lớp: L3B

## 2. Phần việc phụ trách

- Thiết lập Gemini/API tool, baseline và tối ưu v0–v5; đối chiếu hash, đối chứng 14 tool và phân tích lỗi trên nhánh cá nhân.
- Xây dựng deduplicate_sources, check_citations, compare_papers, rank_sources và unit test; bộ eval nhóm 10 case.
- Triển khai UI/chat session, kiểm tra citation, che credential và boundary gửi; thu transcript/receipt Telegram và tổng hợp báo cáo của nhánh.

Người kiểm tra chéo: Tuấn. Phạm vi theo báo cáo cá nhân; kết quả và minh chứng giữ đúng nhánh nguồn. Phần chạy model local của nhóm do Phạm Quang Tuấn thực hiện trên main.

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

**Nguồn minh chứng cá nhân:** [nhánh DoMinhThanh](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/DoMinhThanh/), [báo cáo gốc](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/report/team/2A202603793_DoMinhThanh.md). Các URL bên dưới trỏ tới nhánh cá nhân; số liệu ở đó không thay thế kết quả main trong báo cáo nhóm.

### File và kết quả thực hiện

| Nội dung | File bằng chứng |
|---|---|
| Prompt và tool declaration | [system_prompt.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/artifacts/system_prompt.md), [tools.yaml](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/artifacts/tools.yaml) |
| Lịch sử giả thuyết, metric và hash | [version_log.csv](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/artifacts/version_log.csv) |
| Baseline v0 — 13/20 | [Run v0](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/runs/v0_B_base_gemini_20261110T183632505620.json) |
| v1 — 15/20 | [Run v1](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/runs/v1_B_base_gemini_20261110T192455812815.json) |
| v2 — 17/20 | [Run v2](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/runs/v2_B_base_gemini_20261110T192913379384.json) |
| v3 — 18/20 | [Run v3](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/runs/v3_B_base_gemini_20261110T193212164707.json) |
| Đối chứng 14 tool — 17/20 | [Run v3-cp3](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/runs/v3-cp3_B_base_gemini_20261111T010319101559.json) |
| v4 — 19/20 | [Run v4](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/runs/v4_B_base_gemini_20261111T010552889357.json) |
| v5 — 18/20 | [Run v5](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/runs/v5_B_base_gemini_20261111T010040350391.json) |
| Hoàn thiện C2 và regression test send | [c2_verification.json](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/analysis/c2_verification.json), [send/tool.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/send/tool.py) |
| Tool loại nguồn trùng | [deduplicate_sources/tool.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/deduplicate_sources/tool.py), [TOOL.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/deduplicate_sources/TOOL.md) |
| Tool kiểm tra mã trích dẫn | [check_citations/tool.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/check_citations/tool.py), [TOOL.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/check_citations/TOOL.md) |
| Tool so sánh paper | [compare_papers/tool.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/compare_papers/tool.py), [TOOL.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/compare_papers/TOOL.md) |
| Tool xếp hạng nguồn | [rank_sources/tool.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/rank_sources/tool.py), [TOOL.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tools/rank_sources/TOOL.md) |
| Unit test và kiểm tra phiên chat | [test_tools_todo.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tests/test_tools_todo.py), [test_chat_session.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/tests/test_chat_session.py) |
| Bộ eval nhóm và run 10/10 | [eval_group.json](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/data/eval_group.json), [Run group](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/runs/v5_B_group_gemini_20261111T010751051163.json) |
| UI và backend phiên chat | [app.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/app.py), [web_chat.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/web_chat.py) |
| Chat CLI với Gemini thật | [CLI transcript](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/transcripts/v3_gemini_20261111T000642591554.transcript.json) |
| Phiên UI với Gemini thật | [UI transcript](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/transcripts/ui_v3_gemini_20261111T001107859594_68dcd91e.transcript.json) |
| Kiểm tra UI, public link và toàn suite | [cp5_verification.json](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/analysis/cp5_verification.json) |
| Telegram gửi thật sau xác nhận | [Telegram transcript](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/transcripts/v5_gemini_20261111T011317669763.transcript.json), [receipt message_id=5](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/starter_v0/analysis/telegram_delivery.json) |
| Báo cáo tổng hợp | [group_report.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/DoMinhThanh/report/team/group_report.md) |

### AI/công cụ đã dùng và cách kiểm tra kết quả

- Codex/ChatGPT: giải thích cấu trúc code và hướng dẫn lab; hỗ trợ phân tích log, đề xuất và sửa prompt/tool declaration; hỗ trợ viết bốn tool, unit test và eval nhóm; chạy các lệnh kiểm tra và thu thập bằng chứng; thiết kế UI, xử lý phiên chat và định dạng báo cáo Markdown.
- Gemini `gemini-3.5-flash-lite`: model được dùng trong preflight, base eval, group eval và các phiên chat thật.
- pytest và Streamlit AppTest: kiểm tra contract, xử lý dữ liệu tool, phiên chat độc lập, redaction, allowlist và giao diện.
- Streamlit và Cloudflare Tunnel: chạy UI local, tạo link dùng thử và kiểm tra HTTP/health.
- Kết quả được đối chiếu bằng run JSON, transcript, số test thực tế và hash artifacts. Mỗi run dùng làm bằng chứng đều được kiểm tra số case đã đo và lỗi provider; số liệu báo cáo lấy từ log đã lưu.


Minh chứng theo nhánh: [artifacts](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/DoMinhThanh/starter_v0/artifacts), [tools](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/DoMinhThanh/starter_v0/tools), [tests](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/DoMinhThanh/starter_v0/tests), [data](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/DoMinhThanh/starter_v0/data), [runs](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/DoMinhThanh/starter_v0/runs), [transcripts](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/DoMinhThanh/starter_v0/transcripts).

## 5. Tự đánh giá

Sản phẩm đã có bằng chứng cho chu trình baseline → đặt giả thuyết → sửa → đo lại. Case accuracy base tăng từ 65% lên 90%, tương đương 25 điểm phần trăm. Kết quả routing không tăng đều: v2 đạt 100% nhưng v3 còn 95%; vì vậy cần đối chiếu từng loại lỗi thay vì chỉ nhìn điểm tổng.

Bốn tool mới có test cho đầu vào hợp lệ, input xấu và nhánh trả lỗi. Bộ eval nhóm đạt 10/10 trên dữ liệu đã xây dựng, nhưng chỉ chấm tool calls và subset arguments; chất lượng nội dung và tính đúng của nguồn vẫn cần được kiểm tra riêng. Toàn suite còn 12 test stub bị skip, chưa đạt nhánh 0 skipped; regression test cho lỗi confirmed dạng chuỗi/số trong tool send có sẵn đáp ứng phương án thay thế của test challenge.

v3 còn hai case FAIL: câu hỏi thiếu nội dung gửi có khác biệt giữa kiểu hỏi text và đáp án yes/no; yêu cầu nhiều nguồn còn thiếu social_search. V4 đã bổ sung routing và cho phép nhiều tool. V5 hoàn thiện mô tả và conventions, còn lỗi mở rộng query ở R03 và kiểu câu hỏi ở R12; cần thử ví dụ few-shot cho query và review thủ công đáp án xác nhận khi nội dung chưa có.

UI đã được kiểm tra bằng AppTest và một phiên Gemini thật, link public đã có kiểm tra HTTP/health. Chưa có kiểm thử thao tác trực tiếp bằng Chrome; link Quick Tunnel cần hai tiến trình tiếp tục chạy. Phiên Telegram v5 đã hỏi xác nhận rồi gửi thật một tin vào nhóm riêng tư Test_AILabDay3, message_id=5. User đã chọn đích có chat.type=group; đây không phải private channel theo chữ trong rubric. Chưa thực hiện Small Local Model Challenge.
