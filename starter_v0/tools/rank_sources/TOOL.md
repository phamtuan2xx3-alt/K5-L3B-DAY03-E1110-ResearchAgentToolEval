---
name: rank_sources
track: bonus
kind: local_formatter
requires_env: []
inputs: [query, items, preferred_domains, reference_date, limit]
outputs: [items, total_count, reference_date]
side_effect: false
---
# rank_sources

Xếp hạng nguồn đã có bằng công thức minh bạch, hoàn toàn offline. Điểm không chứng minh độ tin cậy của nguồn.

- `query`: từ khóa không rỗng. Tách từ và bỏ dấu theo helper hiện có, bỏ stopwords.
- `items`: danh sách object có URL HTTP/HTTPS; tùy chọn title, summary (string), published_at (ngày YYYY-MM-DD). Cho phép danh sách rỗng.
- `preferred_domains`: list domain, không có scheme/path/port. Domain chính và subdomain được cộng điểm; domain chỉ có hậu tố gần giống không được cộng.
- `reference_date`: YYYY-MM-DD; mặc định ngày local hiện tại. Truyền ngày cụ thể để tái lập phép tính; output luôn trả ngày đã dùng.
- `limit`: số nguyên dương, mặc định 5.
- Relevance = số từ khóa khớp title/summary chia tổng từ khóa query.
- Freshness = `1 / (1 + age_days / 30)`; thiếu ngày hoặc ngày tương lai nhận 0.
- Score = `0.60 * relevance + 0.25 * freshness + 0.15 * preferred_domain`.
- Mỗi item trả thêm `ranking` gồm score, relevance, freshness và preferred_domain. Các điểm làm tròn 6 chữ số; đồng điểm giữ thứ tự đầu vào. Không sửa dữ liệu đầu vào.
- Ngày/URL/kiểu dữ liệu sai hoặc limit không hợp lệ: trả `{tool, error, message}`.
