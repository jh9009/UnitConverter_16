---
name: unit-converter-tdd
description: >-
  UnitConverter_16 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. 단위 변환 로직,
  CLI 입력 파싱, boundary/control/entity 코드 작성·수정, pytest TDD, 오류 메시지
  검증 시 사용.
---

# UnitConverter_16 — Dual-Track TDD Skill

헌법: 프로젝트 루트 `.cursorrules` · 요구사항: `docs/PRD.md`

## 언제 이 Skill을 켜는가

다음 작업을 시작하기 **전** 이 Skill을 적용한다.

- `src/entity/` 변환 로직·도메인 타입 작성/수정
- `src/control/` 검증·에러 코드 매핑·흐름 조율 작성/수정
- `src/boundary/` 터미널 I/O·입력 파싱 연동·오류 메시지 출력 작성/수정
- `tests/entity/`, `tests/control/`, `tests/boundary/` 테스트 추가/수정
- `UnitConverter.py`를 ECB 구조로 이전하거나 CLI 동작을 바꿀 때
- Mom Test SC-1~3(조용한 실패 방지·명확한 오류·TC 자동 검증) 관련 구현/리뷰

**켜지 않는 경우:** GUI, JSON 설정 외부화, 동적 단위 등록 등 PRD Out of Scope.

---

## 응답 선언 (매 턴 상단)

```
Phase: [RED/GREEN/REFACTOR] | Layer: [E/C/B] | Track: [Logic/UI]
```

---

## Logic Track vs UI Track

| 구분 | Layer | 디렉터리 | 역할 | Mock |
|------|-------|----------|------|------|
| **Logic** | E (Entity) | `src/entity/`, `tests/entity/` | 순수 변환·도메인 타입. I/O·에러코드 모름 | entity·도메인 **Mock 금지** |
| **Logic** | C (Control) | `src/control/`, `tests/control/` | 검증·E001/E002/E003 매핑·entity 호출 | entity **Mock 금지** (실제 entity 사용) |
| **UI** | B (Boundary) | `src/boundary/`, `tests/boundary/` | 터미널 I/O·메시지 포맷·control 위임 | control·입출력 **Mock 허용** |

**import 검증:** entity↛control/boundary · control↛boundary · boundary↛entity (boundary는 control만 import)

**RED 권장 순서:** entity (D-*) → control (D-*) → boundary (U-*)

---

## 테스트 ID·파일 명명

| Track | ID | 파일 패턴 | 위치 |
|-------|-----|-----------|------|
| Logic | `D-01`, `D-02`, … | `test_d_*.py` | `tests/entity/`, `tests/control/` |
| UI | `U-01`, `U-02`, … | `test_u_*.py` | `tests/boundary/` |

- 테스트 함수 docstring 또는 주석에 ID 명시 (예: `"""D-01: meter:2.5 → feet 변환"""`)
- RED 단계: **한 턴에 ID 하나**만 추가

---

## Phase: RED (5~7단계)

1. `.cursorrules`·PRD에서 해당 레이어 책임·에러 코드 확인
2. 대상 Track/Layer 결정 (entity 먼저, boundary는 마지막)
3. `test_d_*` 또는 `test_u_*`에 **실패하는 테스트 1개**만 추가 (ID 부여)
4. 실패 유형 명시: `AssertionError` / `NotImplementedError` 등 **의도적 RED**
5. **구현 코드 작성 금지** (테스트 파일만 변경)
6. 아래 pytest로 **실패 확인** (통과하면 RED 아님 — 테스트 수정)
7. 완료 보고 (템플릿) 작성

**RED 금지:** assert 완화, skip, xfail, entity Mock, 구현 선행

---

## Phase: GREEN (5~7단계)

1. RED에서 추가한 **동일 ID** 테스트만 통과시키는 최소 코드 작성
2. 변경 레이어만 수정 (E/C/B 중 해당 1개 원칙)
3. entity: 순수 로직만 · control: I/O 금지 · boundary: 계산 금지
4. SSOT 상수 사용 (`src/entity/constants.py` 등 — 매직 넘버 금지)
5. 오류 경로: 종료 전 `[코드] + 설명 + (가능하면) input` 출력 (boundary 경유)
6. 아래 pytest로 **해당 ID 통과** 확인
7. 완료 보고 (템플릿) 작성

