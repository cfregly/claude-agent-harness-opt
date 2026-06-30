from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_cli_coverage import check_cli_coverage


ROOT = Path(__file__).resolve().parents[1]


class CheckCliCoverageScriptTests(unittest.TestCase):
    def test_script_passes_current_repo(self):
        result = subprocess.run(
            [sys.executable, "scripts/check_cli_coverage.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CLI coverage check passed", result.stdout)

    def test_cli_coverage_rejects_missing_and_unknown_commands(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workflow = root / ".github" / "workflows"
            workflow.mkdir(parents=True)
            (workflow / "ci.yml").write_text(
                "\n".join(
                    [
                        "steps:",
                        "  - run: python -m claude_agent_harness_opt known",
                        "  - run: python -m claude_agent_harness_opt stale",
                    ]
                ),
                encoding="utf-8",
            )

            failures = check_cli_coverage(root, cli_commands={"known", "missing"})

        joined = "\n".join(failures)
        self.assertIn("missing direct CLI smoke for missing", joined)
        self.assertIn("unknown CLI command stale", joined)


if __name__ == "__main__":
    unittest.main()
