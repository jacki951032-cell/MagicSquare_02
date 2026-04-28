# Magic Square (4×4) — TDD 연습

4×4 격자에 **빈칸(0) 2개**와 1~16의 일부가 주어질 때, **고정된 입·출력 계약**과 **이중 시도(정배치·역배치)**에 따라 `int[6]` 해를 반환하거나 **정의된 오류 코드**로 실패를 보고하는 **순수 도메인** 중심 연습 저장소다. (근거: [`docs/PRD_Magic_Square_4x4_TDD.md`](docs/PRD_Magic_Square_4x4_TDD.md) Executive Summary, §2)

**검증·납기의 정본(Requirements of Record):** 아래 **기능·승인 기준·시나리오**는 **PRD**에 있다. Report는 스토리·용어·ECB·여정을 **보강**한다.

---

## 문서 관계(한 줄)

| 문서 | 역할(한 줄) |
|------|-------------|
| **[`docs/PRD_Magic_Square_4x4_TDD.md`](docs/PRD_Magic_Square_4x4_TDD.md)** | **FR·AC·BR·NFR·테스트 ID·§12 추적** — 구현·리뷰의 1차 근거. |
| [`Report/01_Magic_Square_Problem_Definition_Report.md`](Report/01_Magic_Square_Problem_Definition_Report.md) | 문제를 “정답 찾기”가 아닌 **제약·검증 가능한 계약**으로 정의하는 사고(문제 정의, Invariant). |
| [`Report/02_Magic_Square_Dual_Track_TDD_Clean_Architecture_Report.md`](Report/02_Magic_Square_Dual_Track_TDD_Clean_Architecture_Report.md) | **Dual-Track**·`INV-D-*`·`D-T-*`·도메인 컴포넌트·**ECB(개념)**·도메인 API 실패조건. |
| [`Report/03_Magic_Square_CursorRules_Report.md`](Report/03_Magic_Square_CursorRules_Report.md) | Cursor/에이전트 **품질·금지 룰·TDD 습관**(팀/개인 룰과 병기). |
| [`Report/04_Magic_Square_User_Journey_Traceability_Report.md`](Report/04_Magic_Square_User_Journey_Traceability_Report.md) | **Epic → User Journey → User Story**·Gherkin·**입력검증 100% 계약**·성공 기준 요약. |
| [`Report/05_Magic_Square_PRD_Report.md`](Report/05_Magic_Square_PRD_Report.md) | PRD의 **내부 보고서 본**; Report **01~04**와 **§정렬** 표(동기 권장). |
| [`Report/06_Magic_Square_Layered_Design_TDD_Contracts_Report.md`](Report/06_Magic_Square_Layered_Design_TDD_Contracts_Report.md) | (있을 경우) 레이어·계약 설계 보강. |
| [`docs/TODO_Cursor_Practicum_Magic_Square_4x4.md`](docs/TODO_Cursor_Practicum_Magic_Square_4x4.md) / [`docs/IMPLEMENTATION_TODO_Magic_Square_4x4.md`](docs/IMPLEMENTATION_TODO_Magic_Square_4x4.md) | **Task/Epic/Phase** 수준 **실습 보드**(PRD·Report와 정합). |
| [`Report/07_Magic_Square_README_Repository_Guide_Report.md`](Report/07_Magic_Square_README_Repository_Guide_Report.md) | 본 `README`와 **동기**한 **Report 폴더 수출본**(온보딩·인쇄·배포). |
| [`Report/10_Magic_Square_Local_Execution_and_GUI_Report.md`](Report/10_Magic_Square_Local_Execution_and_GUI_Report.md) | **로컬 실행·`pytest`·GUI** (`python -m magicsquare.gui`) 절차를 Report에만 따로 정리한 보고서. |

*(Report/05 “문서 간 정렬”은 PRD 2절·4~6·8·User Journey·TC와 **동기**를 취한다.)*

---

## 핵심 User Story(요지, Report/04 정렬)

- **As a** 학습자, **I want** 입력이 4×4·규칙(빈칸 수, 범위, 중복)에 맞는지 **경계에서** 검증되기를, **so that** 잘못된 데이터가 Domain으로 **넘어가지 않는다** (FR-01).
- **As a** 학습자, **I want** `0`인 셀의 **좌표**를 (row-major 첫/둘) 정확히, **so that** **이중 대입**이 가능하다 (FR-02, FR-05).
- **As a** 학습자, **I want** 1~16 **누락 2수 (a,b), a&lt;b**·**시도1/2**·**행·열·대각=34** 판정, **so that** **`int[6]`** 또는 “해 없음”이 **결정론**으로 정해진다 (FR-03~05).

