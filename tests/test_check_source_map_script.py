from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

from scripts.check_source_map import check_source_map


ROOT = Path(__file__).resolve().parents[1]


class CheckSourceMapScriptTests(unittest.TestCase):
    def test_script_passes_current_repo(self):
        result = subprocess.run(
            [sys.executable, "scripts/check_source_map.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("source map check passed", result.stdout)

    def test_rejects_missing_doc_source_url(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docs = root / "docs"
            docs.mkdir()
            (root / "README.md").write_text(
                "# sample\n\n## Sources\n\n[Source Map](https://example.org/source-map)\n",
                encoding="utf-8",
            )
            (docs / "source-map.md").write_text(
                textwrap.dedent(
                    """
                    # Source Map

                    Checked on 2026-06-30.

                    ## Known Sources

                    - [Known](https://known.example)
                      - Used for a known claim.
                    """
                ).lstrip(),
                encoding="utf-8",
            )
            (docs / "finding.md").write_text(
                "# finding\n\nSource: [Missing](https://missing.example/docs)\n",
                encoding="utf-8",
            )

            failures = check_source_map(root)

        joined = "\n".join(failures)
        self.assertIn("missing source URL from README.md: https://example.org/source-map", joined)
        self.assertIn("missing source URL from docs/finding.md: https://missing.example/docs", joined)
        self.assertIn("README.md: Sources section missing docs/source-map.md", joined)

    def test_accepts_mapped_sources_and_ignores_fenced_examples(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docs = root / "docs"
            docs.mkdir()
            (root / "README.md").write_text(
                "# sample\n\n"
                "See docs/source-map.md and docs/video-coverage-audit.md.\n"
                "Source: https://known.example\n",
                encoding="utf-8",
            )
            (docs / "source-map.md").write_text(
                textwrap.dedent(
                    """
                    # Source Map

                    Checked on 2026-06-30.

                    ## Known Sources

                    - [Known](https://known.example)
                      - Used for a known claim.
                    """
                ).lstrip(),
                encoding="utf-8",
            )
            (docs / "usage.md").write_text(
                textwrap.dedent(
                    """
                    # usage

                    ```bash
                    curl https://not-a-source.example
                    ```
                    """
                ),
                encoding="utf-8",
            )

            failures = check_source_map(root)

        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
