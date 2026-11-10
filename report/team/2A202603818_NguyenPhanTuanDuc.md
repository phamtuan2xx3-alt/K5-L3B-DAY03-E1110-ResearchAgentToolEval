# Báo cáo cá nhân — Nguyễn Phan Tuấn Đức

## 1. Thông tin thành viên

- Họ tên: Nguyễn Phan Tuấn Đức
- MSSV: 2A202603818
- Email: 26ai.ducnpt@vinuni.edu.vn
- GitHub: `tundut`

## 2. Phần việc phụ trách

- Cải thiện system prompt và tool declarations để agent định tuyến đúng tool, hỏi lại khi thiếu thông tin và không gửi Telegram nếu chưa được xác nhận.
- Thêm tool `source_dedupe` để loại bỏ nguồn nghiên cứu trùng theo URL.
- Viết unit test cho các tool, bao gồm test happy path, input không hợp lệ và boundary của Telegram.
- Tích hợp/chạy UI Streamlit, provider Ollama và kiểm thử Telegram Bot API.
- Chạy các vòng eval v0–v3, eval group và thu thập transcript làm evidence.

## 3. Đóng góp cụ thể

- Cập nhật [system_prompt.md](../../starter_v0/artifacts/system_prompt.md) với quy tắc scope, routing, clarification, giữ nguyên query và yêu cầu xác nhận trước khi gửi.
- Cập nhật [tools.yaml](../../starter_v0/artifacts/tools.yaml) để mô tả rõ tham số và điều kiện sử dụng của tools.
- Thêm [source_dedupe](../../starter_v0/tools/source_dedupe/) và đăng ký trong [tools/__init__.py](../../starter_v0/tools/__init__.py).
- Bổ sung 3 test cho `source_dedupe` và hoàn thiện các test trong [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py).
- Chạy toàn suite đạt `84 passed, 0 failed, 0 skipped`.
- Kiểm thử Telegram với hai boundary: `confirmed=false` trả `need_confirmation`; `confirmed=true` gửi thành công và trả `status: sent`.
- Chạy eval group đạt `8/10` và tạo transcript chứng minh luồng hỏi xác nhận rồi gửi Telegram.

## 4. Bằng chứng

- [system_prompt.md](../../starter_v0/artifacts/system_prompt.md)
- [tools.yaml](../../starter_v0/artifacts/tools.yaml)
- [source_dedupe tool](../../starter_v0/tools/source_dedupe/)
- [unit tests](../../starter_v0/tests/test_tools_todo.py)
- [version log](../../starter_v0/artifacts/version_log.csv)
- [group eval run](../../starter_v0/runs/v3_B_group_gemini_20261110T191929498440.json)
- [Telegram transcript](../../starter_v0/transcripts/v3_gemini_20261110T233455241423.transcript.json)
- [Ollama run](../../starter_v0/runs/v3-llama3b_B_base_ollama_20261110T194845711229.json)

AI/công cụ đã dùng và cách tự kiểm tra:

- Dùng Copilot/AI để hỗ trợ đọc cấu trúc project, đề xuất test và rà soát lỗi.
- Tự kiểm tra bằng `pytest`, contract tests, fake HTTP cho các API tool, chạy eval JSON và kiểm tra transcript.
- Không đưa token Telegram vào source code; file `.env` được giữ ngoài Git.

## 5. Tự đánh giá

Em đã hoàn thành phần tool mới, test challenge, tích hợp Telegram và thu thập evidence chính. Kết quả hiện tại đạt `84 passed` và eval group `8/10`. Hạn chế còn lại là bonus local model chưa đủ hai model/hai vòng tối ưu theo rubric và report nhóm cần được hoàn thiện đồng bộ với evidence.
