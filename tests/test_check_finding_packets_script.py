from pathlib import Path
import subprocess
import sys
import unittest

from scripts.check_finding_packets import ROOT, _check_pr_packet_evidence

REPO_ROOT = Path(__file__).resolve().parents[1]


class CheckFindingPacketsScriptTests(unittest.TestCase):
    def test_script_passes_current_repo(self):
        result = subprocess.run(
            [sys.executable, "scripts/check_finding_packets.py"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("finding packet check passed", result.stdout)

    def test_pr_packet_evidence_requires_promoted_live_variant_result(self):
        failures = _check_pr_packet_evidence(
            ROOT / "evals" / "pr_packets" / "bad" / "evidence.json",
            {
                "cases": [],
                "comparison": {
                    "baseline_score": 0.8,
                    "baseline_variant": "stock",
                    "candidate_score": 0.81,
                    "candidate_variant": "tuned",
                    "delta": 0.01,
                    "minimum_delta": 0.1,
                    "promote": False,
                },
                "matrix": {"tool_variants": [{"name": "stock", "tools": []}]},
                "result": {
                    "cells": [],
                    "live": False,
                    "matrix_path": "evals/model_matrix/missing.json",
                    "results": [],
                    "summary": {"total": 0},
                },
                "source": {},
            },
        )

        joined = "\n".join(failures)
        self.assertIn("cases must be a nonempty list", joined)
        self.assertIn("comparison.promote must be true", joined)
        self.assertIn("comparison delta is below minimum_delta", joined)
        self.assertIn("result.live must be true", joined)
        self.assertIn("comparison variant missing from matrix: tuned", joined)


if __name__ == "__main__":
    unittest.main()
