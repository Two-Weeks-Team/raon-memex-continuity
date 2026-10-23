# Raon × Memex continuity lab

An **independent public proof of concept** for a coding agent that can recover a relevant past error and decision before continuing a task. It uses synthetic sessions only. Memex remains model neutral: retrieval provides context, while the agent model is selected through an OpenAI-compatible Chat Completions endpoint. Raon is the documented default, not a dependency of the memory design.

**Status (2026-10-23):** the local fixture, retrieval, sandboxed task copies, agent tool loop, A/B runner, metrics schema, and tests are implemented. Live Raon A/B results are **not yet measured** because this build environment has no Raon API key. No performance uplift is claimed. This project is neither an official KRAFTON integration nor a publication of the private Memex repository.

## What the demo does

Two invented coding problems each have failing tests and an invented prior session. Arm A gets the task only. Arm B gets the same task plus the top retrieved prior session. Both can read two fixture files, replace `app.py`, and run fixed unit tests in separate temporary directories. The report records test pass/fail, tool and API call counts, token usage when returned by the provider, latency, and whether the expected prior session was retrieved. It does not equate retrieval with a correct model decision.

```bash
python3 src/continuity_demo.py check
# With a Raon key in your own shell (never commit it):
export RAON_API_KEY='...'
python3 src/continuity_demo.py run --report reports/raon-local.json
```

`check` makes **no model call** and verifies only fixture consistency, deterministic retrieval, and that both seeded tasks fail before repair. `run` performs real model calls; see [Quickstart](docs/QUICKSTART.md) for setup and interpretation. It runs only on synthetic code and needs Python 3.10+.

## Documents

| Purpose | Document |
| --- | --- |
| Product requirements | [PRD](docs/PRD.md) |
| Components and interfaces | [Architecture](docs/ARCHITECTURE.md) |
| Local setup and commands | [Quickstart](docs/QUICKSTART.md) |
| Phases and acceptance criteria | [Development plan](docs/DEVELOPMENT_PLAN.md) |
| Disclosure boundary | [Security and data policy](docs/SECURITY_DATA.md) |
| Raon compatibility and source links | [Source verification](docs/SOURCES.md) |
| Event submission preparation | [Build with Raon guide](docs/EVENT_SUBMISSION.md) |

## Relationship to Memex

The private `Two-Weeks-Team/memex` README, architecture, and MCP tool contract were inspected before this repository was made. Memex's public-level concept is local session memory with search, error recall, and replay through an MCP interface. This repo contains a new minimal retrieval fixture and coding-agent experiment; it neither imports Memex's code nor requires access to its private repository. The future integration boundary is a **consented, sanitized memory adapter** returning a small `id/symptom/decision/evidence/outcome` record. That adapter is **not implemented**. The demo does not claim to exercise the private Memex runtime.

## 한국어 요약

이 저장소는 코딩 에이전트가 과거 오류와 의사결정을 회수해 작업을 이어가는지 확인하는 **독립 공개 실증**입니다. 세션·코드·검증 과제는 모두 새로 만든 합성 자료입니다. A는 과거 기록 없이, B는 관련 기록 하나를 받은 뒤 같은 과제를 풉니다. 두 실행은 서로 다른 임시 폴더를 사용하며 테스트 통과 여부, API 호출, 도구 호출, 응답 지연 및 제공된 토큰 사용량을 기록합니다.

Memex의 메모리 계층은 모델에 종속되지 않습니다. 기본 모델 설정만 Raon이며 다른 OpenAI 호환 엔드포인트로 교체할 수 있습니다. **현재 Raon 실측 결과는 없습니다.** API 키가 이 작업 환경에 없어 실제 호출을 실행하지 않았습니다. `check`의 통과는 모델 성능의 증거가 아닙니다. [한국어 빠른 시작](docs/QUICKSTART.md#한국어-빠른-시작), [보안·데이터 정책](docs/SECURITY_DATA.md), [이벤트 안내](docs/EVENT_SUBMISSION.md)를 참고하세요.

## License

This repository's original code and synthetic fixtures are MIT licensed. KRAFTON's hosted service and model weights have separate terms; see [source verification](docs/SOURCES.md).
