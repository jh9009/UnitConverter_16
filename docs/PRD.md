# UnitConverter_16 — PRD (Product Requirements Document)

**버전:** 0.3 (초안)  
**일자:** 2026-06-05  
**근거:** Mom Test STEP 1 인터뷰 · STEP 1 워크북 · STEP 2~4 TDD (Entity GREEN 완료)

---

## 0. 문서 역할 (README와의 분리)

| 문서 | 역할 |
|------|------|
| **본 PRD** | 요구 **계약** — 페르소나, R-G-I-O, FR/SC, Test ID **정의**, In/Out of Scope |
| **[README](../README.md)** | repo **진입** — 실행법, Harness 요약, **STEP·TDD 진행 todo**, pytest 스냅샷 |

진행 상태(RED/GREEN 완료 여부)는 README를 SSOT로 한다. 본 문서 §8은 Test ID가 **무엇을 검증해야 하는지**만 정의한다.

---

## 1. 배경 및 페르소나

**페르소나:** 연구실·회사에서 길이 단위 변환(미터, 피트, 야드) 스크립트를 반복적으로 수동 조작하다가, 입력 오류로 프로그램이 뻗고 시간을 낭비한 작업자.

**Mom Test 진짜 문제 (솔루션 없음):**

입력 형식 오타 하나로 변환이 에러 없이 중단되면, 어디가 틀렸는지 알 수 없어 30분 넘는 수동 추적(터미널·소스·엑셀)과 처음부터 재작업이 반복되고, 그 비용을 줄이려 사용자가 메모장 검사·한 줄씩 복붙 같은 추가 루틴까지 스스로 부담한다.

**Mom Test 증거:**

1. 오타 한 번에 스크립트가 **에러 메시지 없이** 뻗음 (`feet:5.8` 수동 반복 입력 중)
2. 원인 찾기 **30분+** — 터미널 스크롤 → 소스 if-else 훑기 → 엑셀에서 진행 지점 확인 → 처음부터 재실행
3. 이후 **메모장 선작성 → 콜론·공백 눈 검사 → 한 줄씩 복붙** 우회 루틴 자발적 도입

---

## 2. 주제 (두 줄 분리)

**진짜 문제:** 입력 오타(콜론 누락, 공백, 잘못된 단위) 하나로 변환이 에러 없이 끊기면, 어디가 틀렸는지 알 수 없어 30분 넘는 수동 추적·처음부터 재작업과 메모장 검사·한 줄씩 복붙 같은 우회 루틴이 반복된다.

**구현 목표:** 그 조용한 실패를 없애기 위해, 잘못된 입력마다 즉시 무엇이 틀렸는지 알려주는 검증과 정확한 길이 단위 변환을 구현한다.

---

## 3. R-G-I-O

| 항목 | 내용 |
|------|------|
| **Role** | 길이 단위 변환 스크립트를 리팩토링·검증하는 개발자 (수동 입력·오타에 취약한 작업자의 고통을 이해한 입장) |
| **Goal** | `meter:2.5` 형식 입력 시 meter/feet/yard로 정확히 변환하고, 오타·잘못된 형식·없는 단위·음수에 대해 **에러 없이 뻗지 않고** 즉시 이해 가능한 메시지로 알려준다 |
| **Input** | 터미널 한 줄 입력 — `단위:값`. 오류 케이스: `meter 9.1`, `meter:`, `:2.5`, `feet:abc`, `inch:1.0`, `meter:-1` |
| **Output** | **정상:** 모든 지원 단위 변환 결과 출력. **오류:** 원인이 드러나는 명확한 메시지 후 종료 (묵살 종료·성공처럼 보이는 출력 금지) |

---

## 4. 기능 요구사항

### 4.1 핵심 (In Scope — STEP 1 워크북)

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| FR-1 | `단위:값` 형식 파싱 및 meter/feet/yard 변환 | P0 |
| FR-2 | 형식 오류(콜론 누락, 공백, 빈 단위/값) 시 구체적 오류 메시지 | P0 |
| FR-3 | 숫자 아님·음수·미지원 단위 시 구체적 오류 메시지 | P0 |
| FR-4 | OCP 준수 — 단위 추가 시 기존 코드 최소 변경 | P1 |
| FR-5 | SRP 준수 — 파싱·검증·변환·출력 책임 분리 | P1 |
| FR-6 | 정상·오류 케이스 단위 테스트 자동 검증 | P0 |

### 4.2 비즈니스 규칙

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간 비율은 meter 기반 계산
- 지원 단위: meter, feet, yard

### 4.3 Out of Scope (표면 문제 — STEP 1 워크북 제외)

