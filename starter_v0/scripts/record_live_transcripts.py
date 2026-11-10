#!/usr/bin/env python3
"""Record required live-chat transcripts without an interactive TTY."""
from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chat import run_model_tool_loop, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

load_lab_env(ROOT)


SCENARIOS: list[dict[str, Any]] = [
    {
        "name": "research_normal",
        "turns": [
            "Tin tức AI hôm nay có gì nổi bật?",
        ],
    },
    {
        "name": "missing_then_fill",
        "turns": [
            "Tóm tắt 5 tweet mới nhất giúp mình",
            "Handle là sama",
        ],
    },
    {
        "name": "send_confirm",
        "turns": [
            "Đăng bản tin này lên Telegram giúp mình: AI digest demo",
            "Không, dừng lại",
        ],
    },
]


def record_scenario(name: str, user_turns: list[str], *, sleep_s: float = 5.0) -> Path:
    system_prompt_path = ROOT / "artifacts" / "system_prompt.md"
    tools_path = ROOT / "artifacts" / "tools.yaml"
    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    tools = to_openai_tools(load_tool_declarations(tools_path))
    provider = make_provider("gemini")
    model = "gemini-3.5-flash-lite"
    artifact_version = build_artifact_version("v3", system_prompt_path, tools_path)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = f"v3_gemini_{timestamp}_{name}"
    path = ROOT / "transcripts" / f"{transcript_id}.transcript.json"
    transcript: dict[str, Any] = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": "gemini",
        "model": model,
        "scenario": name,
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "turns": [],
    }
    history: list[dict[str, str]] = []
    for index, user_text in enumerate(user_turns, start=1):
        if index > 1:
            time.sleep(sleep_s)
        messages = [
            {"role": "system", "content": system_prompt},
            *trim_history(history, 5),
            {"role": "user", "content": user_text},
        ]
        turn: dict[str, Any] = {
            "turn_index": index,
            "started_at": datetime.now().isoformat(timespec="seconds"),
            "user": user_text,
        }
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=tools,
            model=model,
            max_tool_rounds=4,
        )
        turn.update(result)
        turn["ended_at"] = datetime.now().isoformat(timespec="seconds")
        transcript["turns"].append(turn)
        history.append({"role": "user", "content": user_text})
        history.append({"role": "assistant", "content": result["assistant_text"]})
        write_transcript(path, transcript)
        print(f"[{name}] turn {index}: status={result['status']} tools={[e['tool'] for e in result.get('tool_events', [])]}")
    print(f"Saved {path}")
    return path


def main() -> None:
    for scenario in SCENARIOS:
        record_scenario(scenario["name"], scenario["turns"])
        time.sleep(8)


if __name__ == "__main__":
    main()
