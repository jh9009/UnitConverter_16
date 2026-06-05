# UnitConverter_16 — Entity TDD GREEN 세션 Transcript (STEP 4)

**일자:** 2026-06-05  
**단계:** STEP 4 — Entity Logic Track GREEN — 스켈레톤 교체 · 최소 구현 · pytest PASS · REPL 스모크

---

## 문서 구성

| Part | 내용 |
|------|------|
| A | `/tdd-green` — RED 재확인·GREEN 범위 확정 |
| B | 테스트 Then 교체 (스켈레톤 → assert) |
| C | `src/entity/` 최소 구현 |
| D | import 충돌 해결 · Harness 조정 |
| E | pytest PASS · REPL 스모크 |
| F | Report·Transcript Export · 다음 단계 |

**선행:** [Entity TDD RED Transcript (STEP 3)](./Entity_TDD_RED_Session_Transcript_STEP3.md)

---

# Part A — `/tdd-green` RED 재확인

## A-1. Phase 선언

```
Phase: GREEN | Layer: Entity | Track: Logic
```

- 대상 ID: D-CNV-01~03, D-VAL-01~02
- REFACTOR: **본 턴 범위 외** (사용자 명시)

## A-2. RED 재확인

```bash
pytest tests/entity/ -v
```

STEP 3 종료 시점: 5 failed (`ModuleNotFoundError` — `src/` 미구현).

---

# Part B — 테스트 Then 교체

## B-1. 공통 규칙

| 항목 | RED (STEP 3) | GREEN (STEP 4) |
|------|--------------|----------------|
| Then | `pytest.fail("RED: ...")` | 실제 assert |
| CNV | — | `pytest.approx(expected, rel=1e-5)` |
| VAL | — | `pytest.raises(ValueError, match="...")` |

## B-2. 변환 테스트 (`test_d_cnv_converter.py`)

| ID | assert 요약 |
|----|-------------|
| D-CNV-01 | `to_meter(1.0, "feet")` ≈ `0.3048` |
| D-CNV-02 | `convert_all(2.5, "meter")["feet"]` ≈ `8.20210` |
| D-CNV-03 | `METERS_PER_FOOT`·`METERS_PER_YARD` 기준 meter 경유 일관성 |

## B-3. 검증 테스트 (`test_d_val_validator.py`)

| ID | assert 요약 |
|----|-------------|
| D-VAL-01 | `match="Unsupported unit: inch"` |
| D-VAL-02 | `match="Value must not be negative"` |

---

# Part C — `src/entity/` 최소 구현

## C-1. `constants.py` (SSOT)

```python
FEET_PER_METER = 3.28084
YARDS_PER_METER = 1.09361
METERS_PER_FOOT = 1 / FEET_PER_METER
METERS_PER_YARD = 1 / YARDS_PER_METER
```

## C-2. `converter.py`

- `to_meter(value, unit)` — meter/feet/yard → meter
- `convert_all(value, unit)` — `{"meter", "feet", "yard"}` dict
- 내부 import: `from .constants import ...` (패키지 상대 경로)

## C-3. `validator.py`

- `SUPPORTED_UNITS = frozenset({"meter", "feet", "yard"})`
- 미지원 단위 → `ValueError("Unsupported unit: {unit}")`
- 음수 → `ValueError("Value must not be negative")`
- E001/E002/E003 문자열 **없음**

---

# Part D — import 충돌 · Harness 조정

## D-1. 문제

- `tests/entity/` 디렉터리명이 `entity` 패키지와 이름 충돌
- `pythonpath = ["src"]` + `from entity.*` → pytest 시 `entity.converter` 미발견
- 타 머신 `site-packages`에 다른 프로젝트 `entity` 패키지 존재 가능

## D-2. 해결

| 변경 | 내용 |
|------|------|
| `pyproject.toml` | `pythonpath = ["."]` (프로젝트 루트) |
| 테스트 import | `from src.entity.converter import ...` |
| `converter.py` | `from .constants import ...` (상대 import) |

---

# Part E — pytest PASS · REPL 스모크

## E-1. pytest

```bash
pytest tests/entity/ -v
```

```
collected 5 items
5 passed in 0.02s
```

## E-2. REPL 스모크

```bash
python -c "from src.entity.converter import convert_all; print(convert_all(2.5, 'meter'))"
```

```
{'meter': 2.5, 'feet': 8.2021, 'yard': 2.734025}
```

PRD 비즈니스 규칙과 일치 확인.

---

# Part F — Export · 다음 단계

## F-1. Report·Transcript (본 세션)

- `Report/Entity_TDD_GREEN_Session_Report_STEP4.md`
- `Prompting/Entity_TDD_GREEN_Session_Transcript_STEP4.md` (본 문서)
- `README.md` · `docs/PRD.md` STEP 4 반영

## F-2. GREEN 완료 보고 요약

| 항목 | 값 |
|------|-----|
| Phase | GREEN (REFACTOR 미수행) |
| PASS ID | D-CNV-01~03, D-VAL-01~02 (5/5) |
| 변경 | `src/entity/` 3파일 · `tests/entity/` 2파일 · `pyproject.toml` |

## F-3. 다음 Loop

```
Entity REFACTOR (선택)
  → control RED/GREEN (D-CTL-*)
  → boundary RED/GREEN (U-*)
  → Golden Master (GM-*, Boundary+ECB 연동 후)
  → /review-ecb
```

---

## 산출물 맵

| 산출물 | 경로 |
|--------|------|
| Entity GREEN 보고서 (STEP 4) | `Report/Entity_TDD_GREEN_Session_Report_STEP4.md` |
| Entity GREEN Transcript (STEP 4, 본 문서) | `Prompting/Entity_TDD_GREEN_Session_Transcript_STEP4.md` |
| SSOT·변환·검증 | `src/entity/constants.py`, `converter.py`, `validator.py` |
| Logic 테스트 (PASS) | `tests/entity/test_d_cnv_converter.py`, `test_d_val_validator.py` |

---

*Exported from UnitConverter_16 Entity TDD GREEN session (STEP 4).*
