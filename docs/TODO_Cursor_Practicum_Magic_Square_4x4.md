# Magic Square 4×4 완성 시스템 — Cursor 실습용 To-Do 보드

> **근거 PRD:** `docs/PRD_Magic_Square_4x4_TDD.md` (동시에 아래 `Scenario / Test / Code` 추적)  
> **ECB:** Boundary에 비즈니스 규칙 금지 | Control = 검증·해결 **조율** | Entity = **보드 상태(불변 규칙이 걸릴 수 있는 값 객체)**

---

## 1. Epic

- [ ] **Epic-001** — 4×4 Magic Square(빈칸 0 정확히 2)를 **입력 검증 → 빈칸/후보 → 완성 판정(합 34) → 이중 대입 해** 또는 **정의된 오류 코드**로 끝내는 시스템을 TDD(Dual-Track)로 구현한다.  
  - **완료(개념):** PRD `FR-01`~`FR-05`, NFR(커버리지), §9.1 `T-S-01`~`T-S-05` 충족.

---

## 2. User Story

- [ ] **US-001** (도메인·해답) — *유효한 부분 격자*가 주어지면, row-major **첫/둘 0**과 **누락 2수 (a,b), a&lt;b**를 구하고, **시도1/시도2**로 완성 격자를 만들어 **1-index 좌표+값이 담긴 6-튜플**을 얻는다. 불가면 도메인 실패 `E_NO_VALID_ASSIGNMENT`만 성립한다. (FR-02, FR-03, FR-04, FR-05)  
- [ ] **US-002** (경계·입력) — *유효하지 않은* 격자(형태, 0 개수, 1~16/0 외 값, 0 제외 중복)는 **해를 찾기 전에** 거절되고, **정해진 `code`·`message` 한 줄**만 본다(FR-01, AC-01).  
- [ ] **US-003** (Control·품질) — 검증( Boundary ) 통과 시에만 도메인 해 경로로 들어가고( FR-05 미호출 ), 성공/실패 응답이 **결정론**이며, M **원본 불변**이고, CI에서 **pytest + (선택) 커버리지 게이트**가 닫힌다. (NFR, §7.1)

---

## 3. Phase × Task (개발 보드)

> **Scenario Level:** L0=기능 개요 · L1=정상 흐름 · L2=경계 · L3=실패(오류)  
> **RGR:** 각 Task는 **한 사이클(RED → GREEN → REFACTOR)** 로 끝낸다(체크는 완료 시).  
> **Test 이름**은 PRD `UI-T-*` / `D-T-*` / `T-S-*` 및 보충 `test_*` 규칙.  
> **Code 대상**은 식별자(파일·클래스·함수 수준)로 추적.

---

### Phase 0 — 저장소·보드(상태) 생성·골든 픽스처

| # | RGR(완료 시) | Task ID | 작업 제목 | Scenario L | Test 이름(연결) | Code 대상 | ECB |
|---|:------------:|-----------|-----------|:----------:|-----------------|-----------|-----|
| 1.1 | [ ] RED [ ] GREEN [ ] REFACTOR | **TASK-001** | **프로젝트 뼈대** — 패키지·`pytest`·(선택) `ruff`/`mypy` (L0) | L0 | (스모크) `test_project_imports` | `src/` 루트, `pyproject` 또는 `requirements` | **Boundary** (빌드/도구) |
| 1.2 | [ ] R [ ] G [ ] R | **TASK-002** | **보드 생성(값 객체)** — `M` 4×4 + 불변(복사) 정책 (L0/L1) | L0 / L1 | `test_board_immutable_by_policy` (NFR-03 추적) | `Board` / `Matrix4` **Entity** | **Entity** |
| 1.3 | [ ] R [ ] G [ ] R | **TASK-003** | **보드 Factory** — 원시 `int[4][4]` / 리스트 → Entity (L1) | L1 | `test_board_from_valid_m_matches_cells` | `Board.from_values(...)` (Boundary와 분리) | **Entity** |
| 1.4 | [ ] R [ ] G [ ] R | **TASK-004** | **골든 격자·픽스처(§9.3 예 A)** (L1) | L1 | `conftest` / `fixtures: golden_m_example_a` | `tests/fixtures.py` (데이터) | **Entity** + 테스트 인프라 |

| Task ID | 체크포인트(필요 시) |
|---------|----------------------|
| TASK-002~003 | Entity에 **“행·열·합=34” 같은 규칙 판정 넣지 말 것** — PRD SRP(§10) |

---

