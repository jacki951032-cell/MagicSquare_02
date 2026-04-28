# Git branching strategy for Dual-Track TDD
_Exported on 4/28/2026 at 14:01:19 GMT+9 from Cursor (3.2.11)_

---

**User**

@c:\DEV\MagicSquare _02\ 프로젝트를 구현하기 위한 깃 브랜치 전략을 알려줘.개발방법론은 Dual-Track TDD 이고, 다음의 순서로 진행할 거야.

- Dual-Track UI + Logic TDD
- GREEN 단계 (테스트 통과)
- Dual-Track Refactoring

---

**Cursor**

프로젝트 문서와 저장소 구조를 확인해 Dual-Track TDD 흐름에 맞는 브랜치 전략을 제안합니다.



프로젝트의 [`Report/08`](Report/08_Magic_Square_Git_Branch_PR_Workflow_Report.md)과 README의 Dual-Track·TDD 맥락을 기준으로 정리했습니다.

---

## Dual-Track TDD × Git 브랜치 전략

### 1. 기본 원칙 (Report/08과 동일)

- **작업은 토픽 브랜치**에서만 진행하고, **로컬에서 `main`에 먼저 머지하지 않는다.**  
  그래야 `main` ← 토픽 브랜치 PR에 **diff가 남는다.**
- **한 기능(Epic/User Story 단위)**마다 하나의 “세로축”을 두고, 그 안에서 **RED → GREEN → REFACTOR**를 **커밋으로 구분**하는 방식이 가장 단순하고 Dual-Track과도 잘 맞습니다.

---

### 2. 권장: **한 토픽 브랜치 + 커밋 규약** (연습·소규모에 적합)

브랜치 이름은 **기능 중심**이 좋습니다.

| 패턴 | 예시 |
|------|------|
| `feat/<짧은-설명>` | `feat/boundary-input-validation`, `feat/dual-assignment-solver` |

**커밋 메시지로 트랙·단계를 표시:**

| 단계 | 의미 | 예시 prefix |
|------|------|-------------|
| **Dual-Track RED** | UI(경계)·Logic(도메인) 테스트 추가, 실패 확인 | `test(ui): …`, `test(domain): …` 또는 `RED(ui):`, `RED(domain):` |
| **GREEN** | 최소 구현으로 테스트 통과 | `GREEN: …` |
| **Dual-Track Refactor** | 구조·이름 정리, 테스트 유지 | `REFACTOR(ui):`, `REFACTOR(domain):` 또는 `refactor: …` |

**Dual-Track 순서 예시(한 스토리 안에서):**

1. 경계/프레젠터 쪽 실패 테스트 → 도메인 실패 테스트 (또는 팀이 정한 트랙 순서).
2. GREEN: 양쪽 또는 한쪽씩 최소 구현.
3. REFACTOR: ECB 경계 유지하며 정리.

같은 브랜치에 **연속 커밋**으로 두면, PR 하나로 리뷰·머지가 가능하고, 히스토리만으로 RED/GREEN/REFACTOR와 트랙이 보입니다.

---

### 3. 대안: **단계별 브랜치** (PR을 단계마다 나누고 싶을 때)

리뷰를 RED → GREEN → REFACTOR로 **나누고 싶다면** 스택처럼 씁니다.

| 순서 | 브랜치 | base | 역할 |
|------|--------|------|------|
| 1 | `feat/…-red` | `main` | Dual-Track RED만 (테스트 추가, 실패) |
| 2 | `feat/…-green` | `feat/…-red` | GREEN 머지 후 또는 red 위에 GREEN 커밋 |
| 3 | `feat/…-refactor` | `feat/…-green` | 리팩터만 |

**주의:** `-green`은 보통 **`-red`에 PR 먼저 머지**한 뒤 `main`에서 새 브랜치를 따거나, **한 브랜치에 통합**하는 편이 관리 부담이 적습니다. 연습 프로젝트면 **§2 한 브랜치 방식**을 추천합니다.

---

### 4. 당신이 적은 순서와 매핑

| 당신의 순서 | Git에서의 해석 |
|-------------|----------------|
| **Dual-Track UI + Logic TDD** | 토픽 브랜치에서 **RED 커밋들** (UI 트랙 + Logic 트랙 테스트, 의도적 실패). |
| **GREEN** | **테스트 통과**까지의 커밋(들); CI가 녹색이 되는 지점. 하나의 커밋으로 묶어도 되고, UI/도메인을 나눠도 됨. |
| **Dual-Track Refactoring** | 동작 유지한 채 **REFACTOR 커밋들**; 필요하면 마지막에만 푸시해 PR을 “리팩터 전용”으로 보이게 할 수 있음. |

---

### 5. 실무 체크리스트

