# Review ECB — 계약·아키텍처 리뷰 (코드 수정 금지)

UnitConverter_16 **ECB·Dual-Track 계약 위반만** 검사한다.  
**코드 생성·수정 금지** — 읽기·pytest·grep만 허용.

헌법: `.cursorrules` · Skill: `.cursor/skills/unit-converter-tdd/SKILL.md` · 요구: `docs/PRD.md`

---

## 1. 필수 선언

응답 **첫 줄**:

```
Phase: REVIEW | Layer: [E/C/B/ALL] | Track: [Logic/UI/ALL]
```

---

## 2. 리뷰 절차 (읽기 전용)

1. 대상 범위 확인 — `src/`, `tests/`, (있다면) `UnitConverter.py`
2. import 문·의존 관계 스캔 (`src/boundary/`, `src/control/`, `src/entity/`)
3. 에러 경로·출력 문자열 스캔 (E001/E002/E003, `Done.` 등)
4. 변환 상수 `3.28084`, `1.09361` 등 매직 넘버 출처 추적
5. `tests/entity/`, `tests/control/`에서 Mock·patch·MagicMock 사용 여부 확인
6. (선택) `python -m pytest -v` — 기존 TC 통과 여부 참고 (수정 금지)
7. 아래 **리뷰 결과 표**로만 보고

---

## 3. 체크 항목 및 판정 기준

### 3.1 import 방향 (역방향 금지)

| ID | 검사 | Pass 기준 | Fail 예시 |
|----|------|-----------|-----------|
| IMP-1 | entity → control/boundary | `src/entity/`에 control·boundary import 없음 | `from control import ...` |
| IMP-2 | control → boundary | `src/control/`에 boundary import 없음 | `from boundary import ...` |
| IMP-3 | boundary → entity | `src/boundary/`에 entity import 없음 | `from entity import convert` |
| IMP-4 | boundary → control만 | boundary는 control만 의존 | entity 직접 호출·계산 |

### 3.2 E001~E003 · 조용한 실패

| ID | 검사 | Pass 기준 | Fail 예시 |
|----|------|-----------|-----------|
| ERR-1 | E001 파싱 | `feet 5.8`, `meter:abc` 등 → E001 + 설명 + (가능 시) input | 묵살 return, 메시지 없음 |
| ERR-2 | E002 미지원 단위 | `inch:1.0` → E002 + 설명 | 일반 Exception만, 코드 없음 |
| ERR-3 | E003 음수 | `meter:-1` → E003 + 설명 | 조용히 0 처리 |
| ERR-4 | 종료 전 메시지 | 모든 오류 경로가 boundary 출력 후 종료 | `return`/`exit` without print |
| ERR-5 | 성공 위장 출력 | 오류 후 `Done.` 등 성공처럼 보이는 출력 없음 | 에러 뒤 `Done.` 출력 |
| ERR-6 | entity 순수성 | entity에 E00x 문자열·print/input 없음 | entity에서 `print("E001")` |

**에러 코드 위치:** 매핑 control · 사용자 출력 boundary (entity 금지)

### 3.3 SSOT (단위 변환 비율)

| ID | 검사 | Pass 기준 | Fail 예시 |
|----|------|-----------|-----------|
| SSOT-1 | 단일 정의 | `3.28084`, `1.09361`이 SSOT 모듈 1곳에만 정의 | 여러 파일에 리터럴 중복 |
| SSOT-2 | import 사용 | entity/control/tests가 SSOT에서 import | `* 3.28084` 산재 |
| SSOT-3 | 값 정확성 | `1 m = 3.28084 ft`, `1 m = 1.09361 yd` | 다른 비율 사용 |

**SSOT 후보:** `src/entity/constants.py` (프로젝트에서 지정한 단일 모듈)

### 3.4 Logic Track — Domain Mock

| ID | 검사 | Pass 기준 | Fail 예시 |
|----|------|-----------|-----------|
| MOCK-1 | tests/entity/ | entity·도메인 Mock/patch 없음 | `@patch("entity.convert")` |
| MOCK-2 | tests/control/ | entity Mock 없음, **실제 entity** 사용 | `MagicMock()`으로 변환 대체 |
| MOCK-3 | tests/boundary/ | (UI Track) control·I/O Mock **허용** | — |

---

## 4. 리뷰 결과 보고 형식 (표만 출력)

코드 패치·수정 제안으로 파일을 바꾸지 말고, **아래 표를 채워 보고**한다.

```markdown
### ECB 계약 리뷰 결과
- 범위: [검사한 경로]
- pytest: [실행했다면 요약 / 미실행]

| ID | 항목 | 판정 | 위치 (파일:줄 또는 테스트) | 비고 |
|----|------|------|---------------------------|------|
| IMP-1 | entity 역방향 import | ✅/❌/N/A | | |
| IMP-2 | control → boundary | ✅/❌/N/A | | |
| IMP-3 | boundary → entity | ✅/❌/N/A | | |
| IMP-4 | boundary → control만 | ✅/❌/N/A | | |
| ERR-1 | E001 처리 | ✅/❌/N/A | | |
| ERR-2 | E002 처리 | ✅/❌/N/A | | |
| ERR-3 | E003 처리 | ✅/❌/N/A | | |
| ERR-4 | 종료 전 메시지 | ✅/❌/N/A | | |
| ERR-5 | 성공 위장 출력 없음 | ✅/❌/N/A | | |
| ERR-6 | entity 순수성 | ✅/❌/N/A | | |
| SSOT-1 | 비율 단일 정의 | ✅/❌/N/A | | |
| SSOT-2 | SSOT import | ✅/❌/N/A | | |
| SSOT-3 | 비율 값 정확 | ✅/❌/N/A | | |
| MOCK-1 | entity 테스트 Mock | ✅/❌/N/A | | |
| MOCK-2 | control 테스트 entity Mock | ✅/❌/N/A | | |
| MOCK-3 | boundary Mock (허용) | ✅/N/A | | |

**요약**
- 🔴 Critical (즉시 수정 권고): [ID 목록]
- 🟡 Warning: [ID 목록]
- ✅ Pass: [개수]
```

---

## 5. 🚨 절대 금지 (이 명령에서)

| 금지 | 이유 |
|------|------|
| `src/`, `tests/` **코드 수정** | 리뷰 전용 명령 |
| 위반 사항 **자동 수정** | 사용자·GREEN/REFACTOR 단계에 위임 |
| 리뷰 없이 "통과" 선언 | 표 채우기 필수 |
| Out of Scope 기능 구현 제안을 코드로 반영 | 표 비고에 한 줄만 가능 |

**❌ 1건이라도 있으면:** Critical 목록에 기록 → `tdd-green` / `tdd-red`로 넘기지 않고 사용자에게 보고.

---

## 6. 빠른 스캔 명령 (참고)

```bash
# import 역방향 힌트 (수동 확인 필수)
rg "from (control|boundary)" src/entity/
rg "from boundary" src/control/
rg "from entity" src/boundary/

# 매직 넘버 산재
rg "3\.28084|1\.09361" src/ tests/

# Logic Track Mock 힌트
rg "Mock|patch|MagicMock" tests/entity/ tests/control/

python -m pytest -v
```
