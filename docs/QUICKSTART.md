# Quickstart / 빠른 시작

## Offline fixture check

Python 3.10+ and no dependency install are required. From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 src/continuity_demo.py check
```

`check` verifies that each seeded code task initially fails and the expected synthetic memory is top-ranked. It does **not** call Raon or repair code.

## Live A/B with Raon

Obtain your own key through [Raon's official console flow](https://raon-mini.krafton.ai/ko). Read the [hosted terms](https://raon-mini.krafton.ai/ko/terms) and [privacy policy](https://raon-mini.krafton.ai/ko/privacy) before using it. Keep it in a private shell environment; `.env.example` is a field guide, not a file loaded by this program.

```bash
export RAON_API_KEY='your-own-key'
python3 src/continuity_demo.py run --report reports/raon-local.json
```

For a cheaper first call, add `--case cache-key`. Each case runs both arms. The runner sends only public synthetic task, code, tests, and memory text; it does not scan home directories or invoke Memex. Raon's preview may take minutes and has per-organization request/token limits. The client waits up to 610 seconds per request. A 429 is recorded as an error; wait for the provider's `Retry-After` window before starting another run. An interrupted run does not imply a model result.

To use another compatible model, set `MODEL_API_BASE_URL` (HTTPS), `MODEL_ID`, and `MODEL_API_KEY`. The provider must support Chat Completions function tools. This is an interface option, not proof that all providers behave identically.

## Read the result

`tests_passed` is the outcome for each isolated code task. `relevant_memory_retrieved` is the predeclared record-ID match for B; it is always false for A by design. `input_tokens` and `output_tokens` are sums of provider `usage` fields; zero can mean usage was omitted. `duration_ms` includes API time and local tools. A report with `status=error` is a failed or incomplete run, not a zero-quality model answer. Do not publish a report without checking that it contains no user-added sensitive content.

## 한국어 빠른 시작

저장소 루트에서 `python3 src/continuity_demo.py check`를 실행하면 API 없이 합성 fixture와 검색 결과를 확인할 수 있습니다. 실제 A/B 실행은 본인에게 발급된 키를 터미널 환경 변수 `RAON_API_KEY`에 설정한 뒤 `python3 src/continuity_demo.py run --report reports/raon-local.json`으로 진행합니다. `reports/`는 Git에서 제외됩니다. 테스트 통과는 해당 합성 과제의 결과이며, 메모리 효과를 입증하려면 반복 실험과 더 큰 코퍼스가 필요합니다.
