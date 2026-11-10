# Báo cáo cá nhân — HuynhVanCuong-2A202603866

## 1. Thông tin thành viên

- Họ tên: Huynh Van Cuong
- MSSV: 2A202603866
- Email:

## 2. Phần việc phụ trách

- Setup `.env` / preflight Gemini, chạy baseline v0 và vòng tối ưu v1–v3
- Sửa `system_prompt.md` + `tools.yaml`, thêm tool `cite` + unit test
- Viết `eval_group.json`, Streamlit UI, transcript live, điền group report

## 3. Đóng góp cụ thể

- Baseline v0: case_accuracy 0.65 → tối ưu lên v3 0.95 (provider_error=0)
- Tool mới `cite` + 3 unit test; group suite 10/10
- UI `app.py` + 3 transcript (research / missing-info / send-confirm)

## 4. Bằng chứng

- File/commit/PR: `starter_v0/artifacts/*`, `tools/cite/`, `data/eval_group.json`, `app.py`, `runs/`, `transcripts/`, `report/team/group_report.md`
- AI/công cụ: Cursor agent hỗ trợ viết/sửa; tự kiểm bằng `preflight_provider.py`, `run_eval.py`, `pytest`

## 5. Tự đánh giá

Hoàn thành CP1–CP5 trên nhánh `lab/day03-e1110`. Còn lại: điền đủ TEAM thành viên 2, mở Cloudflare Tunnel khi demo, push + nộp LMS.
