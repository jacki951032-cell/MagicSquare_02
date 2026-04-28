# Magic Square 4×4 — 구현용 To-Do 구조 (PRD 기반)

> **주 소스:** `docs/PRD_Magic_Square_4x4_TDD.md` (할 일·완료 조건)  
> **보조:** `Report/*`는 스토리 분해·INV 전문·여정이 불명확할 때만 참고  
> **적용:** Concept–Code Traceability, Dual-Track TDD, To-Do → Scenario → Test → Code, ECB, RED–GREEN–REFACTOR

---

## 1. 방법론을 To-Do에 싣는 법 (한 장 요약)

| 방법론 | To-Do에 넣는 것 |
|--------|-----------------|
| **Concept-to-Code Traceability** | 각 To-Do에 **Concept(INV/BR) → FR → AC → Test ID → ECB 역할** 한 줄(또는 표)로 표기. PRD **§12 Traceability Matrix**를 상위 뷰로 둔다. |
| **Dual-Track UI + Logic TDD** | **트랡 A( Boundary )**: `code`·`message`·6-튜플 DTO·`pytest` assert (§4.2, §8.1, `UI-T-*`). **트랙 B( Domain )**: FR-02~05·`E_NO_VALID_ASSIGNMENT` 등 도메인 규칙 (`D-T-*`, BR). **같은 스프린트/루프**에서 A·B 둘 다 RED가 있어야 함 (§8.3). |
| **To-Do → Scenario → Test → Code** | (1) To-Do = deliverable + 완료 조건(AC/NFR) (2) **Scenario** = PRD **§9.1** `T-S-*` 또는 Gherkin 수준 Given/When/Then (3) **Test** = `UI-T-*` / `D-T-VAL-*` 등 구체 케이스 ID (4) **Code** = ECB 컴포넌트·최소 구현. **순서: RED(테스트) → GREEN → REFACTOR**. |
| **ECB** | **Entity**: 순수 자료(격자, 좌표, 누락 쌍)와 불변 규칙. **Control**: use-case/오케스트(검증 후 도메인 호출, 시도1→2 순서, 매핑). **Boundary**: 입력 스키마 검사, `E_*`+고정 `message`, 성공 DTO/Presenter (PRD **§10**). |
| **RED–GREEN–REFACTOR** | 항목마다 **(1) RED**: 실패하는 테스트 1개(Boundary) + 1개(Domain) **(2) GREEN**: 최소 통과 **(3) REFACTOR**: 중복 제거, 네이밍, 스위트 전체·계약 유지. |

---

## 2. ECB–PRD 매핑 (구현 시 네이밍 가이드)

| ECB | PRD §10 / 역할 | 비고 |
|-----|----------------|------|
| **Boundary** | Validator Facade, Presenter | FR-01(경계), 도메인 `E_NO_VALID_ASSIGNMENT` → `E_DOMAIN_FAILURE`+`message` (§5.1) |
| **Control** | (선택) Application/Use case 래퍼 | FR-01→FR-05 흐름, FR-01 실패 시 **FR-05 미호출** 보장(스파이) |
| **Entity / Domain** | `BlankCellLocator`, `MissingNumberFinder`, `MagicSquareJudge`, `DualAssignmentResolver` | Domain은 I/O·Boundary **비의존**; FR-04와 FR-05 **분리** (PRD **§10 SRP**) |

---

## 3. Concept-to-Code: 상위 추적 (PRD §12 압축)

| # | 개념·불변 | BR | FR | AC (완료의 법적 근거) | 테스트(예시) | 논리 컴포넌트 |
|---|-----------|----|----|------------------------|-------------|--------------|
| T1 | 입력 구조·0·범위·중복 | BR-01~04 | FR-01 | AC-01-1~4 | D-T-VAL, `UI-T-01`~`04` | `InputMatrixValidator` + Boundary |
| T2 | row-major 첫/둘 0 | BR-04 | FR-02 | AC-02-1,2 | 단위(고정 M) | `BlankCellLocator` |
| T3 | 누락 2수 a&lt;b | BR-05,06 | FR-03 | AC-03-1,2 | 단위 | `MissingNumberFinder` |
| T4 | 합 34·완성 격자 | BR-07 | FR-04 | AC-04-1~4, AC-04-4 | `D-T-JDG-*` | `MagicSquareJudge` |
| T5 | 이중 대입·해/실패 | BR-08~10 | FR-05 | AC-05-1~4 | `D-T-ASG`, `UI-T-05`~`07` | `DualAssignmentResolver` + Presenter |
| T6 | 메시지·지도 | — | FR-01, FR-05, §5.1 | 5.1, AC-05-1,4 | `UI-T-*`, Contract | Boundary Presenter |
| T7 | 품질·데이터 | NFR, §7.1, §9.2, §9.3 | — | 9.2, T-S-05, Golden | CI, 9.3 격자 | 인프라·`pytest` |

