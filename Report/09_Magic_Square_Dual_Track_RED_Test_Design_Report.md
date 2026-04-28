# Magic Square (4×4) Dual-Track RED 테스트 설계 보고서

## 개요

- **문서 목적:** 시나리오를 **실패하는 테스트(RED)** 로 변환하기 위한 **Track A(UI/경계)**·**Track B(Logic/도메인)** 테스트 설계를 Report에 기록한다. 본 문서는 **테스트 설계·Invariant 정렬**만 다루며, 구현 코드·GREEN·REFACTOR는 범위 밖이다.
- **대상 독자:** TDD 실습자, 리뷰어, PRD·[`TEST_SPEC`](../docs/TEST_SPEC_Magic_Square_4x4.md) 추적 담당.
- **작성일:** 2026-04-28
- **버전:** 1.0

| 항목 | 값 |
|------|-----|
| 문서 유형 | 내부 보고서(Dual-Track TDD · RED 단계 설계) |
| 제품/프로젝트명 | Magic Square (4×4) — [`MagicSquare_02`](https://github.com/jacki951032-cell/MagicSquare_02) |
| 요구·테스트 정본 | [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md), [`../docs/TEST_SPEC_Magic_Square_4x4.md`](../docs/TEST_SPEC_Magic_Square_4x4.md) |
| 관련 Report | [`02_Magic_Square_Dual_Track_TDD_Clean_Architecture_Report.md`](02_Magic_Square_Dual_Track_TDD_Clean_Architecture_Report.md), [`08_Magic_Square_Git_Branch_PR_Workflow_Report.md`](08_Magic_Square_Git_Branch_PR_Workflow_Report.md) |

---

## 1. 본 보고서의 범위와 금지 사항

| 구분 | 내용 |
|------|------|
| **포함** | RED 테스트 ID·시나리오(Given/When/Then)·보호 Invariant·PRD·TEST_SPEC과의 ID 정렬 |
| **제외** | 프로덕션 구현, GREEN(통과 구현), REFACTOR |

**RED 상태:** 구현이 없거나 스텁만 있을 때 테스트는 **실패**해야 한다(import 실패, `AssertionError`, FR-01 위반 시 도메인 미호출 단언 등).

---

## 2. 프로젝트 조건(요약)

| 구분 | 내용 |
|------|------|
| 입력 | 4×4 `int[][]`; `0`은 빈칸·**정확히 2개**; 값은 `0` 또는 1~16; 0 제외 **중복 금지** |
| 출력(성공) | `int[6]`; 좌표 **1-index**; `[r1, c1, n1, r2, c2, n2]` |
| 마방진 상수 | 4×4 → **34** |

---

## 3. Dual-Track RED 단계 구조

```
TRACK A — UI / Boundary RED          TRACK B — Logic / Domain RED
(경계·응답 계약)                         (순수 도메인 API)
        ↓                                       ↓
              둘 다 RED(실패) 상태로 유지
```

Dual-Track 루프에서는 **Track A와 Track B 각각**에 RED→이후 GREEN이 존재하도록 한다([`TEST_SPEC` §1.6](../docs/TEST_SPEC_Magic_Square_4x4.md)).

---

## 4. TRACK A — UI / Boundary RED

PRD·[`TEST_SPEC` §3](../docs/TEST_SPEC_Magic_Square_4x4.md)의 `UI-T-01`~`UI-T-04` 및 성공 경로 계약(`UI-T-05`, `UI-T-06` 등)과 정렬한다. 경계 진입점 예: `solve_magic_square(M)`(이름은 팀 표준에 따름).

| Test ID | Scenario | Invariant 보호 내용 |
|---------|----------|---------------------|
| **UI-T-01** | **Given** `M`이 4×4가 아님(예: 3×4, 행 길이 불일치). **When** 경계 API 호출. **Then** FR-01 단일 입력 오류 `E_INPUT_SHAPE`, `message`는 PRD FR-01 표 **문자 그대로**. **(RED 시 실패)** | **INV-A1:** 유효한 격자 형태만 도메인으로 전달된다. |
| **UI-T-02** | **Given** 4×4이나 `0` 개수 ≠ 2. **When** 동일 호출. **Then** `E_ZERO_COUNT` + 표 `message`; **FR-05 경로 미호출**(목·스파이로 단언). **(RED 시 실패)** | **INV-A2:** 빈칸이 정확히 두 칸일 때만 해 탐색이 허용된다. |
| **UI-T-03** | **Given** 값이 0 또는 1~16 밖. **When** 동일 호출. **Then** `E_VALUE_RANGE` + 표 `message`; FR-05 미호출. **(RED 시 실패)** | **INV-A3:** 허용 값 집합 위반 시 결정론적 오류 코드만 사용한다. |
| **UI-T-04** | **Given** 0 제외 중복. **When** 동일 호출. **Then** `E_DUPLICATE_NONZERO` + 표 `message`; FR-05 미호출. **(RED 시 실패)** | **INV-A4:** 1~16은 중복 없이 유지된다. |
| **UI-T-05** | **Given** FR-01 통과·성공 경로(또는 계약 검증용 Given). **When** 호출. **Then** 성공 시 해 벡터는 **길이 6** (`int[6]`). **(RED 시 실패)** | **INV-A5:** 성공 산출물이 항상 6슬롯 튜플 계약을 만족한다. |
| **UI-T-06** | **Given** 성공 경로 Given. **When** 호출. **Then** `r1,c1,r2,c2`는 **1-index**(예: 1~4 범위)·AC-05와 일치. **(RED 시 실패)** | **INV-A6:** 사용자 좌표와 PRD 인덱싱 규칙이 일치한다. |

---

## 5. TRACK B — Logic / Domain RED

도메인 컴포넌트명은 PRD 예시(`BlankCellLocator`, `MissingNumberFinder`, `MagicSquareJudge`, `DualAssignmentResolver` 등)를 참고하되, 본 보고서는 **행위·Invariant**를 우선한다.

| Test ID | Scenario | Invariant 보호 내용 |
|---------|----------|---------------------|
| **D-T-BLANK-01** | **Given** 합법 부분 격자(`0` 정확히 2개). **When** `find_blank_coords(M)`(동등 API). **Then** 길이 2, **row-major** 첫 `0` → 둘째 `0` 순서. **(RED)** | **INV-B1 (FR-02):** 이중 대입 순서가 정의된 빈칸 순서와 같다. |
| **D-T-MISS-01** | **Given** 동일. **When** `find_not_exist_nums(M)`. **Then** 누락 두 수, **오름차순 (a,b), a\<b**. **(RED)** | **INV-B2 (FR-03):** 누락 쌍이 정렬·유일하게 고정된다. |
| **D-T-JDG-01** | **Given** 완전 채워진 4×4(마방진·비마방진 예 각 1). **When** `is_magic_square` / `MagicSquareJudge`. **Then** 행·열·두 대각 합이 모두 같고 **34**이면 true, 아니면 false. **(RED)** | **INV-B3 (FR-04):** 판정은 행·열·대각 동일합 34와 일치한다. |
| **D-T-ASG-01** | **Given** 시도1(작은 수→첫 빈칸)으로 성공하는 검산 격자. **When** `solution` / Resolver. **Then** AC-05-2에 맞는 `[r1,c1,n1,r2,c2,n2]`, 길이 6·1-index. **(RED)** | **INV-B4a (FR-05):** 시도1 규칙이 우선 적용된다. |
| **D-T-ASG-02** | **Given** 시도1 실패·시도2만 성공하는 Golden(PR §9.3 등). **When** 동일. **Then** AC-05-3 `[r1,c1,b,r2,c2,a]`. **(RED)** | **INV-B4b:** 시도1 실패 후 시도2가 규칙대로 반영된다. |
| **D-T-ASG-03** | **Given** 시도1·2 모두 불가 검산 격자. **When** 동일. **Then** 도메인 `E_NO_VALID_ASSIGNMENT`; 임의 길이 6 성공 금지. **(RED)** | **INV-B4c:** 해 없음일 때 성공 튜플이 없다. |

---

## 6. TEST_SPEC·TC 표와의 대응(참고)

| 본 보고서 | [`TEST_SPEC` §3](../docs/TEST_SPEC_Magic_Square_4x4.md) 참고 |
|-----------|---------------------------------------------------------------|
| UI-T-01~04 | TC-MS-A-001~004, `UI-T-01`~`04` |
| 통합 시나리오 | `T-S-01`~`T-S-03` 등 §9.1 — GREEN 이후 통합 검증 |

본 문서 **§4·§5**는 **단위·RED 설계**에 초점을 두고, §6은 추적 편의를 위한 매핑이다.

---

## 7. 다른 Report와의 관계

| Report | 본 문서(09)와의 관계 |
|--------|----------------------|
| `02` | Dual-Track·도메인 컴포넌트·ECB 개념 정본 보강 |
| `08` | 브랜치·PR 워크플로 — RED 작업은 `feature/dual-track-tdd` 등 토픽 브랜치에서 수행 |
| `07` / `README` | 문서 지도·동기 |

---

*납기·기능 판정은 [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md)가 우선한다.*
