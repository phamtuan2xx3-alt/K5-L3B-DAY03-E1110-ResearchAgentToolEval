from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import run_model_tool_loop, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)


def _init_session() -> None:
    defaults: dict[str, Any] = {
        "history": [],
        "display_messages": [],
        "turn_index": 0,
        "transcript": None,
        "transcript_path": None,
        "ready": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _bootstrap_agent(provider_name: str, model: str | None, version: str) -> None:
    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(tools_path)
    openai_tools = to_openai_tools(tool_declarations)
    provider = make_provider(provider_name)
    selected_model = model or getattr(provider, "default_model", None)
    artifact_version = build_artifact_version(version, system_prompt_path, tools_path)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = f"{version}_{provider_name}_{timestamp}_ui"
    transcript_path = ROOT / "transcripts" / f"{transcript_id}.transcript.json"
    transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": selected_model,
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "source": "streamlit_app",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "turns": [],
    }
    st.session_state.provider = provider
    st.session_state.openai_tools = openai_tools
    st.session_state.system_prompt = system_prompt
    st.session_state.selected_model = selected_model
    st.session_state.version = version
    st.session_state.artifact_version = artifact_version.artifact_version
    st.session_state.transcript = transcript
    st.session_state.transcript_path = transcript_path
    st.session_state.history = []
    st.session_state.display_messages = []
    st.session_state.turn_index = 0
    st.session_state.ready = True
    write_transcript(transcript_path, transcript)


def main() -> None:
    st.set_page_config(page_title="E1110 Research Agent", page_icon="🔎", layout="centered")
    _init_session()

    st.title("E1110 Research Agent")
    st.caption("Day 03 — prompt + tool-calling research agent (Gemini)")

    with st.sidebar:
        st.header("Session")
        provider_name = st.selectbox("Provider", ["gemini", "openrouter", "openai", "anthropic", "ollama"], index=0)
        model = st.text_input("Model", value="gemini-3.5-flash-lite")
        version = st.text_input("Version label", value="v3")
        if st.button("Start / Reset session", type="primary"):
            try:
                _bootstrap_agent(provider_name, model.strip() or None, version.strip() or "v3")
                st.success(f"Ready · {st.session_state.artifact_version}")
            except Exception as exc:  # noqa: BLE001
                st.error(f"{type(exc).__name__}: {exc}")
        if st.session_state.ready:
            st.write(f"Model: `{st.session_state.selected_model}`")
            st.write(f"Transcript: `{st.session_state.transcript_path.name}`")

    if not st.session_state.ready:
        st.info("Chọn provider/model ở sidebar rồi bấm **Start / Reset session**.")
        return

    for message in st.session_state.display_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("tools"):
                st.code(message["tools"], language="json")

    prompt = st.chat_input("Ask the research agent…")
    if not prompt:
        return

    st.session_state.display_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.turn_index += 1
    messages = [
        {"role": "system", "content": st.session_state.system_prompt},
        *trim_history(st.session_state.history, 5),
        {"role": "user", "content": prompt},
    ]
    turn_record: dict[str, Any] = {
        "turn_index": st.session_state.turn_index,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking / calling tools…"):
            try:
                result = run_model_tool_loop(
                    provider=st.session_state.provider,
                    messages=messages,
                    tools=st.session_state.openai_tools,
                    model=st.session_state.selected_model,
                    max_tool_rounds=4,
                )
                turn_record.update(result)
                assistant_text = result["assistant_text"] or "(no text)"
                tool_dump = ""
                if result.get("tool_events"):
                    import json

                    tool_dump = json.dumps(result["tool_events"], ensure_ascii=False, indent=2, default=str)
                st.markdown(assistant_text)
                if tool_dump:
                    st.code(tool_dump, language="json")
                st.session_state.display_messages.append(
                    {"role": "assistant", "content": assistant_text, "tools": tool_dump or None}
                )
                st.session_state.history.append({"role": "user", "content": prompt})
                st.session_state.history.append({"role": "assistant", "content": assistant_text})
            except Exception as exc:  # noqa: BLE001
                err = f"{type(exc).__name__}: {exc}"
                turn_record.update({"status": "provider_error", "error": err})
                st.error(err)
                st.session_state.display_messages.append({"role": "assistant", "content": err})

    turn_record["ended_at"] = datetime.now().isoformat(timespec="seconds")
    st.session_state.transcript["turns"].append(turn_record)
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)


if __name__ == "__main__":
    main()
