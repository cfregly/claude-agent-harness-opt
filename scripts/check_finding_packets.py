#!/usr/bin/env python3
"""Validate shareable finding packets and local evidence links."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FINDINGS_DIR = ROOT / "docs" / "findings"
PR_PACKETS_DIR = ROOT / "evals" / "pr_packets"
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
REQUIRED_PR_PACKET_FILES = ("PR_TITLE.txt", "PR_BODY.md", "REPRODUCTION.md", "evidence.json")
REQUIRED_COMPARISON_FIELDS = (
    "baseline_score",
    "baseline_variant",
    "candidate_score",
    "candidate_variant",
    "delta",
    "minimum_delta",
    "promote",
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
    failures.extend(_check_pr_packet_dirs())
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


def _check_pr_packet_dirs() -> list[str]:
    failures: list[str] = []
    if not PR_PACKETS_DIR.exists():
        return ["evals/pr_packets: missing"]
    packet_dirs = [path for path in sorted(PR_PACKETS_DIR.iterdir()) if path.is_dir()]
    if not packet_dirs:
        return ["evals/pr_packets: no PR packet directories found"]
    for packet_dir in packet_dirs:
        failures.extend(_check_pr_packet_dir(packet_dir))
    return failures


def _check_pr_packet_dir(packet_dir: Path) -> list[str]:
    failures: list[str] = []
    rel_dir = packet_dir.relative_to(ROOT)
    for filename in REQUIRED_PR_PACKET_FILES:
        path = packet_dir / filename
        if not path.exists():
            failures.append(f"{rel_dir}: missing {filename}")
            continue
        if not path.read_text(encoding="utf-8").strip():
            failures.append(f"{path.relative_to(ROOT)}: empty")

    evidence_path = packet_dir / "evidence.json"
    if not evidence_path.exists():
        return failures
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"{evidence_path.relative_to(ROOT)}: invalid JSON: {exc}")
        return failures
    if not isinstance(evidence, dict):
        failures.append(f"{evidence_path.relative_to(ROOT)}: evidence must be an object")
        return failures
    failures.extend(_check_pr_packet_evidence(evidence_path, evidence))
    return failures


def _check_pr_packet_evidence(path: Path, evidence: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    rel = path.relative_to(ROOT)
    cases = evidence.get("cases")
    if not isinstance(cases, list) or not cases:
        failures.append(f"{rel}: cases must be a nonempty list")
    comparison = evidence.get("comparison")
    if not isinstance(comparison, dict):
        failures.append(f"{rel}: comparison must be an object")
        comparison = {}
    for field in REQUIRED_COMPARISON_FIELDS:
        if field not in comparison:
            failures.append(f"{rel}: comparison missing {field}")
    baseline_variant = str(comparison.get("baseline_variant", "")).strip()
    candidate_variant = str(comparison.get("candidate_variant", "")).strip()
    for field in ("baseline_score", "candidate_score", "delta", "minimum_delta"):
        if field in comparison and not isinstance(comparison[field], (int, float)):
            failures.append(f"{rel}: comparison.{field} must be numeric")
    if comparison.get("promote") is not True:
        failures.append(f"{rel}: comparison.promote must be true for committed PR packets")
    if (
        isinstance(comparison.get("delta"), (int, float))
        and isinstance(comparison.get("minimum_delta"), (int, float))
        and comparison["delta"] < comparison["minimum_delta"]
    ):
        failures.append(f"{rel}: comparison delta is below minimum_delta")

    result = evidence.get("result")
    if not isinstance(result, dict):
        failures.append(f"{rel}: result must be an object")
        result = {}
    if result.get("live") is not True:
        failures.append(f"{rel}: result.live must be true")
    if not isinstance(result.get("results"), list) or not result.get("results"):
        failures.append(f"{rel}: result.results must be a nonempty list")
    if not isinstance(result.get("cells"), list) or not result.get("cells"):
        failures.append(f"{rel}: result.cells must be a nonempty list")
    if not isinstance(result.get("summary"), dict) or not result["summary"].get("total"):
        failures.append(f"{rel}: result.summary.total must be present")
    matrix_path = str(result.get("matrix_path", "")).strip()
    if matrix_path and not (ROOT / matrix_path).exists():
        failures.append(f"{rel}: result.matrix_path missing locally: {matrix_path}")

    matrix = evidence.get("matrix")
    if not isinstance(matrix, dict):
        failures.append(f"{rel}: matrix must be an object")
        matrix = {}
    matrix_variants = {
        str(variant.get("name", ""))
        for variant in matrix.get("tool_variants", [])
        if isinstance(variant, dict)
    }
    for variant_name in (baseline_variant, candidate_variant):
        if variant_name and variant_name not in matrix_variants:
            failures.append(f"{rel}: comparison variant missing from matrix: {variant_name}")
    result_variants = {
        str(item.get("tool_variant", ""))
        for item in result.get("results", [])
        if isinstance(item, dict)
    }
    for variant_name in (baseline_variant, candidate_variant):
        if variant_name and variant_name not in result_variants:
            failures.append(f"{rel}: comparison variant missing from result cells: {variant_name}")

    source = evidence.get("source")
    if not isinstance(source, dict) or not source:
        failures.append(f"{rel}: source must be a nonempty object")
    return failures


def _read_required(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"{path.relative_to(ROOT)}: missing")
        return ""
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
