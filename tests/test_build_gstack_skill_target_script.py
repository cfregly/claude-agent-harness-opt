import unittest

from scripts.build_gstack_skill_target import (
    _case,
    _frontmatter,
    _no_tool,
    _tool_name,
)


class BuildGstackSkillTargetScriptTests(unittest.TestCase):
    def test_tool_name_normalizes_generated_skill_names(self):
        self.assertEqual("gstack_gstack", _tool_name("gstack", "gstack"))
        self.assertEqual("gstack_upgrade", _tool_name("gstack-upgrade", "gstack-upgrade"))
        self.assertEqual("gstack_plan_eng_review", _tool_name("gstack-plan-eng-review", "plan-eng-review"))

    def test_frontmatter_reads_literal_blocks(self):
        payload = _frontmatter(
            "---\n"
            "name: sample\n"
            "description: |\n"
            "  First line\n"
            "  second line\n"
            "---\n"
            "body\n"
        )

        self.assertEqual("sample", payload["name"])
        self.assertEqual("First line\nsecond line", payload["description"])

    def test_case_marks_no_tool_as_safe_boundary(self):
        case = _case("no-tool-general-answer", "Explain without tools.", "NO_TOOL", [], ["gstack_qa"])

        self.assertTrue(case["allow_no_tool"])
        self.assertEqual([], case["expected_tools"])
        self.assertEqual(["gstack_qa"], case["forbidden_tools"])
        self.assertNotIn("expected_args_contains", case)

    def test_no_tool_pseudo_tool_has_quality_checks(self):
        tool = _no_tool()

        self.assertEqual("NO_TOOL", tool["name"])
        self.assertTrue(tool["quality_checks"])
        self.assertIn("rationale", tool["input_schema"]["required"])


if __name__ == "__main__":
    unittest.main()
