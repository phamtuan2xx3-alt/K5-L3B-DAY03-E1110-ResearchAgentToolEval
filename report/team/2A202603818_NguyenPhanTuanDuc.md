# Báo cáo cá nhân — Nguyễn Phan Tuấn Đức

## 1. Thông tin thành viên

- Họ tên: Nguyễn Phan Tuấn Đức
- MSSV: 2A202603818
- GitHub: `tundut`

## 2. Phần việc phụ trách

- Tối ưu system prompt/tool declaration và đối chiếu các run trên nhánh cá nhân.
- Xây dựng source_dedupe, unit test và test boundary gửi Telegram.
- Tích hợp UI Streamlit, chạy eval nhóm, thu transcript và kiểm tra Telegram; hỗ trợ rà soát demo nhóm.

Người kiểm tra chéo: Thanh. Phạm vi theo báo cáo cá nhân; kết quả và minh chứng giữ đúng nhánh nguồn. Phần chạy model local của nhóm do Phạm Quang Tuấn thực hiện trên main.

## 3. Đóng góp cụ thể


- Cập nhật [system_prompt.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/artifacts/system_prompt.md) với quy tắc scope, routing, clarification, giữ nguyên query và yêu cầu xác nhận trước khi gửi.
- Cập nhật [tools.yaml](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/artifacts/tools.yaml) để mô tả rõ tham số và điều kiện sử dụng của tools.
- Thêm [source_dedupe](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/starter_v0/tools/source_dedupe) và đăng ký trong [tools/**init**.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/tools/__init__.py).
- Bổ sung 3 test cho `source_dedupe` và hoàn thiện các test trong [test_tools_todo.py](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/tests/test_tools_todo.py).
- Chạy toàn suite đạt `84 passed, 0 failed, 0 skipped`.
- Kiểm thử Telegram với hai boundary: `confirmed=false` trả `need_confirmation`; `confirmed=true` gửi thành công và trả `status: sent`.
- Chạy eval group đạt `8/10` và tạo transcript chứng minh luồng hỏi xác nhận rồi gửi Telegram.

## 4. Bằng chứng

**Nguồn minh chứng cá nhân:** [nhánh tuanduc](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/), [báo cáo gốc](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/report/team/2A202603818_NguyenPhanTuanDuc.md). Các URL bên dưới trỏ tới nhánh cá nhân; số liệu ở đó không thay thế kết quả main trong báo cáo nhóm.

- [system_prompt.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/artifacts/system_prompt.md)
- [tools.yaml](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/artifacts/tools.yaml)
- [source_dedupe tool](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/starter_v0/tools/source_dedupe)
- [unit tests](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/tests/test_tools_todo.py)
- [version log](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/artifacts/version_log.csv)
- [group eval run](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/runs/v3_B_group_gemini_20261110T191929498440.json)
- [Telegram transcript](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/transcripts/v3_gemini_20261110T233455241423.transcript.json)
- [Ollama run](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/tuanduc/starter_v0/runs/v3-llama3b_B_base_ollama_20261110T194845711229.json)

AI/công cụ đã dùng và cách tự kiểm tra:

- Dùng Copilot/AI để hỗ trợ đọc cấu trúc project, đề xuất test và rà soát lỗi.
- Tự kiểm tra bằng `pytest`, contract tests, fake HTTP cho các API tool, chạy eval JSON và kiểm tra transcript.
- Không đưa token Telegram vào source code; file `.env` được giữ ngoài Git.


Minh chứng theo nhánh: [artifacts](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/starter_v0/artifacts), [tools](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/starter_v0/tools), [tests](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/starter_v0/tests), [data](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/starter_v0/data), [runs](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/starter_v0/runs), [transcripts](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/starter_v0/transcripts).

## 5. Tự đánh giá

Em đã hoàn thành phần tool mới, test challenge, tích hợp Telegram và thu thập evidence chính. Kết quả hiện tại đạt `84 passed` và eval group `8/10`. Hạn chế còn lại là bonus local model chưa đủ hai model/hai vòng tối ưu theo rubric và report nhóm cần được hoàn thiện đồng bộ với evidence.
