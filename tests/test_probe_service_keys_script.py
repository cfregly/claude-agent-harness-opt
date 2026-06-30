import base64
from pathlib import Path
import tempfile
import unittest

from scripts.probe_service_keys import (
    basic_auth,
    load_env_file,
    parse_json,
    probe_firecrawl,
    probe_stripe,
    render_result,
    summarize_error,
)


class ProbeServiceKeysScriptTests(unittest.TestCase):
    def test_load_env_file_accepts_exports_comments_and_quotes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / ".env"
            path.write_text(
                "# comment\n"
                "export FIRECRAWL_API_KEY='abc123'\n"
                'STRIPE_SECRET_KEY="sk_test_sample"\n'
                "EMPTY=\n",
                encoding="utf-8",
            )

            env = load_env_file(path)

        self.assertEqual("abc123", env["FIRECRAWL_API_KEY"])
        self.assertEqual("sk_test_sample", env["STRIPE_SECRET_KEY"])
        self.assertEqual("", env["EMPTY"])

    def test_basic_auth_builds_header_without_printing_secret(self):
        header = basic_auth("user", "secret")
        token = header["Authorization"].removeprefix("Basic ")

        self.assertEqual("user:secret", base64.b64decode(token).decode("ascii"))

    def test_parse_json_and_error_summary_are_bounded(self):
        self.assertEqual({"ok": True}, parse_json(b'{"ok": true}'))
        self.assertEqual({"body_prefix": "not-json"}, parse_json(b"not-json"))
        self.assertEqual("bad", summarize_error({"message": "bad"}))
        self.assertLessEqual(len(summarize_error({"errors": "x" * 500})), 240)

    def test_missing_keys_skip_without_network(self):
        self.assertEqual("skip", probe_firecrawl({}, timeout=1)["status"])
        self.assertEqual("skip", probe_stripe({}, timeout=1)["status"])

    def test_render_result_uses_status_label_and_service(self):
        text = render_result({"detail": "missing key", "service": "stripe", "status": "skip"})

        self.assertEqual("SKIP stripe: missing key", text)


if __name__ == "__main__":
    unittest.main()
