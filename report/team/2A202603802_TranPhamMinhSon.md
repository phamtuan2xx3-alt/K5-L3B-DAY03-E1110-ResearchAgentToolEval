# Báo cáo cá nhân — TranPhamMinhSon-2A202603802

## 1. Thông tin thành viên

- Họ tên: Trần Phạm Minh Sơn
- MSSV: 2A202603802
- Vai trò: Core Agent Developer & Tool Engineer

## 2. Phần việc phụ trách

- Thiết lập môi trường ảo, kết nối và xử lý độ ổn định provider Google Gemini API (CP1).
- Chủ trì vòng lặp tối ưu hóa Prompt và Tool Declaration dựa trên bằng chứng thực nghiệm qua các phiên bản `v0` → `v1` → `v2` → `v3` (CP1 & CP2).
- Thiết kế, lập trình và kiểm thử Tool mới `github_search` (CP3).
- Xây dựng 6 test case (3 single-turn, 3 multi-turn) đo lường khả năng điều hướng tool mới và kiểm tra boundary bảo mật (CP4).

## 3. Đóng góp cụ thể

1. **CP1 & CP2 (Tối ưu Prompt & Tool Declaration):**
   - Phân tích 7 case thất bại ở `v0` (accuracy 65%), chỉ ra các chỉ dẫn sai lệch cố ý trong starter prompt.
   - `v1`: Xóa bỏ hướng dẫn đoán mò; thêm quy tắc bắt buộc gọi `clarify(response_type="text")` khi thiếu thông tin tài khoản/URL; cho phép gọi tool song song → tăng accuracy lên 75%.
   - `v2`: Xây dựng boundary xác nhận an toàn: bắt buộc gọi `clarify(response_type="yes_no")` trước khi thực hiện hành động gửi tin (`send`) → tăng accuracy lên 80%.
   - `v3`: Chuẩn hóa lại toàn bộ `tools.yaml`, quy ước rõ ràng tham số `query` chỉ chứa thực thể cốt lõi, không nhồi từ thời gian/tin tức → đưa accuracy nhảy vọt lên 95% (multi-turn đạt 100%).
2. **CP3 (Tool mới & Unit Test):**
   - Viết tool `github_search` (`tools/github_search/tool.py` + `TOOL.md`) cho phép tìm kiếm repository open-source trên GitHub.
   - Đăng ký đồng bộ trong `tools/__init__.py` và `artifacts/tools.yaml`.
   - Viết 3 unit test độc lập trong `tests/test_tools_todo.py` (happy path mock HTTP, bad input & failure path trả về error dict, không raise exception).
   - Đảm bảo toàn bộ test contract và unit test xanh (70 passed, 0 failed).
3. **CP4 (Group Eval Cases):**
   - Đóng góp 6 test cases trong `starter_v0/data/eval_group.json` (3 single-turn + 3 multi-turn), kiểm tra khả năng route tới tool mới `github_search` và xác nhận hành động gửi tin.
   - Chạy eval suite group đạt độ chính xác tuyệt đối 100% (6/6 passed, 0 provider error).

## 4. Bằng chứng

- **File đã chỉnh sửa/tạo mới:**
  - `starter_v0/artifacts/system_prompt.md`
  - `starter_v0/artifacts/tools.yaml`
  - `starter_v0/artifacts/version_log.csv` (ghi đủ 4 dòng `v0`–`v3` kèm hash và metric)
  - `starter_v0/tools/github_search/` (`tool.py`, `TOOL.md`)
  - `starter_v0/tests/test_tools_todo.py` (3 test cho tool mới)
  - `starter_v0/data/eval_group.json` (6 test case)
  - `report/team/group_report.md` (Bảng B1, B2, B3, B5a)
- **Run logs minh chứng:**
  - Base suite: `runs/v0_B_base_gemini_20261110T175315502560.json` (65%)
  - Base suite: `runs/v1_B_base_gemini_20261110T181300856029.json` (75%)
  - Base suite: `runs/v2_B_base_gemini_20261110T181725050339.json` (80%)
  - Base suite: `runs/v3_B_base_gemini_20261110T182011558241.json` (95%)
  - Group suite: `runs/v3_B_group_gemini_20261110T185417522678.json` (100%)
- **AI/công cụ đã dùng và cách tự kiểm tra:**
  - Dùng AI hỗ trợ phân tích JSON log và viết fixture mock HTTP.
  - Tự kiểm tra bằng lệnh: `pytest tests/` (kiểm tra contract và code tool) và `run_eval.py` (kiểm tra model routing, đảm bảo `provider_error_cases == 0`).

## 5. Tự đánh giá

- Đạt 9/10 tiêu chí C8: Có đầy đủ commit kỹ thuật, bằng chứng log thật không bịa đặt, hoàn thành tốt mức mục tiêu độ chính xác của agent.
