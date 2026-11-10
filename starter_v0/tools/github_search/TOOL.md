---
name: github_search
track: bonus
kind: live_api
provider: GitHub
requires_env: []
inputs: [query, sort, limit]
outputs: [repositories, total_count]
side_effect: false
---
# github_search

Tìm kiếm các kho lưu trữ mã nguồn mở (repositories) trên GitHub theo từ khóa hoặc chủ đề. Trả về danh sách repository kèm số sao (stars), mô tả, ngôn ngữ và đường dẫn URL.