1. `git switch main && git pull` 후 `git switch -c feat/…`.
2. RED → GREEN → REFACTOR 순으로 커밋 (메시지에 단계·트랙 명시).
3. **`main`에 로컬 머지하지 않은 채** `git push -u origin feat/…` 후 PR (**base: `main`**, **compare: `feat/…`**).
4. 머지 후 로컬 `main` 정리: `git switch main && git pull`.

---

요약하면, **Magic Square 연습에는 `feat/<기능명>` 하나에 RED(ui/domain) → GREEN → REFACTOR(ui/domain) 커밋 규약**을 쓰고, Report/08의 **“머지는 PR로만”** 규칙을 지키면 Dual-Track TDD 흐름과 Git이 잘 맞습니다. 더 쪼갠 PR이 필요할 때만 `-red` / `-green` / `-refactor` 같은 브랜치 분할을 고려하면 됩니다.

---

**User**

develop 브랜치를 만들어줘.

---

**Cursor**

저장소 상태 확인 후 `develop` 브랜치 생성 중입니다.



`main`과 동일한 커밋에서 `develop` 브랜치를 생성하고 원격에 푸시합니다.



다음이 적용되었습니다.

### 로컬
- **`develop` 브랜치**를 `main`과 같은 커밋(`HEAD`)에서 생성했습니다.
- 전환하려면: `git switch develop`

### 원격
- `git push -u origin develop`는 **GitHub에 연결되지 않아** 실패했습니다(네트워크/방화벽/DNS 등).  
  연결이 되면 아래를 한 번 실행하세요.

```powershell
cd c:\DEV\MagicSquare_02
git push -u origin develop
```

이후 GitHub 기본 브랜치를 `develop`으로 쓰고 싶다면 저장소 **Settings → Branches**에서 기본 브랜치를 바꾸면 됩니다(팀 규칙에 맞게 선택).

---

**User**

feature/dual-track-tdd 브랜치를 생성해줘.

---

**Cursor**

작업했습니다.

- **`feature/dual-track-tdd`** 브랜치를 현재 **`main` HEAD**에서 만들었고, 지금 그 브랜치로 체크아웃된 상태입니다.
- 원격에 올리려면: `git push -u origin feature/dual-track-tdd`

---

**User**


당신은 Dual-Track UI + Logic TDD 전문가입니다.

우리는 이미 Magic Square(4x4) 시나리오를 작성했습니다.
지금 단계는 구현이 아니라,
시나리오를 “실패하는 테스트(RED)”로 변환하는 것입니다.

중요
- 구현 코드를 작성하지 마십시오.
- GREEN 단계로 가지 마십시오.
- REFACTOR 단계로 가지 마십시오.
- 오직 RED 테스트만 작성하십시오.
- 모든 테스트는 현재 구현이 없기 때문에 실패해야 합니다.

------------------------------------------------------------
프로젝트 조건
------------------------------------------------------------

입력:
- 4x4 int[][]
- 0은 빈칸
- 정확히 2개의 0
- 값 범위 1~16
- 중복 금지 (0 제외)

출력:
- int[6]
- 좌표는 1-index
- [r1, c1, n1, r2, c2, n2]

마방진 상수:
- 4x4 → 34

------------------------------------------------------------
Dual-Track RED 단계 구조
------------------------------------------------------------

UI RED        Logic RED
   ↓              ↓
(둘 다 실패 상태)

------------------------------------------------------------
TRACK A — UI / Boundary RED
------------------------------------------------------------

다음을 실패 테스트로 변환하십시오:

1. 4x4가 아닌 입력은 예외 발생
2. 빈칸이 2개가 아니면 예외 발생
3. 값 범위 위반 시 예외 발생
4. 중복 숫자 존재 시 예외 발생
5. 반환 배열 길이는 6이어야 한다
6. 반환 좌표는 1-index여야 한다

각 테스트에 대해:
- 테스트 이름
- Given (입력)
- When (호출)
- Then (기대)
- 이 테스트가 보호하는 계약 설명

------------------------------------------------------------
TRACK B — Logic RED
------------------------------------------------------------

다음을 실패 테스트로 작성하십시오:

1. find_blank_coords()
   - row-major 순서로 정확히 2개 반환

2. find_not_exist_nums()
   - 누락 숫자 2개 반환
   - 오름차순

3. is_magic_square()
   - 모든 행 합 동일
   - 모든 열 합 동일
   - 두 대각선 합 동일
   - 34와 일치

4. solution()
   - small → first blank 시도
   - 실패 시 reverse 시도
   - 6-length 반환
   - 1-index 좌표

각 테스트는:
- 실패 상태임을 명확히 설명
- 어떤 Invariant를 검증하는지 명시

------------------------------------------------------------
출력 형식
------------------------------------------------------------

# UI RED Tests
- Test ID
- Scenario
- Invariant 보호 내용

