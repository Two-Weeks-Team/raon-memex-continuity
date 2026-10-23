# Build with Raon submission guide / 이벤트 제출 안내

The [official Raon page](https://raon-mini.krafton.ai/ko) currently invites projects and ideas for **Build with Raon!** and links to [this form](https://forms.gle/CFXarNSq9qdXE9Ny5). The form itself was not readable through the available source access on 2026-10-23, so its deadline, eligibility, required fields, prize rules, and license terms remain **unverified**. Open the live form and verify those before submitting. This repository has **not** been submitted.

## Submission-ready evidence to prepare

1. Link the public repository and a short video showing the fixture `check` and, after a real key-backed run, one A/B task.
2. Include the exact model ID, run date, number of cases/repetitions, and raw per-case metric report after reviewing it for disclosure.
3. Show both success and failure. Explain that retrieval @1 measures the memory layer; passing tests measures only the synthetic coding task. Do not describe two cases as a general benchmark.
4. State that Memex's private runtime is not embedded and that the future MCP bridge is planned, not implemented.
5. Review the hosted terms, privacy policy, and any event-specific content/IP consent in the live form. Keep the API key and private sessions out of all submission material.

## Suggested concise project description

Raon × Memex continuity lab is an independent, model-neutral coding-agent experiment. It compares a fresh agent task with the same task supplied with a relevant synthetic past error and decision. Its public harness runs both arms in isolated copies, measures test outcome and effort, and keeps private Memex sessions and source outside the hosted API. The current release includes the runnable harness and synthetic fixtures; live Raon A/B results will be added only after verified runs.

## 제출 전 확인

공식 양식에서 마감일·참가 자격·필수 자료·저작물 이용조건을 직접 재확인하세요. 키나 실제 세션은 제출하지 마세요. 합성 fixture 검사 결과를 Raon 모델 성능으로 표현하지 마세요.
