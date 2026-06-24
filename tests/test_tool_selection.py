from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from claude_agent_prompting.tool_selection import (
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
                "claude_agent_prompting",
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


if __name__ == "__main__":
    unittest.main()
