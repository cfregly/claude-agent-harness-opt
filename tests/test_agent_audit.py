from pathlib import Path
import subprocess
import sys
import unittest

from claude_agent_prompting.agent_audit import review_agent_bundle


ROOT = Path(__file__).resolve().parents[1]


def fake_claude_request(payload, headers, url, timeout):
    return {
        "content": [
            {
                "type": "text",
                "text": (
                    '{"passed": true, "score": 0.93, "scores": {'
                    '"tool_effectiveness": 0.95, "reasoning_quality": 0.9, '
                    '"tool_output_use": 0.95, "final_answer_grounding": 0.9, '
                    '"value_over_baseline": 0.95}, "findings": ["good"], '
                    '"recommended_changes": []}'
                ),
            }
        ]
    }


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

    def test_agent_bundle_can_require_claude_judge(self):
        result = review_agent_bundle(
            ROOT / "evals" / "examples" / "agent_audit_bundle.json",
            claude_judge=True,
            judge_api_key="test-key",
            judge_model="claude-test",
            judge_request_fn=fake_claude_request,
            require_claude_judge=True,
        )
        self.assertTrue(result["passed"])
        self.assertTrue(result["claude_judge"]["enabled"])
        self.assertTrue(result["claude_judge"]["required"])
        self.assertEqual(0.93, result["claude_judge"]["traces"][0]["score"])


if __name__ == "__main__":
    unittest.main()
