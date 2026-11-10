# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 |Trần Phạm Minh Sơn | 2A202603802 |      |  sontpm      |   Thành viên      |
|   2 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## TranPhamMinhSon-2A202603802

### Phần việc phụ trách

- Setup môi trường và provider Gemini (CP1).
- Tối ưu hóa prompt và tool declaration qua các vòng v0–v3 (CP1 & CP2).
- Viết tool mới github_search và unit test (CP3).
- Soạn 6 test cases và chạy eval bộ group (CP4).

### Đóng góp cụ thể

- Nâng độ chính xác agent từ 65% lên 95% (multi-turn đạt 100%).
- Code tool `github_search` + 3 unit test (pytest xanh 70 passed, 0 failed).
- Soạn 6 eval cases trong `eval_group.json` đạt 100% pass (0 provider error).

### Bằng chứng

- File báo cáo cá nhân: `report/team/2A202603802_TranPhamMinhSon.md`
- Run files: `v0`–`v3` trong `starter_v0/runs/` và `version_log.csv`
