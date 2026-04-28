# 테스트 케이스 명세 (Magic Square 4×4)

| 항목 | 내용 |
|------|------|
| 문서 유형 | Test Case Specification (실행·RED 스켈레톤 포함) |
| 정본(요구·문자열) | [`PRD_Magic_Square_4x4_TDD.md`](PRD_Magic_Square_4x4_TDD.md) |
| 갱신일 | 2026-04-28 |

---

## 1. 프로젝트·대상·환경

### 1.1 프로젝트명

**MagicSquare_02** — 4×4 부분 마방진(빈칸 `0` 정확히 2개), 고정 입·출력 계약·이중 시도 규칙에 따른 해(`int[6]` 동치) 또는 오류 보고.

### 1.2 대상 시스템(SUT)

| 구분 | 범위 |
|------|------|
| **경계(Boundary)** | 입력 행렬 `M` 검증(FR-01), 최종 응답의 `code`·`message`·성공 시 6-튜플. 공개 진입점 예: `solve_magic_square(M)` (구현체 이름은 팀 표준에 따름). |
| **도메인(Domain)** | 빈칸 좌표(FR-02), 누락 두 수 `(a,b)`(FR-03), 완성 격자 마방진 판정(FR-04), 이중 대입·해 또는 `E_NO_VALID_ASSIGNMENT`(FR-05). 예시 컴포넌트명: `BlankCellLocator`, `MissingNumberFinder`, `MagicSquareJudge`, `DualAssignmentResolver`. |

### 1.3 테스트 환경(본 레포 기준)

| 항목 | 기준 |
|------|------|
| 언어 런타임 | Python **3.10+** |
| 테스트 러너 | **`pytest`** — 로컬·CI 동일 러너([PRD §3, §7.1](PRD_Magic_Square_4x4_TDD.md)) |
| 의존성 | 최소: `pytest`; (선택) `pytest-cov`, 시간 상한은 PRD NFR·T-S-05 |
| 소스 배치 | 예: `src/magic_square/` + `tests/` 루트에 `pytest.ini` 또는 `pyproject.toml`로 `pythonpath` 설정 |

### 1.4 로컬 실행(복붙용)

프로젝트 루트에서:

```bash
python -m pytest tests/ -q
```

(선택) 한 파일만:

```bash
python -m pytest tests/boundary/test_solve_magic_square.py -q
```

### 1.5 전제조건(공통)

1. 입력 `M`은 **`list[list[int]]`** 형태의 4×4 정수 격자로 표현한다.
2. **Magic constant** = **34**(4×4 고정).
3. 성공 시 좌표·튜플은 **1-index**, 빈칸 순서는 **row-major** 첫 `0` → 둘째 `0`(FR-02).
4. 계약 검증 시 `message`는 PRD FR-01 표 및 §5.1 도메인 실패 문구와 **문자 그대로**(공백·마침표 포함) 일치해야 한다.
5. FR-01 실패 시 **FR-05는 호출되지 않음**; 테스트에서는 **목(mock)·스파이·주입 가능한 의존성**으로 경로 미실행을 단언한다([PRD §5.1](PRD_Magic_Square_4x4_TDD.md)).

### 1.6 성공·실패 기준(판정)

| 결과 유형 | 성공 판정 |
|-----------|-----------|
| **경계 성공** | FR-01 통과 후 유효한 `int[6]` 산출, 응답이 PRD AC-05-2·5-3과 일치, 완성 격자 FR-04 true. |
| **경계 입력 오류** | `code`가 `E_INPUT_SHAPE` \| `E_ZERO_COUNT` \| `E_VALUE_RANGE` \| `E_DUPLICATE_NONZERO` 중 **정확히 하나**, `message`가 FR-01 표와 **완전 일치**. |
| **도메인 실패(해 없음)** | 도메인 `E_NO_VALID_ASSIGNMENT`; 경계 표현은 `E_DOMAIN_FAILURE` + `message` = `failed to resolve a valid magic-square assignment.` (**한 줄**). |
| **불합격** | 다른 `code`/`message`, 성공 튜플 순서 오류, FR-01 실패인데 FR-05 호출, 입력 `M` 원본 변형(NFR-03), 동일 입력에 서로 다른 결과(NFR-02). |

### 1.7 특별 절차

