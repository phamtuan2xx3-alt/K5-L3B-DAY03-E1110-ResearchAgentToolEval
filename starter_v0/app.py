from __future__ import annotations

from datetime import datetime
from time import perf_counter
from typing import Any

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    ROOT,
    ProgressPhase,
    json_text,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


TRANSCRIPTS_DIR = ROOT / "transcripts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
PROVIDERS = ["gemini", "openai", "openrouter", "anthropic", "ollama"]
SUGGESTIONS = [
    ("Tin tức AI", "Tóm tắt các tin AI đáng chú ý trong tuần này và dẫn nguồn."),
    ("Bài báo khoa học", "Tìm 3 bài báo arXiv về đánh giá khả năng gọi công cụ của LLM."),
    ("Quy định nội bộ", "Quy định nội bộ về trích dẫn nguồn khi nghiên cứu là gì?"),
]

WORKSPACE_STYLE = """
<style>
    .block-container { max-width: 64rem; padding-top: 3.5rem; }
    .research-hero {
        border: 1px solid #304960;
        border-radius: 1.25rem;
        padding: clamp(1.25rem, 4vw, 2.5rem);
        background:
            radial-gradient(ellipse at 95% 0%, #20565e, transparent 63%),
            linear-gradient(120deg, #101e32, #172c46);
        color: #f4f8fc;
    }
    .research-hero .research-tag {
        color: #a3ebd7;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
    }
    .research-hero h1 {
        color: inherit;
        margin: .3rem 0;
        padding: 0;
        font-size: clamp(1.9rem, 5vw, 3rem);
        line-height: 1.14;
        letter-spacing: -.035em;
    }
    .research-hero p {
        color: #d3e0eb;
        margin: .65rem 0 0;
        max-width: 38rem;
        font-size: .98rem;
    }
    .st-key-suggestions button { min-height: 3.25rem; }
    [data-testid="stCode"] pre { max-height: 18rem; overflow: auto; }
    @media (max-width: 640px) {
        .block-container { padding: 3.5rem 1rem 1rem; }
    }
</style>
"""

HERO = """
<header class="research-hero">
    <div class="research-tag">Phòng lab · Đánh giá gọi công cụ</div>
    <h1>Research Agent</h1>
    <p>Tra cứu nguồn, kiểm chứng thông tin và theo dõi từng công cụ trong lúc agent làm việc.</p>
</header>
"""


def reset_chat() -> None:
    st.session_state.turns = []
    st.session_state.transcript = None
    st.session_state.agent_inputs = None
    st.session_state.pending_prompt = None
    st.session_state.save_error = None


