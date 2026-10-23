# Technical architecture / 기술 아키텍처

```text
public synthetic records ── lexical top-1 retrieval ──┐
                                                     │ only B
public task + failing tests ── fresh temp copy ─────┼── agent tool loop ── OpenAI-compatible Chat Completions
                                                     │                  └── default Raon model
                                      A: no note ─────┘
        read_file(app.py|test_app.py) · replace_app(app.py) · run_tests()
                              ↓
            per-run metadata report (no prompts, code, key, or responses)
```

`src/continuity_demo.py` is a clean, small harness. It intentionally has no dependency on or import from private Memex. The current retrieval is deterministic token overlap over `symptom`, `decision`, `evidence`, and `outcome`, with an ID tie break. This is a transparent baseline, not Memex's actual semantic index.

The intended future adapter is a user-authorized local MCP client. A safe adapter should request a sanitized result with `id`, short `symptom`, `decision`, `evidence`, and `outcome`, then apply a disclosure allowlist before sending any text to a hosted model. This document describes an **interface proposal**, not an assertion that the private Memex MCP server already returns this shape. The private Memex MCP contract exposes session search and error recall, summary/turn inspection, next-action prediction, and other memory tools over local stdio; its implementation and raw outputs are not copied here.

## Request and tool boundary

- The model receives a synthetic task and, for B only, one synthetic note. Chat Completions history is included on every request because Raon does not store conversation state.
- `read_file` accepts only `app.py` and `test_app.py`; `replace_app` writes only `app.py` inside the temporary case copy. `run_tests` invokes a fixed unittest command. There is no arbitrary shell tool.
- Each arm receives at most six completion requests and runs sequentially. Raon function tools are executed by this client, then returned as `tool` messages with matching IDs.
- A local JSON report contains only metrics and IDs. The report path defaults to no file; `reports/` is gitignored. The API key is read from environment and used only in an Authorization header.

## A/B protocol

Tasks, tests, tool schema, model, output budget, and rules are fixed. Arm B alone gets the retrieved record. The first case runs A then B, the second B then A to reduce simple order bias. Each arm has an independent temporary directory; retrieval itself is done before either arm. The code does not fix a random seed or control model nondeterminism, so a proper evaluation needs repeated runs and a larger predeclared corpus.

## Current gaps

No actual Memex MCP adapter, no semantic vector retrieval, no explicit error/decision extraction from real sessions, no independent human grading, no live Raon measurement, and no assurance that an agent used the retrieved note rather than solving from the task alone. Issues track these additions.
