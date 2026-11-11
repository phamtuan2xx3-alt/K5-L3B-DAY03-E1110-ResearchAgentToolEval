---
name: check_citations
track: bonus
kind: local_formatter
requires_env: []
inputs: [draft, sources]
outputs: [citations, missing_sources, unused_sources, valid]
side_effect: false
---
# check_citations

Kiểm tra mã trích dẫn trong bản nháp so với nguồn đã cung cấp, hoàn toàn offline.

- `draft`: chuỗi không rỗng, trích dẫn dạng `[id]` hoặc `[1, 2]`.
- `sources`: danh sách `{id, url}`; id là chuỗi duy nhất gồm chữ ASCII, số, `_`, `-`, phân biệt hoa thường; URL HTTP/HTTPS hợp lệ. Cho phép danh sách rỗng.
- Bỏ qua link/ảnh Markdown, reference link dạng `[label][ref]` và định nghĩa `[ref]: URL`, fenced code và inline code với số backtick mở/đóng khớp nhau. Không phải parser Markdown đầy đủ.
- `citations`: mã duy nhất theo thứ tự xuất hiện; `missing_sources`: mã không có nguồn; `unused_sources`: nguồn không được trích dẫn.
- `valid=true` nghĩa là mọi mã nhận diện được đều có nguồn. Bản nháp không có mã sẽ có `citations=[]`; tool không xác minh nội dung, khả năng truy cập URL hay sự thật của nhận định.
- Input sai, id trùng hoặc thiếu URL: trả `{tool, error, message}`.

Ví dụ: `draft="Kết quả [1, 2]."`, `sources=[{"id":"1","url":"https://example.org/a"}]` trả `missing_sources=["2"]`, `valid=false`.
