# Báo cáo cá nhân — Phạm Quang Tuấn — 2A202603824

## 1. Thông tin thành viên

- Họ tên: Phạm Quang Tuấn.
- MSSV: 2A202603824.
- Nhóm: E1110; lớp: L3B.
- Vai trò: Nhóm trưởng.

## 2. Phần việc phụ trách

- Điều phối, tích hợp main, cấu hình Gemini 3.5 Flash Lite và queue/retry; kiểm tra API social_search.
- Thực hiện baseline, tối ưu prompt/tool, source_audit và kiểm thử trên main; tổng hợp kết quả nhóm.
- Trực tiếp tải và chạy hai model local Qwen2.5:3B, Llama3.2:1B; chạy base eval, hai vòng tối ưu local và kiểm tra ngược Gemini.
- Phụ trách minh chứng bonus local và private channel Telegram của main, rà soát bản nộp.

Người kiểm tra chéo: Tuấn Đức. Phạm vi theo báo cáo cá nhân; kết quả và minh chứng giữ đúng nhánh nguồn. Phần chạy model local của nhóm do Phạm Quang Tuấn thực hiện trên main.

## 3. Công việc và kết quả

Các thay đổi được thực hiện trong phiên làm việc có Codex hỗ trợ theo yêu cầu của nhóm trưởng. Không mô tả là toàn bộ mã do cá nhân tự viết; thành viên cần tự kiểm tra và giải thích phần phụ trách khi nghiệm thu.

- Giữ baseline v0; đo v0–v3 trên Gemini đạt lần lượt 65%, 70%, 75%, 90%. V3 còn hai case FAIL; các run được chọn đủ 20 case, không lỗi provider.
- Bản main có tool source_audit và test; eval nhóm đủ 5 single và 5 multi, đạt 10/10 về routing/arguments.
- Có UI, transcript CLI ít nhất ba lượt và flow xác nhận nội dung trước khi gửi Telegram. Gửi thật có receipt message_id 4.
- Chạy qwen2.5:3b và llama3.2:1b, hai vòng tối ưu và kiểm tra ngược trên Gemini. Rút gọn prompt/tool làm Qwen giảm chất lượng; báo cáo giữ nguyên kết quả thực tế.
- Kiểm tra social_search bằng API thật: HTTP 403, message “You are not subscribed to this API.” Key RapidAPI chưa có subscription Twitter API45. Đã sửa thông báo lỗi hướng dẫn xử lý, chưa tuyên bố truy xuất social thành công.
- Test sau sửa: 105 passed, 14 skipped, 0 failed. Test mock không thay thế kiểm tra quyền truy cập thật.

## 4. Bằng chứng

- [Báo cáo nhóm](group_report.md), [phân công](../../TEAM.md).
- [CP2](../../starter_v0/analysis/cp2_experiments.json), [version log](../../starter_v0/artifacts/version_log.csv).
- [Eval nhóm](../../starter_v0/runs/cp3_B_group_gemini_20261110T185301567314.json).
- [Transcript CLI](../../starter_v0/transcripts/cp5-cli_gemini_20261110T195651906996.transcript.json).
- [Minh chứng bonus](../../starter_v0/analysis/bonus/README.md), [Telegram](../../starter_v0/analysis/bonus/telegram_send_flow.json), [local metrics](../../starter_v0/analysis/bonus/local_metrics.csv).
- [API social thật](../../starter_v0/analysis/social_search_live_check.json), [test subscription](../../starter_v0/tests/test_social_search_access.py).
- Commit/PR: chưa chốt, thay đổi đang trong working tree main.

## 5. Tự đánh giá và phần còn lại

Subscription Twitter API45 đã được xử lý và social_search đã kiểm tra thành công; còn việc có người ngoài nhóm dùng thử và chốt commit/push/nộp bài. Chưa có bằng chứng Phần A hoàn thành trước 16:30. Thành viên tự bổ sung nhận xét trải nghiệm cá nhân sau khi rà soát; không tạo nhận xét cá nhân thay thành viên.

## Cập nhật social_search sau đăng ký API

Đã gọi trực tiếp social_search với query OpenAI, search_type Latest, limit 2 sau khi đăng ký Twitter API45: trả về hai bài có URL, không còn lỗi 403 trong lượt kiểm tra này. [Minh chứng API thật](../../starter_v0/analysis/social_search_after_subscription.json). Lỗi 403 trước đó giữ lại như lịch sử; không còn là việc đang chờ xử lý. Đây là kiểm tra trực tiếp tool, không phải chạy lại toàn bộ eval hoặc flow agent.