| 절차 | 목적 |
|------|------|
| **Dual-Track TDD** | 매 루프에서 **Track A(Boundary)** 와 **Track B(Domain)** 에 각각 RED→GREEN이 존재([PRD §8.3](PRD_Magic_Square_4x4_TDD.md)). |
| **Golden 데이터** | §5의 리터럴은 검산값; 변경 시 PR·근거 기록([PRD §9.2·9.3](PRD_Magic_Square_4x4_TDD.md)). |
| **FR-05 미호출** | FR-01 실패 케이스에서 솔버 경로가 실행되지 않았음을 **관측 가능하게** 단언. |
| **FR-04와 0 셀** | AC-04-4: 미완성 격자에 대해 `false` **또는** assert 중 **한 가지**로 팀 통일 + **단위 테스트 1건** 고정([PRD §11](PRD_Magic_Square_4x4_TDD.md)). |
| **회귀** | 통과한 테스트 **삭제 금지**. |

---

## 2. 계약 상수(테스트에서 문자열 그대로 사용)

### 2.1 FR-01 `code` / `message`

| `code` | `message` |
|--------|-----------|
| `E_INPUT_SHAPE` | `matrix must be a 4x4 integer array.` |
| `E_ZERO_COUNT` | `matrix must contain exactly two zeros.` |
| `E_VALUE_RANGE` | `matrix values must be 0 or between 1 and 16.` |
| `E_DUPLICATE_NONZERO` | `non-zero values must be unique.` |

### 2.2 해 없음(경계·Presenter)

| 항목 | 값 |
|------|-----|
| 경계 `code` | `E_DOMAIN_FAILURE` |
| `message` (한 줄) | `failed to resolve a valid magic-square assignment.` |

### 2.3 도메인 전용(단위에서 직접 검사할 때)

| 항목 | 값 |
|------|-----|
| 도메인 `code` | `E_NO_VALID_ASSIGNMENT` |

---

## 3. Golden 픽스처 (PRD §9.3 예 A — 검산)

아래는 PRD §9.3과 동일한 격자다. **누락 두 수**는 1~16 중 미등장인 **1**과 **6**이므로 \(a=1, b=6\) ( \(a&lt;b\) ).

**리터럴 `M_EXAMPLE_A`** (Python):

```python
M_EXAMPLE_A = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]
```

**빈칸 (1-index):** 첫 `0` → `(3, 3)`, 둘째 `0` → `(4, 4)` (row-major).

**시도1** (첫 빈칸에 `a`, 둘째에 `b`): `(3,3)←1`, `(4,4)←6` → 행·열·대각 중 최소 한 줄이 합 34가 아니므로 **시도1 = false**.

**시도2** (첫 빈칸에 `b`, 둘째에 `a`): `(3,3)←6`, `(4,4)←1` → 완성 격자가 마방진(합 34)이므로 **시도2 = true**.

**기대 성공 튜플 (AC-05-3):** `[r1,c1,b,r2,c2,a]` = **`[3, 3, 6, 4, 4, 1]`** (좌표·값 모두 1-index 규약).

따라서 **예 A는 `T-S-02`(시도2 성공) 검증에 직접 쓰인다.** `T-S-01`(시도1만 성공)용 격자는 별도로 검산해 `fixtures/golden_ts01.py` 등에 두거나, 팀이 동일 규칙으로 생성한 Golden을 문서화한다.

**`T-S-03`(시도1·2 모두 실패)** 용 `M_NO_SOLUTION`은 PRD에 고정 리터럴이 없으므로, 수작업·스크립트로 검산한 뒤 **`tests/fixtures/no_solution_matrix.py`** 같은 한 곳에만 두고 TC ID와 함께 주석으로 근거를 남긴다.

---

## 4. 최소 입력 샘플(FR-01 경계 TC용)

테스트 코드에 그대로 넣을 수 있도록 예시 리터럴을 적는다. (팀은 동등한 다른 예도 가능하되, **기대 `code`는 동일**해야 한다.)

| 목적 | 예시 `M` | 기대 `code` |
|------|-----------|-------------|
| 형태 오류 `UI-T-01` | 3행만 있거나 행 길이 불일치 | `E_INPUT_SHAPE` |
| 0 개수 `UI-T-02` | 4×4이나 `0`이 1개 또는 3개 이상 | `E_ZERO_COUNT` |
| 값 범위 `UI-T-03` | `17` 또는 `-1` 포함 | `E_VALUE_RANGE` |
| 중복 `UI-T-04` | 0 제외 동일 값 2칸 | `E_DUPLICATE_NONZERO` |

예시 (값 범위):

```python
M_INVALID_RANGE = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 17],  # 17 ∉ [0]∪[1,16]
]
```

---

## 5. 권장 디렉터리·모듈 이름 (pytest)

