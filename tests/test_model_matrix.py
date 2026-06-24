from pathlib import Path
import tempfile
import unittest

from claude_agent_prompting.model_matrix import (
    MatrixFilters,
    evaluate_model_choice,
    load_env_file,
    run_model_matrix,
)


ROOT = Path(__file__).resolve().parents[1]


class ModelMatrixTests(unittest.TestCase):
    def test_load_env_file_reads_keys_without_shelling_out(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_path = Path(tmpdir) / ".env"
            env_path.write_text(
                "export ANTHROPIC_API_KEY='test-anthropic'\nOPENAI_API_KEY=\"test-openai\"\n",
                encoding="utf-8",
            )
            values = load_env_file(env_path)
        self.assertEqual("test-anthropic", values["ANTHROPIC_API_KEY"])
        self.assertEqual("test-openai", values["OPENAI_API_KEY"])

    def test_evaluate_model_choice_checks_expected_forbidden_and_args(self):
        result = evaluate_model_choice(
            {"arguments": {"pattern": "**/*.py"}, "tool_name": "Glob"},
            {
                "expected_args_contains": {"pattern": "*.py"},
                "expected_tools": ["Glob"],
                "forbidden_tools": ["Grep", "Read"],
            },
        )
        self.assertTrue(result["passed"])

    def test_evaluate_model_choice_fails_wrong_tool(self):
        result = evaluate_model_choice(
            {"arguments": {"path": "README.md"}, "tool_name": "Read"},
            {
                "expected_tools": ["Grep"],
                "forbidden_tools": ["Read"],
            },
        )
        self.assertFalse(result["passed"])
        self.assertEqual(["Grep"], result["missing_expected"])
        self.assertEqual(["Read"], result["forbidden_used"])

    def test_dry_run_model_matrix_plans_selected_cells(self):
        result = run_model_matrix(
            ROOT / "evals" / "model_matrix" / "coding_tool_selection.json",
            filters=MatrixFilters(
                providers={"anthropic"},
                harnesses={"prompt_json"},
                variants={"tuned_boundaries"},
                instruction_variants={"boundary_rules"},
            ),
            max_cases=2,
        )
        self.assertTrue(result["passed"])
        self.assertFalse(result["live"])
        self.assertEqual(2, result["summary"]["total"])
        self.assertEqual("planned", result["results"][0]["status"])


if __name__ == "__main__":
    unittest.main()
