# Development plan / 개발 계획

GitHub tracking: [project EPIC #2](https://github.com/Two-Weeks-Team/raon-memex-continuity/issues/2). Each phase issue contains its child task checklist.

| Phase | Deliverable | Exit gate | State |
| --- | --- | --- | --- |
| [0 — disclosure](https://github.com/Two-Weeks-Team/raon-memex-continuity/issues/3) | Inspect private Memex README, architecture and MCP contract; define copy boundary and source citations | No private source or real transcript enters the public tree | Done for this initial release |
| [1 — public harness](https://github.com/Two-Weeks-Team/raon-memex-continuity/issues/4) | Synthetic cases, deterministic retrieval, bounded tools, A/B runner, CI, key handling | `check` and tests pass; branch review and public repository | Implemented, review pending |
| [2 — live Raon study](https://github.com/Two-Weeks-Team/raon-memex-continuity/issues/5) | Authorized key, repeated A/B runs, documented model/limits, raw metadata reports | Real completed runs; honest failures and paired summaries | Pending key and run |
| [3 — Memex bridge](https://github.com/Two-Weeks-Team/raon-memex-continuity/issues/6) | User-consented local MCP adapter with field-level redaction and schema validation | Adapter contract tests against approved synthetic MCP fixture | Not implemented |
| [4 — event submission](https://github.com/Two-Weeks-Team/raon-memex-continuity/issues/7) | Demo capture, results interpretation, current event requirements, final form | Human review of public material and event form | Not submitted |

## Milestone rules

The phase-1 smoke check is not a model benchmark. Do not mark phase 2 complete from CI. If Raon API shape or terms change, update `docs/SOURCES.md` before running. If hosted-model use would send any non-synthetic user data, stop and obtain explicit data-owner consent. Keep event eligibility, deadline, prize, and licensing statements tied to current official materials.

GitHub issues define the work breakdown. Each task links to one phase issue and has a clear acceptance check. Close implemented tasks after their code and CI are verified on the default branch; leave live-measurement and event tasks open until evidence exists.
