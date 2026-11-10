"""Streamlit-independent session logic, transcript persistence and send approval."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from chat import execute_tool_call, now_iso, run_model_tool_loop, trim_history
from env_loader import load_lab_env
from providers import make_provider
from providers.base import ToolCall
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).resolve().parent


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        for key, secret in os.environ.items():
            if ("API_KEY" in key or "TOKEN" in key or key == "DEMO_ACCESS_CODE") and len(secret) >= 8:
                value = value.replace(secret, "[REDACTED]")
    return value


class ResearchSession:
    def __init__(self, provider_name: str = "gemini", model: str = "gemini-3.5-flash-lite", *, root: Path = ROOT) -> None:
        self.root = root
        self.provider_name = provider_name
        self.model = model
        self.history: list[dict[str, str]] = []
        self.pending_send: str | None = None
        self.pending_target: str | None = None
        self.prompt = (root / "artifacts/system_prompt.md").read_text(encoding="utf-8")
        self.tools = to_openai_tools(load_tool_declarations(root / "artifacts/tools.yaml"))
        version = build_artifact_version("cp3-ui", root / "artifacts/system_prompt.md", root / "artifacts/tools.yaml")
        session_id = f"cp3_ui_{uuid4().hex}"
        self.path = root / "transcripts" / f"{session_id}.transcript.json"
        self.transcript = {"transcript_id": session_id, **artifact_version_dict(version), "origin": "streamlit",
                           "provider": provider_name, "model": model, "created_at": now_iso(), "turns": []}

    def _record(self, user: str, result: dict[str, Any]) -> dict[str, Any]:
        turn = redact({"turn_index": len(self.transcript["turns"]) + 1, "user": user, "ended_at": now_iso(), **result})
        self.transcript["turns"].append(turn)
        self.transcript["updated_at"] = now_iso()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(redact(self.transcript), ensure_ascii=False, indent=2), encoding="utf-8")
        self.history.extend([{"role": "user", "content": user}, {"role": "assistant", "content": result.get("assistant_text", "")}])
        return turn

    def _guarded_execute(self, call: ToolCall) -> dict[str, Any]:
        if call.name != "send":
            return execute_tool_call(call)
        text = call.args.get("text")
        if not isinstance(text, str) or not text.strip():
            return {"tool": "send", "args": call.args, "result": {"error": "missing_content", "message": "Cần nội dung cụ thể trước khi gửi."}}
        self.pending_send = text
        self.pending_target = os.getenv("TELEGRAM_CHAT_ID", "")
        return {"tool": "send", "args": call.args, "result": {"awaiting_user": True, "status": "pending_ui_approval",
                "question": "Bản tin đã sẵn sàng. Hãy đọc nội dung bên dưới và chọn Xác nhận và gửi để đăng lên kênh nhóm."}}

    def run(self, user: str, *, provider: Any = None) -> dict[str, Any]:
        if self.pending_send is not None:
            raise ValueError("Resolve the pending send before starting another turn")
        load_lab_env(self.root)
        try:
            result = run_model_tool_loop(provider=provider or make_provider(self.provider_name),
                        messages=[{"role": "system", "content": self.prompt}, *trim_history(self.history, 6), {"role": "user", "content": user}],
                        tools=self.tools, model=self.model, max_tool_rounds=4, tool_executor=self._guarded_execute)
        except Exception as exc:
            result = {"status": "provider_error", "error": redact(f"{type(exc).__name__}: {exc}"),
                      "assistant_text": "Chưa hoàn tất yêu cầu do lỗi kết nối hoặc provider. Xem chi tiết lỗi bên dưới.", "rounds": [], "tool_events": []}
        return self._record(user, result)

    def resolve_send(self, approved: bool, *, executor: Callable[[ToolCall], dict[str, Any]] = execute_tool_call) -> dict[str, Any]:
        if self.pending_send is None:
            raise ValueError("No pending send")
        text = self.pending_send
        target = self.pending_target
        # Consume approval before network I/O; a rerun must not send twice.
        self.pending_send = None
        self.pending_target = None
        if not approved:
            return self._record("Hủy gửi bản tin đang chờ duyệt.", {"status": "cancelled", "assistant_text": "Đã hủy. Chưa gửi tin lên Telegram.", "tool_events": [], "rounds": []})
        load_lab_env(self.root)
        if target is not None and os.getenv("TELEGRAM_CHAT_ID", "") != target:
            return self._record("Xác nhận gửi bản tin đang chờ duyệt.", {"status": "target_changed",
                                "assistant_text": "Kênh nhận đã thay đổi. Chưa gửi tin; hãy tạo lại yêu cầu và kiểm tra kênh mới.", "tool_events": [], "rounds": []})
        event = executor(ToolCall(name="send", args={"text": text, "confirmed": True}))
        sent = event.get("result", {}).get("status") == "sent"
        return self._record("Tôi xác nhận gửi đúng nội dung sau lên kênh Telegram đã cấu hình:\n" + text,
                            {"status": "sent" if sent else "tool_error", "origin": "user_confirmation",
                             "assistant_text": "Đã gửi bản tin lên Telegram." if sent else "Chưa xác nhận gửi thành công. Xem kết quả tool; không tự thử gửi lại.",
                             "tool_events": [event], "rounds": []})