# Logic RED Tests
- Test ID
- Scenario
- Invariant 보호 내용

------------------------------------------------------------

구현 금지
GREEN 단계 금지
REFACTOR 금지
오직 RED 테스트 설계만 수행하십시오

---

**Cursor**

프로젝트 테스트 명세의 ID·용어와 맞추기 위해 `TEST_SPEC`과 PRD의 테스트 추적 방식을 확인합니다.



아래는 프로젝트 [`TEST_SPEC`](docs/TEST_SPEC_Magic_Square_4x4.md)·PRD 추적 ID(`UI-T-*`, `D-T-*`)에 맞춘 **RED 전용 테스트 설계**입니다. (코드·GREEN·REFACTOR 없음.)

---

# UI RED Tests

| Test ID | Scenario | Invariant 보호 내용 |
|---------|----------|---------------------|
| **UI-T-01** | **Given** `M`이 4×4가 아님(예: 3×4, 가변 행 길이). **When** 경계 진입점 `solve_magic_square(M)`(또는 팀이 고정한 Boundary API) 호출. **Then** 단일 입력 오류로 처리되고, PRD FR-01 표의 `E_INPUT_SHAPE`·`message`(문자 그대로)와 일치한다. **(RED 시 구현 부재로 예외/DTO 단언 실패)** | **INV-A1:** 유효한 격자 형태만 도메인으로 넘어간다. 잘못된 형태는 항상 동일 계약으로 거부된다. |
| **UI-T-02** | **Given** 4×4이지만 `0`의 개수가 2가 아님(0개·1개·3개 이상). **When** 동일 호출. **Then** `E_ZERO_COUNT` + FR-01 표 `message`. FR-05/솔버 경로 미호출(스파이·목으로 관측). **(RED 시 실패)** | **INV-A2:** 빈칸이 정확히 두 칸일 때만 해 탐색이 허용된다. |
| **UI-T-03** | **Given** 4×4·`0` 두 개이나 값이 `0` 또는 `1~16` 밖(예: `-1`, `17`). **When** 동일 호출. **Then** `E_VALUE_RANGE` + 표 `message`, FR-05 미호출. **(RED 시 실패)** | **INV-A3:** 허용 값 집합 위반 시 결정론적 오류 코드로만 실패한다. |
| **UI-T-04** | **Given** 4×4·`0` 두 개·범위 내이나 `0` 제외 값이 중복. **When** 동일 호출. **Then** `E_DUPLICATE_NONZERO` + 표 `message`, FR-05 미호출. **(RED 시 실패)** | **INV-A4:** 1~16 치역은 부분칙 입장에서 중복 없이 유지된다. |
| **UI-T-05** | **Given** FR-01을 통과하는 입력으로 경계가 성공 경로를 반환하는 경우(또는 성공 응답을 모의하기 위한 최소 Given). **When** 호출. **Then** 성공 페이로드의 해 벡터는 **길이 6**인 `int[6]`에 해당한다(타입/길이 단언). **(구현 없으면 RED)** | **INV-A5:** 성공 시 산출물이 항상 6슬롯 `(r1,c1,n1,r2,c2,n2)` 계약을 만족한다. |
| **UI-T-06** | **Given** 동일 성공 경로 Given. **When** 호출. **Then** 반환 좌표 `r1,c1,r2,c2`는 모두 **1-index** 범위(1~4) 내이며, 해석 시 off-by-one 오류가 없다. **(RED 시 실패)** | **INV-A6:** 사용자가 보는 좌표와 PRD AC-05의 row-major·인덱싱 규칙이 일치한다. |

---

# Logic RED Tests

