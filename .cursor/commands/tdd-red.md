# TDD RED — 실패 테스트 먼저 작성

UnitConverter_16 Dual-Track TDD **RED 단계 전용** 명령.  
상세 절차·pytest 명령·Track 표: `.cursor/skills/unit-converter-tdd/SKILL.md` 참조.  
헌법: `.cursorrules` · 요구: `docs/PRD.md`

---

## 1. 필수 선언

- 응답 **첫 줄**에 항상 출력:

```
Phase: RED | Layer: [E/C/B] | Track: [Logic/UI]
```

| Layer | Track | 테스트 위치 | ID | 파일 패턴 |
|-------|-------|-------------|-----|-----------|
| E | Logic | `tests/entity/` | `D-*` | `test_d_*.py` |
| C | Logic | `tests/control/` | `D-*` | `test_d_*.py` |
| B | UI | `tests/boundary/` | `U-*` | `test_u_*.py` |

---

## 2. 절차

1. **대상 확인** — `.cursorrules`·PRD·Skill에서 레이어 책임·에러 코드(E001/E002/E003) 확인
2. **Track/Layer 결정** — RED 권장 순서: entity → control → boundary
3. **테스트 ID 할당** — 기존 `D-*` / `U-*` 목록 확인 후 **새 ID 1개**만 부여 (한 턴 1 ID)
4. **AAA 패턴으로 테스트 작성**
   - **Arrange:** 입력·픽스처·(UI Track만) control/입출력 Mock 준비
   - **Act:** 테스트 대상 호출 (아직 없으면 `NotImplementedError` 유도 가능)
   - **Assert:** 기대 결과·에러 코드·메시지 필드 명시 (완화 금지)
5. **docstring/주석에 ID 명시** — 예: `"""D-01: meter:2.5 → feet 변환"""`
6. **pytest 실행** — 의도적 **FAIL** 확인

```bash
# Layer에 맞는 하나만 실행
python -m pytest tests/entity/test_d_<name>.py -v
python -m pytest tests/control/test_d_<name>.py -v
python -m pytest tests/boundary/test_u_<name>.py -v
```

7. **FAIL이 아니면** (통과·0 collected) — 테스트를 수정해 RED 상태를 만든 뒤 다시 실행

---

## 3. 완료 보고

다음 항목을 반드시 포함한다.

```markdown
### RED 완료 보고
- Phase: RED | Layer: [E/C/B] | Track: [Logic/UI]
- Test ID: [D-xx / U-xx]
- 테스트 요약: [한 줄 — 무엇을 검증하려 하는지]

**pytest FAIL 요약**
- 명령: `[실행한 pytest 명령]`
- 실패 유형: [AssertionError / NotImplementedError / ImportError 등]
- 핵심 메시지: [1~3줄]

**변경 파일**
- [tests/... 경로만 나열 — src/ 없어야 함]
```

---

## 4. 🚨 절대 금지 사항 (위반 시 즉시 중단)

| 금지 | 이유 |
|------|------|
| `src/` 디렉터리 실제 로직 **생성·수정** | RED는 테스트만. 구현은 GREEN |
| Logic Track(Entity/Control) **도메인·entity Mock** | `.cursorrules` Domain Mock 금지 |
| assert 조건 **완화** | RED 우회 |
| `@pytest.mark.skip` · `xfail` 적용 | RED 우회 |
| 한 턴에 **테스트 ID 2개 이상** 추가 | 범위 통제 위반 |
| FAIL 없이 RED 완료 선언 | TDD 게이트 위반 |

**위반 감지 시:** 작업 중단 → 사용자에게 위반 항목 보고 → GREEN 명령(`tdd-green`)으로 넘어가지 않음.

---

## 참고 — Logic vs UI Mock (RED 시)

| Track | Mock |
|-------|------|
| Logic (E/C) | entity·도메인 Mock **금지** |
| UI (B) | control·입출력 Mock **허용** |
