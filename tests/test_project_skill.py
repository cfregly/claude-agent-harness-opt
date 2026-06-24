from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProjectSkillTests(unittest.TestCase):
    def test_agent_audit_skill_metadata_and_body_are_complete(self):
        skill = ROOT / ".claude" / "skills" / "agent-audit" / "SKILL.md"
        text = skill.read_text(encoding="utf-8")

        self.assertIn("name: agent-audit", text)
        self.assertIn("description:", text)
        self.assertIn("audit-agent", text)
        self.assertIn("trace-suite", text)
        self.assertIn("adversarially-confirmed to add value", text)
        self.assertNotIn("TODO", text)

    def test_agent_audit_openai_metadata_exists(self):
        metadata = ROOT / ".claude" / "skills" / "agent-audit" / "agents" / "openai.yaml"
        text = metadata.read_text(encoding="utf-8")

        self.assertIn("display_name", text)
        self.assertIn("Agent Audit", text)
        self.assertIn("value-bar", text)
        self.assertNotIn("TODO", text)


if __name__ == "__main__":
    unittest.main()
