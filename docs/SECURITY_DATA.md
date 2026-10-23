# Security and data policy / 보안·데이터 정책

## Public disclosure boundary

The private `Two-Weeks-Team/memex` README, architecture, and MCP contract were reviewed as background. This public repository contains only new code, newly written documentation, and invented fixtures. Do not copy private source files, actual session JSONL, screenshots, debug logs, home paths, personal prompts, private repository paths, or MCP responses here. A license notice in a private repository is not a substitute for reviewing the contents of each file before publication.

The synthetic records have fictional incidents and stable synthetic IDs. The demo never scans `~/.claude`, `~/.codex`, or any other user-session directory. A future Memex adapter must be opt-in, local, and perform explicit redaction before data enters a hosted model. It is not implemented.

## Keys, requests, logs

- Use a personal Raon key under the official hosted service terms. Never commit it or share it with another participant. `.env` and `reports/` are ignored by Git; `.env.example` has no key.
- The runner reads `MODEL_API_KEY` or `RAON_API_KEY` from the environment, requires HTTPS, and sends it only as a Bearer header. It does not print request bodies, response bodies, key values, model reasoning, edited code, or full prompts.
- Reports contain case ID, arm, status, task test result, call counts, token counts, elapsed time, and retrieved synthetic memory ID. Review any modified code before publishing a report or adding more fixtures.
- CI requires no key and makes no Raon call. Never put a live key in a GitHub Actions secret for this public proof of concept without a separate security review.
- The agent's only write tool targets `app.py` in a temporary synthetic task copy; test execution has a time limit. This is a bounded demo, **not a hardened sandbox**. Run only reviewed public fixtures on a trusted development machine.

## Hosted processing

Raon's [privacy policy](https://raon-mini.krafton.ai/ko/privacy) says prompt text is stored for response delivery, service improvement, and usage statistics, then deleted after 14 days; model training use requires separate opt-in consent. It also describes service metadata and possible processing in other regions. The [terms](https://raon-mini.krafton.ai/ko/terms) restrict key sharing and simple API resale/proxying. Therefore no actual Memex transcript, credentials, personal data, or customer code should be sent to the hosted API by this experiment.

## Incident response

If a secret is committed, revoke/rotate it through the issuer before relying on Git history cleanup; remove it from the repository and stop affected runs. If private content is published, restrict access where possible, notify the data owner, and document the exposure. Do not paste the secret or private text into an issue.
