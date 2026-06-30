from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_command_surfaces import (
    _extract_cli_invocations,
    check_command_surfaces,
)


ROOT = Path(__file__).resolve().parents[1]


class CheckCommandSurfacesScriptTests(unittest.TestCase):
    def test_script_passes_current_repo(self):
        result = subprocess.run(
            [sys.executable, "scripts/check_command_surfaces.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("command surface check passed", result.stdout)

    def test_command_surface_check_rejects_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "scripts").mkdir()
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "fixtures").mkdir()
            (root / "fixtures" / "known.json").write_text("{}", encoding="utf-8")
            (root / "scripts" / "check_example.py").write_text("print('ok')\n", encoding="utf-8")
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "python -m claude_agent_harness_opt known-command fixtures/known.json",
                        "python -m claude_agent_harness_opt stale-command fixtures/missing.json",
                    ]
                ),
                encoding="utf-8",
            )
            (root / ".github" / "workflows" / "ci.yml").write_text(
                "steps:\n  - run: python scripts/check_example.py\n",
                encoding="utf-8",
            )

            failures = check_command_surfaces(root, cli_commands={"known-command"})

        joined = "\n".join(failures)
        self.assertIn("scripts/check_example.py: missing from README Verify it commands", joined)
        self.assertIn("scripts/check_example.py: missing test file", joined)
        self.assertIn("unknown CLI command 'stale-command'", joined)
        self.assertIn("missing local path 'fixtures/missing.json'", joined)

    def test_extract_cli_invocations_handles_multiline_commands(self):
        invocations = _extract_cli_invocations(
            Path("README.md"),
            """python -m claude_agent_harness_opt model-matrix \\
  evals/model_matrix/coding_tool_selection.json \\
  --providers anthropic
""",
        )

        self.assertEqual(1, len(invocations))
        self.assertEqual("model-matrix", invocations[0].command)
        self.assertIn("evals/model_matrix/coding_tool_selection.json", invocations[0].tokens)


if __name__ == "__main__":
    unittest.main()
