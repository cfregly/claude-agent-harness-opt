import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "claude_agent_prompting", *args],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

    def test_render_command(self):
        result = self.run_cli("render", "recipes/agentic_search.json")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("<operating_loop>", result.stdout)
        self.assertIn("<value_bar>", result.stdout)

    def test_score_command(self):
        result = self.run_cli("score", "recipes/agentic_search.json")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"verdict": "agent"', result.stdout)

    def test_eval_command(self):
        result = self.run_cli("eval", "evals/examples/search_answer.json")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"passed": true', result.stdout)

    def test_model_matrix_command(self):
        result = self.run_cli(
            "model-matrix",
            "evals/model_matrix/coding_tool_selection.json",
            "--providers",
            "anthropic",
            "--harnesses",
            "native_tools",
            "--variants",
            "tuned_boundaries",
            "--instruction-variants",
            "boundary_rules",
            "--max-cases",
            "1",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"matrix": "coding file-tool selection matrix"', result.stdout)

    def test_claude_judge_requires_api_key(self):
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "claude_agent_prompting",
                "review-trace",
                "evals/examples/agent_trace_good.json",
                "--claude-judge",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("ANTHROPIC_API_KEY is required", result.stdout)


if __name__ == "__main__":
    unittest.main()
