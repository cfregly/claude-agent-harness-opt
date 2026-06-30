import json
from pathlib import Path
import sys
import tempfile
import unittest

from claude_agent_harness_opt.live_harness import (
    LiveHarnessFilters,
    render_live_harness_markdown,
    run_live_harness_spec,
)


ROOT = Path(__file__).resolve().parents[1]


class LiveHarnessTests(unittest.TestCase):
    def test_dry_run_renders_selected_command_and_markdown(self):
        spec = {
            "name": "dry live harness",
            "cases": [
                {
                    "name": "pwd case",
                    "prompt_template": "Run {shell_command}. HARNESS_OK {marker}",
                    "required_marker_template": "HARNESS_OK {marker}",
                    "shell_command": "pwd",
                }
            ],
            "harnesses": [
                {
                    "name": "fake_harness",
                    "marker": "fake",
                    "adapter": "codex_jsonl",
                    "command": ["echo", "{prompt}"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            spec_path = Path(temp_dir) / "live.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")

            result = run_live_harness_spec(
                spec_path,
                out_dir=Path(temp_dir) / "artifacts",
                filters=LiveHarnessFilters(harnesses={"fake_harness"}, cases={"pwd case"}),
                dry_run=True,
            )

        self.assertTrue(result["passed"])
        self.assertEqual({"planned": 1, "passed": 0, "failed": 0, "errors": 0, "not_installed": 0, "directed_thinking_visible": 0}, result["summary"])
        self.assertEqual(["echo", "Run pwd. HARNESS_OK fake"], result["results"][0]["command"])
        self.assertIn("fake_harness", render_live_harness_markdown(result))

    def test_fake_local_harness_normalizes_trace_and_redacts_env_file_values(self):
        fake_events = [
            {
                "type": "item.started",
                "item": {
                    "id": "call_1",
                    "type": "command_execution",
                    "command": "pwd",
                    "status": "in_progress",
                },
            },
            {
                "type": "item.completed",
                "item": {
                    "id": "call_1",
                    "type": "command_execution",
                    "command": "pwd",
                    "aggregated_output": str(ROOT),
                    "status": "completed",
                },
            },
            {
                "type": "item.completed",
                "item": {
                    "id": "message_1",
                    "type": "agent_message",
                    "text": f"HARNESS_OK fake {ROOT} secret-value-123",
                },
            },
        ]
        code = "import json; events = " + repr(fake_events) + "; [print(json.dumps(item)) for item in events]"
        spec = {
            "name": "fake live harness",
            "cases": [
                {
                    "name": "fake pwd",
                    "prompt_template": "Run {shell_command}. HARNESS_OK {marker}",
                    "required_marker_template": "HARNESS_OK {marker}",
                }
            ],
            "harnesses": [
                {
                    "name": "fake_codex",
                    "marker": "fake",
                    "adapter": "codex_jsonl",
                    "command": [sys.executable, "-c", code],
                    "expected_args_contains": {"command": "pwd"},
                    "expected_tool": "Bash",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            spec_path = root / "fake-live-harness.json"
            env_path = root / ".env"
            out_dir = root / "artifacts"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            env_path.write_text("TOKEN=secret-value-123\n", encoding="utf-8")

            result = run_live_harness_spec(spec_path, env_file=env_path, out_dir=out_dir)
            combined = Path(result["results"][0]["artifacts"]["combined"]).read_text(encoding="utf-8")

        self.assertTrue(result["passed"])
        self.assertEqual("passed", result["results"][0]["status"])
        self.assertTrue(result["results"][0]["tool_use_passed"])
        self.assertIn("[REDACTED]", combined)
        self.assertNotIn("secret-value-123", combined)


if __name__ == "__main__":
    unittest.main()
