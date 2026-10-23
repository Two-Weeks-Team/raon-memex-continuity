import json
import tempfile
import unittest
from pathlib import Path

from src import continuity_demo as demo


class FixtureTests(unittest.TestCase):
    def test_retrieval_and_seeded_failure(self):
        corpus, cases = demo.load_fixtures()
        self.assertEqual(len(cases), 2)
        for case in cases:
            self.assertEqual(demo.retrieve(case["query"], corpus)["id"], case["expected_memory_id"])
            self.assertFalse(demo.run_tests(case["folder"])["passed"])

    def test_tool_allowlist(self):
        with tempfile.TemporaryDirectory() as folder_name:
            folder = Path(folder_name)
            (folder / "app.py").write_text("value = 1\n")
            (folder / "test_app.py").write_text("", encoding="utf-8")
            self.assertIn("error", demo.execute_tool(folder, "read_file", {"filename": "../secret"}))
            self.assertIn("error", demo.execute_tool(folder, "shell", {"cmd": "true"}))
            self.assertIn("error", demo.execute_tool(folder, "read_file", []))
            self.assertEqual((folder / "app.py").read_text(), "value = 1\n")

    def test_model_client_requires_https(self):
        with self.assertRaises(ValueError):
            demo.ChatClient("http://localhost:8000/v1", "fixture", "secret")

    def test_report_contains_no_key_or_prompt(self):
        corpus, cases = demo.load_fixtures()

        class FakeClient:
            model = "synthetic-test-double"

            def complete(self, messages):
                self.messages = messages
                return {"choices": [{"message": {"content": "stop"}}], "usage": {"prompt_tokens": 3, "completion_tokens": 1}}

        client = FakeClient()
        result = demo.run_arm(client, cases[0], demo.retrieve(cases[0]["query"], corpus), "B")
        self.assertIn("synthetic-cache-001", client.messages[1]["content"])
        payload = json.dumps(result)
        self.assertNotIn(cases[0]["task"], payload)
        self.assertNotIn("secret", payload)
        self.assertEqual(result["status"], "completed")
        self.assertFalse(result["tests_passed"])

    def test_agent_tool_loop_can_edit_and_verify_synthetic_task(self):
        _, cases = demo.load_fixtures()

        class FakeClient:
            def __init__(self):
                self.calls = 0

            def complete(self, messages):
                self.calls += 1
                if self.calls == 1:
                    corrected = "_values = {}\n\ndef put(tenant_id, key, value):\n    _values[(tenant_id, key)] = value\n\ndef get(tenant_id, key):\n    return _values.get((tenant_id, key))\n\ndef clear():\n    _values.clear()\n"
                    calls = [{"id": "one", "type": "function", "function": {"name": "replace_app", "arguments": json.dumps({"content": corrected})}}]
                elif self.calls == 2:
                    calls = [{"id": "two", "type": "function", "function": {"name": "run_tests", "arguments": "{}"}}]
                else:
                    self.assert_tool_result = messages[-1]["content"]
                    calls = []
                return {"choices": [{"message": {"content": None, "tool_calls": calls}}], "usage": {"prompt_tokens": 1, "completion_tokens": 1}}

        client = FakeClient()
        result = demo.run_arm(client, cases[0], None, "A")
        self.assertTrue(result["tests_passed"])
        self.assertEqual(result["tool_calls"], 2)
        self.assertTrue(json.loads(client.assert_tool_result)["passed"])


if __name__ == "__main__":
    unittest.main()