def create_transcript(
    provider_name: str,
    model: str | None,
    version: str,
    history_window: int,
    max_tool_rounds: int,
) -> dict[str, Any]:
    artifact_version = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    return {
        "transcript_id": "_".join([safe_slug(version), safe_slug(provider_name), timestamp]),
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model,
        "system_prompt": str(SYSTEM_PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


def has_tool_error(event: dict[str, Any]) -> bool:
    result = event.get("result")
    return isinstance(result, dict) and "error" in result


def render_tool_details(event: dict[str, Any]) -> None:
    st.caption("Đầu vào")
    st.code(json_text(event.get("args", {}), max_chars=24000), language="json")
    if "result" in event:
        st.caption("Kết quả")
        st.code(json_text(event["result"], max_chars=24000), language="json")


def render_answer(turn: dict[str, Any]) -> None:
    status = turn["status"]
    if status == "provider_error":
        st.error(turn["error"])
    elif status == "waiting_for_user":
        st.info(turn["assistant_text"])
    elif status == "max_tool_rounds":
        st.warning("Agent đã đạt giới hạn số vòng gọi công cụ. Bạn có thể xem các kết quả thu được trong nhật ký.")
    elif turn["assistant_text"]:
        st.markdown(turn["assistant_text"])
    else:
        st.info("Model trả về phản hồi trống.")


def render_turn(turn: dict[str, Any]) -> None:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        render_answer(turn)
        events = turn["tool_events"]
        errors = sum(has_tool_error(event) for event in events)
        summary = f"{len(events)} lượt gọi"
        if errors:
            summary += f" · {errors} lỗi"
        if "elapsed_s" in turn:
            summary += f" · {turn['elapsed_s']:.1f} giây"
        if events:
            with st.expander(f"Nhật ký công cụ · {summary}"):
                labels = []
                for index, event in enumerate(events, start=1):
                    state = "Lỗi" if has_tool_error(event) else "Hoàn tất"
                    labels.append(f"{index:02d} · {event['tool']} · {state}")
                for tab, event in zip(st.tabs(labels), events):
                    with tab:
                        render_tool_details(event)
        else:
            elapsed = f" · {turn['elapsed_s']:.1f} giây" if "elapsed_s" in turn else ""
            st.caption(f"Không gọi công cụ{elapsed}")


def run_turn(
    user_text: str,
    provider_name: str,
    model: str,
    version: str,
    history_window: int,
    max_tool_rounds: int,
) -> None:
    with st.chat_message("user"):
        st.markdown(user_text)

    started = perf_counter()
    turn = {
        "turn_index": len(st.session_state.turns) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "assistant_text": "",
        "rounds": [],
        "tool_events": [],
    }
    with st.chat_message("assistant"):
        progress = st.status("Đang chuẩn bị phiên nghiên cứu…")
        trace = st.container()
        tool_slot = None
        completed_events = []

        def on_progress(phase: ProgressPhase, round_index: int, event: dict[str, Any] | None) -> None:
            nonlocal tool_slot
            if phase == "model_started":
                progress.update(label=f"Vòng {round_index}/{max_tool_rounds} · Đang chờ model…")
                return

            assert event is not None
            if phase == "tool_started":
                progress.update(label=f"Vòng {round_index}/{max_tool_rounds} · Đang chạy `{event['tool']}`")
                tool_slot = trace.empty()
                with tool_slot.expander(f"{len(completed_events) + 1:02d} · `{event['tool']}` · Đang chạy"):
                    render_tool_details(event)
            else:
                assert tool_slot is not None
                completed_events.append(event)
                state = "Lỗi" if has_tool_error(event) else "Hoàn tất"
                with tool_slot.expander(f"{len(completed_events):02d} · `{event['tool']}` · {state}"):
                    render_tool_details(event)

        try:
            provider = make_provider(provider_name)
            selected_model = model.strip() or getattr(provider, "default_model", None)
            if st.session_state.transcript is None:
                system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
                tools = to_openai_tools(load_tool_declarations(TOOLS_PATH))
                st.session_state.transcript = create_transcript(
                    provider_name, selected_model, version, history_window, max_tool_rounds
                )
                st.session_state.agent_inputs = (system_prompt, tools)

            system_prompt, tools = st.session_state.agent_inputs
            history = []
            for previous in st.session_state.turns:
                if previous["status"] != "provider_error":
                    history.extend([
                        {"role": "user", "content": previous["user"]},
                        {"role": "assistant", "content": previous["assistant_text"]},
                    ])
            messages = [
                {"role": "system", "content": system_prompt},
                *trim_history(history, history_window),
                {"role": "user", "content": user_text},
            ]
            turn.update(run_model_tool_loop(
                provider=provider,
                messages=messages,
                tools=tools,
                model=selected_model,
                max_tool_rounds=max_tool_rounds,
                on_progress=on_progress,
            ))
        except Exception as exc:
            turn.update(
                status="provider_error",
                error=f"{type(exc).__name__}: {exc}",
                tool_events=completed_events,
            )

        turn.update(ended_at=now_iso(), elapsed_s=round(perf_counter() - started, 2))
        st.session_state.turns.append(turn)
        transcript = st.session_state.transcript
        if transcript is not None:
            transcript["turns"].append(turn)
            path = TRANSCRIPTS_DIR / f"{transcript['transcript_id']}.transcript.json"
            try:
                write_transcript(path, transcript)
                st.session_state.save_error = None
            except OSError as exc:
                st.session_state.save_error = f"Không ghi được transcript vào thư mục dự án. {exc}"

    st.rerun()


def render_sidebar(busy: bool) -> tuple[str, str, str, int, int]:
    transcript = st.session_state.transcript
    locked = busy or transcript is not None
    with st.sidebar:
        st.subheader("Phiên nghiên cứu")
        st.button(
            "Cuộc trò chuyện mới",
            on_click=reset_chat,
            type="primary",
            use_container_width=True,
            disabled=busy,
        )
        st.divider()
        provider_name = st.selectbox("Nhà cung cấp", PROVIDERS, disabled=locked)
        model = st.text_input(
            "Model",
            value="gemini-3.5-flash-lite" if provider_name == "gemini" else "",
            placeholder="Mặc định của nhà cung cấp",
            key=f"model_{provider_name}",
            disabled=locked,
        )
        with st.expander("Cài đặt đánh giá"):
            version = st.text_input("Phiên bản artifact", value="v3", disabled=locked)
            history_window = st.slider("Số cặp hội thoại trong ngữ cảnh", 1, 10, 5, disabled=locked)
            max_tool_rounds = st.slider("Giới hạn vòng gọi công cụ", 1, 6, 4, disabled=locked)
        if transcript is not None:
            st.caption("Mở cuộc trò chuyện mới để đổi cấu hình.")
            st.divider()
            st.markdown("**Transcript**")
            st.caption(f"{transcript['model']} · {transcript['version']} · {len(transcript['turns'])} lượt")
            st.download_button(
                "Tải transcript JSON",
                data=json_text(transcript),
                file_name=f"{transcript['transcript_id']}.transcript.json",
                mime="application/json",
                use_container_width=True,
                disabled=busy,
                on_click="ignore",
            )
            if st.session_state.save_error:
                st.warning(st.session_state.save_error)
    return provider_name, model, version.strip() or "v3", history_window, max_tool_rounds


def queue_prompt(prompt: str | None = None) -> None:
    text = (prompt or st.session_state.research_prompt or "").strip()
    st.session_state.pending_prompt = text or None


def main() -> None:
    st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="wide")
    if "pending_prompt" not in st.session_state:
        reset_chat()

    st.markdown(WORKSPACE_STYLE + HERO, unsafe_allow_html=True)
    pending_prompt = st.session_state.pending_prompt
    busy = pending_prompt is not None
    settings = render_sidebar(busy)

    for turn in st.session_state.turns:
        render_turn(turn)

    if not st.session_state.turns and not busy:
        with st.container(key="suggestions"):
            st.subheader("Bạn muốn tìm hiểu gì?")
            st.caption("Chọn một yêu cầu mẫu hoặc nhập câu hỏi của bạn bên dưới.")
            for column, (label, prompt) in zip(st.columns(len(SUGGESTIONS)), SUGGESTIONS):
                column.button(
                    label, help=prompt, on_click=queue_prompt, args=(prompt,), use_container_width=True
                )

    st.chat_input(
        "Nhập câu hỏi hoặc yêu cầu nghiên cứu…",
        key="research_prompt",
        on_submit=queue_prompt,
        disabled=busy,
    )
    if pending_prompt is not None:
        # A rerun after Streamlit's Stop action must not replay tool calls.
        st.session_state.pending_prompt = None
        run_turn(pending_prompt, *settings)


if __name__ == "__main__":
    main()