---

## 4. To-Do 목록: 스토리 단위 (Dual-Track + RGR 내장)

아래 **각 To-Do**는 동일 템플릿으로 실행한다.  
**Scenario**는 PRD **§9.1** `T-S-*`에 연결. **완료 조건** = 해당 **AC** + (해당 시) **NFR** + 스위트 녹색.

### 템플릿 (모든 본문 항목에 복붙·채움)

```text
[To-Do ID] 제목
- Concept / Trace: INV… / BR… / FR…
- Scenario: T-S-__ (§9.1) + 한 줄 Given/When/Then
- Test (RED 대상):
  - Track A (Boundary): UI-T-__ …
  - Track B (Domain):   D-T-__ …
- ECB: Boundary … / Control … / Entity …
- RGR: RED → GREEN → REFACTOR (이 항목에서 멈출 때 스위트 전부 통과)
- PRD 완료 조건: AC-__-__; (선택) NFR-__; §9.2/§9.3 준수
```

---

### Phase 0 — 뼈대·CI·골든 데이터 (T7 선행, 반복)

| ID | 내용 | PRD | 완료 조건 |
|----|------|-----|----------|
| **P0-1** | `pytest` 프로젝트·최소 패키지 구조(도메인/boundary 분리 폴더) | §3, §10 | `pytest` 실행 가능, import 경로 확정 |
| **P0-2** | CI(로컬 스크립트도 가능)에서 `pytest` + (선택) coverage 게이트 | §7.1, NFR-01 | T-S-05: 전부 통과(선택: Domain≥95%, Boundary≥85%) |
| **P0-3** | §9.3 **예 A** 격자 등 Golden `M`을 **한 곳**에 상수/픽스처로 두고, 출처 주석(Report/04 동기) | §9.3, §9.2 | 변경 시 PR+검산 원칙 문서와 일치(§9.2) |

---

### Phase 1 — T1: 입력 검증 (Boundary + Domain 일부)

| ID | 내용 | PRD | 완료 조건 |
|----|------|-----|----------|
| **1-1** | `E_INPUT_SHAPE` — 4×4가 아님, FR-05 **미호출** | AC-01-1, T-S-04 | **A:** `UI-T-01` (Visible `message` 표) **B:** (필요 시) D-T-VAL, Validator 단위 **RGR** **ECB:** Validator(Boundary) |
| **1-2** | `E_ZERO_COUNT` | AC-01-2, T-S-04 | A: `UI-T-02` **RGR** |
| **1-3** | `E_VALUE_RANGE` | AC-01-3, T-S-04 | A: `UI-T-03` **RGR** |
| **1-4** | `E_DUPLICATE_NONZERO` | AC-01-4, T-S-04 | A: `UI-T-04` **RGR** |
| **1-5** | 4종 `code`+`message` **문자 그대로**(FR-01 표), Dual-Track 병행 확인 | FR-01 §표, AC-01 전부, §5.1 | 통합/Contract: 네 케이스 `message` 정확 일치, **NFR-02** 결정론 |

**Scenario 루트:** T-S-04.  
**Code:** `InputMatrixValidator` + Facade(Control 경계)에서 “유효할 때만” FR-02 이후로 진입.

---

### Phase 2 — T2+T3: 좌표·누락 (Domain, 트랙 A는 성공 경로에 연동)

| ID | 내용 | PRD | 완료 조건 |
|----|------|-----|----------|
| **2-1** | Row-major 첫/둘 0, 1-index | AC-02-1,2, BR-04 | B: `BlankCellLocator` 단위 + FR-01 통과 고정 M **RGR** |
| **2-2** | 누락 (a,b), a&lt;b | AC-03-1,2 | B: `MissingNumberFinder` **RGR** |
| **2-3** | Control: FR-01 통과 시에만 2-1+2-2 연결(부작용 없음) | FR-01→02→03 | 통합: 유효 M 한 건에 좌표+쌍이 BR과 일치 |

