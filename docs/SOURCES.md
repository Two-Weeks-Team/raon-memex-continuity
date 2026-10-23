# Official source verification / 공식 자료 확인

Checked 2026-10-23 (Asia/Seoul). Recheck before live runs or submission because this is a preview service. Links point to KRAFTON's own pages.

| Topic | Verified current statement | Source |
| --- | --- | --- |
| Endpoint and authentication | Chat Completions is `POST /v1/chat/completions` at `https://raon-api.krafton.ai`; use `Authorization: Bearer <key>`. | [Chat Completions](https://raon-mini.krafton.ai/en/docs/chat-completions), [API overview](https://raon-mini.krafton.ai/ko/docs/api-reference) |
| Model | Documented ID is `raon-1-mini-preview`, text in/out, Chat Completions/Responses/Messages support. `GET /v1/models` lists IDs available to a key. | [Models](https://raon-mini.krafton.ai/en/docs/models) |
| Agent compatibility | Raon documents client-run function tools in Chat Completions. The client must execute calls and return results. Server conversation state is not retained; send history on each turn. | [Tool calling](https://raon-mini.krafton.ai/en/docs/tool-calling), [Chat Completions](https://raon-mini.krafton.ai/en/docs/chat-completions) |
| Unsupported features | Responses `previous_response_id`, hosted MCP tools and code interpreter are unsupported; the demo uses local client tools and no server state. | [Unsupported requests](https://raon-mini.krafton.ai/ko/docs/limits) |
| Usage and limits | Preview price is currently zero, with organization limits and token reservations. Rate-limit responses may carry `retry-after`. | [Usage](https://raon-mini.krafton.ai/en/docs/usage), [Rate limits](https://raon-mini.krafton.ai/en/docs/rate-limits) |
| Service terms | Hosted API/Playground have separate beta terms from Apache-2.0 model weights; key sharing, simple proxy/resale, and large-scale response harvesting for competing model training are restricted. | [Terms, revised 2026-10-21](https://raon-mini.krafton.ai/ko/terms), [model card](https://huggingface.co/KRAFTON/Raon-1-mini-preview) |
| Data handling | Prompt text storage and 14-day deletion are described; training use requires separate consent. Avoid real sessions. | [Privacy policy, effective 2026-10-21](https://raon-mini.krafton.ai/ko/privacy) |
| Event | Official Raon page announces **Build with Raon!** and links to a participation form. The form's fields, eligibility, deadline, prizes, and submission license could not be independently read through the available source access. | [Official Raon page](https://raon-mini.krafton.ai/ko), [official linked form](https://forms.gle/CFXarNSq9qdXE9Ny5) |

The model card's Apache-2.0 grant applies to downloadable weights, not KRAFTON's hosted API. The current free-preview statement is not a future pricing guarantee. This project makes no claim that an event submission has been accepted.
