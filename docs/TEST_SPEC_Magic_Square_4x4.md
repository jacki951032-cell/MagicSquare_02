# 테스트 케이스 명세 (Magic Square 4×4)

| 항목 | 내용 |
|------|------|
| 문서 유형 | Test Case Specification (PRD·README와 병행) |
| 정본(요구·문자열) | [`PRD_Magic_Square_4x4_TDD.md`](PRD_Magic_Square_4x4_TDD.md) |
| 갱신일 | 2026-04-28 |

---

## 1. 프로젝트·대상·환경

### 1.1 프로젝트명

**MagicSquare_02** — 4×4 부분 마방진(빈칸 `0` 정확히 2개), 고정 입·출력 계약·이중 시도 규칙에 따른 해(`int[6]`) 또는 오류 보고.

### 1.2 대상 시스템(SUT)

| 구분 | 범위 |
|------|------|
| **경계(Boundary / UX Contract)** | 입력 행렬 `M` 검증(FR-01), 최종 응답의 `code`·`message`·성공 시 6-튜플(경계/Presenter 매핑 포함). 공개 진입점 예: `solve_magic_square(M)` (구현체 이름은 팀 표준에 따름). |
| **도메인(Domain / Logic)** | 빈칸 좌표(FR-02), 누락 두 수 `(a,b)`(FR-03), 완성 격자 마방진 판정(FR-04), 이중 대입·해 또는 `E_NO_VALID_ASSIGNMENT`(FR-05). 논리 컴포넌트 예: `BlankCellLocator`, `MissingNumberFinder`, `MagicSquareJudge`, `DualAssignmentResolver`(이름은 PRD 예시). |

시각 UI는 **기본 범위 Out**; 동일 계약을 `pytest`로 검증하면 Track A 요건을 만족한다([PRD §4.2](PRD_Magic_Square_4x4_TDD.md)).

### 1.3 테스트 환경

| 항목 | 기준 |
|------|------|
| 언어 런타임 | Python **3.10+**(또는 팀이 고정한 동일 버전) |
| 테스트 러너 | **`pytest`**(PRD §3, §7.1 — 로컬·CI **동일 러너**) |
| 의존성 | 최소: `pytest`; (선택) 커버리지·시간 상한 측정은 PRD NFR·§9.1 T-S-05 |
| 소스 배치 | 팀 표준(예: `src/` 레이아웃 + `pythonpath` 설정) |

### 1.4 전제조건(공통)

1. 입력 `M`은 PRD 기준 **`list[list[int]]` 등 4×4 정수 격자**로 표현 가능할 것(행 길이·타입은 FR-01에서 검증).
2. **Magic constant**는 **34**(4×4 고정).
3. 성공 시 좌표·튜플은 **1-index**, 빈칸 순서는 **row-major** 첫 `0`/둘째 `0`(FR-02).
4. 계약 검증 시 `message`는 PRD **표와 문자 그대로**(공백·마침표·대소문자 포함) 일치해야 한다(FR-01 표, `E_DOMAIN_FAILURE` 한 줄 문구).
5. FR-01 실패 시 **FR-05(해 찾기)는 호출되지 않음**; 테스트에서는 스파이·주입 목 등으로 **경로 불가(Impossible)** 를 검증한다([PRD §5.1](PRD_Magic_Square_4x4_TDD.md)).

### 1.5 성공·실패 기준(판정)

| 결과 유형 | 성공 판정 |
|-----------|-----------|
| **경계 성공** | FR-01 통과 후 도메인이 유효한 `int[6]`를 산출하고, 응답 DTO가 PRD AC-05-2·5-3과 일치(완성 격자 FR-04 true). |
| **경계 입력 오류** | `code`가 `E_INPUT_SHAPE` \| `E_ZERO_COUNT` \| `E_VALUE_RANGE` \| `E_DUPLICATE_NONZERO` 중 **정확히 하나**, `message`가 FR-01 표와 **완전 일치**. |
| **도메인 실패(해 없음)** | 도메인 `E_NO_VALID_ASSIGNMENT`; 경계 표현은 `E_DOMAIN_FAILURE` + `message` = `failed to resolve a valid magic-square assignment.` (**한 줄**, PRD §5.1). |
| **실패(불합격)** | 위와 다른 `code`/`message` 조합, 성공 튜플 좌표·순서 오류, FR-01 실패인데 FR-05가 호출됨, 입력 `M` 원본 변형(NFR-03 위반), 동일 입력에 비결정론적 상이 결과(NFR-02 위반). |

### 1.6 특별히 필요한 절차

| 절차 | 목적 |
|------|------|
| **Dual-Track TDD** | 매 루프에서 **Track A(Boundary)** 와 **Track B(Domain)** 에 각각 RED→GREEN이 존재하도록 한다([PRD §8.3](PRD_Magic_Square_4x4_TDD.md)). 도메인만 먼저 끝내고 경계만 나중에 붙이는 순서는 **금지**. |
| **Golden·검산 데이터** | §9.3 예시 격자 등은 **검산된 값**으로 고정; 변경 시 PR·근거 기록([PRD §9.2·9.3](PRD_Magic_Square_4x4_TDD.md)). |
| **FR-05 미호출 검증** | FR-01 실패 케이스에서 이중 대입/솔버 경로가 실행되지 않았음을 **관측 가능한 방식**(목/스파이/후킹)으로 단언. |
| **FR-04와 0 셀** | AC-04-4: `M`에 0이 남아 있는 채 FR-04를 호출하는 경우, 팀이 `(가) false` 또는 `(나) assert` **한 가지**로 통일하고, **단위 테스트 1건**으로 고정([PRD §11](PRD_Magic_Square_4x4_TDD.md)). |
| **회귀** | 통과한 테스트 **삭제 금지**; 계약 변경은 RED 선반영 후 GREEN([PRD §9.2](PRD_Magic_Square_4x4_TDD.md)). |
| **(선택)** | T-S-05: 1건 해 탐지·검증 **50ms** 상한 등(NFR-04). |

