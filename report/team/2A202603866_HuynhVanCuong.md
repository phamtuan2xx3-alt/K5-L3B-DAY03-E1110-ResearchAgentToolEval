# Báo cáo cá nhân — Huỳnh Văn Cường — 2A202603866

## 1. Thông tin thành viên

- Họ tên: Huỳnh Văn Cường
- MSSV: 2A202603866
- Email:

## 2. Phần việc phụ trách

Phân công cập nhật theo TEAM.md cho bản main hiện tại:

- Rà soát prompt/tools v0–v3, snapshot/hash và version log.
- Phân tích các case FAIL và đối chiếu metric trước/sau.
- Kiểm tra eval nhóm đủ 5 single và 5 multi, liên kết run đúng artifact.

Đầu ra: Bảng metric, phân tích lỗi và eval nhóm. Người kiểm tra chéo: Sơn. Đây là trách nhiệm được giao, không phải xác nhận các đầu việc đã hoàn tất.

## 3. Đóng góp cụ thể

> Báo cáo nguồn từ nhánh thành viên: nội dung lịch sử dưới đây được giữ để đối chiếu, không xác nhận rằng mã/run của nhánh đó đã được tích hợp vào main. Phân công hiện hành nằm ở mục 2; số đo bản nộp theo group report.


- Baseline v0: case_accuracy 0.65 → tối ưu lên v3 0.95 (provider_error=0)
- Tool mới `cite` + 3 unit test; group suite 10/10
- UI `app.py` + 3 transcript (research / missing-info / send-confirm)

## 4. Bằng chứng

- File/commit/PR: `starter_v0/artifacts/*`, `tools/cite/`, `data/eval_group.json`, `app.py`, `runs/`, `transcripts/`, `report/team/group_report.md`
- AI/công cụ: Cursor agent hỗ trợ viết/sửa; tự kiểm bằng `preflight_provider.py`, `run_eval.py`, `pytest`

## 5. Tự đánh giá

Hoàn thành CP1–CP5 trên nhánh `lab/day03-e1110`. Còn lại: điền đủ TEAM thành viên 2, mở Cloudflare Tunnel khi demo, push + nộp LMS.
