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


if __name__ == "__main__":
    unittest.main()
