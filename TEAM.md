# Nhóm E1110

- Lớp: L3B.
- Repo: https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval
- Bản nhóm sử dụng: main. Minh chứng cá nhân dẫn tới nhánh riêng; không gộp số đo khác artifact vào kết quả nhóm.

## Thành viên và phân công

Phân công theo nội dung báo cáo cá nhân; các thành viên có thể cùng phụ trách setup, prompt/tool, eval, UI và test trên nhánh riêng. Không ép chia phần không trùng hoặc quy đổi số đầu việc thành tỷ lệ đóng góp. Phạm Quang Tuấn phụ trách thực hiện Small Local Model Challenge của nhóm trên main.

| Thành viên | MSSV | Vai trò | Nhánh minh chứng | Kiểm tra chéo |
|---|---|---|---|---|
| Phạm Quang Tuấn | 2A202603824 | Nhóm trưởng, provider và bonus local | [main](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/main/) | Tuấn Đức |
| Trần Phạm Minh Sơn | 2A202603802 | Prompt, github_search và unit test | [feature/sontpm](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/feature%2Fsontpm/) | Cường |
| Huỳnh Văn Cường | 2A202603866 | Prompt, cite và eval nhóm | [lab/day03-e1110](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/lab%2Fday03-e1110/) | Sơn |
| Nguyễn Phan Tuấn Đức | 2A202603818 | Prompt, source_dedupe, UI và Telegram | [tuanduc](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/tuanduc/) | Thanh |
| Đỗ Minh Thanh | 2A202603793 | Prompt, bốn tool xử lý nguồn và chat session | [DoMinhThanh](https://github.com/phamtuan2xx3-alt/K5-L3B-DAY03-E1110-ResearchAgentToolEval/tree/DoMinhThanh/) | Tuấn |

## Đầu việc và báo cáo cá nhân

### Phạm Quang Tuấn — 2A202603824

- Điều phối, tích hợp main, cấu hình Gemini 3.5 Flash Lite và queue/retry; kiểm tra API social_search.
- Thực hiện baseline, tối ưu prompt/tool, source_audit và kiểm thử trên main; tổng hợp kết quả nhóm.
- Trực tiếp tải và chạy hai model local Qwen2.5:3B, Llama3.2:1B; chạy base eval, hai vòng tối ưu local và kiểm tra ngược Gemini.
- Phụ trách minh chứng bonus local và private channel Telegram của main, rà soát bản nộp.

[Báo cáo cá nhân](report/team/2A202603824_PhamQuangTuan.md).

### Trần Phạm Minh Sơn — 2A202603802

- Thiết lập và kiểm tra Gemini; phân tích baseline và tối ưu prompt/tool declaration v0–v3 trên nhánh cá nhân.
- Xây dựng github_search, đăng ký contract/schema và viết unit test.
- Xây dựng và chạy group eval 6 case, kiểm tra boundary gửi; lưu run/hash và phân tích lỗi trên nhánh.

[Báo cáo cá nhân](report/team/2A202603802_TranPhamMinhSon.md).

### Huỳnh Văn Cường — 2A202603866

- Thiết lập baseline và tối ưu prompt/tool declaration v0–v3; phân tích routing/arguments trên nhánh cá nhân.
- Xây dựng cite và unit test, bộ eval nhóm 10 case.
- Triển khai UI, thu transcript research/thiếu thông tin/xác nhận gửi và tổng hợp báo cáo của nhánh.

[Báo cáo cá nhân](report/team/2A202603866_HuynhVanCuong.md).

### Nguyễn Phan Tuấn Đức — 2A202603818

- Tối ưu system prompt/tool declaration và đối chiếu các run trên nhánh cá nhân.
- Xây dựng source_dedupe, unit test và test boundary gửi Telegram.
- Tích hợp UI Streamlit, chạy eval nhóm, thu transcript và kiểm tra Telegram; hỗ trợ rà soát demo nhóm.

[Báo cáo cá nhân](report/team/2A202603818_NguyenPhanTuanDuc.md).

### Đỗ Minh Thanh — 2A202603793

- Thiết lập Gemini/API tool, baseline và tối ưu v0–v5; đối chiếu hash, đối chứng 14 tool và phân tích lỗi trên nhánh cá nhân.
- Xây dựng deduplicate_sources, check_citations, compare_papers, rank_sources và unit test; bộ eval nhóm 10 case.
- Triển khai UI/chat session, kiểm tra citation, che credential và boundary gửi; thu transcript/receipt Telegram và tổng hợp báo cáo của nhánh.

[Báo cáo cá nhân](report/team/2A202603793_DoMinhThanh.md).

## Quy ước minh chứng

Run, test và transcript cá nhân được đối chiếu trên đúng nhánh nêu trong báo cáo. Nhánh cá nhân có thể có tool, số test hoặc metric khác main; việc dẫn liên kết không xác nhận mã đã merge. Có sử dụng AI hỗ trợ theo khai báo của từng thành viên.
