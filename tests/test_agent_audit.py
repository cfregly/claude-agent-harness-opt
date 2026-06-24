from pathlib import Path
import subprocess
import sys
import unittest

from claude_agent_prompting.agent_audit import review_agent_bundle


ROOT = Path(__file__).resolve().parents[1]


class AgentAuditTests(unittest.TestCase):
    def test_agent_bundle_passes(self):
        result = review_agent_bundle(ROOT / "evals" / "examples" / "agent_audit_bundle.json")
        self.assertTrue(result["passed"])
        self.assertEqual(1.0, result["overall_score"])
        self.assertTrue(result["value_bar"]["passed"])

    def test_cli_agent_audit_markdown(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "claude_agent_prompting",
                "audit-agent",
                "evals/examples/agent_audit_bundle.json",
                "--markdown",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("# sample research agent audit", result.stdout)
        self.assertIn("## Value Bar", result.stdout)

    def test_agent_bundle_missing_value_bar_fails(self):
        result = review_agent_bundle(
            ROOT / "evals" / "examples" / "agent_audit_missing_value_bar.json"
        )
        self.assertFalse(result["passed"])
        self.assertEqual(0.0, result["value_bar"]["score"])
        self.assertIn("missing value_bar", result["value_bar"]["details"][0])


if __name__ == "__main__":
    unittest.main()
