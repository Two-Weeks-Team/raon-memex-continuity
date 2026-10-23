# PRD — coding-agent session continuity

## Problem and audience

A coding agent can repeat a past debugging detour after a session boundary. A developer should be able to supply a relevant, inspectable prior error and decision before the agent edits code. The first audience is a developer evaluating continuity on safe synthetic tasks, not users' actual private transcripts.

## Hypothesis

For matched synthetic coding tasks, adding a relevant prior-session note may improve test completion or reduce effort. This is a hypothesis; the repository contains no live Raon result yet. Retrieval quality and agent task success are measured separately.

## Scope / 범위

1. Maintain a public, human-readable synthetic corpus with stable IDs and explicit expected matches.
2. Run each case in two fresh copies: A has no memory; B receives one retrieved note.
3. Give both arms the same model, tools, prompt rules, task, request budget, and tests.
4. Record raw per-run metrics without invented numbers: test pass, API/tool calls, response time, reported tokens, and memory retrieval hit.
5. Keep Memex's memory boundary model neutral. The provider is configurable; Raon is the default demonstration target.
6. Publish sources, methodology, failures, and limitations before an event submission.

## Non-goals / 제외

No private transcript migration, publication of private Memex code, production agent integration, autonomous operation over user repositories, quality claim based on two examples, or claim of official KRAFTON affiliation. Actual Memex MCP calls and a provider-independent MCP adapter remain future work.

## Success criteria

| Milestone | Acceptance |
| --- | --- |
| Fixture gate | Every synthetic case has unique ground-truth memory, failing seed test, and deterministic retrieval check. |
| Runnable harness | With an authorized key, both arms invoke the same Chat Completions model and only the three bounded tools; failures are recorded. |
| Measured study | Repeated runs with model/version, date, request limits, case-level output, and uncertainty disclosed; no uplift claim from harness tests. |
| Public release | Docs, key exclusion, CI, and source audit complete; no private source, transcript, secret, or prompt in published metrics. |

## Metrics and interpretation

- **Task success:** fraction of arm runs passing the fixed unit tests. This checks the synthetic coding outcome, not general software correctness.
- **Error/decision retrieval @1:** fraction of B cases whose returned record ID matches the predeclared expected ID. This measures retrieval only; it does not prove the agent used the note.
- **Effort:** API calls, tool calls, elapsed milliseconds, and `usage` token fields if supplied. Zero token counts may mean the provider omitted usage; report this caveat.
- **A/B comparison:** paired per-case differences, with repetitions and both execution orders. Two hand-built cases are a plumbing demonstration and cannot establish a general effect.

## Risks and mitigations

The note could be irrelevant or misleading; the system prompt instructs verification against source and tests. The provider may reject tools or change preview behavior; record HTTP status and model identifier, and update compatibility notes. Generated code is run only against public synthetic fixtures; do not point this runner at a real repository. Rate limits may prevent completion; keep runs sequential and respect `Retry-After`.