**GREEN 금지:** RED 없이 구현, 다른 ID까지 한꺼번에 통과시키기, 테스트 삭제

---

## Phase: REFACTOR (5~7단계)

1. GREEN 상태 유지 확인 (`pytest` 전체 또는 해당 Track)
2. ECB·SRP 위반 여부 점검 (책임 섞임, import 역방향)
3. 중복 제거·이름 정리·SSOT 일원화
4. **동작 변경 없음** — 테스트 수정 최소화
5. REFACTOR 후 **전체 pytest** 재실행
6. 묵살 종료 방지 절차(아래) 재확인
7. 완료 보고 (템플릿) 작성

---

## 묵살 종료(조용한 실패) 방지 확인

Mom Test SC-1·SC-2 충족용. GREEN/REFACTOR 마지막에 수행.

| # | 확인 항목 | 기대 |
|---|-----------|------|
| 1 | `feet 5.8` (콜론 누락) | E001 + 설명 + input, 묵살 종료 없음 |
| 2 | `meter:` / `:2.5` | E001 + 설명, 빈 단위/값 구분 가능한 문구 |
| 3 | `inch:1.0` | E002 + 미지원 단위 명시 |
| 4 | `meter:-1` | E003 + 음수 명시 |
| 5 | `feet:abc` | E001 + 숫자 아님 명시 |
| 6 | 성공 위장 출력 | `Done.` 등 오류 후 성공처럼 보이는 출력 **없음** |
| 7 | entity 순수성 | entity에 print/input/에러코드 문자열 **없음** |

U-* 테스트 또는 수동 boundary 실행으로 위 케이스 중 **이번 변경과 관련된 항목** 최소 1개 이상 검증.

---

## Test / Review Loop — pytest 명령

프로젝트 루트에서 실행.

| 시점 | 명령 | 목적 |
|------|------|------|
| RED 직후 | `python -m pytest tests/entity/test_d_<name>.py -v` | entity RED 실패 확인 |
| RED 직후 | `python -m pytest tests/control/test_d_<name>.py -v` | control RED 실패 확인 |
| RED 직후 | `python -m pytest tests/boundary/test_u_<name>.py -v` | boundary RED 실패 확인 |
| GREEN 직후 | 위와 **동일 파일** `-v` | 해당 ID 통과 확인 |
| REFACTOR 후 | `python -m pytest tests/entity/ -v` | Logic entity 전체 |
| REFACTOR 후 | `python -m pytest tests/control/ -v` | Logic control 전체 |
| REFACTOR 후 | `python -m pytest tests/boundary/ -v` | UI boundary 전체 |
| Review (최종) | `python -m pytest -v` | Dual-Track 전체 통과 |

**Review 체크 (Mom Test):**

- SC-1: 오류 입력이 조용히 뻗지 않는가?
- SC-2: 메시지만으로 원인 특정 가능한가?
- SC-3: 정상·오류가 TC로 자동 검증되는가?

**0 collected:** 테스트 없이 GREEN/완료 선언 금지.

---

## 단계별 완료 보고 템플릿

매 Phase 종료 시 사용자에게 보고.

```markdown
### TDD 완료 보고
- Phase: [RED/GREEN/REFACTOR]
- Layer: [E/C/B] | Track: [Logic/UI]
- Test ID: [D-xx / U-xx]
- 파일: [변경한 src/ tests 경로]

**pytest 결과**
- 실행: `[실행한 명령]`
- 통과: [목록 또는 개수]
- 실패: [목록 또는 "없음 (RED 의도 실패: …)"]

**묵살 종료 점검** (GREEN/REFACTOR만)
- [ ] 관련 오류 케이스 메시지 출력 확인
- [ ] entity 순수성 유지

**다음 단계**
- [한 줄]
```

---

## Quick Reference — 에러 코드

| 코드 | 의미 | 예시 |
|------|------|------|
| E001 | 파싱 오류 | `feet 5.8`, `meter:abc` |
| E002 | 미지원 단위 | `inch:1.0` |
| E003 | 음수 | `meter:-1` |

에러 코드 매핑: **control** · 사용자 출력: **boundary**
