from __future__ import annotations

import json
import hashlib
import hmac
import os

import streamlit as st

from env_loader import load_lab_env
from tools import load_tool_declarations
from ui_session import ROOT, ResearchSession, redact

st.set_page_config(page_title="E1110 · Research desk", page_icon="🔎", layout="wide")
load_lab_env(ROOT)
access_code = os.getenv("DEMO_ACCESS_CODE", "")
access_hash = hashlib.sha256(access_code.encode()).hexdigest()
if access_code and st.session_state.get("demo_auth_hash") != access_hash:
    st.title("E1110 · Research desk")
    st.caption("Bản demo dành cho nhóm. Nhập mã được nhóm trưởng cung cấp để bắt đầu.")
    with st.form("demo_access"):
        entered = st.text_input("Mã truy cập demo", type="password")
        submitted = st.form_submit_button("Mở bàn nghiên cứu")
    if submitted:
        if hmac.compare_digest(entered.encode(), access_code.encode()):
            st.session_state.demo_auth_hash = access_hash
            st.rerun()
        st.error("Mã truy cập chưa đúng.")
    st.stop()
st.markdown("""<style>
.block-container {max-width:1120px;padding-top:2.5rem;padding-bottom:3rem}
[data-testid="stSidebar"] {border-right:1px solid #dce5e0}
.eyebrow {color:#147d6a;font-size:.76rem;letter-spacing:.16em;font-weight:700;margin-bottom:.7rem}
[data-testid="stChatMessage"] {border:1px solid #e0e7e3;border-radius:12px}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### E1110")
    st.caption("RESEARCH DESK · AI20K")
    engine = st.selectbox("Model", ["Gemini 3.5 Flash Lite", "Local · Qwen2.5 3B", "Local · Llama3.2 1B"])
    provider, model = {"Gemini 3.5 Flash Lite": ("gemini", "gemini-3.5-flash-lite"),
                       "Local · Qwen2.5 3B": ("ollama", "qwen2.5:3b"),
                       "Local · Llama3.2 1B": ("ollama", "llama3.2:1b")}[engine]
    if provider == "gemini":
        st.caption("Gọi tuần tự · dưới 15 RPM")
    else:
        st.caption("Cần khởi động Ollama portable trước khi dùng.")
    if st.button("Cuộc trò chuyện mới", use_container_width=True):
        st.session_state.pop("research_session", None)
        st.rerun()
    st.divider()
    declarations = load_tool_declarations(ROOT / "artifacts/tools.yaml")
    with st.expander(f"{len(declarations)} công cụ nghiên cứu"):
        for item in declarations:
            st.markdown(f"**{item['name']}**")
            st.caption(item["description"])
    st.caption("Nhóm trưởng: Phạm Quang Tuấn")

if "research_session" not in st.session_state:
    st.session_state.research_session = ResearchSession(provider, model)
session = st.session_state.research_session
local_ready = session.provider_name != "ollama" or (ROOT.parent / ".local-models/weights-ready.json").exists()
if not local_ready:
    st.warning("Model local đang tải. Dùng Gemini hoặc đợi tải và kiểm checksum xong trước khi bắt đầu phiên local.")
if (provider, model) != (session.provider_name, session.model):
    st.info("Chọn Cuộc trò chuyện mới để bắt đầu với model vừa chọn; phiên hiện tại được giữ nguyên.")

st.markdown('<div class="eyebrow">E1110 / RESEARCH DESK</div>', unsafe_allow_html=True)
st.title("Từ câu hỏi đến bản tin có nguồn")
st.caption("Tìm tài liệu, rà soát nguồn và duyệt nội dung trước khi chia sẻ.")


def show_turn(turn):
    with st.chat_message("user"):
        st.text(turn["user"])
    with st.chat_message("assistant"):
        st.markdown(turn.get("assistant_text", ""))
        if turn.get("error"):
            st.error(turn["error"])
        events = turn.get("tool_events", [])
        for event in events:
            result = event.get("result", {})
            if "error" in result:
                st.error(f"{event['tool']}: {result['error']} — {result.get('message', '')}")
        if events:
            with st.expander(f"Công cụ và nguồn · {len(events)} lượt gọi"):
                st.json(redact(events))
        if turn.get("status") == "max_tool_rounds":
            st.warning("Đã chạm giới hạn bước xử lý. Kiểm tra kết quả tool trước khi tiếp tục.")


for turn in session.transcript["turns"]:
    show_turn(turn)

sample = None
if not session.transcript["turns"]:
    st.markdown("#### Bắt đầu từ một việc cụ thể")
    left, middle, right = st.columns(3)
    if left.button("Rà soát nguồn mẫu", use_container_width=True, disabled=not local_ready):
        sample = 'Kiểm tra URL trùng và metadata của nguồn sau, không yêu cầu ngày: [{"title":"Nghiên cứu A","url":"https://example.org/paper#one"},{"title":"Nghiên cứu A","url":"https://example.org/paper#two"}]. Chỉ kiểm tra dữ liệu đã cho, không gọi mạng.'
    if middle.button("Tra chính sách trích dẫn", use_container_width=True, disabled=not local_ready):
        sample = "Tra chính sách nội bộ công ty về trích dẫn nguồn."
    if right.button("Tóm tắt một bài viết", use_container_width=True, disabled=not local_ready):
        sample = "Tôi muốn tóm tắt một bài viết; hãy hỏi tôi URL trước."

if session.pending_send is not None:
    st.subheader("Duyệt nội dung gửi Telegram")
    st.caption(f"Kênh nhận: {session.pending_target or 'chưa cấu hình'}. Chỉ nút xác nhận bên dưới mới thực hiện gửi.")
    st.code(session.pending_send, language=None, wrap_lines=True)
    approve, cancel = st.columns(2)
    if approve.button("Xác nhận và gửi", type="primary", use_container_width=True):
        with st.spinner("Đang gửi bản tin đã duyệt…"):
            session.resolve_send(True)
        st.rerun()
    if cancel.button("Hủy gửi", use_container_width=True):
        session.resolve_send(False)
        st.rerun()

user_text = st.chat_input("Nhập chủ đề, URL hoặc danh sách nguồn cần kiểm tra…", disabled=session.pending_send is not None or not local_ready)
if user_text or sample:
    with st.spinner("Agent đang xử lý và kiểm tra kết quả công cụ…"):
        session.run(user_text or sample)
    st.rerun()

if session.transcript["turns"]:
    st.download_button("Tải transcript JSON", data=json.dumps(redact(session.transcript), ensure_ascii=False, indent=2),
                       file_name=session.path.name, mime="application/json")
    st.caption("Phiên chat được lưu cục bộ. Các key/token đã biết được ẩn khỏi nội dung log.")
