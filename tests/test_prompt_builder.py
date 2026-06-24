from pathlib import Path
import unittest

from claude_agent_prompting.prompt_builder import lint_tools, load_recipe, render_prompt


ROOT = Path(__file__).resolve().parents[1]


class PromptBuilderTests(unittest.TestCase):
    def test_render_search_prompt_contains_core_sections(self):
        recipe = load_recipe(ROOT / "recipes" / "agentic_search.json")
        prompt = render_prompt(recipe)

        self.assertIn("<agent_task>", prompt)
        self.assertIn("<tool_selection>", prompt)
        self.assertIn("<tool_call_budgets>", prompt)
        self.assertIn("web_search", prompt)
        self.assertIn("stop searching", prompt)

    def test_tool_lint_passes_for_search_recipe(self):
        recipe = load_recipe(ROOT / "recipes" / "agentic_search.json")
        self.assertEqual([], lint_tools(recipe))

    def test_tool_lint_catches_overlap(self):
        issues = lint_tools(
            [
                {"name": "web_search", "purpose": "Find public web sources now", "use_when": "Use for broad source discovery", "avoid_when": "Known URLs"},
                {"name": "doc_search", "purpose": "Find internal docs fast", "use_when": "Use for internal docs", "avoid_when": "Public web"},
            ]
        )
        self.assertTrue(any("overlap" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
