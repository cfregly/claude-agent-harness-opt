import unittest

from scripts.sdk_surface_inventory import (
    SURFACE_CHECKS,
    _can_import,
    _signature_params,
)


class SdkSurfaceInventoryScriptTests(unittest.TestCase):
    def test_surface_checks_cover_expected_sdk_packages(self):
        self.assertEqual({"claude-agent-sdk", "google-adk", "openai-agents"}, set(SURFACE_CHECKS))
        for package, spec in SURFACE_CHECKS.items():
            with self.subTest(package=package):
                self.assertIn("module", spec)
                self.assertIn("source", spec)
                self.assertTrue(spec["checks"])
                self.assertTrue(all("name" in check for check in spec["checks"]))

    def test_signature_params_handles_missing_and_callable_objects(self):
        def sample(first: str, second: int = 0) -> None:
            return None

        self.assertEqual({"first", "second"}, _signature_params(sample))
        self.assertEqual(set(), _signature_params(None))

    def test_can_import_reports_known_modules(self):
        self.assertTrue(_can_import("json"))
        self.assertFalse(_can_import("definitely_missing_aho_module"))


if __name__ == "__main__":
    unittest.main()
