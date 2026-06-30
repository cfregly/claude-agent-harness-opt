#!/usr/bin/env python3
"""Validate shareable finding packets and local evidence links."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINDINGS_DIR = ROOT / "docs" / "findings"
REPO_LINK_RE = re.compile(
    r"https://github\.com/cfregly/claude-agent-harness-opt/(?:blob|tree)/main/([^)\s]+)"
)
LOCAL_ARTIFACT_RE = re.compile(r"`((?:docs|evals|README\.md)[^`]+)`")
MATRIX_LINK_RE = re.compile(r"evals/model_matrix/[^)`\s]+\.json")
REQUIRED_PACKET_SECTIONS = ("## Result", "## Evidence", "## Reproduce")
REQUIRED_PACKET_FILES = ("README.md",)
REQUIRED_PACKET_ARTIFACT_PREFIXES = (
    "docs/",
    "evals/model_matrix/",
    "evals/results/",
    "evals/pr_packets/",
)


def main() -> int:
    failures = check_finding_packets()
    if failures:
        print("\n".join(sorted(failures)))
        return 1
    print("finding packet check passed")
    return 0


def check_finding_packets() -> list[str]:
    failures: list[str] = []
    index_text = _read_required(FINDINGS_DIR / "README.md", failures)
    ledger_text = _read_required(ROOT / "docs" / "confirmed-improvements.md", failures)
    if not index_text or not ledger_text:
        return failures

    packet_dirs = [
        path
        for path in sorted(FINDINGS_DIR.iterdir())
        if path.is_dir()
    ]
    if not packet_dirs:
        return ["docs/findings: no finding packet directories found"]

    for packet_dir in packet_dirs:
        failures.extend(_check_packet_dir(packet_dir, index_text, ledger_text))
    failures.extend(_check_repo_links(FINDINGS_DIR / "README.md", index_text))
    failures.extend(_check_repo_links(ROOT / "docs" / "confirmed-improvements.md", ledger_text))
    return failures


def _check_packet_dir(packet_dir: Path, index_text: str, ledger_text: str) -> list[str]:
    failures: list[str] = []
    rel_dir = packet_dir.relative_to(ROOT)
    slug = packet_dir.name
    for filename in REQUIRED_PACKET_FILES:
        path = packet_dir / filename
        if not path.exists():
            failures.append(f"{rel_dir}: missing {filename}")
            return failures

    readme = packet_dir / "README.md"
    text = readme.read_text(encoding="utf-8")
    rel_readme = readme.relative_to(ROOT)
    for section in REQUIRED_PACKET_SECTIONS:
        if section not in text:
            failures.append(f"{rel_readme}: missing section {section}")
    if "Share link:" not in text:
        failures.append(f"{rel_readme}: missing share link")
    if "adversarially-confirmed to add value" not in text:
        failures.append(f"{rel_readme}: missing value-bar phrase")
    if not MATRIX_LINK_RE.search(text):
        failures.append(f"{rel_readme}: missing matrix link")
    if f"docs/findings/{slug}" not in index_text:
        failures.append(f"{rel_dir}: missing from docs/findings/README.md")
    if f"docs/findings/{slug}" not in ledger_text:
        failures.append(f"{rel_dir}: missing from docs/confirmed-improvements.md")

    local_refs = _local_refs(text)
    evidence_refs = [
        ref
        for ref in local_refs
        if ref.startswith(REQUIRED_PACKET_ARTIFACT_PREFIXES)
    ]
    if not evidence_refs:
        failures.append(f"{rel_readme}: no local evidence references")
    for ref in sorted(local_refs):
        failures.extend(_check_local_ref(rel_readme, ref))
    failures.extend(_check_repo_links(readme, text))
    return failures


def _local_refs(text: str) -> set[str]:
    refs = {match.group(1) for match in REPO_LINK_RE.finditer(text)}
    for match in LOCAL_ARTIFACT_RE.finditer(text):
        ref = match.group(1).strip()
        if ref.startswith(("docs/", "evals/", "README.md")):
            refs.add(ref)
    return refs


def _check_repo_links(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    rel = path.relative_to(ROOT)
    for ref in sorted({match.group(1) for match in REPO_LINK_RE.finditer(text)}):
        failures.extend(_check_local_ref(rel, ref))
    return failures


def _check_local_ref(rel_source: Path, ref: str) -> list[str]:
    failures: list[str] = []
    candidate = ROOT / ref
    if not candidate.exists():
        failures.append(f"{rel_source}: local evidence link missing: {ref}")
    return failures


def _read_required(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"{path.relative_to(ROOT)}: missing")
        return ""
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
