from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from claude_agent_harness_opt.tool_selection import (
    render_tool_selection_markdown,
    review_tool_selection_bundle,
)


ROOT = Path(__file__).resolve().parents[1]


class ToolSelectionTests(unittest.TestCase):
    def test_sample_bundle_passes_tool_selection_review(self):
        review = review_tool_selection_bundle(ROOT / "evals" / "examples" / "agent_audit_bundle.json")
        self.assertTrue(review.passed)
        self.assertEqual(1.0, review.score)

    def test_bad_bundle_recommends_description_and_schema_changes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle = Path(tmpdir) / "bundle.json"
            bundle.write_text(
                """{
  "tools": [
    {
      "name": "search",
      "purpose": "Search stuff.",
      "use_when": "Use it."
    }
  ],
  "tool_selection_cases": [],
  "traces": [
    {
      "name": "bad",
      "trace": "%s"
    }
  ]
}
"""
                % (ROOT / "evals" / "examples" / "agent_trace_bad.json"),
                encoding="utf-8",
            )
            review = review_tool_selection_bundle(bundle)
        self.assertFalse(review.passed)
        joined = "\n".join(review.recommendations)
        self.assertIn("input_schema", joined)
        self.assertIn("tool_selection_cases", joined)
        self.assertIn("heldout_tool_selection_cases", joined)

    def test_before_bundle_recommends_actionable_contract_changes(self):
        review = review_tool_selection_bundle(
            ROOT / "evals" / "examples" / "tool_tuning_before_bundle.json"
        )
        self.assertFalse(review.passed)
        joined = "\n".join(review.recommendations)
        self.assertIn("input_schema", joined)
        self.assertIn("tool_selection_cases", joined)
        self.assertIn("heldout_tool_selection_cases", joined)

    def test_selection_cases_require_verifiable_outcomes_without_exact_order(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle = Path(tmpdir) / "bundle.json"
            bundle.write_text(
                """{
  "tools": [
    {
      "name": "web_search",
      "purpose": "Find sources.",
      "use_when": "Use for unknown facts.",
      "avoid_when": "Avoid for known URLs.",
      "input_schema": {"properties": {"query": "Search query"}, "required": ["query"]},
      "output_schema": {"results": "Source candidates"},
      "context_controls": ["query specificity"],
      "error_guidance": "Ask for a narrower query.",
      "quality_checks": ["Prefer primary sources"]
    }
  ],
  "tool_selection_cases": [
    {
      "name": "too exact",
      "task": "Find a source.",
      "expected_tools": ["web_search"],
      "required_sequence": ["web_search"],
      "rationale": "Search is required."
    }
  ],
  "heldout_tool_selection_cases": [
    {
      "name": "heldout",
      "task": "Find another source.",
      "expected_tools": ["web_search"],
      "rationale": "Search is required.",
      "verifier": {"type": "flexible_text", "must_include_any": [["source"]]}
    }
  ],
  "traces": []
}
""",
                encoding="utf-8",
            )
            review = review_tool_selection_bundle(bundle)

        failed = {finding.check for finding in review.findings if not finding.passed}
        self.assertIn("selection_cases.verifiable_outcome", failed)
        self.assertIn("selection_cases.avoids_exact_strategy", failed)

    def test_markdown_renderer(self):
        review = review_tool_selection_bundle(ROOT / "evals" / "examples" / "agent_audit_bundle.json")
        markdown = render_tool_selection_markdown(review)
        self.assertIn("# Tool Selection Optimizer", markdown)
        self.assertIn("Passed: yes", markdown)

    def test_cli_optimize_tools(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "claude_agent_harness_opt",
                "optimize-tools",
                "evals/examples/agent_audit_bundle.json",
                "--markdown",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("# Tool Selection Optimizer", result.stdout)

    def test_cli_optimize_tools_before_bundle_fails_with_recommendations(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "claude_agent_harness_opt",
                "optimize-tools",
                "evals/examples/tool_tuning_before_bundle.json",
                "--markdown",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Passed: no", result.stdout)
        self.assertIn("input_schema", result.stdout)


if __name__ == "__main__":
    unittest.main()
