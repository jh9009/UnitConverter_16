# TDD GREEN & REFACTOR — 최소 코드 구현 및 정리

UnitConverter_16 Dual-Track TDD **GREEN·REFACTOR 단계 전용** 명령.  
**전제:** 직전 `/tdd-red`에서 동일 Test ID가 **FAIL** 확인됨.  
상세 절차·pytest 명령·Track 표: `.cursor/skills/unit-converter-tdd/SKILL.md` 참조.  
헌법: `.cursorrules` · 요구: `docs/PRD.md`

---

## 1. 필수 선언

- 응답 **첫 줄**에 항상 출력 (GREEN 중이면 `GREEN`, REFACTOR 중이면 `REFACTOR`):

```
Phase: GREEN | Layer: [E/C/B] | Track: [Logic/UI]
```

```
Phase: REFACTOR | Layer: [E/C/B] | Track: [Logic/UI]
```

| Layer | Track | 구현 위치 | 테스트 위치 | ID |
|-------|-------|-----------|-------------|-----|
| E | Logic | `src/entity/` | `tests/entity/` | `D-*` |
| C | Logic | `src/control/` | `tests/control/` | `D-*` |
| B | UI | `src/boundary/` | `tests/boundary/` | `U-*` |

---

## 2. GREEN 절차 (최소 통과)

1. **RED 확인** — 대상 Test ID(`D-xx` / `U-xx`)와 실패했던 테스트 파일 경로 확인
2. **Layer 1개만 수정** — 해당 레이어 `src/` 하위에 **최소 코드**만 추가·수정
3. **책임 준수**
   - **E:** 순수 변환·도메인만. I/O·E00x·print/input 금지
   - **C:** 검증·에러 코드 매핑·entity 호출. I/O 금지
   - **B:** I/O·메시지 포맷·control 위임. 변환 계산 직접 수행 금지
4. **조용한 실패 방지 (Mom Test)**
   - 오류 시 `print("Done.")` 등 **성공 위장 출력 후 묵살 종료 금지**
   - E001(파싱)·E002(미지원 단위)·E003(음수) — control에서 매핑, boundary에서 `[코드] + 설명 + (가능 시) input` 출력
   - 메시지 없이 `return` / `exit` 금지
5. **SSOT** — `3.28084`, `1.09361` 등 비율은 SSOT 모듈에서 import (GREEN에서도 매직 넘버 산재 금지)
6. **pytest 실행** — **동일 ID** 테스트만 우선 PASS 확인

```bash
python -m pytest tests/entity/test_d_<name>.py -v
python -m pytest tests/control/test_d_<name>.py -v
python -m pytest tests/boundary/test_u_<name>.py -v
```

7. **PASS가 아니면** GREEN 완료 선언 금지 — 구현 보완 또는 (테스트 오류 시) 사용자와 RED 재검토

### GREEN 절대 금지

| 금지 | 이유 |
|------|------|
| RED 없이 `src/` 구현 | TDD 게이트 위반 |
| **tests/** assert 완화·삭제·skip | GREEN 우회 |
| RED와 **무관한 ID**까지 한꺼번에 통과시키기 | 범위 통제 위반 |
| Logic Track에서 **entity Mock** | `.cursorrules` 위반 |
| boundary → entity 직접 import | ECB 우회 |

---

## 3. REFACTOR 절차 (구조 개선)

**전제:** 해당 ID 테스트가 이미 **PASS**.

1. **동작 불변** — 테스트 수정 최소화, 기대값 변경 금지 (필요 시 사용자 확인)
2. **ECB 정리** — import 역방향 없음, 레이어 책임 분리, boundary→control→entity 유지
3. **SSOT 정리** — 중복 상수·매직 넘버를 SSOT로 일원화
4. **SRP·OCP** — 한 함수/클래스 한 책임, 단위 추가 시 entity 확장 위주
5. **pytest 재실행** — 해당 파일 → 해당 Track → (권장) 전체

```bash
python -m pytest tests/entity/test_d_<name>.py -v   # 또는 control/boundary
python -m pytest tests/entity/ -v
python -m pytest tests/control/ -v
python -m pytest tests/boundary/ -v
python -m pytest -v
```

6. **PASS 유지** 확인 후 REFACTOR 완료

---

## 4. 완료 보고

```markdown
### GREEN / REFACTOR 완료 보고
- Phase: [GREEN / REFACTOR] | Layer: [E/C/B] | Track: [Logic/UI]
- Test ID: [D-xx / U-xx]
- 구현 요약: [한 줄 — 무엇을 추가/정리했는지]

**pytest PASS 결과**
- 명령: `[실행한 pytest 명령]`
- 결과: PASS [n/n]
- (REFACTOR 시) 리팩터 요약: [ECB/SSOT 변경 한 줄]

**변경 파일**
- [src/... 및 (REFACTOR 시) 관련 경로]

**다음 단계**
- `/review-ecb` 실행하여 IMP/ERR/SSOT/MOCK 표로 최종 계약 위반 여부 점검 권장
- 위반 없으면 다음 RED(`tdd-red`) 또는 다음 Layer GREEN 진행
```

---

## 5. review-ecb 연동

GREEN·REFACTOR 종료 후 **반드시 사용자에게 제안**:

> `/review-ecb`를 실행해 ECB·E001~E003·SSOT·Logic Mock 계약을 표로 self-check 하세요.

이 명령(`tdd-green`)에서는 **리뷰 표를 대신 채우지 않음** — `review-ecb` 전용.