---

## 2. 요약 매핑: 일반 TC 표 ↔ PRD

아래는 참고용 대응이다. 실제 TC ID·추적은 팀 도구와 PRD `UI-T-*` / `D-T-*` / `T-S-*` 를 맞춘다.

| 일반 설명(예시) | PRD 대응 |
|-----------------|----------|
| 빈칸 좌표 찾기 | FR-02, `BlankCellLocator` |
| 완성 격자 마방진 여부 | FR-04, `MagicSquareJudge` |
| 빈칸에 두 수를 넣어 해 구하기 | FR-05, `DualAssignmentResolver` + 경계 응답 |
| 입력 형태·0 개수·범위·중복 | FR-01, 경계 `UI-T-01`~`04` |

---

## 3. 테스트 케이스 표(핵심 시나리오)

**※ Given / When / Then** 형식으로 작성한다. 입력 `M`은 필요 시 §9.3·Report/04와 동일 출처의 Golden으로 고정한다.

| TC ID | 기능 분류 | 테스트 항목 | 테스트 목적 | 입력값 / 전제조건 | 테스트 절차 (Given / When / Then) | 예상 결과 | 우선순위 | 비고 |
|-------|-----------|-------------|-------------|-------------------|-------------------------------------|-----------|----------|------|
| TC-MS-A-001 | FR-01 경계 | `UI-T-01` 형태 오류 | 4×4 아님 시 단일 입력 오류 | `M`이 3×4 등 비정형 | **Given** 비정형 `M` **When** `solve_magic_square(M)` **Then** `code=E_INPUT_SHAPE`, message는 FR-01 표 **그대로**, FR-05 경로 미호출 | 위와 동일 | P1 | Boundary Value |
| TC-MS-A-002 | FR-01 경계 | `UI-T-02` 0 개수 | 0이 2개가 아님 | 0이 1개 또는 3개 이상인 4×4 | 위와 동일 절차 | `E_ZERO_COUNT` + 표의 message, FR-05 미호출 | P1 | |
| TC-MS-A-003 | FR-01 경계 | `UI-T-03` 값 범위 | 0·1~16 밖 값 | 17 또는 음수 등 | 위와 동일 | `E_VALUE_RANGE` + 표의 message, FR-05 미호출 | P1 | |
| TC-MS-A-004 | FR-01 경계 | `UI-T-04` 중복 | 0 제외 중복 | 동일 non-zero 2칸 | 위와 동일 | `E_DUPLICATE_NONZERO` + 표의 message, FR-05 미호출 | P1 | |
| TC-MS-B-001 | 통합 §9.1 | `T-S-01` 시도1 성공 | 시도1만으로 완성·FR-04 true | FR-01 합법·시도1 true인 Golden `M` | **Given** `M` **When** solve **Then** `ok`, 6-튜플이 `[r1,c1,a,r2,c2,b]`(AC-05-2) | 성공 튜플 + 완성 격자 합 34 | P1 | |
| TC-MS-B-002 | 통합 §9.1 | `T-S-02` 시도2 성공 | 시도1 false, 시도2 true | PRD §9.3 예 A 등 검산된 `M` | 위와 동일 | 6-튜플이 `[r1,c1,b,r2,c2,a]`(AC-05-3) | P1 | Golden |
| TC-MS-B-003 | 통합 §9.1 | `T-S-03` 해 없음 | 시도1·2 모두 false | 검산된 전용 `M` | 위와 동일 | 도메인/경계 매핑 §5.1 준수 | P1 | Given 검산 필수 |
| TC-MS-B-004 | 통합 §9.1 | `T-S-04` 입력 오류 묶음 | 4종 각각 단일 코드 | TC-MS-A-001~004와 동일 입력 | 경계 호출 | 각 `E_*` 단일·FR-05 미호출 | P1 | |
| TC-MS-B-005 | CI / 비기능 | `T-S-05` 스위트·(선택) 성능 | 회귀·동일 러너·(선택) 상한 | 동일 환경 | `pytest` 전체 실행·(선택) 1건 시간 측정 | 전부 통과·(선택) ≤50ms | P2 | NFR |

---

## 4. 추적

| Concept | PRD 참조 |
|---------|-----------|
| 시나리오 ID | §9.1 `T-S-01`~`T-S-05` |
| 경계 계약 ID | §8.1 `UI-T-01`~`UI-T-07` |
| 도메인 단위 예시 | §8.2 `D-T-VAL-*`, `D-T-JDG-*`, `D-T-ASG-*` |
| 추적 행렬 | PRD §12 |

---

*본 명세의 법적·납기 판정 문구는 PRD가 우선한다.*
