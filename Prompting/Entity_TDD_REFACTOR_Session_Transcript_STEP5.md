# UnitConverter_16 — Entity TDD REFACTOR 세션 Transcript (STEP 5)

**일자:** 2026-06-05  
**단계:** STEP 5 — Entity Logic Track REFACTOR — 스멜 스캔 · `/refactor-safe` 2턴 · pytest PASS 6/6

---

## 문서 구성

| Part | 내용 |
|------|------|
| A | `/refactor-smell` — P1 스멜 스캔·우선순위 확정 |
| B | `/refactor-safe` 턴 1 — Primitive Obsession (UNIT_* SSOT) |
| C | `/refactor-safe` 턴 2 — Silent Failure Risk (`to_meter` ValueError) |
| D | pytest PASS · Report·Transcript Export |
| E | 다음 Loop |

**선행:** [Entity TDD GREEN Transcript (STEP 4)](./Entity_TDD_GREEN_Session_Transcript_STEP4.md)

---

# Part A — `/refactor-smell`

## A-1. Phase·범위

```
Phase: REFACTOR | Scope: src/entity/ tests/entity/ | Track: Logic
```

- Change Budget: 턴당 파일 ≤2, 메서드 ≤2
- 코드 수정·commit 없이 스캔만 수행

## A-2. 전제 조건

```bash
pytest tests/entity/ -v
```

→ PASS 5/5 (GREEN 상태) 확인 후 스캔 진행.

## A-3. 스멜 표 (요약)

| 우선순위 | 스멜 | 위치 | 리팩터 후보 |
|----------|------|------|-------------|
| — | P0 (Long Method, ECB, src Magic Number) | — | 해당 없음 |
| **P1** | Primitive Obsession | `converter.py`, `validator.py` | `constants.py`에 UNIT_* SSOT |
| **P1** | Silent Failure Risk | `converter.py:to_meter` | KeyError → ValueError |
| P2 | 테스트 import 반복 | `test_d_*.py` | 모듈 상단 import (미착수) |

**P0 없음** → P1 Primitive Obsession을 1턴째 `/refactor-safe`로 제안.

---

# Part B — `/refactor-safe` 턴 1 (Primitive Obsession)

## B-1. 사용자 지시

```
Change Budget: 파일 2개, 메서드 2개 이하
- constants.py: UNIT_METER, UNIT_FEET, UNIT_YARD, ALL_UNITS
- converter.py: _TO_METER_FACTORS, convert_all dict 키가 SSOT 참조
- tests/ assert 변경 금지
```

## B-2. 적용 내용

**`constants.py` 추가:**

```python
UNIT_METER = "meter"
UNIT_FEET = "feet"
UNIT_YARD = "yard"
ALL_UNITS = (UNIT_METER, UNIT_FEET, UNIT_YARD)
```

**`converter.py` 치환:**

- `_TO_METER_FACTORS` 키: `"meter"` 등 → `UNIT_METER` 등
- `convert_all` 반환 키: 동일 SSOT 참조

## B-3. 검증

```bash
pytest tests/entity/ -v
```

→ PASS 5/5

---

# Part C — `/refactor-safe` 턴 2 (Silent Failure Risk)

## C-1. 사용자 지시

```
Change Budget: 파일 1개(converter), 메서드 1개(to_meter)
- KeyError → ValueError("Unsupported unit: {unit}")
- validate와 동일 도메인 예외 성격
- test_to_meter_unsupported_unit 추가
```

## C-2. `to_meter` 변경

```python
try:
    factor = _TO_METER_FACTORS[unit]
except KeyError:
    raise ValueError(f"Unsupported unit: {unit}") from None
return value * factor
```

- `validate` 메시지: `f"Unsupported unit: {unit}"` — **동일 형식**

## C-3. 신규 테스트

```python
def test_to_meter_unsupported_unit():
    with pytest.raises(ValueError, match="Unsupported unit: inch"):
        to_meter(1.0, "inch")
```

## C-4. 검증

```bash
pytest tests/entity/test_d_cnv_converter.py -v
```

→ PASS 4/4 (D-CNV-01~03 + 신규 1건)

전체:

```bash
pytest tests/entity/ -v
```

→ PASS **6/6**

---

# Part D — Export

## D-1. 산출 문서

- `Report/Entity_TDD_REFACTOR_Session_Report_STEP5.md`
- `Prompting/Entity_TDD_REFACTOR_Session_Transcript_STEP5.md` (본 문서)
- `README.md` · `docs/PRD.md` STEP 5 반영

## D-2. REFACTOR 완료 요약

| 턴 | 해소 스멜 | 파일 | TC |
|----|-----------|------|-----|
| 1 | Primitive Obsession | `constants.py`, `converter.py` | 5 (불변) |
| 2 | Silent Failure Risk | `converter.py`, `test_d_cnv_converter.py` | 6 (+1) |

**잔여:** `validator.SUPPORTED_UNITS` → `ALL_UNITS` (선택, 다음 턴)

---

# Part E — 다음 Loop

```
/review-ecb (Entity self-check 권장)
  → control RED/GREEN (D-CTL-*)
  → boundary RED/GREEN (U-*)
  → Golden Master (GM-*)
```

---

## 산출물 맵

| 산출물 | 경로 |
|--------|------|
| Entity REFACTOR 보고서 (STEP 5) | `Report/Entity_TDD_REFACTOR_Session_Report_STEP5.md` |
| Entity REFACTOR Transcript (STEP 5, 본 문서) | `Prompting/Entity_TDD_REFACTOR_Session_Transcript_STEP5.md` |
| SSOT·변환 | `src/entity/constants.py`, `converter.py` |
| 변환·REFACTOR TC | `tests/entity/test_d_cnv_converter.py` |

---

*Exported from UnitConverter_16 Entity TDD REFACTOR session (STEP 5).*
