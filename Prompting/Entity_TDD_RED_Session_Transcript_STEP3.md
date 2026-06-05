# UnitConverter_16 — Entity TDD RED 세션 Transcript (STEP 3)

**일자:** 2026-06-05  
**단계:** STEP 3 — Entity Logic Track RED 설계 확정 · RED 스켈레톤 작성 · pytest FAIL 확인

---

## 문서 구성

| Part | 내용 |
|------|------|
| A | `/tdd-red` — Entity 설계표 확정 (D-CNV·D-VAL) |
| B | `/red-skeleton` — 스켈레톤 규칙·파일 작성 |
| C | pytest 실행·FAIL 보고 |
| D | GREEN 전 준비·다음 Command |

**선행:** [Cursor 설계 STEP 2 Transcript](./Cursor_Design_Session_Transcript_STEP2.md)

---

# Part A — `/tdd-red` Entity 설계 확정

## A-1. 대상 Layer·Track

```
Phase: RED | Layer: Entity | Track: Logic
```

- 위치: `tests/entity/`
- 파일 패턴: `test_d_*.py`
- Mock: Domain Mock **금지** (`.cursorrules`)

## A-2. 변환 테스트 (converter)

| ID | 함수 | 시나리오 |
|----|------|----------|
| D-CNV-01 | `to_meter` | 1 feet → 0.3048 m (±ε) |
| D-CNV-02 | `convert_all` | 2.5 m → feet 8.20210 (5 decimals) |
| D-CNV-03 | `convert_all` | feet → yard, meter 경유 일관성 |

## A-3. 검증 테스트 (validator)

| ID | 함수 | 시나리오 |
|----|------|----------|
| D-VAL-01 | `validate` | `inch` → 거부 (control E002 예정) |
| D-VAL-02 | `validate` | `-1` → 거부 (control E003 예정) |

## A-4. Entity 경계

- E001/E002/E003 **문자열 출력 금지** — control/boundary 책임
- `validate`는 도메인 거부만 (예외·Result 타입 등 GREEN에서 결정)
- SSOT: `1 m = 3.28084 ft`, `1 m = 1.09361 yd` → `constants.py` 단일 정의

---

# Part B — `/red-skeleton` 실행

## B-1. 사용자 지시 요약

- 대상 파일 2개:
  1. `tests/entity/test_d_cnv_converter.py` (D-CNV-01~03)
  2. `tests/entity/test_d_val_validator.py` (D-VAL-01~02)
- AAA 주석 필수
- Then: `pytest.fail("RED: [Test ID] — 구현 없음, 의도적 실패")` 한 줄만
- assert/skip/xfail/더미 통과 금지
- `src/` 수정·생성 금지
- `from src.entity.*` 가상 import → `ModuleNotFoundError` 유도

## B-2. 작성 패턴 (예: D-CNV-01)

```python
def test_d_cnv_01_to_meter_one_feet():
    """D-CNV-01: 1 feet → 0.3048 m (±ε, SSOT)."""
    # Given: ...
    value = 1.0
    unit = "feet"

    # When: to_meter(value, unit) — SSOT 상수 로드
    from src.entity.constants import METERS_PER_FOOT
    from src.entity.converter import to_meter
    _ = METERS_PER_FOOT
    _ = to_meter(value, unit)

    # Then:
    pytest.fail("RED: D-CNV-01 — 구현 없음, 의도적 실패")
```

## B-3. 산출 파일

| 파일 | Test ID |
|------|---------|
| `tests/entity/test_d_cnv_converter.py` | D-CNV-01, 02, 03 |
| `tests/entity/test_d_val_validator.py` | D-VAL-01, 02 |

---

# Part C — pytest FAIL 확인

## C-1. 실행

```bash
pytest tests/entity/ -v
```

## C-2. 결과

```
collected 5 items
5 failed in 0.13s
```

## C-3. 실패 메시지 (공통)

```
ModuleNotFoundError: No module named 'src'
```

- `pythonpath=["src"]` 설정으로 루트 패키지 `src`는 없음 → RED 의도와 일치
- GREEN 시 `entity.*` import로 정렬·모듈 생성 예정

## C-4. RED 완료 보고 (요약)

| 항목 | 값 |
|------|-----|
| Test ID | D-CNV-01~03, D-VAL-01~02 |
| FAIL 유형 | ModuleNotFoundError |
| 변경 | `tests/` 2파일만 |

---

# Part D — GREEN 전 준비

## D-1. Report·Transcript Export (본 세션)

- `Report/Entity_TDD_RED_Session_Report_STEP3.md`
- `Prompting/Entity_TDD_RED_Session_Transcript_STEP3.md` (본 문서)
- `README.md` · `docs/PRD.md` STEP 3 반영

## D-2. 다음 Command

```
/tdd-green
```

| GREEN 대상 `src/` | 책임 |
|-------------------|------|
| `entity/constants.py` | SSOT 비율 |
| `entity/converter.py` | `to_meter`, `convert_all` |
| `entity/validator.py` | `validate` |

| GREEN 시 `tests/` | Then 블록을 실제 assert로 교체 |

## D-3. 이후 Loop

```
entity GREEN/REFACTOR
  → control RED/GREEN (D-*)
  → boundary RED/GREEN (U-*)
  → /review-ecb
```

---

## 산출물 맵

| 산출물 | 경로 |
|--------|------|
| Entity RED 보고서 (STEP 3) | `Report/Entity_TDD_RED_Session_Report_STEP3.md` |
| Entity RED Transcript (STEP 3, 본 문서) | `Prompting/Entity_TDD_RED_Session_Transcript_STEP3.md` |
| 변환 RED 테스트 | `tests/entity/test_d_cnv_converter.py` |
| 검증 RED 테스트 | `tests/entity/test_d_val_validator.py` |

---

*Exported from UnitConverter_16 Entity TDD RED session (STEP 3).*