레포 루트 기준 예시:

```
tests/
  conftest.py                 # 공통 fixture, 상수 import
  fixtures/
    golden_example_a.py       # M_EXAMPLE_A 등
    boundary_invalid_inputs.py
  boundary/
    test_solve_magic_square.py    # TC-MS-A-*, UI-T-*, T-S-04 통합
  domain/
    test_blank_cell_locator.py    # D-T-BLANK-01
    test_missing_number_finder.py # D-T-MISS-01
    test_magic_square_judge.py    # D-T-JDG-*, FR-04 AC-04-4
    test_dual_assignment_resolver.py  # D-T-ASG-*
  integration/
    test_scenarios_ts01_ts03.py     # T-S-01~03 (또는 boundary에 통합)
```

공개 API 모듈 예: `src/magic_square/solve.py` (`solve_magic_square`), 도메인은 `src/magic_square/domain/` 등 팀 규약에 따름.

---

## 6. 요약 매핑: TC ↔ PRD

| 일반 설명 | PRD |
|-----------|-----|
| 빈칸 좌표 | FR-02, `BlankCellLocator` |
| 완성 격자 마방진 | FR-04, `MagicSquareJudge` |
| 빈칸에 두 수 대입 | FR-05, `DualAssignmentResolver` + 경계 응답 |
| 입력 형태·0·범위·중복 | FR-01, `UI-T-01`~`04` |

---

## 7. 테스트 케이스 표 (실행 관점 상세)

**형식:** 각 행에 **Given / When / Then**, **기대 코드·메시지 리터럴**, **매핑 테스트 함수명(§8 참조)**.

| TC ID | 기능 | Given | When | Then | 우선순위 |
|-------|------|-------|------|------|----------|
| TC-MS-A-001 | FR-01 `UI-T-01` | 비정형 `M`(예: 3×4) | `solve_magic_square(M)` | `code=E_INPUT_SHAPE`, `message=` §2.1 첫 행 **전체 일치**, FR-05 경로 **미실행** | P1 |
| TC-MS-A-002 | FR-01 `UI-T-02` | 4×4, `0` 개수 ≠ 2 | 동일 | `E_ZERO_COUNT` + §2.1 표, FR-05 미실행 | P1 |
| TC-MS-A-003 | FR-01 `UI-T-03` | §4 `M_INVALID_RANGE` 등 | 동일 | `E_VALUE_RANGE` + 표, FR-05 미실행 | P1 |
| TC-MS-A-004 | FR-01 `UI-T-04` | 0 제외 중복 | 동일 | `E_DUPLICATE_NONZERO` + 표, FR-05 미실행 | P1 |
| TC-MS-B-001 | `T-S-01` | 검산된 Golden `M`(시도1만 성공) | 동일 | 성공, 튜플 형식 AC-05-2 `[r1,c1,a,r2,c2,b]`, 완성 격자 FR-04 true | P1 |
| TC-MS-B-002 | `T-S-02` | §3 `M_EXAMPLE_A` | 동일 | 성공, AC-05-3 `[3,3,6,4,4,1]` (예 A 검산), FR-04 true | P1 |
| TC-MS-B-003 | `T-S-03` | 검산된 `M_NO_SOLUTION` | 동일 | 도메인 `E_NO_VALID_ASSIGNMENT` 또는 경계 `E_DOMAIN_FAILURE` + §2.2 `message` **전체 일치** | P1 |
| TC-MS-B-004 | `T-S-04` | TC-MS-A-001~004 입력 집합 | 경계 호출 | 각각 단일 `E_*`, FR-05 미실행 | P1 |
| TC-MS-B-005 | `T-S-05` | 전체 스위트 | `pytest` | 전부 통과; (선택) 해 탐색 1건 ≤50ms | P2 |

---

## 8. RED 단계: pytest 스켈레톤 (함수명·파일명만 — 본문은 항상 실패)

아래는 **구현 전 RED**용이다. 각 테스트 본문은 **`assert False`** 또는 **`pytest.fail("RED")`** 한 줄만 두어 **항상 실패**하게 한다. (import 되는 SUT가 없으면 **import 단계에서 실패**해도 RED로 간주 가능.)

### 8.1 경계 — `tests/boundary/test_solve_magic_square.py`

