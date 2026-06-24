"""Adapters that normalize provider transcripts into trace-review events."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def claude_messages_to_trace(payload: dict[str, Any] | list[dict[str, Any]]) -> dict[str, Any]:
    """Normalize Claude-style Messages API content blocks into trace steps."""

    if isinstance(payload, list):
        messages = payload
        name = "claude_trace"
        task = ""
        rubric = {}
    else:
        messages = payload.get("messages", [])
        name = payload.get("name", "claude_trace")
        task = payload.get("task", "")
        rubric = payload.get("rubric", {})

    steps: list[dict[str, Any]] = []
    for message in messages:
        role = message.get("role")
        content = _content_blocks(message.get("content", []))
        for index, block in enumerate(content):
            block_type = block.get("type")
            if role == "assistant":
                if block_type == "thinking":
                    steps.append(
                        {
                            "source": "claude_thinking",
                            "summary": block.get("thinking", ""),
                            "signature_present": bool(block.get("signature")),
                            "type": "reasoning",
                        }
                    )
                elif block_type == "redacted_thinking":
                    steps.append(
                        {
                            "opaque": True,
                            "source": "claude_redacted_thinking",
                            "summary": "",
                            "type": "reasoning",
                        }
                    )
                elif block_type == "tool_use":
                    steps.append(
                        {
                            "args": block.get("input", {}),
                            "id": block.get("id"),
                            "name": block.get("name"),
                            "type": "tool_call",
                        }
                    )
                elif block_type == "text":
                    step_type = "reasoning" if _has_later_tool_use(content, index) else "final"
                    key = "summary" if step_type == "reasoning" else "text"
                    steps.append(
                        {
                            key: block.get("text", ""),
                            "source": "assistant_text" if step_type == "reasoning" else "assistant_final_text",
                            "type": step_type,
                        }
                    )
            elif role == "user" and block_type == "tool_result":
                steps.append(
                    {
                        "ok": not bool(block.get("is_error", False)),
                        "output": _stringify_tool_result(block.get("content", "")),
                        "tool_call_id": block.get("tool_use_id"),
                        "type": "tool_result",
                    }
                )

    return {
        "name": name,
        "rubric": rubric,
        "steps": steps,
        "task": task,
    }


def runtime_events_to_trace(payload: dict[str, Any] | list[dict[str, Any]]) -> dict[str, Any]:
    """Normalize generic Agent SDK or IDE-agent event exports into trace steps."""

    if isinstance(payload, list):
        events = payload
        name = "runtime_trace"
        task = ""
        rubric = {}
        harness = ""
    else:
        events = _runtime_events(payload)
        name = payload.get("name", "runtime_trace")
        task = payload.get("task", "")
        rubric = payload.get("rubric", {})
        harness = payload.get("harness", payload.get("source_harness", ""))

    steps = [_runtime_event_to_step(event) for event in events if isinstance(event, dict)]
    steps = [step for step in steps if step]
    return {
        "metadata": {"source_harness": harness} if harness else {},
        "name": name,
        "rubric": rubric,
        "steps": steps,
        "task": task,
    }


def _content_blocks(content: Any) -> list[dict[str, Any]]:
    if isinstance(content, str):
        return [{"text": content, "type": "text"}]
    if isinstance(content, list):
        return [block for block in content if isinstance(block, dict)]
    return []


def _runtime_events(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("events", "steps", "trace", "messages"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    run = payload.get("run")
    if isinstance(run, dict):
        value = run.get("events")
        if isinstance(value, list):
            return value
    return []


def _runtime_event_to_step(event: dict[str, Any]) -> dict[str, Any]:
    event_type = _event_type(event)
    if event_type in {"reasoning", "thinking", "assistant_thinking", "thought", "plan", "reflection", "decision"}:
        return {
            "source": event.get("source", event_type),
            "summary": _first_text(event, "summary", "text", "thinking", "message", "content"),
            "type": "reasoning",
        }
    if event_type in {"tool_call", "tool_use", "function_call", "mcp_call", "action"}:
        return {
            "args": _event_args(event),
            "id": _first_value(event, "id", "call_id", "tool_call_id", "tool_use_id"),
            "name": _first_value(event, "tool", "tool_name", "name", "function", "action"),
            "parallel_group": _first_value(event, "parallel_group", "batch_id"),
            "type": "tool_call",
        }
    if event_type in {"tool_result", "tool_output", "observation", "result", "mcp_result"}:
        return {
            "ok": not bool(event.get("error") or event.get("is_error")),
            "output": _first_text(event, "output", "result", "content", "text", "message"),
            "parallel_group": _first_value(event, "parallel_group", "batch_id"),
            "tool_call_id": _first_value(event, "tool_call_id", "call_id", "tool_use_id", "id"),
            "type": "tool_result",
        }
    if event_type in {"final", "assistant_final", "final_answer", "message"}:
        return {
            "text": _first_text(event, "text", "message", "content", "output"),
            "type": "final",
        }
    if _looks_like_tool_result(event):
        return _runtime_event_to_step({**event, "type": "tool_result"})
    if _looks_like_tool_call(event):
        return _runtime_event_to_step({**event, "type": "tool_call"})
    if _looks_like_reasoning(event):
        return _runtime_event_to_step({**event, "type": "reasoning"})
    return {}


def _event_type(event: dict[str, Any]) -> str:
    value = _first_value(event, "type", "event", "kind", "role")
    text = str(value).strip()
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", text)
    return text.lower().replace("-", "_").replace(".", "_")


def _event_args(event: dict[str, Any]) -> dict[str, Any]:
    for key in ("args", "arguments", "input", "parameters", "tool_input"):
        value = event.get(key)
        if isinstance(value, dict):
            return value
        if isinstance(value, str) and value.strip().startswith("{"):
            try:
                decoded = json.loads(value)
            except json.JSONDecodeError:
                decoded = None
            if isinstance(decoded, dict):
                return decoded
    for key in ("function", "tool_call", "toolCall"):
        value = event.get(key)
        if isinstance(value, dict):
            args = _event_args(value)
            if args:
                return args
    return {}


def _first_value(event: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = event.get(key)
        if value not in (None, ""):
            return value
        camel = _to_camel_case(key)
        value = event.get(camel)
        if value not in (None, ""):
            return value
        for nested_key in ("function", "tool_call", "toolCall"):
            nested = event.get(nested_key)
            if not isinstance(nested, dict):
                continue
            value = nested.get(key)
            if value not in (None, ""):
                return value
            value = nested.get(camel)
            if value not in (None, ""):
                return value
    return ""


def _to_camel_case(key: str) -> str:
    parts = key.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


def _first_text(event: dict[str, Any], *keys: str) -> str:
    value = _first_value(event, *keys)
    if isinstance(value, str):
        return value
    if value in (None, ""):
        return ""
    return json.dumps(value, sort_keys=True)


def _looks_like_tool_call(event: dict[str, Any]) -> bool:
    return bool(_first_value(event, "tool", "tool_name", "function")) and any(
        key in event for key in ("args", "arguments", "input", "parameters", "tool_input", "toolInput")
    )


def _looks_like_tool_result(event: dict[str, Any]) -> bool:
    return bool(_first_value(event, "tool_call_id", "tool_use_id", "call_id")) and any(
        key in event for key in ("output", "result", "content", "error")
    )


def _looks_like_reasoning(event: dict[str, Any]) -> bool:
    return bool(_first_value(event, "summary", "thinking")) and not _looks_like_tool_call(event)


def _has_later_tool_use(content: list[dict[str, Any]], index: int) -> bool:
    return any(block.get("type") == "tool_use" for block in content[index + 1 :])


def _stringify_tool_result(content: Any) -> str:
    if isinstance(content, str):
        return content
    return json.dumps(content, sort_keys=True)