**Scenario:** T-S-01의 전단(“유효 입력 준비”)을 자동으로 만족.  
**트랙 A:** 아직 `UI-T-05`는 Phase 3 이후 **완전 기대**와 묶는 것이 자연(아래 3-3~3-4).

---

### Phase 3 — T4: 마방진 판정 (FR-04)

| ID | 내용 | PRD | 완료 조건 |
|----|------|-----|----------|
| **3-1** | 합=34인 알려진 완성 4×4 → true | AC-04-1 | B: D-T-JDG(성공 예) **RGR** `MagicSquareJudge` |
| **3-2** | 행/열/주/부 **최소** 반례 false | AC-04-2,3 | B: 세분 단위 **RGR** |
| **3-3** | 0이 하나라도 있을 때: **(가) false (나) assert** **한 가지** + 단위 1건 | AC-04-4, §11 | 팀이 한 가지로 결정, PRD §11 **혼용 금지** **RGR** |
| **3-4** | (선택) NFR-04: 1건 50ms | NFR-04, T-S-05 | (선택) `timeout` 테스트 1 |

**Scenario:** T-S-01의 “완성 격자가 34” 부분.  
**ECB:** Entity성 판정 + 순수 함수 유지(도메인).

---

### Phase 4 — T5+T6: 이중 대입 + 경계 메시지 (핵심)

| ID | 내용 | PRD | 완료 조건 |
|----|------|-----|----------|
| **4-1** | 시도1 성공 → `[r1,c1,a,r2,c2,b]`, M 불변 | AC-05-2, NFR-03 | B: D-T-ASG **A:** `UI-T-05`, `UI-T-07` **RGR** T-S-01, Golden(§9.3) |
| **4-2** | 시도1 false, 시도2 true → `[r1,c1,b,r2,c2,a]` | AC-05-3 | B+A **RGR** T-S-02 (9.3 전용 M) |
| **4-3** | 둘 다 false: 도메인 `E_NO_VALID_ASSIGNMENT`, 경계 `E_DOMAIN_FAILURE`+고정 `message` | AC-05-4, BR-10, §5.1 | B: D-T-ASG(실패) A: `UI-T-06` (Includes 한 줄) **RGR** T-S-03 |
| **4-4** | FR-01 실패 시 **어느 경로에서도** FR-05(해찾기) **미호출** | AC-05-1 | Control/Facade 스파이/목 **A+B** **RGR** |
| **4-5** | 전 use case 통합: NFR-02, NFR-03(사본/깊은 동등) | NFR-02, 03 | 통합 테스트: 동일 M 반복, 원본 보존 |

**ECB:** `DualAssignmentResolver`(Control+Domain) + `Presenter`/`Facade`(Boundary).  
**RGR:** Phase 4가 끝날 때 **T-S-01~04**를 모두 통과(§9.1).

---

### Phase 5 — 품질·(선택) Property

| ID | 내용 | PRD | 완료 조건 |
|----|------|-----|----------|
| **5-1** | NFR-01 커버리지 게이트(팀 툴) | NFR-01 | T-S-05, CI |
| **5-2** | §9.4 Property(선택): 임의 합법 M, 성공 6-튜플 복원 시 FR-04 | §9.4 | (선택) Hypothesis 등, 실패 시 스킵 아닌 “미구현” 명시 |
| **5-3** | (선택) `print` 대신 `logging`·검증 캡 | NFR-05 | — |

---

## 5. Dual-Track 체크리스트 (리뷰/일일)

- [ ] **오늘** Boundary RED(`UI-T-*` 또는 `message` 계약) **1건 이상** 있음  
- [ ] **오늘** Domain RED(`D-T-*` 또는 FR-04/05) **1건 이상** 있음  
- [ ] REFACTOR 후 **전 스위트** 녹색, §9.2 “통과 테스트 삭제 없음”  
- [ ] 계약( `code`·`message`·6-튜플 ) 변경 시 **RED 선반영** + CHANGELOG(§9.2)  

---

## 6. 문서 동기 (Report는 언제 열까)

- **INV-D-01~10 전문**·문장: PRD **§12**는 참조만 → 상세는 **Report/02** (PRD에 명시).  
- **사용자 여정·Gherkin 출처**가 필요하면 **Report/04**만.  
- 기본 To-Do 완료 판정은 **항상 PRD의 AC·NFR**으로 확정.

---

*본 문서는 `docs/PRD_Magic_Square_4x4_TDD.md`의 요구·식별자를 옮겼을 뿐, 구현 본문은 포함하지 않는다.*