### Phase 1 — 보드 유효성 검사 + 잘못된 입력( Boundary )

| # | RGR | Task ID | 작업 제목 | Scenario L | Test 이름(연결) | Code 대상 | ECB |
|---|-----|----------|------------|:----------:|-----------------|-----------|-----|
| 2.1 | [ ] R [ ] G [ ] R | **TASK-010** | **4×4 형태** — `E_INPUT_SHAPE` + PRD 표 `message` (L2/L3) | L2 / L3 | `UI-T-01`, `D-T-VAL-01` | `InputMatrixValidator` | **Boundary** (규칙: PRD **표**만) |
| 2.2 | [ ] R [ ] G [ ] R | **TASK-011** | **0이 정확히 2개** — `E_ZERO_COUNT` (L3) | L3 | `UI-T-02`, `D-T-VAL-02` | 동상 | **Boundary** |
| 2.3 | [ ] R [ ] G [ ] R | **TASK-012** | **값 0 or 1~16** — `E_VALUE_RANGE` (L3) | L3 | `UI-T-03`, `D-T-VAL-03` | 동상 | **Boundary** |
| 2.4 | [ ] R [ ] G [ ] R | **TASK-013** | **0 제외 중복** — `E_DUPLICATE_NONZERO` (L3) | L3 | `UI-T-04`, `D-T-VAL-04` | 동상 | **Boundary** |
| 2.5 | [ ] R [ ] G [ ] R | **TASK-014** | **통합 Facade(경계 API)** — 실패 시 **FR-05 미호출** (스파이) (L3) | L3 | `T-S-04`, `AC-05-1` 추적, `test_resolver_not_called_on_invalid` | `SolveMagicSquareUseCase` 입구 또는 `MagicSquareService` (Facade) | **Control** |

| Task ID | 체크포인트(필요 시) |
|---------|----------------------|
| TASK-010~014 | `message` **대소·마침표** PRD 표 **문자 그대로** (PRD §11) · 비즈니스(34·대입)는 **Control/Domain**으로만 |

---

### Phase 2 — 빈칸 탐지 + 후보값(누락 2수) 필터링

> **“후보값 필터링”** = 1~16에서 격자에 **없는 2수** (a,b), a&lt;b — **일반 CSP 전수 탐색** 아님(PRD 4.2).  

| # | RGR | Task ID | 작업 제목 | Scenario L | Test 이름(연결) | Code 대상 | ECB |
|---|-----|----------|------------|:----------:|-----------------|-----------|-----|
| 3.1 | [ ] R [ ] G [ ] R | **TASK-020** | **빈칸 탐지** — row-major 첫/둘 0, 1-index (L1) | L1 | `AC-02-1,2` 단위, `test_blank_positions_match_zeros` | `BlankCellLocator` | **Control**(순수 로직) 또는 **Entity** 헬퍼(팀 합의) ※ PRD: Domain 쪽 |
| 3.2 | [ ] R [ ] G [ ] R | **TASK-021** | **누락 2수 (a,b)** — 0 제외 14칸 기반 여집합, a&lt;b (L1) | L1 | `AC-03-1,2`, `D-T-MISS-01` | `MissingNumberFinder` | **Control** / **Domain** (I/O 없음) |
| 3.3 | [ ] R [ ] G [ ] R | **TASK-022** | **후보 쌍 제약** — (a,b)가 유효 입력이면 0칸에만 넣힌다는 전제(스모크) (L2) | L2 | `test_missing_pair_size_always_2_when_fr01_ok` | 위 컴포넌트 + 고정 M | (연결) FR-01 통과 M만 |

| Task ID | 체크포인트(필요 시) |
|---------|----------------------|
| TASK-021 | **Boundary에 “어떤 수가 앞으로 옳다” 판정 금지** — (a,b)는 FR-01 통과 격자에 대한 **기계적** 여집합이면 충분 |

---

### Phase 3 — 완성 로직: 합 34 판정 + 이중 대입(완성)