---

## 오류·계약 요약(검증 시 이 표와 PRD 본문·테스트가 **일치**해야 함)

### 입력(경계) — FR-01

| `code` | `message` (PRD **문자 그대로** Contract) |
|--------|-------------------------------------------|
| `E_INPUT_SHAPE` | `matrix must be a 4x4 integer array.` |
| `E_ZERO_COUNT` | `matrix must contain exactly two zeros.` |
| `E_VALUE_RANGE` | `matrix values must be 0 or between 1 and 16.` |
| `E_DUPLICATE_NONZERO` | `non-zero values must be unique.` |

- FR-01 실패 시 **FR-05(해 찾기)는 호출되지 않는다** (AC-01, AC-05-1).

### 도메인 ↔ 경계(응답) — FR-05, PRD §5.1

| 내부(도메인) | 경계(사용자/응답) |
|--------------|-------------------|
| `E_NO_VALID_ASSIGNMENT` (이중 시도 모두 실패) | `E_DOMAIN_FAILURE` + `message` = `failed to resolve a valid magic-square assignment.` (Presenter/Boundary **매핑**; `UI-T-06`) |

### 성공(출력)

- **`int[6]`** = `[r1, c1, n1, r2, c2, n2]` (좌표 **1-index**). 시도1/2 정의·순서는 **PRD FR-05** (§4.1, AC-05-2, AC-05-3).

---

## 아키텍처(ECB, PRD §10 + Report/04 Journey “Domain 분리”)

| ECB | 책임(한 줄) |
|-----|-------------|
| **Entity** | 4×4 **상태**·값 객체(좌표, 누락 쌍 등); **“합=34” 판정 로직**은 Entity에 **넣지 말고** `MagicSquareJudge`·Resolver 쪽 SRP(Report/04 “**BlankFinder… Solver** 경계”, PRD §10 SRP). |
| **Control** | **FR-01 통과 후에만** blank·missing·judge·**DualAssignment** 순(또는 use case Facade). 입력 `M` **불변**(NFR-03), 해는 **사본**에 대입. |
| **Boundary** | **입력 스키마** 검사, **`code` / 고정 `message`**, 성공 DTO. **화면이 없어도** `pytest`로 `code`·`message`·6-튜플이 “visible”/“includes”이면 **Dual-Track Track A** 충족(§4.2, §8.1). |

**의존:** Boundary → (Application 선택) → **Domain**; **Domain**은 UI/DB/HTTP **비의존**(PRD §10).

---

## 실행·테스트(근거: PRD §3, §7, §9)

### 환경 준비

| 항목 | 요구 |
|------|------|
| Python | **3.10 이상** (`python --version`) |
| 저장소 루트 | 프로젝트 디렉터리에서 아래 명령 실행 (예: `MagicSquare_02`) |

**(선택)** 가상환경으로 격리:

