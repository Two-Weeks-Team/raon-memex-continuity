# Development plan / 개발 계획

| Phase | Deliverable | Exit gate | State |
| --- | --- | --- | --- |
| 0 — disclosure | Inspect private Memex README, architecture and MCP contract; define copy boundary and source citations | No private source or real transcript enters the public tree | Done for this initial release |
| 1 — public harness | Synthetic cases, deterministic retrieval, bounded tools, A/B runner, CI, key handling | `check` and tests pass; branch review and public repository | Implemented, review pending |
| 2 — live Raon study | Authorized key, repeated A/B runs, documented model/limits, raw metadata reports | Real completed runs; honest failures and paired summaries | Pending key and run |
| 3 — Memex bridge | User-consented local MCP adapter with field-level redaction and schema validation | Adapter contract tests against approved synthetic MCP fixture | Not implemented |
| 4 — event submission | Demo capture, results interpretation, current event requirements, final form | Human review of public material and event form | Not submitted |

## Milestone rules

The phase-1 smoke check is not a model benchmark. Do not mark phase 2 complete from CI. If Raon API shape or terms change, update `docs/SOURCES.md` before running. If hosted-model use would send any non-synthetic user data, stop and obtain explicit data-owner consent. Keep event eligibility, deadline, prize, and licensing statements tied to current official materials.

GitHub issues define the work breakdown. Each task links to one phase EPIC and has a clear acceptance check; completed initial tasks remain open until the project owner reviews the first public release.
