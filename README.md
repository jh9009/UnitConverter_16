
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)

### Overview

- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### Mom Test 배경 (STEP 1)

**진짜 문제:** 입력 오타(콜론 누락, 공백, 잘못된 단위)로 변환이 에러 없이 끊기면, 30분 넘는 수동 추적·재작업과 메모장 검사·복붙 같은 우회 루틴이 반복된다.

**구현 목표:** 조용한 실패를 없애기 위해, 잘못된 입력마다 즉시 원인을 알려주는 검증과 정확한 길이 단위 변환을 구현한다.

### 아키텍처 (ECB + Dual-Track TDD)

```
boundary (입출력) → control (검증·흐름) → entity (순수 변환)
tests/boundary (U-*)  tests/control (D-*)  tests/entity (D-*)
```

| Cursor 산출물 | 경로 |
|---------------|------|
| Rule | [.cursorrules](./.cursorrules) |
| Skill | [.cursor/skills/unit-converter-tdd/SKILL.md](./.cursor/skills/unit-converter-tdd/SKILL.md) |
| Command RED | [.cursor/commands/tdd-red.md](./.cursor/commands/tdd-red.md) |
| Command GREEN | [.cursor/commands/tdd-green.md](./.cursor/commands/tdd-green.md) |
| Command Review | [.cursor/commands/review-ecb.md](./.cursor/commands/review-ecb.md) |

**TDD 워크플로:** `/tdd-red` → `/red-skeleton` → `/tdd-green` → `/review-ecb`

**Harness 골격 (STEP 2):** `pyproject.toml` · `src/{entity,control,boundary}/` · `tests/{entity,control,boundary}/` · 레거시 [`UnitConverter.py`](./UnitConverter.py) (ECB 미연동)

### 문서 역할

| 문서 | 역할 |
|------|------|
| **README** (본 문서) | 진입·실행·**진행 todo**·문서 링크 |
| **[docs/PRD.md](./docs/PRD.md)** | 요구 계약 — R-G-I-O, FR/SC, Test ID 정의, 범위 (진행 스냅샷은 README) |

### 프로젝트 진행 (STEP)

| STEP | 내용 | 상태 |
|------|------|------|
| 1 | Mom Test · 워크북(8/10) · PRD 초안 | ✅ |
| 2 | ECB Harness · `.cursorrules` · Skill · Command×3 | ✅ |
| 3 | Entity Logic RED (D-CNV/D-VAL 스켈레톤) | ✅ |
| 3 | Entity GREEN (`src/entity/`) | ⏳ **다음** |
| — | Control RED/GREEN · Boundary(U-*) · `UnitConverter.py` ECB 연동 | ⏳ |

### TDD Todo (권장 순서: entity → control → boundary)

- [x] STEP 2 Harness 골격 (`src/`, `tests/`, `pyproject.toml`)
- [x] Entity RED — D-CNV-01~03, D-VAL-01~02 (`tests/entity/test_d_*.py`)
- [ ] Entity GREEN — `constants.py`, `converter.py`, `validator.py` + Then assert
- [ ] Entity REFACTOR
- [ ] Control RED/GREEN — E001/E002/E003 매핑
- [ ] Boundary RED/GREEN — U-* CLI·I/O
- [ ] `/review-ecb` — Mom Test SC-1~3 회귀 확인

| Layer | RED | GREEN | REFACTOR |
|-------|-----|-------|----------|
| Entity | ✅ | ⏳ | ⏳ |
| Control | ⏳ | ⏳ | ⏳ |
| Boundary | ⏳ | ⏳ | ⏳ |

**다음 작업:** `Phase: GREEN | Layer: Entity` — `/tdd-green`

```bash
# Entity RED 확인 (의도적 FAIL — ModuleNotFoundError)
pytest tests/entity/ -v
```

### 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](./docs/PRD.md) | 제품 요구사항·Test ID 정의 (진행 현황은 본 README) |
| [Report/Entity_TDD_RED_Session_Report_STEP3.md](./Report/Entity_TDD_RED_Session_Report_STEP3.md) | Entity TDD RED 세션 보고서 (STEP 3) |
| [Report/Cursor_Design_Session_Report_STEP2.md](./Report/Cursor_Design_Session_Report_STEP2.md) | Cursor 8계층 설계 세션 보고서 (STEP 2) |
| [Report/Mom_Test_Report_STEP1.md](./Report/Mom_Test_Report_STEP1.md) | Mom Test STEP 1 인터뷰 보고서 |
| [Report/Mom_Test_Workbook_Report_STEP1.md](./Report/Mom_Test_Workbook_Report_STEP1.md) | Mom Test STEP 1 워크북 보고서 |
| [Prompting/Entity_TDD_RED_Session_Transcript_STEP3.md](./Prompting/Entity_TDD_RED_Session_Transcript_STEP3.md) | Entity TDD RED Transcript (STEP 3) |
| [Prompting/Cursor_Design_Session_Transcript_STEP2.md](./Prompting/Cursor_Design_Session_Transcript_STEP2.md) | Cursor 설계 세션 Transcript (STEP 2) |
| [Prompting/Mom_Test_Transcript_STEP1.md](./Prompting/Mom_Test_Transcript_STEP1.md) | Mom Test STEP 1 인터뷰 Transcript |
| [Prompting/Mom_Test_Workbook_Transcript_STEP1.md](./Prompting/Mom_Test_Workbook_Transcript_STEP1.md) | Mom Test STEP 1 워크북 Transcript |

### 가상환경 설정 및 실행

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행 (레거시)
python UnitConverter.py

# Dual-Track 테스트
python -m pytest -v

# 가상환경 비활성화
deactivate
```

### 기본 요구사항

1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항

- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)
- **조용한 실패 금지** — 오류 시 명확한 메시지 출력 (Mom Test SC-1, SC-2)

### 성공 기준 (STEP 1 워크북)

| ID | 기준 |
|----|------|
| SC-1 | 콜론 누락·공백 입력 시 명확한 오류 메시지 (조용히 뻗지 않음) |
| SC-2 | 오류 메시지만으로 몇 초 안에 원인 특정 |
| SC-3 | 정상·오류 케이스 테스트 코드 자동 검증 |

### 추가 요구사항 (Out of Scope — STEP 1 워크북)

- **설정 외부화** — 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적 단위 등록** — `1 cubit = 0.4572 meter` 등록 및 사용
- **출력 포맷 선택** — JSON / CSV / 표 형태 출력

## 생성형AI를 활용한 Activities (6 시간)

| # | Activity | 상태 | 비고 |
|---|----------|------|------|
| 1 | 문제 코드·요구사항 분석 (0.5h) | ✅ | Mom Test STEP 1, PRD, STEP 2 Cursor 설계 |
| 2 | 기본·품질 요구 구현 (2h) | ⏳ | Entity GREEN부터 (`/tdd-green`) |
| 3 | TC 구현 (0.5h) | △ | Entity RED 스켈레톤 5건; PASS·U-* 미착수 |
| 4 | 추가 요구 구현 (2h) | ⏳ | Out of Scope 항목 — [PRD §4.3](./docs/PRD.md) |
| 5 | 회고 및 발표 (1h) | △ | Report·Prompting STEP 1~3 기록 |

상세 세션 기록: [Report/](./Report/) · [Prompting/](./Prompting/)