| Test ID | Scenario | Invariant 보호 내용 |
|---------|----------|---------------------|
| **D-T-BLANK-01** | **Given** 합법적인 부분 격자 `M`(0 정확히 2개). **When** `find_blank_coords(M)`(또는 팀 명명). **Then** 길이 2의 좌표 리스트이고, **row-major**로 첫 `0` → 둘째 `0` 순서이다(예: `(r,c)` 쌍의 선형 순서 일치). **(구현 없으면 RED)** | **INV-B1 (FR-02):** 이중 대입의 물리적 순서가 항상 정의된 빈칸 순서와 같다. |
| **D-T-MISS-01** | **Given** 동일 전제. **When** `find_not_exist_nums(M)`(또는 동등 API). **Then** `{1..16} \\ set(M의 비영)`인 두 수를 반환하고 **오름차순 `(a,b)`, a\<b**이다. **(RED)** | **INV-B2 (FR-03):** 누락 쌍이 정렬·유일하게 고정되어 시도 규칙과 결합 가능하다. |
| **D-T-JDG-01** | **Given** 완전히 채워진 4×4 정수 격자(테스트용 고정 예: 마방진 한 개·비마방진 한 개). **When** `is_magic_square(grid)`(또는 `MagicSquareJudge`). **Then** 모든 행 합·모든 열 합·두 대각 합이 **서로 같고** 그 공통값이 **34**(4×4 마방진 상수)이면 `true`, 아니면 `false`. **(RED)** | **INV-B3 (FR-04):** “마방진”은 행·열·대각 동일합 34와 동치로 판정된다. |
| **D-T-ASG-01** | **Given** FR-01 합법 격자로, 누락 수 `(a,b)`가 작은 수를 첫 빈칸에 두는 **시도1** 정의에 맞는 입력(검산 가능한 Golden·스텁). **When** `solution(M)`(또는 `DualAssignmentResolver`). **Then** 시도1이 유효 완성 격자를 만들면 **시도1 결과**가 채택되고, 반환은 길이 6·좌표 1-index·`[r1,c1,n1,r2,c2,n2]` 순서가 PRD AC-05-2와 맞다. **(RED)** | **INV-B4a (FR-05):** 작은 수 우선 시도가 규칙대로 적용된다. |
| **D-T-ASG-02** | **Given** 시도1은 실패하고 **시도2**(역순: 큰 수를 첫 빈칸)만 성공하는 검산 격자(PR §9.3 예 A 등). **When** `solution(M)`. **Then** 6-튜플이 AC-05-3(`[r1,c1,b,r2,c2,a]`)을 따른다. **(RED)** | **INV-B4b:** 시도1 실패 후에만 시도2가 의미 있게 적용된다. |
| **D-T-ASG-03** | **Given** 시도1·시도2 모두 완성 불가인 검산 격자. **When** `solution(M)`. **Then** 도메인은 `E_NO_VALID_ASSIGNMENT`(경계 매핑은 별도 UI RED); 임의의 길이 6 “가짜 성공”을 내지 않는다. **(RED)** | **INV-B4c:** 해가 없을 때는 성공 튜플이 존재하면 안 된다. |

---

**메모 (RED 유지):** 위 시나리오는 **pytest에서 import 실패·`NameError`·빈 구현이 `None`을 반환**하는 등으로 **의도적으로 실패**해야 하며, FR-01 실패 케이스에서는 **도메인 솔버가 호출되지 않음**을 테스트 더블로 단언하는 것이 [`TEST_SPEC` §1.5·§1.6](docs/TEST_SPEC_Magic_Square_4x4.md)과 정합합니다.

---

**User**

작업한 내용을 모두 Report 폴더에 보고서로 업데이트 해줘

---

**Cursor**

Report 폴더 구조와 기존 보고서 형식을 확인한 뒤, 대화에서 다룬 내용을 반영한 보고서를 작성합니다.



새 보고서 `09`를 추가하고, `08`·`07`·`README`의 문서 교차 참조를 갱신합니다.



작업 반영 내용입니다.

### 신규: [`Report/09_Magic_Square_Dual_Track_RED_Test_Design_Report.md`](Report/09_Magic_Square_Dual_Track_RED_Test_Design_Report.md)
- Dual-Track RED **범위·금지 사항**(구현/GREEN/REFACTOR 제외)
- 입력·출력·상수 34 요약
- Track A/B 구조 설명
- **UI-T-01~06** 표(시나리오·Invariant)
- **D-T-BLANK/MISS/JDG/ASG** 표(시나리오·Invariant)
- `TEST_SPEC` TC 매핑, Report `02`·`08`과의 관계

### 갱신: [`Report/08_Magic_Square_Git_Branch_PR_Workflow_Report.md`](Report/08_Magic_Square_Git_Branch_PR_Workflow_Report.md) **v1.0 → v1.1**
- **§7** Dual-Track에 맞춘 브랜치 전략(토픽 브랜치 + 커밋 규약, 선택적 단계 브랜치)
- **§8** 로컬 브랜치 **`develop`**, **`feature/dual-track-tdd`** 목적·`git push` 안내
- **§9** 변경 이력
- 관련 문서에 Report `09` 링크, **§6**에 `09` 한 줄 추가

### 갱신: [`Report/07_Magic_Square_README_Repository_Guide_Report.md`](Report/07_Magic_Square_README_Repository_Guide_Report.md) **v1.2 → v1.3**
- `01`~`09` 표기, 부록에 **`09`** 행, 본문 문서 표에 **`09`** 행
- Document change log에 **1.3** 항목 추가

### 갱신: [`README.md`](README.md)
- 문서 관계 표에 **`09`** 한 줄, 말미 각주 **`01~09`**로 정리 (07과 동일한 문서 지도 유지)

원하시면 다음 커밋 예시는 다음과 같이 쓸 수 있습니다:  
`docs(report): add 09 Dual-Track RED design; extend 08 branch strategy and sync 07/README`

