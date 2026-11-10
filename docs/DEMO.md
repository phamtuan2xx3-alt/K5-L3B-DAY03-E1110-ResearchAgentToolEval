# UI demo E1110

Link đang dùng: **https://angel-modification-priced-validation.trycloudflare.com**

Đây là Cloudflare Quick Tunnel tạm thời tới Streamlit local. Cần máy này bật,
app và tunnel tiếp tục chạy; khi tạo tunnel mới URL sẽ thay đổi. Không coi đây
là hosting cố định.

## Truy cập

Mã nằm ở biến `DEMO_ACCESS_CODE` trong `starter_v0/.env`; nhóm trưởng chia sẻ mã
riêng cho người thử. Không ghi mã vào Git hoặc báo cáo công khai. Người chưa có
mã chỉ thấy màn hình đăng nhập, không gửi được yêu cầu tới model.

Đã kiểm tra: public URL trả HTTP 200, browser hiển thị màn hình nhập mã;
Streamlit AppTest chặn chưa đăng nhập, từ chối mã sai và mở chat với mã đúng.
Không có API key trên giao diện. Telegram vẫn cần nút duyệt exact nội dung/kênh.

## Trạng thái / tắt demo

Từ root repo:

```powershell
.\starter_v0\scripts\demo.ps1 status
.\starter_v0\scripts\demo.ps1 stop
```

Lệnh stop chỉ dừng đúng PID/executable/thời điểm tạo của UI và tunnel đã ghi nhận,
không dừng Ollama hoặc xóa model. Thư mục `.local-demo/` chứa cloudflared và log,
được Git bỏ qua. Mã đăng nhập vẫn ở `.env` sau khi dừng demo.

## Chạy lại

Terminal 1, từ `starter_v0/`:

```powershell
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Terminal 2, từ root, dùng executable đã chuẩn bị:

```powershell
.\.local-demo\cloudflared.exe tunnel --config .\.local-demo\quick-tunnel.yml --url http://127.0.0.1:8501 --no-autoupdate
```

Cấu hình riêng chỉ chứa `loglevel: info`, tránh bị ingress trong cấu hình
Cloudflare toàn máy chi phối. Không đổi/di chuyển cấu hình Cloudflare của user.
Nếu đã xóa `.local-demo/`, tải lại executable từ [release chính thức](https://github.com/cloudflare/cloudflared/releases),
tạo lại file cấu hình riêng rồi chạy lệnh trên. Cập nhật link mới vào báo cáo.
Metadata process của script status/stop áp dụng phiên do agent đã khởi tạo;
nếu chạy lại thủ công, dừng hai terminal bằng Ctrl+C.

Nguồn: [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/).