```python
import pytest


def test_tc_ms_a_001_ui_t01_input_shape_e_input_shape_message_fr05_not_called():
    assert False  # RED


def test_tc_ms_a_002_ui_t02_zero_count_e_zero_count_message_fr05_not_called():
    assert False  # RED


def test_tc_ms_a_003_ui_t03_value_range_e_value_range_message_fr05_not_called():
    assert False  # RED


def test_tc_ms_a_004_ui_t04_duplicate_nonzero_message_fr05_not_called():
    assert False  # RED


def test_ui_t05_success_returns_length_six_tuple():
    assert False  # RED


def test_ui_t06_success_coordinates_are_one_indexed():
    assert False  # RED


def test_ui_t07_domain_failure_e_domain_failure_message_exact():
    assert False  # RED


def test_ts02_example_a_matches_ac_05_3_tuple():
    assert False  # RED


def test_ts03_no_solution_domain_or_boundary_mapping():
    assert False  # RED
```

### 8.2 도메인 — `tests/domain/test_blank_cell_locator.py`

```python
import pytest


def test_d_t_blank_01_row_major_two_zeros_order():
    assert False  # RED
```

### 8.3 도메인 — `tests/domain/test_missing_number_finder.py`

```python
import pytest


def test_d_t_miss_01_missing_pair_sorted_a_less_than_b():
    assert False  # RED
```

### 8.4 도메인 — `tests/domain/test_magic_square_judge.py`

```python
import pytest


def test_d_t_jdg_01_known_magic_square_complete_grid_true():
    assert False  # RED


def test_d_t_jdg_02_break_row_sum_false():
    assert False  # RED


def test_fr04_ac04_4_incomplete_grid_policy_false_or_assert():  # 팀 정책 1건 고정
    assert False  # RED
```

### 8.5 도메인 — `tests/domain/test_dual_assignment_resolver.py`

```python
import pytest


def test_d_t_asg_01_attempt_one_success_tuple_ac_05_2():
    assert False  # RED


def test_d_t_asg_02_attempt_two_only_success_tuple_ac_05_3():
    assert False  # RED


def test_d_t_asg_03_both_attempts_fail_e_no_valid_assignment():
    assert False  # RED
```

### 8.6 통합 — `tests/integration/test_scenarios_ts01_ts03.py` (선택 분리 시)

```python
import pytest


def test_ts01_attempt_one_success_integrated():
    assert False  # RED


def test_ts04_same_as_boundary_fr01_pack():
    assert False  # RED
```

---

## 9. RED 단계: JUnit 5 스켈레톤 (Java 트랙·이름만)

동일 계약을 JVM에서 연습할 때 파일·클래스·메서드 이름 예시다. 본문은 **`fail()`** 또는 **`assertTrue(false)`** 한 줄.

### 9.1 경계 — `src/test/java/com/magicsquare/boundary/SolveMagicSquareTest.java`

```java
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.fail;

class SolveMagicSquareTest {

    @Test void tc_ms_a_001_ui_t01_input_shape_e_input_shape_message_fr05_not_called() { fail("RED"); }

    @Test void tc_ms_a_002_ui_t02_zero_count_e_zero_count_message_fr05_not_called() { fail("RED"); }

    @Test void tc_ms_a_003_ui_t03_value_range_e_value_range_message_fr05_not_called() { fail("RED"); }

    @Test void tc_ms_a_004_ui_t04_duplicate_nonzero_message_fr05_not_called() { fail("RED"); }

    @Test void ui_t05_success_returns_length_six_tuple() { fail("RED"); }

    @Test void ui_t06_success_coordinates_are_one_indexed() { fail("RED"); }

    @Test void ui_t07_domain_failure_e_domain_failure_message_exact() { fail("RED"); }

    @Test void ts02_example_a_matches_ac_05_3_tuple() { fail("RED"); }

    @Test void ts03_no_solution_domain_or_boundary_mapping() { fail("RED"); }
}
```

### 9.2 도메인 — 예: `BlankCellLocatorTest.java`, `MissingNumberFinderTest.java`, `MagicSquareJudgeTest.java`, `DualAssignmentResolverTest.java`

각 클래스에 §8.2~8.5와 동일한 **`@Test void ...`** 메서드 이름을 두고, 메서드 본문은 모두 `{ fail("RED"); }`.

---

## 10. 추적

| Concept | PRD 참조 |
|---------|-----------|
| 시나리오 ID | §9.1 `T-S-01`~`T-S-05` |
| 경계 계약 ID | §8.1 `UI-T-01`~`UI-T-07` |
| 도메인 단위 예시 | §8.2 `D-T-*` |
| 추적 행렬 | PRD §12 |

---

*본 명세의 법적·납기 판정 문구는 PRD가 우선한다.*
