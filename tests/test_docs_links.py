from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ALLOWED_PREFIXES = ("https://", "http://", "#", "mailto:")


class DocsLinksTests(unittest.TestCase):
    def test_readme_and_docs_use_shareable_markdown_links(self):
        paths = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]

        failures: list[str] = []
        for path in paths:
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT)
            for match in MARKDOWN_LINK_RE.finditer(text):
                target = match.group(1).strip()
                if not target.startswith(ALLOWED_PREFIXES):
                    failures.append(f"{rel}: {target}")

        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