| 제외 항목 | 이유 |
|-----------|------|
| 화려한 GUI / 웹 UI | 핵심 불편은 UI 부재가 아닌 조용한 실패 |
| JSON/YAML 설정 외부화 | 추가 요구사항, STEP 1 워크북 범위 밖 |
| 동적 단위 등록 (`1 cubit = 0.4572 meter`) | 추가 요구사항, STEP 1 워크북 범위 밖 |
| JSON/CSV 출력 포맷 선택 | 추가 요구사항, STEP 1 워크북 범위 밖 |
| 대규모 아키텍처·프레임워크 도입 | 검증·메시지·TC가 우선 |
| 배치 입력·중간 저장·재시작 복구 | 다음 세션 후보 |

---

## 5. 성공 기준

| ID | 기준 | Mom Test 증거 연결 |
|----|------|-------------------|
| **SC-1** | 콜론 누락(`feet 5.8`), 공백·형식 오류 입력 시 조용히 뻗지 않고, 기대 형식과 받은 입력이 담긴 **명확한 오류 메시지** 즉시 출력 | 증거 1: 에러 메시지 없이 뻗음 |
| **SC-2** | 잘못된 단위·음수·숫자 아님 입력 시 **소스·엑셀 대조 없이** 메시지만으로 **몇 초 안에** 원인 특정 가능 | 증거 2: 30분+ 수동 추적 |
| **SC-3** | 정상 입력 변환 및 위 오류 케이스가 **테스트 코드로 자동 검증** (메모장 수동 검사에 의존하지 않음) | 증거 3: 메모장 눈 검사 우회 |

---

## 6. 8계층 — STEP 1 워크북 적용 범위

### Rule

- Mom Test 진짜 문제 우선: 입력 오타 시 조용히 실패하지 말 것
- OCP·SRP 준수
- 모든 잘못된 입력은 명확한 오류 메시지와 함께 종료
- 비즈니스 비율 고정 (meter 기준)
- 테스트 없이 검증 로직 완료 선언 금지

### Command

1. `UnitConverter.py` 구조 분석 (입력 파싱 → 변환 → 출력)
2. 입력 검증 분리 (형식·숫자·단위·음수별 메시지)
3. OCP/SRP에 맞게 클래스·인터페이스로 변환 로직 분리
4. 정상 변환 TC + 오류 입력 TC 작성 (SC-1~3 커버)
5. 오류 메시지가 수동 추적 없이 원인 특정 가능한지 Review

### Skill (참고)

- Python 입력 파싱·예외 처리
- 단위 테스트 작성 (pytest)
- OCP/SRP 리팩토링
- Mom Test 증거 → 성공 기준 추적

### Test / Review Loop

**Test**

- 정상: `meter:2.5` → meter/feet/yard 출력 값 검증
- 오류: `feet 5.8`, `meter:`, `:2.5`, `unknown:1`, `meter:-1`, `meter:abc` → 즉시 실패 + 구체 메시지

**Review (Mom Test 체크)**

- SC-1: 증거 1 케이스(에러 없이 뻗음) 재현 불가?
- SC-2: 오류 메시지만으로 30분 추적 루틴 없이 원인 특정?
- SC-3: TC로 정상·오류 자동 검증?

---

## 7. 워크북 채점 (참고)

**점수:** 8 / 10

| 체크 항목 | 결과 |
|-----------|------|
| 미래 가정 배제 | ✅ |
| 과거 행동·시간·실수 구체성 | ✅ |
| 진짜 문제에 솔루션명 미혼입 | ⚠️ (주제 한 문장 혼합 → 두 줄 분리로 개선) |
| 표면/진짜 문제 분리·범위 통제 | ✅ |
| UnitConverter 도메인 반영 | ✅ |

---

## 8. Test ID 추적표 (요구 정의)

> **진행 현황:** [README § 프로젝트 진행](../README.md) · TDD Todo

### 8.1 Entity — Logic Track (`tests/entity/`, `D-*`)

| ID | 테스트 파일 | 대상 | Given → Then (검증 의도) | FR/SC 연결 |
|----|-------------|------|--------------------------|------------|
| D-CNV-01 | `test_d_cnv_converter.py` | `to_meter` | 1 feet → 0.3048 m (±ε, SSOT) | FR-1 |
| D-CNV-02 | 동일 | `convert_all` | 2.5 m → feet 8.20210 (5 decimals) | FR-1 |
| D-CNV-03 | 동일 | `convert_all` | feet→yard, meter 경유 일관성 | FR-1 |
| D-VAL-01 | `test_d_val_validator.py` | `validate` | `inch` → 도메인 거부 (control→E002) | FR-3, SC-2 |
| D-VAL-02 | 동일 | `validate` | `-1` → 도메인 거부 (control→E003) | FR-3, SC-2 |

