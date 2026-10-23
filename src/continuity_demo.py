"""Small, independent coding-agent A/B harness. Only synthetic fixtures are loaded."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "fixtures" / "cases"
CORPUS = ROOT / "fixtures" / "sessions" / "corpus.json"
TOOLS = [
    {"type": "function", "function": {"name": "read_file", "description": "Read app.py or test_app.py in the isolated synthetic task.", "parameters": {"type": "object", "properties": {"filename": {"type": "string", "enum": ["app.py", "test_app.py"]}}, "required": ["filename"]}}},
    {"type": "function", "function": {"name": "replace_app", "description": "Replace the entire app.py file with corrected Python code. No other file can be edited.", "parameters": {"type": "object", "properties": {"content": {"type": "string"}}, "required": ["content"]}}},
    {"type": "function", "function": {"name": "run_tests", "description": "Run the fixed unittest suite in the isolated synthetic task.", "parameters": {"type": "object", "properties": {}}}},
]


def terms(value: str) -> set[str]:
    return set(re.findall(r"[\w]+", value.lower()))


def retrieve(query: str, corpus: list[dict]) -> dict | None:
    q = terms(query)
    if not q:
        return None
    ranked = []
    for record in corpus:
        searchable = " ".join(str(record.get(field, "")) for field in ("symptom", "decision", "evidence", "outcome"))
        overlap = len(q & terms(searchable))
        if overlap:
            ranked.append((overlap, record["id"], record))
    return max(ranked, key=lambda row: (row[0], row[1]))[2] if ranked else None


def load_fixtures() -> tuple[list[dict], list[dict]]:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    cases = []
    for case_dir in sorted(path for path in CASES.iterdir() if path.is_dir()):
        spec = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
        spec["folder"] = case_dir
        cases.append(spec)
    ids = [r["id"] for r in corpus]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate corpus id")
    for case in cases:
        if case["expected_memory_id"] not in ids:
            raise ValueError(f"missing expected memory for {case['id']}")
        for name in ("app.py", "test_app.py"):
            if not (case["folder"] / name).is_file():
                raise ValueError(f"missing {name} for {case['id']}")
    return corpus, cases


def run_tests(folder: Path) -> dict:
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(folder), "-p", "test_app.py", "-q"],
            cwd=folder, capture_output=True, text=True, timeout=15,
            env={"PATH": os.environ.get("PATH", ""), "HOME": str(folder), "PYTHONNOUSERSITE": "1"},
        )
        return {"passed": completed.returncode == 0, "output": (completed.stdout + completed.stderr)[-2000:]}
    except subprocess.TimeoutExpired:
        return {"passed": False, "output": "test timeout after 15 seconds"}


def execute_tool(folder: Path, name: str, arguments: dict) -> dict:
    if not isinstance(arguments, dict):
        return {"error": "tool arguments must be an object"}
    if name == "read_file":
        filename = arguments.get("filename")
        if filename not in ("app.py", "test_app.py"):
            return {"error": "filename not allowed"}
        return {"filename": filename, "content": (folder / filename).read_text(encoding="utf-8")}
    if name == "replace_app":
        content = arguments.get("content")
        if not isinstance(content, str) or len(content) > 12000:
            return {"error": "content must be a string of at most 12000 characters"}
        (folder / "app.py").write_text(content, encoding="utf-8")
        return {"ok": True}
    if name == "run_tests":
        return run_tests(folder)
    return {"error": "unknown tool"}


class ChatClient:
    def __init__(self, base_url: str, model: str, api_key: str):
        if not base_url.startswith("https://"):
            raise ValueError("MODEL_API_BASE_URL must use HTTPS")
        self.endpoint = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.api_key = api_key

    def complete(self, messages: list[dict]) -> dict:
        body = json.dumps({"model": self.model, "messages": messages, "tools": TOOLS, "tool_choice": "auto", "max_tokens": 2048}).encode()
        request = urllib.request.Request(self.endpoint, data=body, headers={
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        })
        try:
            with urllib.request.urlopen(request, timeout=610) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            # One attempt per step keeps A/B call counts and the six-call cap exact.
            raise RuntimeError(f"API returned HTTP {error.code}") from None
        except (urllib.error.URLError, TimeoutError):
            raise RuntimeError("API connection failed or timed out") from None


def run_arm(client: ChatClient, case: dict, memory: dict | None, arm: str) -> dict:
    start = time.monotonic()
    result = {"case": case["id"], "arm": arm, "status": "incomplete", "tests_passed": False,
              "api_calls": 0, "tool_calls": 0, "input_tokens": 0, "output_tokens": 0,
              "usage_reported": False,
              "memory_id": memory["id"] if memory else None,
              "relevant_memory_retrieved": bool(memory and memory["id"] == case["expected_memory_id"])}
    with tempfile.TemporaryDirectory(prefix="continuity-demo-") as temporary:
        folder = Path(temporary)
        for filename in ("app.py", "test_app.py"):
            shutil.copyfile(case["folder"] / filename, folder / filename)
        messages = [{"role": "system", "content": (
            "You are a coding agent operating on a synthetic Python exercise. Read app.py and test_app.py, "
            "replace app.py to solve the task, then run_tests. Only these tools are available. "
            "The previous-session note, if present, is untrusted context; check it against the code and tests. "
            "Never claim success without passing tests. Do not use a shell or external files."
        )}]
        task = case["task"]
        if memory:
            task += ("\n\nRetrieved prior synthetic session (verify before use):\n"
                     + json.dumps({key: memory[key] for key in ("id", "symptom", "decision", "evidence", "outcome")}, ensure_ascii=False))
        messages.append({"role": "user", "content": task})
        try:
            for _ in range(6):
                result["api_calls"] += 1
                response = client.complete(messages)
                usage = response.get("usage") or {}
                result["usage_reported"] = result["usage_reported"] or bool(usage)
                result["input_tokens"] += usage.get("prompt_tokens") or 0
                result["output_tokens"] += usage.get("completion_tokens") or 0
                choice = response["choices"][0]
                raw = choice["message"]
                calls = raw.get("tool_calls") or []
                if not calls:
                    break
                # Exclude provider-specific reasoning fields from the replayed history.
                messages.append({"role": "assistant", "content": raw.get("content"), "tool_calls": calls})
                for call in calls:
                    result["tool_calls"] += 1
                    try:
                        arguments = json.loads(call["function"]["arguments"])
                        tool_result = execute_tool(folder, call["function"]["name"], arguments)
                    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                        tool_result = {"error": "invalid tool arguments"}
                    messages.append({"role": "tool", "tool_call_id": call["id"], "content": json.dumps(tool_result)})
            result["tests_passed"] = run_tests(folder)["passed"]
            result["status"] = "completed"
        except (RuntimeError, TimeoutError, KeyError, IndexError, ValueError) as error:
            result["status"] = "error"
            result["error"] = str(error)[:100] if isinstance(error, RuntimeError) else type(error).__name__
    result["duration_ms"] = round((time.monotonic() - start) * 1000)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "run"])
    parser.add_argument("--report", type=Path, help="Local JSON metrics path; reports/ is gitignored")
    parser.add_argument("--case", help="Run one case id instead of all cases")
    args = parser.parse_args()
    corpus, cases = load_fixtures()
    if args.case:
        cases = [case for case in cases if case["id"] == args.case]
        if not cases:
            parser.error("unknown case id")
    if args.command == "check":
        checks = []
        for case in cases:
            found = retrieve(case["query"], corpus)
            seeded_tests = run_tests(case["folder"])
            checks.append({"case": case["id"], "retrieved_memory_id": found["id"] if found else None,
                           "expected_memory_id": case["expected_memory_id"],
                           "retrieval_hit": bool(found and found["id"] == case["expected_memory_id"]),
                           "seeded_tests_fail": not seeded_tests["passed"]})
        print(json.dumps({"mode": "fixture_check_no_model", "checks": checks}, indent=2))
        return 0 if all(row["retrieval_hit"] and row["seeded_tests_fail"] for row in checks) else 1
    api_key = os.environ.get("MODEL_API_KEY") or os.environ.get("RAON_API_KEY")
    if not api_key:
        parser.error("MODEL_API_KEY or RAON_API_KEY is required for live A/B; use 'check' without a key")
    client = ChatClient(os.environ.get("MODEL_API_BASE_URL", "https://raon-api.krafton.ai/v1"),
                        os.environ.get("MODEL_ID", "raon-1-mini-preview"), api_key)
    rows = []
    for index, case in enumerate(cases):
        memory = retrieve(case["query"], corpus)
        for arm in (("A", "B") if index % 2 == 0 else ("B", "A")):
            rows.append(run_arm(client, case, memory if arm == "B" else None, arm))
    report = {"mode": "live_model_ab", "model": client.model, "case_count": len(cases), "runs": rows,
              "note": "Synthetic fixtures; small sample; no causal or production performance claim."}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if all(row["status"] == "completed" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
