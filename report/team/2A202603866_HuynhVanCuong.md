# Báo cáo cá nhân — Huỳnh Văn Cường — 2A202603866

## 1. Thông tin thành viên

- Họ tên: Huỳnh Văn Cường
- MSSV: 2A202603866
- Email:

## 2. Phần việc phụ trách

- Thiết lập baseline và tối ưu prompt/tool declaration v0–v3; phân tích routing/arguments trên nhánh cá nhân.
- Xây dựng cite và unit test, bộ eval nhóm 10 case.
- Triển khai UI, thu transcript research/thiếu thông tin/xác nhận gửi và tổng hợp báo cáo của nhánh.

Người kiểm tra chéo: Sơn. Phạm vi theo báo cáo cá nhân; kết quả và minh chứng giữ đúng nhánh nguồn. Phần chạy model local của nhóm do Phạm Quang Tuấn thực hiện trên main.

## 3. Đóng góp cụ thể



- Baseline v0: case_accuracy 0.65 → tối ưu lên v3 0.95 (provider_error=0)
- Tool mới `cite` + 3 unit test; group suite 10/10
- UI `app.py` + 3 transcript (research / missing-info / send-confirm)

## 4. Bằng chứng

**Nguồn minh chứng cá nhân:** [nhánh lab/day03-e1110](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/), [báo cáo gốc](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/lab%2Fday03-e1110/report/team/2A202603866_HuynhVanCuong.md). Các URL bên dưới trỏ tới nhánh cá nhân; số liệu ở đó không thay thế kết quả main trong báo cáo nhóm.

- File/commit/PR: `starter_v0/artifacts/*`, [tools/cite/](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/starter_v0/tools/cite), [data/eval_group.json](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/lab%2Fday03-e1110/starter_v0/data/eval_group.json), `app.py`, `runs/`, `transcripts/`, [report/team/group_report.md](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/blob/lab%2Fday03-e1110/report/team/group_report.md)
- AI/công cụ: Cursor agent hỗ trợ viết/sửa; tự kiểm bằng `preflight_provider.py`, `run_eval.py`, `pytest`


Minh chứng theo nhánh: [artifacts](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/starter_v0/artifacts), [tools](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/starter_v0/tools), [tests](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/starter_v0/tests), [data](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/starter_v0/data), [runs](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/starter_v0/runs), [transcripts](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/starter_v0/transcripts).

## 5. Tự đánh giá

Hoàn thành CP1–CP5 trên nhánh `lab/day03-e1110`. Còn lại: điền đủ TEAM thành viên 2, mở Cloudflare Tunnel khi demo, push + nộp LMS.
