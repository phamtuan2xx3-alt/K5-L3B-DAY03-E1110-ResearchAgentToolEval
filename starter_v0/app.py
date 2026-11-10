from __future__ import annotations

import streamlit as st

from privacy import redact_secrets
from web_chat import ChatSession


st.set_page_config(page_title="E1110 · Research Desk", page_icon="🔎", layout="wide")

if "conversation" not in st.session_state:
    st.session_state.conversation = ChatSession()

with st.sidebar:
    st.markdown("### E1110 / Research Desk")
    st.caption("L3B · Trợ lý nghiên cứu")
    if st.button("Cuộc trò chuyện mới", use_container_width=True):
        st.session_state.conversation = ChatSession()
        st.rerun()
    conversation = st.session_state.conversation
    st.divider()
    st.markdown("**Gemini**")
    st.caption(conversation.model)
    st.markdown("**Tìm nguồn · Đọc bài · Đối chiếu**")
    st.caption("Có thể dùng dữ liệu bạn cung cấp hoặc tìm nguồn trên web. Khi thiếu thông tin, trợ lý sẽ hỏi lại.")
    with st.expander("Công cụ có thể sử dụng"):
        for tool in conversation.tools:
            st.markdown(f"- `{tool['function']['name']}`")
    st.caption("Bản demo hỗ trợ soạn nội dung và hỏi xác nhận Telegram; việc gửi thật được tắt.")
    st.download_button(
        "Tải transcript JSON", data=conversation.export(), file_name=conversation.path.name,
        mime="application/json", disabled=not conversation.transcript["turns"], use_container_width=True,
    )

st.caption("E1110 / TRỢ LÝ NGHIÊN CỨU")
st.title("Research Desk")
st.markdown("Từ câu hỏi đến nguồn đáng kiểm tra.")
st.caption("Tìm tài liệu, đọc nội dung và tổ chức bằng chứng trong một cuộc trò chuyện.")

pending = None
if not conversation.transcript["turns"]:
    st.divider()
    examples = [
        ("Tìm nguồn", "Tìm 2 nguồn trên web về robotics trong tuần này, kèm URL."),
        ("So sánh paper", 'So sánh năm và phương pháp của hai paper: [{"title":"Paper A","year":2024,"method":"Survey"},{"title":"Paper B","year":2025,"method":"Experiment"}].'),
        ("Kiểm tra trích dẫn", 'Kiểm tra bản nháp "Kết luận [s1], hạn chế [s2]." với nguồn [{"id":"s1","url":"https://example.org/study"}]. Không tìm thêm nguồn.'),
    ]
    for column, (label, example) in zip(st.columns(3), examples):
        with column:
            if st.button(label, use_container_width=True):
                pending = example
    st.info("Bạn có thể dán URL, danh sách nguồn hoặc metadata paper để bắt đầu.")

for turn in conversation.transcript["turns"]:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        if turn["status"] == "provider_error":
            st.error(turn["assistant_text"])
        else:
            st.markdown(turn["assistant_text"])
        if turn["status"] == "waiting_for_user":
            st.caption("Đang chờ bạn bổ sung thông tin.")
        if turn.get("tool_events"):
            with st.expander("Nguồn và công cụ đã dùng"):
                st.json(redact_secrets(turn["tool_events"]))

prompt = st.chat_input("Nhập câu hỏi hoặc dán dữ liệu cần nghiên cứu…", max_chars=16000)
if pending or prompt:
    with st.spinner("Đang xử lý yêu cầu và kiểm tra nguồn…"):
        conversation.submit(pending or prompt)
    st.rerun()
