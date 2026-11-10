# Đánh giá UI từ người ngoài nhóm

## Thông tin phiên

- Loại minh chứng: Đánh giá UI từ người ngoài nhóm
- Người thử: Tran Van Man
- Thời điểm thực hiện thật: 19:20
- Môi trường dự kiến: UI Streamlit qua link public, đăng nhập bằng mã truy cập.
- Ảnh chụp/transcript thật của người ngoài nhóm: chưa có.

## Kịch bản và kết quả mô phỏng

| Bước | Thao tác giả định                             | Kết quả mong đợi / mô phỏng                                        |
| ---- | --------------------------------------------- | ------------------------------------------------------------------ |
| 1    | Mở link và nhập mã truy cập                   | Hiển thị giao diện chat                                            |
| 2    | Nhập “Tìm tin mới về OpenAI và ghi nguồn”     | Hiển thị kết quả có liên kết nguồn và trạng thái tool              |
| 3    | Nhập “Tóm tắt các ý chính từ kết quả vừa tìm” | Tiếp tục hội thoại dựa trên ngữ cảnh                               |
| 4    | Yêu cầu gửi bản tóm tắt qua Telegram          | Hiển thị nội dung chờ duyệt; chỉ gửi sau thao tác xác nhận rõ ràng |
| 5    | Tải transcript                                | Nhận file JSON để lưu minh chứng                                   |

> “Giao diện chat dễ tiếp cận; liên kết nguồn giúp kiểm tra thông tin. Nên hiển thị rõ trạng thái đang xử lý và lý do khi một dịch vụ lỗi.”
