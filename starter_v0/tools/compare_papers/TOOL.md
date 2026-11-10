---
name: compare_papers
track: bonus
kind: local_formatter
requires_env: []
inputs: [papers, fields]
outputs: [comparison, markdown, paper_count]
side_effect: false
---
# compare_papers

So sánh metadata của ít nhất hai paper, trả danh sách dữ liệu và bảng Markdown. Không tìm paper hoặc tự suy diễn metadata.

- `papers`: mỗi object có `title` không rỗng; tùy chọn `year` (integer 1000–9999), `authors` (list string), `topic`, `method`, `limitations`, `summary`, `url` (HTTP/HTTPS).
- `fields`: các cột duy nhất từ `year`, `authors`, `topic`, `method`, `limitations`, `summary`, `url`. Mặc định năm, tác giả, chủ đề, phương pháp, hạn chế; cột title luôn có.
- Trường thiếu là `null` trong comparison và `Chưa cung cấp` trong bảng. Danh sách tác giả được nối bằng dấu phẩy trong bảng; dấu `|`, HTML và xuống dòng được escape.
- Không thay đổi dữ liệu đầu vào. Không gọi model hoặc API.
- Input sai, thiếu title, dưới hai paper hoặc field không hỗ trợ: trả `{tool, error, message}`.

Ví dụ: `papers=[{"title":"A","year":2025},{"title":"B","year":2026}]`, `fields=["year"]` tạo bảng đối chiếu năm của hai paper.
