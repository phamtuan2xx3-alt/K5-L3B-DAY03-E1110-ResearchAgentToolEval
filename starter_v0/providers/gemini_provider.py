from __future__ import annotations

import json
import os
import time
from threading import Lock
from typing import Any

from providers.base import ModelResponse, ToolCall


def _to_gemini_declarations(tools: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    declarations: list[dict[str, Any]] = []
    for item in tools or []:
        function = item.get("function", item)
        declarations.append({
            "name": function["name"],
            "description": function.get("description", ""),
            "parameters": function.get("parameters", {"type": "object", "properties": {}}),
        })
    return declarations


def _to_gemini_contents(messages: list[dict[str, str]]) -> tuple[str | None, list[dict[str, Any]]]:
    system_parts: list[str] = []
    contents: list[dict[str, Any]] = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "system":
            system_parts.append(content)
        elif role == "assistant":
            contents.append({"role": "model", "parts": [{"text": content}]})
        elif role == "user":
            contents.append({"role": "user", "parts": [{"text": content}]})
    return ("\n\n".join(system_parts) if system_parts else None), contents


def _part_text(part: Any) -> str | None:
    if hasattr(part, "text"):
        return getattr(part, "text")
    if isinstance(part, dict):
        return part.get("text")
    return None


def _part_function_call(part: Any) -> Any | None:
    if hasattr(part, "function_call"):
        return getattr(part, "function_call")
    if isinstance(part, dict):
        return part.get("function_call")
    return None


def _function_call_name(call: Any) -> str | None:
    if hasattr(call, "name"):
        return getattr(call, "name")
    if isinstance(call, dict):
        return call.get("name")
    return None


def _function_call_args(call: Any) -> dict[str, Any]:
    if hasattr(call, "args"):
        return dict(getattr(call, "args") or {})
    if isinstance(call, dict):
        return dict(call.get("args") or {})
    return {}


class GeminiProvider:
    """Google Gemini API provider with normalized tool_calls output."""

    # Shared by provider instances in this process, including chat and retries.
    _request_lock = Lock()
    _last_request_at: float | None = None
    MIN_REQUEST_INTERVAL = 4.5  # below 15 RPM, with a small timing margin

    def __init__(
        self,
        *,
        api_key_env: str = "GEMINI_API_KEY",
        default_model: str = "gemini-3.5-flash-lite",
    ) -> None:
        self.api_key_env = api_key_env
        self.default_model = default_model
        self.last_model: str | None = None

    def _paced_generate(self, client: Any, **kwargs: Any) -> Any:
        with GeminiProvider._request_lock:
            previous = GeminiProvider._last_request_at
            if previous is not None:
                delay = self.MIN_REQUEST_INTERVAL - (time.monotonic() - previous)
                if delay > 0:
                    time.sleep(delay)
            GeminiProvider._last_request_at = time.monotonic()
            return client.models.generate_content(**kwargs)

    def _generate_with_retry(self, client: Any, *, model: str, contents: Any, config: Any) -> Any:
        self.last_model = None
        for attempt in range(3):
            try:
                response = self._paced_generate(client, model=model, contents=contents, config=config)
                self.last_model = model
                return response
            except Exception as exc:
                code = getattr(exc, "code", None)
                transport_error = isinstance(exc, (ConnectionError, TimeoutError)) or (
                    type(exc).__name__ in {"ConnectError", "ConnectTimeout", "ReadError", "ReadTimeout", "RemoteProtocolError"}
                    and type(exc).__module__.startswith(("httpx", "httpcore", "google.genai"))
                )
                if (code not in (429, 500, 502, 503, 504) and not transport_error) or attempt == 2:
                    raise
                print(f"Gemini {model}: {code or type(exc).__name__}; waiting 60 seconds before retry {attempt + 1}/2.", flush=True)
                time.sleep(60)

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError("Install live provider dependency first: pip install google-genai") from exc

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing API key env var: {self.api_key_env}")

        system_instruction, contents = _to_gemini_contents(messages)
        declarations = _to_gemini_declarations(tools)
        config_kwargs: dict[str, Any] = {"temperature": temperature}
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
        if declarations:
            config_kwargs["tools"] = [types.Tool(function_declarations=declarations)]

        client = genai.Client(api_key=api_key)
        resp = self._generate_with_retry(client,
            model=model or self.default_model,
            contents=contents,
            config=types.GenerateContentConfig(**config_kwargs),
        )

        text_parts: list[str] = []
        calls: list[ToolCall] = []

        def append_call(function_call: Any) -> None:
            name = _function_call_name(function_call)
            if name:
                calls.append(ToolCall(name=name, args=_function_call_args(function_call)))

        for candidate in getattr(resp, "candidates", []) or []:
            content = getattr(candidate, "content", None)
            for part in getattr(content, "parts", []) or []:
                text = _part_text(part)
                if text:
                    text_parts.append(text)
                function_call = _part_function_call(part)
                if function_call:
                    append_call(function_call)

        # Some SDK versions expose function calls directly on the response.
        for function_call in getattr(resp, "function_calls", []) or []:
            append_call(function_call)

        deduped_calls: list[ToolCall] = []
        seen: set[tuple[str, str]] = set()
        for call in calls:
            key = (call.name, json.dumps(call.args, ensure_ascii=False, sort_keys=True))
            if key not in seen:
                seen.add(key)
                deduped_calls.append(call)

        return ModelResponse(text="\n".join(part for part in text_parts if part) or None, tool_calls=deduped_calls, raw=resp)
