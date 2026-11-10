# Nhóm E1110

- Lớp: L3B.
- Repo: https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval
- Bản sử dụng: main của nhóm trưởng và working tree hiện tại; chưa chốt commit nộp.
- Mã và số đo của bản nộp lấy từ main. Báo cáo cá nhân nhập từ nhánh thành viên được giữ như tài liệu nguồn, không thay thế kết quả main.

## Thành viên

| Họ tên | MSSV | Vai trò |
|---|---|---|
| Phạm Quang Tuấn | 2A202603824 | Nhóm trưởng, provider và đóng gói |
| Trần Phạm Minh Sơn | 2A202603802 | Tool và kiểm thử |
| Huỳnh Văn Cường | 2A202603866 | Prompt và đánh giá |
| Nguyễn Phan Tuấn Đức | 2A202603818 | UI và Telegram |
| Đỗ Minh Thanh | 2A202603793 | Local model và tài liệu minh chứng |

## Phân công

Mỗi người phụ trách ba đầu việc, khối lượng dự kiến khoảng 20%. Đây là phân công rà soát và hoàn thiện, không phải tỷ lệ đóng góp đã hoàn thành. Các công việc thực hiện trên bản main hiện tại.

| Thành viên | Phần việc | Đầu ra | Kiểm tra chéo |
|---|---|---|---|
| Phạm Quang Tuấn | Rà soát Gemini 3.5 Flash Lite, queue RPM 15 và retry. Quản lý cấu hình, kiểm tra bảo mật key và môi trường chạy. Tổng hợp nghiệm thu, chốt commit/push và bản nộp. | Cấu hình, log provider và checklist bản nộp | Tuấn Đức |
| Trần Phạm Minh Sơn | Rà soát source_audit và contract đầu vào/đầu ra trên main. Kiểm tra unit test, trường hợp lỗi và test hồi quy. Đối chiếu kết quả social_search sau subscription với minh chứng API thật. | Tool contract, kết quả test và log API | Cường |
| Huỳnh Văn Cường | Rà soát prompt/tools v0–v3, snapshot/hash và version log. Phân tích các case FAIL và đối chiếu metric trước/sau. Kiểm tra eval nhóm đủ 5 single và 5 multi, liên kết run đúng artifact. | Bảng metric, phân tích lỗi và eval nhóm | Sơn |
| Nguyễn Phan Tuấn Đức | Rà soát UI Streamlit, hướng dẫn truy cập và transcript CLI/UI. Kiểm tra flow duyệt Telegram, receipt và chống gửi khi chưa xác nhận. Rà soát tài liệu dùng thử ngoài nhóm; giữ nhãn MOCK đến khi có phiên thật. | Hướng dẫn demo, transcript và receipt Telegram | Thanh |
| Đỗ Minh Thanh | Rà soát hai model local, lệnh chạy và hướng dẫn cleanup. Đối chiếu hai vòng tối ưu local và kiểm tra ngược Gemini, ghi đúng kết quả giảm/tăng. Kiểm tra liên kết group report, chỉ mục minh chứng và định dạng hồ sơ cá nhân. | Bảng local metrics, hướng dẫn và chỉ mục minh chứng | Tuấn |

## Minh chứng và báo cáo cá nhân

Có Codex hỗ trợ triển khai và tổng hợp. Mỗi thành viên tự kiểm tra phần phụ trách và cập nhật đóng góp thực tế; phân công mới không xác nhận thay cho lịch sử commit. Minh chứng dùng thử ngoài nhóm hiện là MOCK, chưa được tính là phiên thật.

- [Phạm Quang Tuấn — 2A202603824](report/team/2A202603824_PhamQuangTuan.md)
- [Trần Phạm Minh Sơn — 2A202603802](report/team/2A202603802_TranPhamMinhSon.md)
- [Huỳnh Văn Cường — 2A202603866](report/team/2A202603866_HuynhVanCuong.md)
- [Nguyễn Phan Tuấn Đức — 2A202603818](report/team/2A202603818_NguyenPhanTuanDuc.md)
- [Đỗ Minh Thanh — 2A202603793](report/team/2A202603793_DoMinhThanh.md)