```powershell
# PowerShell (Windows)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
# Bash / macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 패키지 설치

테스트와 라이브러리만 필요할 때:

```bash
pip install -e .
```

**GUI(Window)** 를 띄우거나 `tests/ui/` 가 PyQt를 쓰려면 **`[gui]` extra**까지 설치합니다.

```bash
pip install -e ".[gui]"
```

설치 확인: `pip show PyQt6` 가 나오면 GUI 실행에 필요한 의존성이 들어간 상태입니다.

### 단위·통합 테스트 (`pytest`)

프로젝트 루트에서:

```bash
pytest
```

선택 실행 예:

```bash
pytest tests/domain -v
pytest tests/boundary -v
pytest tests/ui -v
```

PyQt를 설치하지 않았다면 **`tests/ui/test_ui_magic.py`** 한 건은 `pytest.importorskip` 으로 **자동 스킵**됩니다. UI 테스트까지 돌리려면 위의 `pip install -e ".[gui]"` 가 필요합니다.

### GUI 프로그램 실행 (공식 진입점)

패키지 모듈로 MVP 격자 창을 엽니다 (**PyQt6 필요**).

```bash
python -m magicsquare.gui
```

- 창 제목은 `Magic Square 4×4 — Grid (MVP)` 형태이며, 4×4 숫자 스핀박스 격자만 제공합니다 (풀이 버튼·연동은 추후 과제에서 확장 가능).
- 실행이 끝나려면 연 창을 닫거나 터미널에서 프로세스를 종료하면 됩니다.

**(참고)** 디스플레이가 없는 Linux CI 등에서는 `QT_QPA_PLATFORM=offscreen` 같은 설정이 필요할 수 있습니다. 로컬 데스크톱에서는 통상 불필요합니다.

---

- **권장:** 위와 같이 `pytest` 로컬·CI **동일** 러너 (PRD §3, §7.1).
- (구현 후) **품질 게이트(예):** Domain 분기/라인 **≥95%**, Boundary **≥85%** (NFR-01) — `coverage` 등, CI optional.
- **시나리오(납기 검증):** PRD **§9.1** `T-S-01`~`T-S-05` (정상 시도1/2, 해 없음, 입력 오류 4종, `pytest` 전부·(선택) 50ms).
- **골든 격자·회귀:** **§9.3** 예 A(및 T-S-02/03 **전용 M**) — `Report/04` 출처와 **검산** 동기 권장(§9.2 삭제 금지).

---

## TDD( Dual-Track + RGR, PRD §1.1, §8 )

- **Track A (Boundary / UX Contract):** `code`·`message`·6-튜플(또는 DTO) — `UI-T-01`~`07`·Contract **Includes/Visible** (§5.1, §8.1).
- **Track B (Domain / Logic):** `D-T-VAL-*`, `D-T-JDG-*`, `D-T-ASG-*` — `Allow`/`Reject`/`Return` (§5.1, §8.2).
- **RGR:** **같은 루프**에 A·B **둘 다** RED → GREEN → **REF** (§8.3). **“도메인 전부 먼저, 경계는 나중”** 순서 **금지**(§8.3).

---

## 1.3 To-Do — 체크박스 · 단계 번호 · Requirements(C2C) 추적

**정본:** PRD `FR-01`~`FR-05`, `AC`, §9.1 `T-S-*` — [`docs/PRD_Magic_Square_4x4_TDD.md`](docs/PRD_Magic_Square_4x4_TDD.md) · [상세 Task·Epic 전개](docs/TODO_Cursor_Practicum_Magic_Square_4x4.md)  
**식별자:** `Epic-001` → `US-00n` → `TASK-0xx` (필요 시 `TASK-0xx-y` = RED / GREEN / REFACTOR)  
**시나리오 레벨:** L0=개요 · L1=정상(Happy) · L2=경계(Edge) · L3=실패(Fail) · (선택) **UI**=경계 계약(Track A)  
**C2C 실천:** **Task → Req(=PRD의 FR) → 시나리오 L·테스트 → 코드**가 한 줄로 잡히면 추적 끊김이 없다.

### 왜 이 순서인가 (sequence / 의존성)

1. **FR-01 먼저** — “격자가 도메인에 **넘어갈 자격**이 있나”만 본다. 실패면 **FR-05(해 찾기)는 절대 호출하지 않는다**는 계약( AC-01, AC-05-1 )이 상위다.  
2. **Control( Facade / 유스케이스 )** — 경계가 실패를 반환할 때, 내부 `DualAssignment`가 **실수로도** 호출되지 않게 **스파이/목**으로 끊는다( `T-S-04` ).  
3. **FR-02 → FR-03** — 유효 격자에서만 **빈칸 좌표(1-index)**·**누락 2수 (a,b), a&lt;b**가 결정론으로 나온다(둘은 이후 `FR-05`의 입력).  
4. **FR-04** — “완성 격자가 합=34냐” **판정만**. **이중 대입( FR-05 )**은 Judge를 **의존**하므로 먼저(또는 **Dual-Track으로 같은 루프**에서) 깨끗한 `MagicSquareJudge`가 있어야 한다( PRD §10 SRP ).  
5. **FR-05 + Presenter** — **사본에** 대입 → 시도1/2 → 성공 `int[6]` 또는 `E_NO_VALID_ASSIGNMENT` → 경계 `E_DOMAIN_FAILURE`+고정 `message` ( §5.1 ) · **M 원본 불변**( NFR-03 ).  
6. **NFR/CI** — 마지막에 “전체 스위트+커버리지”로 **한 번** 묶는다( §7.1, T-S-05 ).

*PRD **§8.3**: “**도메인 전부** 먼저, **경계만** 나중” **금지** — 루프마다 **Track A·B 둘 다** RED가 있어야 한다.*

---

### Epic-001: Magic Square 4×4 **완성·검증** 시스템

- [ ] **Epic-001** (전체) — 4×4, 빈칸 0 두 개, 이중 대입+합 34, **4종 입력 오류+도메인 실패**·**C2C** 정합

#### US-000: 사전 조건(저장소·골든)

- [ ] **US-000** — `pytest` + 패키지 뼈대, §9.3 **골든** `M`, (선택) CI
  - [ ] **TASK-001:** `src/`·`pytest`·최소 `test_smoke` — *Req: (인프라)* — 시나 L0 — `test_smoke` — (스켈) 패키지
  - [ ] **TASK-002:** `conftest` / `fixtures`에 **§9.3 예 A** (및 T-S-02/03 **전용 M** 검산 후) — *Req: §9.3* — L1 — (픽스처) — *Checkpoint 아래*

> **[Checkpoint] TASK-001~002** — `pytest`가 **0 exit**; 골든 `M` **한 곳**에서만 import(§9.2 “데이터=평가 세트”).

#### US-001: 입력 검증( Boundary / **FR-01** )

*Dual-Track: `UI-T-01`~`04` + `D-T-VAL`.*

- [ ] **US-001** — 잘못된 `M`은 4종 **하나**의 `code`+**표 `message` 그대로**; 이후 도메인 **불가**
  - [ ] **TASK-010:** 4×4·정수 구조 아님 → `E_INPUT_SHAPE` + 메시지 — *Req: **FR-01** (AC-01-1)* — L3 / UI·계약 — `UI-T-01`, `D-T-VAL-01` — `InputMatrixValidator` / Boundary
    - [ ] **TASK-010-1:** `validate_shape` **RED** (실패 케이스)
    - [ ] **TASK-010-2:** **GREEN** (최소 통과)
    - [ ] **TASK-010-3:** **REFACTOR** (중복·이름, 메시지 상수 `matrix must be a 4x4…` 1:1)
  - [ ] **TASK-011:** 0이 2개가 아님 → `E_ZERO_COUNT` — *FR-01 (AC-01-2)* — L2/L3 — `UI-T-02` — **Boundary**
  - [ ] **TASK-012:** 0 or 1~16 위반 → `E_VALUE_RANGE` — *FR-01 (AC-01-3)* — L3 — `UI-T-03` — **Boundary**
  - [ ] **TASK-013:** 0 제외 중복 → `E_DUPLICATE_NONZERO` — *FR-01 (AC-01-4)* — L3 — `UI-T-04` — **Boundary**

> **[Checkpoint] US-001** — 네 `message` **문자**가 PRD 표와 **완전 일치**( §11 오타 주의).

#### US-002: Control( FR-01 실패 시 **FR-05 미호출** )

- [ ] **US-002** — Facade / `solve(M)`: 검증 실패 → **Resolver/DualAssignment 0회**
  - [ ] **TASK-020:** **스파이/목**으로 `T-S-04` — *Req: **AC-05-1**+FR-01* — L3(경로 불가) — `test_fr05_not_called_when_fr01_fails` — `SolveMagicSquare`·**Control**

> **[Checkpoint] TASK-020** — `Impossible(경로)`(§5.1)을 테스트로 명시(Dual-Track A·B **동시**).

#### US-003: 빈칸 + 누락 2수( **FR-02**, **FR-03** )

- [ ] **US-003** — **유효 M**에만: row-major **첫/둘 0(1-index)**; **(a,b), a&lt;b**
  - [ ] **TASK-030:** `BlankCellLocator` — *FR-02* — L1 / L2 — `AC-02-1,2` 단위 — `BlankCellLocator`·**Control/Domain**
  - [ ] **TASK-031:** `MissingNumberFinder` — *FR-03* — L1 — `AC-03-1,2` — `MissingNumberFinder`

#### US-004: 합=34 **판정**( **FR-04** )

*Dual-Track: `D-T-JDG-*`.*

- [ ] **US-004** — **완성(0 없음) 4×4**만: 행·열·주·부 **=34**; 최소 반례; 0이 있을 때 **false 또는 assert 1가지** ( AC-04-4 )
  - [ ] **TASK-040:** 알려진 마방진 + 행/열/대각 **최소** 깨뜨리기 — *FR-04* — L1, L2 — `D-T-JDG-01`~`05` — `MagicSquareJudge`
  - [ ] **TASK-041:** 미완성(0 섞임) + Judge 정책·단위 1 — *FR-04* — L2 — `test_judge_incomplete_matrix_*` — `MagicSquareJudge`

#### US-005: 이중 대입·6-튜플·경계 매핑( **FR-05** )

*Dual-Track: `D-T-ASG`, `UI-T-05`~`07`, `T-S-01`~`03`.*

- [ ] **US-005** — 시도1( a→첫, b→둘 ) → 실패 시 시도2( b→첫, a→둘 ); **M 사본**; 해 없으면 **도메인** `E_NO_VALID_ASSIGNMENT` → **Presenter** `E_DOMAIN_FAILURE`+한 줄 `message`
  - [ ] **TASK-050:** `DualAssignmentResolver` + **M 불변** — *FR-05* — L1(성공) / L3(해 없음) — `D-T-ASG`, `T-S-01`~`03` — `DualAssignmentResolver` + 통합
  - [ ] **TASK-051:** `Presenter` / DTO: `E_DOMAIN_FAILURE` **Includes** (§5.1) — *FR-05* — L3(도메인 실패) — `UI-T-06` — **Boundary**

> **[Checkpoint] US-005** — 성공 6-튜플 `T-S-01`(시도1) / `T-S-02`(시도2) + §9.3; **NFR-03** 원본 동등 assert.

*선택:*
- [ ] `TASK-052` — NFR-04: **&lt;50ms** 1건만 — *NFR-04* — L0 — `T-S-05` 부분 — (선택)

#### US-006: NFR / 회귀 / MLOps(비-ML)

- [ ] **US-006** — 커버리지( Domain ≥95%, Boundary ≥85% ), **결정론(NFR-02)**, **통과 테스트 삭제 금지**( §9.2 ) — *NFR-01,02* — L0 — `T-S-05` — `coverage`·CI
  - [ ] **TASK-060:** `pytest` + (선택) `coverage` gate, CI
  - [ ] **TASK-060-1:** (선택) **REFACTOR** — 중복 제거, 네이밍; **스위트 전부 녹색**

---

### Requirements Traceability(요약 매트릭스)

*상태 란은 **로컬 실습**에서 `PASS` / `RED` / `TODO`로 갱신.*

| Task ID | Req ID (PRD) | Scenario (L) | 테스트 (Track) | 상태(예) |
| :---: | :---: | :--- | :--- | :---: |
| TASK-001 | — (인프라) | L0 개요 | `test_smoke` | ⬜ TODO |
| TASK-002 | §9.3 | L1 Golden | (fixtures) | ⬜ TODO |
| TASK-010~013 | **FR-01** | L2/L3, **UI** | `UI-T-01`~`04` | ⬜ TODO |
| TASK-020 | **FR-01**+**AC-05-1** | L3(경로 불가) | `T-S-04` | ⬜ TODO |
| TASK-030 | **FR-02** | L1 Happy | (단위+고정 M) | ⬜ TODO |
| TASK-031 | **FR-03** | L1 Happy | `AC-03` | ⬜ TODO |
| TASK-040~041 | **FR-04** | L1, L2 Edge | `D-T-JDG-*` | ⬜ TODO |
| TASK-050~051 | **FR-05** | L1, L3 Fail | `D-T-ASG`, `T-S-01`~`03`, `UI-T-05`~`07` | ⬜ TODO |
| TASK-060 | NFR-01,02, §7.1 | L0 / 회귀 | `T-S-05` | ⬜ TODO |

**C2C 한 문장:** `TASK-0xx` — **다음 Req·시나 L·(Dual-Track) Test 이름** — `Boundary|Control|Entity` 코드 — (체크) → PRD `AC`와 **일치**하면 “완료”로 본다.

---

**구현·최종 판정(요지):** PRD **AC** + **NFR-01,02,03** + `T-S-01`~`05` **전부** 통과. `INV-D-*` **전문**은 [Report/02](Report/02_Magic_Square_Dual_Track_TDD_Clean_Architecture_Report.md)와 PRD **§6·§12** **동기**.

---

## 라이선스 / 기여

레포지토리 정책에 맞게 추가(미정 시 생략).

---

*이 README는 [`docs/PRD_Magic_Square_4x4_TDD.md`](docs/PRD_Magic_Square_4x4_TDD.md)를 **중심**으로, 스토리·ECB·TDD·문서 링크를 [`Report/`](Report/) **01~05**(및 06)에서 **참고**해 정리했으며, **법적/납기 판정은 PRD**가 우선한다.*
