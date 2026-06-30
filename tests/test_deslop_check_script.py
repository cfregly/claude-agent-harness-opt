import subprocess
import sys
import unittest

from scripts import deslop_check


class DeslopCheckScriptTests(unittest.TestCase):
    def test_script_passes_current_repo(self):
        result = subprocess.run(
            [sys.executable, "scripts/deslop_check.py"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("deslop check passed", result.stdout)

    def test_forbidden_tokens_and_buzzwords_are_configured(self):
        self.assertEqual("em dash", deslop_check.FORBIDDEN["\u2014"])
        self.assertEqual("en dash", deslop_check.FORBIDDEN["\u2013"])
        self.assertIn("synergy", deslop_check.BUZZWORDS)
        self.assertIn("docs/*.md", deslop_check.CHECKED_GLOBS)


if __name__ == "__main__":
    unittest.main()