| # | RGR | Task ID | 작업 제목 | Scenario L | Test 이름(연결) | Code 대상 | ECB |
|---|-----|----------|------------|:----------:|-----------------|-----------|-----|
| 4.1 | [ ] R [ ] G [ ] R | **TASK-030** | **마방진 판정(FR-04)** — 완성 격자·합 34, 최소 반례 (L1/L2) | L1 / L2 | `D-T-JDG-01`~`D-T-JDG-05` | `MagicSquareJudge` | **Control**(순수) |
| 4.2 | [ ] R [ ] G [ ] R | **TASK-031** | **0 포함 격자(미완성)에 FR-04 호출** — (가) false (나) assert **1가지** + 단위 1 (L2) | L2 | `AC-04-4` (§11) | `MagicSquareJudge` 정책 + `test_incomplete_to_judge_*` | **Control** |
| 4.3 | [ ] R [ ] G [ ] R | **TASK-032** | **해 완성(시도1/2·M 불변·6-튜플)** (L1) | L1 | `D-T-ASG-*`, `AC-05-2,3,4` | `DualAssignmentResolver` | **Control** |
| 4.4 | [ ] R [ ] G [ ] R | **TASK-033** | **경계 응답** — `E_NO_VALID_ASSIGNMENT` → `E_DOMAIN_FAILURE`+주문 (L2/L3) | L2 / L3 | `UI-T-06`, `T-S-03` | `ResponsePresenter` / DTO | **Boundary** |
| 4.5 | [ ] R [ ] G [ ] R | **TASK-034** | **시도1 성공(T-S-01) / 시도2(T-S-02) / Golden §9.3** (L1) | L1 | `T-S-01`~`03`, `UI-T-05`~`07` | Facade+Resolver+Presenter **통합** | **Control**·**Boundary** |

| Task ID | 체크포인트(필요 시) |
|---------|----------------------|
| TASK-030~032 | PRD **읽기 전용 M** — 대입은 **사본** (NFR-03) |
| TASK-032~033 | `DualAssignmentResolver` = 도메인 실패, **Present**만 `E_DOMAIN_FAILURE` |

---

### Phase 4 — 품질·정적 분석 (테스트 커퍼리지 체크포인트)

| # | RGR | Task ID | 작업 제목 | Scenario L | Test 이름(연결) | Code 대상 | ECB |
|---|-----|----------|------------|:----------:|-----------------|-----------|-----|
| 5.1 | [ ] R [ ] G [ ] R | **TASK-040** | **커버리지 수집** — Domain **≥95%** / Boundary **≥85%** (NFR-01) (L0) | L0 | `pytest --cov=...` → CI, `T-S-05` | `tooling`, CI 스크립트, `pyproject` `[tool.coverage]` | **Boundary**(도구) |
| 5.2 | [ ] R [ ] G [ ] R | **TASK-041** | **결정론·회귀** — 동일 입력 동일 `code`/`int[6]`, **통과 테스트 삭제 금지** (L0/L2) | L0 / L2 | `T-S-05`, NFR-02, §9.2 | 문서(CHANGELOG) + 스위트 정책 | (프로세스) |
| 5.3 | (선택) R G R | **TASK-042** | **(선택) 50ms 상한 1건** (NFR-04) (L0) | L0 | `test_solve_single_case_under_50ms` | 성능용 단위 1 | **Control** |

---

## 4. Task 상세 (카드 형식) — 복붙·체크용

> 아래 **각 Task**는 *Scenario, Test, Code* 로 추적됨(요구 사항).  
> **RGR:** 작업을 시작하면 RED부터 체크.

- [ ] **TASK-001** (Epic-001)  
  - **RGR:** [ ] RED [ ] GREEN [ ] REFACTOR  
  - **제목:** Phase0 — 프로젝트 뼈대  
  - **Scenario:** L0 / 수동 시나리오: “`pytest`가 빈 스윗이라도 0 exit”  
  - **Test:** `test_project_imports`  
  - **Code:** 패키지 루트, 설정 파일  
  - **ECB:** Boundary(툴)  
  - **체크포인트:** (없음)  

- [ ] **TASK-002** (Epic-001)  
  - **RGR:** [ ] RED [ ] GREEN [ ] REFACTOR  
  - **제목:** 보드 Entity — 불변·값 표현  
  - **Scenario:** L0/L1 / 정상: 유효 M → 그 격자 값 보존  
  - **Test:** `test_board_values_equal_input`, (선택) NFR-03 `test_solve_does_not_mutate_original` 선행·연동  
  - **Code:** `domain/board.py` (예시) `class Board`  
  - **ECB:** **Entity**  

- [ ] **TASK-010** (US-002)  
  - **RGR:** [ ] RED [ ] GREEN [ ] REFACTOR  
  - **제목:** 4×4·정수 구조 `E_INPUT_SHAPE`  
  - **Scenario:** L2/L3 (실패) — 3×3, 가변 길이 행  
  - **Test:** `UI-T-01`  
  - **Code:** `InputMatrixValidator`  
  - **ECB:** **Boundary**  
  - **체크:** `message` = PRD 표 1:1  

