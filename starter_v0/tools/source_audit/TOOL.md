---
name: source_audit
track: core
kind: local_formatter
provider: Python standard library
requires_env: []
inputs: [items, require_date]
outputs: [status, summary, results, issues, limitations]
side_effect: false
---
# source_audit

Kiểm tra metadata của các nguồn đã thu thập trước khi định dạng/xuất bản. Không
cần API key, không gọi mạng và không sửa danh sách đầu vào.

## Khi nào dùng

- User yêu cầu rà soát URL, nguồn trùng, tiêu đề hoặc ngày xuất bản còn thiếu.
- Đã có danh sách nguồn từ user hoặc kết quả tìm kiếm; không cần tìm lại trên web.
- Không dùng để đánh giá sự thật, độ uy tín, link sống/chết hoặc độ mới của bài.
  Nếu chưa có nguồn, hỏi lại hoặc thực hiện bước research phù hợp trước.

## Input và output

`items`: danh sách không rỗng các object, trường `url`, `title` và tùy chọn
`published_at` / `published_date` / `date`. `require_date` mặc định true;
false bỏ cảnh báo thiếu ngày. Ngày chỉ được kiểm tra có chuỗi không rỗng, chưa
được kiểm chứng là ngày hợp lệ hoặc ngày của bài thực tế.

HTTP(S) URL phải có hostname, không chứa khoảng trắng hoặc credentials, port hợp
lệ. Khi kiểm tra trùng, chuẩn hóa scheme/hostname, port mặc định và bỏ fragment;
giữ nguyên chữ hoa/thường của path và query để tránh gộp nhầm các tài nguyên.

`status`: ok hoặc needs_review. `summary` đếm item, URL hợp lệ duy nhất, vấn đề
và bản trùng. `issues` chứa index **bắt đầu từ 0**, code (`missing_url`,
`invalid_url`, `duplicate_url`, `missing_title`, `missing_date`) và `duplicate_of`
nếu có. Item trùng vẫn được giữ trong input; tool không tự xóa nguồn.

Input sai kiểu/rỗng hoặc lỗi nội bộ trả error dict, không raise ra agent.

## Ví dụ

```json
{"items":[{"title":"Bài A","url":"https://example.org/a","published_at":"2026-11-10"}],"require_date":true}
```

Kết quả: status=ok, item_count=1, unique_url_count=1, issue_count=0.

Unit test: `python -m pytest tests/test_tools_todo.py -k source_audit -v`.
