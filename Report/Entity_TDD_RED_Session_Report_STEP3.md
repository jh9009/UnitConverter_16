# UnitConverter_16 — Entity TDD RED 세션 보고서 (STEP 3)

**일자:** 2026-06-05  
**단계:** STEP 3 — Entity Logic Track RED (Dual-Track TDD)  
**선행:** Mom Test STEP 1 · Cursor 설계 STEP 2 · [Cursor 설계 보고서](./Cursor_Design_Session_Report_STEP2.md)

---

## 1. 주제 (한 문장)

ECB **entity** 레이어에 대해 변환·검증 로직의 **실패 테스트(RED 스켈레톤)** 를 먼저 작성하고, `src/` 구현 없이 pytest FAIL을 확인한 뒤 GREEN으로 넘길 준비를 마친다.

---

## 2. Phase 선언

```
Phase: RED | Layer: Entity | Track: Logic
```

| 항목 | 값 |
|------|-----|
| Layer | E (Entity) |
| Track | Logic |
| 테스트 위치 | `tests/entity/` |
| ID 접두 | `D-CNV-*`, `D-VAL-*` |
| `src/` 변경 | **없음** (RED 규칙) |

---

## 3. 확정 설계표 (Entity RED)

### 3.1 변환 (converter)

| Test ID | 대상 함수 | Given | Then (GREEN 시 검증) |
|---------|-----------|-------|----------------------|
| **D-CNV-01** | `to_meter` | 1 feet | 0.3048 m (±ε, SSOT) |
| **D-CNV-02** | `convert_all` | 2.5 meter | feet = 8.20210 (소수 5자리) |
| **D-CNV-03** | `convert_all` | 3.0 feet | meter 경유 feet·yard 일관성 |

### 3.2 검증 (validator)

| Test ID | 대상 함수 | Given | Then (GREEN 시 검증) |
|---------|-----------|-------|----------------------|
| **D-VAL-01** | `validate` | unit=`inch`, value=1.0 | 거부 (control → E002 매핑 예정) |
| **D-VAL-02** | `validate` | unit=`meter`, value=-1.0 | 거부 (control → E003 매핑 예정) |

**Entity 원칙:** E001/E002/E003 문자열·I/O 없음. 도메인 거부만 표현.

### 3.3 SSOT (GREEN 예정 모듈)

| 상수 | 값 | 근거 |
|------|-----|------|
| `METERS_PER_FOOT` | `0.3048` (역산: 1/3.28084) | `1 m = 3.28084 ft` |
| `METERS_PER_YARD` | 역산 | `1 m = 1.09361 yd` |
| 모듈 | `src/entity/constants.py` | `.cursorrules` SSOT |

---

## 4. RED 스켈레톤 규칙 (`/red-skeleton`)

| 규칙 | 적용 |
|------|------|
| AAA 주석 | Given / When / Then 필수 |
| Then 블록 | `pytest.fail("RED: [Test ID] — 구현 없음, 의도적 실패")` **한 줄만** |
| 금지 | assert 본문, skip, xfail, 더미 통과 |
| `src/` | 생성·수정 **금지** |
| import 경로 | `src.entity.constants` 등 가상 경로 → `ModuleNotFoundError` 유도 |

---

## 5. 산출물

| 산출물 | 경로 |
|--------|------|
| 변환 RED 스켈레톤 | `tests/entity/test_d_cnv_converter.py` (D-CNV-01~03) |
| 검증 RED 스켈레톤 | `tests/entity/test_d_val_validator.py` (D-VAL-01~02) |
| Entity RED Transcript | [Prompting/Entity_TDD_RED_Session_Transcript_STEP3.md](../Prompting/Entity_TDD_RED_Session_Transcript_STEP3.md) |

---

## 6. pytest 결과 (RED 확인)

**명령:** `pytest tests/entity/ -v`

| 항목 | 결과 |
|------|------|
| collected | 5 |
| passed | 0 |
| failed | **5** |
| 소요 | ~0.13s |

**실패 유형:** `ModuleNotFoundError: No module named 'src'`

- `When` 블록의 `from src.entity.constants` / `converter` / `validator` import 시점에 실패
- `Then`의 `pytest.fail` 도달 전 중단 → **의도적 RED** (구현 부재)

| Test ID | 실패 위치 |
|---------|-----------|
| D-CNV-01 | `from src.entity.constants import METERS_PER_FOOT` |
| D-CNV-02 | `from src.entity.constants import METERS_PER_FOOT` |
| D-CNV-03 | `from src.entity.constants import METERS_PER_FOOT, METERS_PER_YARD` |
| D-VAL-01 | `from src.entity.validator import validate` |
| D-VAL-02 | `from src.entity.validator import validate` |

---

## 7. RED 완료 점검

| 체크 | 상태 |
|------|------|
| Test ID 5개 docstring·주석 명시 | ✅ |
| AAA 패턴 | ✅ |
| assert/skip/xfail 없음 | ✅ |
| `src/` 미변경 | ✅ |
| pytest 5 failed (RED) | ✅ |
| Logic Track Domain Mock 없음 | ✅ |

**판정:** Entity RED 스켈레톤 **완료**. `/tdd-green` 진행 가능.

---

## 8. GREEN 예고 (다음 단계)

| 우선 | 작업 | 대상 `src/` |
|------|------|-------------|
| 1 | SSOT 상수 | `src/entity/constants.py` |
| 2 | `to_meter`, `convert_all` | `src/entity/converter.py` |
| 3 | `validate` | `src/entity/validator.py` |
| 4 | RED 스켈레톤 → 실제 assert | `tests/entity/test_d_*.py` (GREEN 시 Then 교체) |

**권장 GREEN 순서:** D-CNV-01 → D-CNV-02 → D-CNV-03 → D-VAL-01 → D-VAL-02 (또는 Command 범위에 따라 일괄 최소 구현 후 assert 활성화)

**import 정리:** `pyproject.toml`의 `pythonpath=["src"]` 기준 GREEN 시 `from entity.constants import ...` 로 정렬 권장 (RED는 `src.entity.*` 가상 경로 유지).

---

## 9. Test/Review Loop 진행 상태

| Layer | RED | GREEN | REFACTOR |
|-------|-----|-------|----------|
| Entity (E) | ✅ STEP 3 | ⏳ 다음 | ⏳ |
| Control (C) | ⏳ | ⏳ | ⏳ |
| Boundary (B) | ⏳ | ⏳ | ⏳ |

---

## 10. 관련 문서

- [Entity TDD RED Transcript (STEP 3)](../Prompting/Entity_TDD_RED_Session_Transcript_STEP3.md)
- [Cursor 설계 보고서 (STEP 2)](./Cursor_Design_Session_Report_STEP2.md)
- [PRD](../docs/PRD.md)
- [`.cursorrules`](../.cursorrules)
- [Skill: unit-converter-tdd](../.cursor/skills/unit-converter-tdd/SKILL.md)
