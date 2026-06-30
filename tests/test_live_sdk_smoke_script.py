import unittest

from scripts.live_sdk_smoke import (
    PROMPT_TEMPLATE,
    _json_or_empty,
    _openai_text,
    _stringify,
)


class LiveSdkSmokeScriptTests(unittest.TestCase):
    def test_prompt_template_requires_directed_decision_notes_and_marker(self):
        prompt = PROMPT_TEMPLATE.format(marker="sample")

        self.assertIn("DECISION_NOTE_BEFORE", prompt)
        self.assertIn("DECISION_NOTE_AFTER", prompt)
        self.assertIn("HARNESS_OK sample", prompt)
        self.assertIn("pwd_tool", prompt)

    def test_json_or_empty_accepts_only_objects(self):
        self.assertEqual({"command": "pwd"}, _json_or_empty('{"command": "pwd"}'))
        self.assertEqual({}, _json_or_empty("[1, 2]"))
        self.assertEqual({}, _json_or_empty("not-json"))

    def test_stringify_preserves_strings_and_serializes_objects(self):
        self.assertEqual("text", _stringify("text"))
        self.assertEqual('{"a": 1}', _stringify({"a": 1}))

    def test_openai_text_joins_message_parts(self):
        class Part:
            def __init__(self, text: str) -> None:
                self.text = text

        class Raw:
            content = [Part("one"), Part("two")]

        self.assertEqual("one\ntwo", _openai_text(Raw()))


if __name__ == "__main__":
    unittest.main()
