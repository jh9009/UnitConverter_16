# UnitConverter_16 — Cursor 설계 세션 Transcript (STEP 2)

**일자:** 2026-06-05  
**단계:** STEP 2 — 8계층 설계 · Harness · Rule · Skill · Command · Test/Review Loop · 마무리 점검

---

## 문서 구성

| Part | 내용 |
|------|------|
| A | 8계층 역할 설명 (초보자용 비유) |
| B | Harness·Rule·Skill·Command 구축 |
| C | Rule 리뷰 (P0 권고 반영) |
| D | Tool/MCP · Test/Review Loop SC-L1~5 |
| E | 설계 세션 마무리 8계층 점검 · tdd-green 추가 |

**선행:** [Mom Test STEP 1 Transcript](./Mom_Test_Transcript_STEP1.md) · [워크북 Transcript](./Mom_Test_Workbook_Transcript_STEP1.md)

---

# Part A — 8계층 역할 (요약)

| 계층 | 비유 | UnitConverter_16 |
|------|------|------------------|
| Model | 숙련공 두뇌 | 코드·테스트 초안 생성 |
| Agent | 현장 반장 | RED/GREEN/Review 조율 |
| Harness | 작업대 | `src/`, `tests/`, `pyproject.toml` |
| Rule | 헌법 | `.cursorrules` |
| Skill | 전문 매뉴얼 | `unit-converter-tdd/SKILL.md` |
| Command | 작업 지시서 | `tdd-red`, `tdd-green`, `review-ecb` |
| Tool/MCP | 렌치·pytest | Shell, Read/Write/Grep |
| Test/Review Loop | 품질 컨베이어 | pytest + review-ecb 표 |

Hook: 의도적 생략 (사용자 직접 통제)

---

# Part B — 산출물 구축 순서

## B-1. Harness (ECB + Dual-Track)

- `pyproject.toml` — `testpaths`, `pythonpath`
- `src/boundary/`, `src/control/`, `src/entity/` — 빈 `__init__.py`
- `tests/boundary/`, `tests/control/`, `tests/entity/` — 빈 `__init__.py`
- 로직·테스트 본문 없음 (골격만)

## B-2. Rule

- `.cursorrules` 초안 (ECB, E001~E003, Dual-Track, TDD, SSOT, AI 행동)

## B-3. Skill

- `.cursor/skills/unit-converter-tdd/SKILL.md`
- RED/GREEN/REFACTOR 7단계, Track 표, pytest 명령, 묵살 종료 체크, 완료 보고 템플릿

## B-4. Command (1차)

- `.cursor/commands/tdd-red.md` — RED 전용, `src/` 금지
- `.cursor/commands/review-ecb.md` — ECB 계약 표 리뷰, 수정 금지

---

# Part C — Rule 리뷰 및 P0 반영

## C-1. Ask 모드 리뷰 요약

| 항목 | 판정 |
|------|------|
| ECB import | ⚠️ → P0 보강 |
| Mock 정책 | ⚠️ control 테스트 명시 |
| E001~E003 | ⚠️ 메시지 형식 |
| TDD 게이트 | ✅ |
| Skill/Command 모호성 | ⚠️ |

## C-2. P0 반영 (`.cursorrules`만 수정)

1. import 금지 목록 (entity↛, control↛boundary, boundary↛entity)
2. 종료 전 메시지 의무
3. control 테스트 entity Mock 금지

---

# Part D — Tool/MCP · Loop 성공 기준

## D-1. Tool/MCP 매핑

- Shell `pytest` → Test Loop
- Read/Write/Grep → Rule·Skill·Command
- GitHub MCP → 선택 (PR/이슈)

## D-2. SC-L1 ~ SC-L5 (STEP 2)

1. Rule 존재 → 개발자 `.cursorrules` 확인
2. Skill·Harness → 개발자 디렉터리·Skill 대조
3. `/tdd-red` → Phase·금지·보고 확인
4. `/review-ecb` → 표·수정 없음
5. `pytest -v` → AI 실행 · configfile 확인

---

# Part E — 마무리 점검 · tdd-green 추가

## E-1. 8계층 점검 (STEP 2)

- ✅ Model, Harness, Rule, Skill, Tool/MCP
- ⚠️ Agent, Test/Review Loop, Hook (Hook·일부 ⚠️는 의도)
- ⚠️ Command → **tdd-green 부재** 지적

## E-2. 권고 1가지 — `/tdd-green` 추가

**이유:** RED ↔ review-ecb 사이 GREEN 게이트 없음 → Test Loop 단절

**조치:** `.cursor/commands/tdd-green.md` 생성

- Phase: GREEN / REFACTOR
- `src/` 최소 구현 · pytest PASS
- E001~E003·묵살 종료 방지
- REFACTOR: ECB·SSOT · PASS 유지
- 완료 후 `/review-ecb` 제안

## E-3. Command 최종 목록

| Command | 파일 |
|---------|------|
| `/tdd-red` | `tdd-red.md` |
| `/tdd-green` | `tdd-green.md` |
| `/review-ecb` | `review-ecb.md` |

---

## 산출물 맵

| 산출물 | 경로 |
|--------|------|
| 설계 세션 보고서 (STEP 2) | `Report/Cursor_Design_Session_Report_STEP2.md` |
| 설계 세션 Transcript (STEP 2, 본 문서) | `Prompting/Cursor_Design_Session_Transcript_STEP2.md` |
| Rule | `.cursorrules` |
| Skill | `.cursor/skills/unit-converter-tdd/SKILL.md` |
| Commands | `.cursor/commands/tdd-red.md`, `tdd-green.md`, `review-ecb.md` |

---

*Exported from UnitConverter_16 Cursor design session (STEP 2).*
