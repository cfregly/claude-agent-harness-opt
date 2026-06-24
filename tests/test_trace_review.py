from pathlib import Path
import subprocess
import sys
import unittest

from claude_agent_prompting.trace_review import load_trace, review_trace


ROOT = Path(__file__).resolve().parents[1]


class TraceReviewTests(unittest.TestCase):
    def test_good_trace_passes(self):
        result = review_trace(load_trace(ROOT / "evals" / "examples" / "agent_trace_good.json"))
        self.assertTrue(result.passed)
        self.assertEqual(1.0, result.score)

    def test_bad_trace_fails(self):
        result = review_trace(load_trace(ROOT / "evals" / "examples" / "agent_trace_bad.json"))
        self.assertFalse(result.passed)
        self.assertLess(result.score, 1.0)

    def test_parallel_trace_passes(self):
        result = review_trace(
            load_trace(ROOT / "evals" / "examples" / "agent_trace_parallel_good.json")
        )
        self.assertTrue(result.passed)
        self.assertEqual(1.0, result.score)
        details = "\n".join(finding.detail for finding in result.findings)
        self.assertIn("parallel group 'initial_research'", details)

    def test_directed_thinking_requires_specific_content(self):
        trace = {
            "rubric": {
                "pass_score": 1.0,
                "require_directed_after_tool_reasoning": True,
                "require_directed_initial_reasoning": True,
            },
            "steps": [
                {"type": "reasoning", "summary": "I should look something up."},
                {"type": "tool_call", "id": "call_1", "name": "web_search", "args": {}},
                {"type": "tool_result", "tool_call_id": "call_1", "ok": True, "output": "result"},
                {"type": "reasoning", "summary": "Looks fine."},
                {"type": "final", "text": "Done."},
            ],
        }

        result = review_trace(trace)
        failed = {finding.check for finding in result.findings if not finding.passed}
        self.assertIn("reasoning.initial_complexity", failed)
        self.assertIn("reasoning.initial_tool_budget", failed)
        self.assertIn("reasoning.initial_evidence_stop", failed)
        self.assertIn("reasoning.after_tool_verification", failed)
        self.assertIn("reasoning.after_tool_next_decision", failed)

    def test_cli_review_trace(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "claude_agent_prompting",
                "review-trace",
                "evals/examples/agent_trace_good.json",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"passed": true', result.stdout)


if __name__ == "__main__":
    unittest.main()
