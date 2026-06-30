from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_regression_ownership import check_regression_ownership


ROOT = Path(__file__).resolve().parents[1]


class CheckRegressionOwnershipScriptTests(unittest.TestCase):
    def test_script_passes_current_repo(self):
        result = subprocess.run(
            [sys.executable, "scripts/check_regression_ownership.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("regression ownership check passed", result.stdout)

    def test_accepts_minimal_owned_sources(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _touch(root / "claude_agent_harness_opt" / "__init__.py")
            _touch(root / "claude_agent_harness_opt" / "__main__.py")
            _touch(root / "claude_agent_harness_opt" / "example.py")
            _touch(root / "scripts" / "check_example.py")
            _touch(root / "tests" / "test_check_package_surface_script.py")
            _touch(root / "tests" / "test_cli.py")
            _touch(root / "tests" / "test_example.py")
            _touch(root / "tests" / "test_check_example_script.py")

            failures = check_regression_ownership(root)

        self.assertEqual([], failures)

    def test_rejects_missing_package_and_script_owners(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _touch(root / "claude_agent_harness_opt" / "unowned.py")
            _touch(root / "scripts" / "utility.py")

            failures = check_regression_ownership(root)

        joined = "\n".join(failures)
        self.assertIn("claude_agent_harness_opt/unowned.py: missing regression owner tests/test_unowned.py", joined)
        self.assertIn("scripts/utility.py: missing regression owner mapping", joined)


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("sample\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
