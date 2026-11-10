# Báo cáo cá nhân — Nguyễn Phan Tuấn Đức

## 1. Thông tin thành viên

- Họ tên: Nguyễn Phan Tuấn Đức
- MSSV: 2A202603818
- GitHub: `tundut`

## 2. Phần việc phụ trách

Phân công cập nhật theo TEAM.md cho bản main hiện tại:

- Rà soát UI Streamlit, hướng dẫn truy cập và transcript CLI/UI.
- Kiểm tra flow duyệt Telegram, receipt và chống gửi khi chưa xác nhận.

Đầu ra: Hướng dẫn demo, transcript và receipt Telegram. Người kiểm tra chéo: Thanh. Đây là trách nhiệm được giao, không phải xác nhận các đầu việc đã hoàn tất.

## 3. Đóng góp cụ thể

> Báo cáo nguồn từ nhánh thành viên: nội dung lịch sử dưới đây được giữ để đối chiếu, không xác nhận rằng mã/run của nhánh đó đã được tích hợp vào main. Phân công hiện hành nằm ở mục 2; số đo bản nộp theo group report.

- Cập nhật [system_prompt.md](../../starter_v0/artifacts/system_prompt.md) với quy tắc scope, routing, clarification, giữ nguyên query và yêu cầu xác nhận trước khi gửi.
- Cập nhật [tools.yaml](../../starter_v0/artifacts/tools.yaml) để mô tả rõ tham số và điều kiện sử dụng của tools.
- Thêm [source_dedupe](../../starter_v0/tools/source_dedupe/) và đăng ký trong [tools/**init**.py](../../starter_v0/tools/__init__.py).
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