**Entity 구현 모듈 (GREEN — STEP 4 완료):**

| 모듈 | 책임 |
|------|------|
| `src/entity/constants.py` | SSOT (`FEET_PER_METER`, `YARDS_PER_METER` 및 역산) |
| `src/entity/converter.py` | `to_meter`, `convert_all` |
| `src/entity/validator.py` | `validate` — 도메인 `ValueError` (E00x 문자열 없음) |

**Harness·import (STEP 4):** `tests/entity/` 디렉터리명과 `entity` 패키지 충돌 회피 — `pyproject.toml` `pythonpath = ["."]`, 테스트·REPL은 `from src.entity.*`.

**GREEN assert 규약:** CNV → `pytest.approx(..., rel=1e-5)` · VAL → `pytest.raises(ValueError, match=...)`.

### 8.2 Control — Logic Track (예정, `tests/control/`)

| ID (예정) | 검증 의도 | FR/SC |
|-----------|-----------|-------|
| D-CTL-* | E001 파싱·형식 오류 매핑 | FR-2, SC-1 |
| D-CTL-* | E002 미지원 단위 매핑 | FR-3, SC-2 |
| D-CTL-* | E003 음수 매핑 | FR-3, SC-2 |

### 8.3 Boundary — UI Track (예정, `tests/boundary/`, `U-*`)

| ID (예정) | 검증 의도 | FR/SC |
|-----------|-----------|-------|
| U-* | 터미널 I/O·`[코드]+설명+input` 출력 | FR-2, FR-3, SC-1, SC-2 |
| U-* | 조용한 실패·`Done.` 등 성공 위장 없음 | SC-1 |

**권장 TDD 순서:** entity (D-CNV/D-VAL) → control → boundary (U-*)

### 8.4 Golden Master / E2E (예정 — Entity 범위 외)

> **진행:** Boundary GREEN + `UnitConverter.py` ECB 연동 **이후**. Entity Logic Track에서는 수행하지 않음.

| ID (예정) | 위치 (예정) | 검증 의도 | FR/SC |
|-----------|-------------|-----------|-------|
| GM-01 | `tests/golden/` | `meter:2.5` 정상 CLI 출력 전체 스냅샷 | FR-1, SC-3 |
| GM-02 | 동일 | `feet 5.8` → E001 메시지 전체 | FR-2, SC-1 |
| GM-03 | 동일 | `inch:1.0` → E002 메시지 전체 | FR-3, SC-2 |

---

## 9. 관련 문서

- [Entity TDD GREEN 보고서 (STEP 4)](../Report/Entity_TDD_GREEN_Session_Report_STEP4.md)
- [Entity TDD GREEN Transcript (STEP 4)](../Prompting/Entity_TDD_GREEN_Session_Transcript_STEP4.md)
- [Entity TDD RED 보고서 (STEP 3)](../Report/Entity_TDD_RED_Session_Report_STEP3.md)
- [Entity TDD RED Transcript (STEP 3)](../Prompting/Entity_TDD_RED_Session_Transcript_STEP3.md)
- [Cursor 설계 세션 보고서 (STEP 2)](../Report/Cursor_Design_Session_Report_STEP2.md)
- [Cursor 설계 세션 Transcript (STEP 2)](../Prompting/Cursor_Design_Session_Transcript_STEP2.md)
- [Mom Test 보고서 (STEP 1)](../Report/Mom_Test_Report_STEP1.md)
- [Mom Test Transcript (STEP 1)](../Prompting/Mom_Test_Transcript_STEP1.md)
- [Mom Test 워크북 보고서 (STEP 1)](../Report/Mom_Test_Workbook_Report_STEP1.md)
- [Mom Test 워크북 Transcript (STEP 1)](../Prompting/Mom_Test_Workbook_Transcript_STEP1.md)

## 10. Cursor TDD Command (설계 세션)

| Command | 용도 |
|---------|------|
| `/tdd-red` | 실패 테스트 설계·ID 확정 (`tests/` only) |
| `/red-skeleton` | RED 스켈레톤 작성 (`pytest.fail`, `src/` 금지) |
| `/tdd-green` | 최소 구현·REFACTOR (`src/`) |
| `/review-ecb` | ECB·Mom Test 계약 리뷰 (수정 금지) |

Rule: [`.cursorrules`](../.cursorrules) · Skill: [`.cursor/skills/unit-converter-tdd/SKILL.md`](../.cursor/skills/unit-converter-tdd/SKILL.md)
