# Verification record — 2026-10-23

The first public release was merged in [PR #1](https://github.com/Two-Weeks-Team/raon-memex-continuity/pull/1). Its final head commit was `e8cc08e`. The [GitHub Actions fixture-and-harness run](https://github.com/Two-Weeks-Team/raon-memex-continuity/actions/runs/39942125676) passed.

Local verification in the dedicated linked worktree:

- `python3 -m unittest discover -s tests -v`: **6 tests passed**. These cover fixture retrieval, failing seed tasks, tool allowlist, HTTPS endpoint requirement, metadata-only report behavior, a scripted tool loop, and timeout accounting.
- `python3 src/continuity_demo.py check`: both synthetic cases returned the predeclared memory ID at rank 1; both unmodified case tests failed as intended.
- `python3 src/continuity_demo.py run --case cache-key`: exited with the documented missing-key error before any network call.

**No live Raon A/B trial was executed.** `RAON_API_KEY` was absent in this environment. The scripted tool-loop test is a test double for the harness and is not a model result. No success rate, latency, token usage, or continuity improvement is claimed for Raon.