- [ ] **TASK-011~013** — 동일 테이블, **L3** 실패 전용(0 개수·범위·중복)  

- [ ] **TASK-020** (US-001)  
  - **RGR:** [ ] R [ ] G [ ] R  
  - **제목:** 빈칸 탐지(첫/둘 0)  
  - **Scenario:** L1 — T-S-01/02/03 전 `Given`  
  - **Test:** `test_blank_order_row_major_1index`  
  - **Code:** `BlankCellLocator`  
  - **ECB:** **Control**(또는 Domain **순수 함수**; PRD §10에 맞춤)  

- [ ] **TASK-021**  
  - **RGR:** [ ] R [ ] G [ ] R  
  - **제목:** 후보값(누락 2수) 필터링 (a,b), a&lt;b  
  - **Scenario:** L1, L2 — 유효 격자에서 2수만 누락 (대규칙)  
  - **Test:** `D-T-MISS-01`  
  - **Code:** `MissingNumberFinder`  
  - **ECB:** **Control**  

- [ ] **TASK-030**  
  - **RGR:** [ ] R [ ] G [ ] R  
  - **제목:** 완성·합 34 **판정**  
  - **Scenario:** L1(성공 격자), L2(행/열/대각 최소 반례)  
  - **Test:** `D-T-JDG-*`  
  - **Code:** `MagicSquareJudge`  
  - **ECB:** **Control**  
  - **체크:** FR-04=판정만, “해”는 TASK-032  

- [ ] **TASK-032**  
  - **RGR:** [ ] R [ ] G [ ] R  
  - **제목:** **완성 로직** — 이중 대입(시도1/2) + 6-튜플/도메인 실패  
  - **Scenario:** L1(시도1, 시도2) / L3(둘 다 실패)  
  - **Test:** `D-T-ASG-*`, `T-S-01`~`03`  
  - **Code:** `DualAssignmentResolver`  
  - **ECB:** **Control** (도메인 비-I/O)  

- [ ] **TASK-040** (US-003)  
  - **RGR:** [ ] R [ ] G [ ] R  
  - **제목:** **테스트 커버리지** 체크포인트  
  - **Scenario:** L0 — `pytest` + `coverage` 게이트  
  - **Test:** (메타) NFR-01, `T-S-05`  
  - **Code:** CI, `.coveragerc`  
  - **ECB:** Boundary(도구)  
  - **체크:** Domain ≥95%, Boundary ≥85% (PRD)  

---

## 5. 추적(요약 매트릭스)

| 도메인 규칙(질문 문구) | Phase / Task | Scenario L(주) | Test(대표) | Code |
|------------------------|--------------|---------------|------------|------|
| 4×4, 0 두 칸, 1~16, 0 이외 중복 없음 | P1 / TASK-010~014 | L2, L3 | `UI-T-01`~`04` | `InputMatrixValidator` |
| 0=빈칸, 첫/둘 0 (row-major) | P2 / TASK-020 | L1, L2 | AC-02 | `BlankCellLocator` |
| 후보 2수(누락) a&lt;b | P2 / TASK-021~022 | L1, L2 | AC-03 | `MissingNumberFinder` |
| 행·열·대각=34(완성) | P3 / TASK-030~031 | L1, L2, L3 | `D-T-JDG-*` | `MagicSquareJudge` |
| 이중 대입 + 해/실패 + 6-튜플 | P3 / TASK-032~034 | L1, L3 | `D-T-ASG`, `T-S-01`~`03` | `DualAssignmentResolver` + **Presenter** |
| 잘못된 보드(형태/값) | P1 / TASK-010~014 + Control | L3 | `T-S-04` | **Boundary**+Control |

---

## 6. RGR·ECB(보드) 한 줄 수칙 (실습 시)

- [ ] **RED** first: *연결 Test 이름*이 실패 → **GREEN**: 최소 구현 → **REFACTOR**: SRP(판정/대입 분리).  
- [ ] **Boundary** = 스키마·`code`/`message`·응답 DTO. **34·대입**은 **Domain/Control**만.  
- [ ] **Entity** = `Board`(또는 4×4) **상태**; *규칙*은 `Judge`/`Resolver` 쪽.  

---

*식별자: Epic-001, US-001~003, TASK-001~042(번호 공백은 의도적: 삽입 여지). PRD `INV-D-*` 상세는 Report/02 동기 — 본 To-Do 판정은 **PRD AC** 우선.*
