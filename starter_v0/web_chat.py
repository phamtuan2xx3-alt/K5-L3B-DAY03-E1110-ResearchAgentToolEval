from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from chat import now_iso, run_model_tool_loop, trim_history, write_transcript
from privacy import redact_secrets
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).resolve().parent


class ChatSession:
    def __init__(self, *, transcripts_dir: Path | None = None) -> None:
        self.provider = make_provider("gemini")
        self.model = self.provider.default_model
        self.system_prompt = (ROOT / "artifacts/system_prompt.md").read_text(encoding="utf-8")
        self.tools = [tool for tool in to_openai_tools(load_tool_declarations(ROOT / "artifacts/tools.yaml"))
                      if tool["function"]["name"] != "send"]
        self.allowed_tools = {tool["function"]["name"] for tool in self.tools}
        self.history: list[dict[str, str]] = []
        session_id = f"ui_v5_gemini_{datetime.now():%Y%m%dT%H%M%S%f}_{uuid4().hex[:8]}"
        self.path = (transcripts_dir if transcripts_dir is not None else ROOT / "transcripts") / f"{session_id}.transcript.json"
        version = build_artifact_version("v5", ROOT / "artifacts/system_prompt.md", ROOT / "artifacts/tools.yaml")
        self.transcript: dict[str, Any] = {
            "transcript_id": session_id, **artifact_version_dict(version),
            "provider": "gemini", "model": self.model, "interface": "streamlit",
            "system_prompt": "artifacts/system_prompt.md", "tools": "artifacts/tools.yaml",
            "disabled_tools": ["send"], "history_window": 5, "max_tool_rounds": 6,
            "created_at": now_iso(), "updated_at": now_iso(), "turns": [],
        }

    def submit(self, user_text: str) -> dict[str, Any]:
        if not isinstance(user_text, str) or not user_text.strip():
            raise ValueError("Message must be a non-empty string")
        user_text = user_text.strip()
        record = {
            "turn_index": len(self.transcript["turns"]) + 1,
            "started_at": now_iso(), "user": user_text,
        }
        messages = [{"role": "system", "content": self.system_prompt},
                    *trim_history(self.history, 5), {"role": "user", "content": user_text}]
        try:
            result = run_model_tool_loop(
                provider=self.provider, messages=messages, tools=self.tools, model=self.model,
                max_tool_rounds=6, allowed_tools=self.allowed_tools,
            )
        except Exception as exc:
            result = {
                "status": "provider_error", "error": f"{type(exc).__name__}: {exc}",
                "assistant_text": "Chưa thể xử lý yêu cầu lúc này. Bạn hãy thử lại sau.",
                "rounds": [], "tool_events": [],
            }
        record.update(redact_secrets(result))
        record["ended_at"] = now_iso()
        record = redact_secrets(record)
        self.transcript["turns"].append(record)
        if record["status"] != "provider_error":
            self.history.extend([
                {"role": "user", "content": record["user"]},
                {"role": "assistant", "content": record["assistant_text"]},
            ])
        write_transcript(self.path, self.transcript)
        return record

    def export(self) -> str:
        return json.dumps(redact_secrets(self.transcript), ensure_ascii=False, indent=2, default=str)
