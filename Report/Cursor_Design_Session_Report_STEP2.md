# UnitConverter_16 — Cursor 설계 세션 보고서 (STEP 2)

**일자:** 2026-06-05  
**단계:** STEP 2 — Cursor 8계층 설계 (ECB + Dual-Track TDD)  
**선행:** Mom Test STEP 1 · [워크북 보고서](./Mom_Test_Workbook_Report_STEP1.md)

---

## 1. 주제 (한 문장)

입력 오타 하나로 변환이 에러 없이 끊겨 30분 넘게 수동 추적하는 **조용한 실패**를 없애기 위해, 잘못된 입력마다 즉시 원인을 알려주는 **검증 로직**을 구현한다.

---

## 2. 설계 산출물 목록

| 산출물 | 경로 | 역할 (8계층) |
|--------|------|--------------|
| Rule (헌법) | `.cursorrules` | ECB·E001~E003·조용한 실패 금지·Mock·SSOT·TDD 게이트 |
| Harness | `pyproject.toml`, `src/`, `tests/` | ECB 디렉터리·pytest 설정 |
| Skill | `.cursor/skills/unit-converter-tdd/SKILL.md` | Dual-Track TDD 절차·pytest·완료 보고 |
| Command RED | `.cursor/commands/tdd-red.md` | 실패 테스트 먼저 (`tests/`만) |
| Command GREEN/REFACTOR | `.cursor/commands/tdd-green.md` | 최소 구현·정리 (`src/`) |
| Command Review | `.cursor/commands/review-ecb.md` | ECB 계약 리뷰 (코드 수정 금지) |
| PRD | `docs/PRD.md` | R-G-I-O·SC-1~3·범위 |
| Hook | *(없음 — 의도)* | 사용자 직접 통제 |

---

## 3. `.cursorrules` 핵심 (P0 반영)

- **ECB import 금지:** entity↛control/boundary · control↛boundary · boundary↛entity
- **조용한 실패 금지:** 종료 전 `[코드]+설명+(input)` · `Done.` 등 성공 위장 출력 금지
- **에러 코드:** E001 파싱 · E002 미지원 단위 · E003 음수 (entity 모름)
- **Dual-Track Mock:** Logic(entity/control) Domain Mock 금지 · UI(boundary) Mock 허용
- **테스트 명명:** D-* / U-* · `test_d_*` / `test_u_*`
- **SSOT:** `3.28084`, `1.09361` 단일 모듈

---

## 4. 8계층 마무리 점검

| 계층 | 상태 | 근거 |
|------|------|------|
| Model | ✅ | IDE 모델 선택 (프로젝트 산출물 외) |
| Agent | ⚠️ | Ask/Agent 역할은 워크플로에 맞으나 Rule에 문장 고정 없음 |
| Harness | ✅ | `src/{entity,control,boundary}`, `tests/` 골격·`pyproject.toml` |
| Rule | ✅ | `.cursorrules` 완료 |
| Skill | ✅ | `unit-converter-tdd/SKILL.md` |
| Command | ✅ | `/tdd-red`, `/tdd-green`, `/review-ecb` (GREEN 추가로 Loop 보완) |
| Tool/MCP | ✅ | Shell(pytest), Read/Write/Grep — Skill·Command 연동 |
| Test/Review Loop | ⚠️ | review-ecb·pytest Harness OK · D-/U-* TC 본문 미착수 |
| Hook | ⚠️ | 의도적 생략 — 자동 게이트 없음 |

**요약:** STEP 2 설계 목표(헌법·절차·골격·리뷰 루프 정의) **달성**. 구현 TDD 착수 가능.

---

## 5. Test/Review Loop 성공 기준 (STEP 2)

| ID | 기준 | 검증자 | 방법 |
|----|------|--------|------|
| SC-L1 | Rule 존재·계약 완전 | 개발자 | `.cursorrules` 확인 |
| SC-L2 | Skill·Harness 연동 | 개발자 | Skill + `pyproject.toml` + 디렉터리 대조 |
| SC-L3 | RED Command 작동 | 개발자 | `/tdd-red` → Phase 선언·금지·보고 |
| SC-L4 | review-ecb 작동 | 개발자 | `/review-ecb` → 표 출력·코드 수정 없음 |
| SC-L5 | pytest Harness | AI | `python -m pytest -v` · configfile 인식 |

---

## 6. TDD Command 워크플로

```
/tdd-red     → tests/ only · FAIL 확인
/tdd-green   → src/ 최소 구현 · PASS · REFACTOR · review-ecb 제안
/review-ecb  → IMP/ERR/SSOT/MOCK 표 · 수정 금지
```

**권장 순서 (Logic):** entity (D-*) → control (D-*) → boundary (U-*)

---

## 7. 구현 준비 상태

| 항목 | 상태 |
|------|------|
| Mom Test STEP 1 | ✅ |
| PRD·워크북 | ✅ |
| Cursor Rule·Skill·Command (STEP 2) | ✅ |
| ECB Harness | ✅ |
| `src/` 로직·`test_*.py` | ⏳ 다음 단계 (TDD RED부터) |
| `UnitConverter.py` ECB 이전 | ⏳ boundary 연동 예정 |

---

## 8. 관련 문서

- [Cursor 설계 세션 Transcript (STEP 2)](../Prompting/Cursor_Design_Session_Transcript_STEP2.md)
- [Mom Test 워크북 보고서 (STEP 1)](./Mom_Test_Workbook_Report_STEP1.md)
- [PRD](../docs/PRD.md)
