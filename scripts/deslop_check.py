#!/usr/bin/env python3
"""Small prose gate for public markdown artifacts."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CHECKED_GLOBS = ("*.md", "docs/*.md", "prompts/*.md")
FORBIDDEN = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    ";": "semicolon",
}
BUZZWORDS = {
    "cutting-edge",
    "game-changing",
    "seamless",
    "synergy",
    "unlock",
    "delve",
    "leverage",
}


def main() -> int:
    failures: list[str] = []
    for pattern in CHECKED_GLOBS:
        for path in ROOT.glob(pattern):
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT)
            for token, label in FORBIDDEN.items():
                if token in text:
                    failures.append(f"{rel}: contains {label}")
            lower = text.lower()
            for word in BUZZWORDS:
                if word in lower:
                    failures.append(f"{rel}: contains buzzword '{word}'")

    if failures:
        print("\n".join(sorted(failures)))
        return 1
    print("deslop check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
