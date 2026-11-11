---
name: deduplicate_sources
track: bonus
kind: local_formatter
requires_env: []
inputs: [items]
outputs: [items, original_count, unique_count, removed_count]
side_effect: false
---
# deduplicate_sources

Loại nguồn trùng theo URL, giữ metadata của lần xuất hiện đầu tiên và thứ tự nguồn. Không sửa danh sách đầu vào, không gọi mạng.

- Input: `items` là danh sách object có `url` HTTP/HTTPS hợp lệ; chấp nhận danh sách rỗng.
- Chuẩn hóa host và port mặc định; bỏ fragment, `utm_*`, `fbclid`, `gclid`. URL gốc vẫn được giữ trong output.
- Giữ nguyên scheme, chữ hoa/thường của path, thứ tự và giá trị query có ý nghĩa. Không gộp HTTP với HTTPS hoặc host khác nhau.
- Fragment được coi là vị trí trong cùng tài liệu; không dùng để gộp route ứng dụng phụ thuộc hash.
- Thiếu URL, URL chứa credentials hoặc sai định dạng: trả `{tool, error, message}`; không trả kết quả một phần.

Ví dụ: `items=[{"url":"https://example.org/a?utm_source=feed"},{"url":"https://example.org/a"}]` trả `unique_count=1`, `removed_count=1`.
