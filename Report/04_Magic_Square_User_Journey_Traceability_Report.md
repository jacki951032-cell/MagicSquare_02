# Magic Square 사용자 여정 및 추적성 보고서

## 개요

- **문서 목적:** 4×4 Magic Square(빈칸 2개) 과제에 대해 **Epic → User Journey → User Story → Technical (Gherkin) → 시나리오 검증**까지 한 흐름으로 정리한 보고서이다.
- **대상 독자:** TDD·Clean Architecture·Invariant(불변조건) 사고 훈련에 참여하는 **소프트웨어 개발 학습자**와 리뷰·멘토.
- **작성일:** 2026-04-28 (필요 시 팀이 갱신)

---

## Level 1: Epic (비즈니스 목표)

### EPIC — Business Goal

**Epic**  
Invariant(불변조건) 기반 사고 훈련 시스템 구축

**목적**  
4×4 Magic Square 문제를 활용하여:

- Invariant 중심 설계 사고 훈련
- Dual-Track TDD 적용 훈련
- 입출력 계약 명확화 훈련
- 설계 → 테스트 → 구현 → 리팩터링 흐름 체화

**성공 기준**

| 항목 | 기준 |
|------|------|
| 도메인 | Domain logic **95% 이상** 테스트 커버리지 |
| 계약 | **입력 검증 100%** 계약 테스트 통과 |
| 품질 | **하드코딩 없음**, **매직 넘어 없음** (이름 있는 상수·도메인 값) |
| 추적성 | **Invariant → Test**로 추적 가능(테스트 이름, 주석, 문서, 트레이서빌리티 등 팀 합의 방식) |

---

## Level 2: User Journey (사용자 여정)

### 2.1 Persona

| 항목 | 내용 |
|------|------|
| 역할 | 소프트웨어 개발 학습자 |
| 맥락 | TDD 훈련 중, Clean Architecture 이해 중 |
| 지향 | “기능이 돌아간다”를 넘어, 계약·도메인·UI 분리와 테스트에 의한 보장을 습관화 |

### 2.2 Journey(단계형) — 例1

1. **문제 인식**  
   “마방진을 **구현한다**”가 아니라, **불변조건과 경계(입력/출력)**로 문제를 정의한다.

2. **계약 정의**  
   입력 스키마, 출력 스키마, **예외 정책**을 명시한다.

3. **Domain 분리**  
   `BlankFinder` · `MissingNumberFinder` · `MagicSquareValidator` · `Solver` 등 SRP에 맞게 경계를 나눈다.

4. **Dual-Track 진행**  
   **UI RED / Logic RED**를 병렬, **GREEN**은 최소 구현, **REFACTOR**로 통합·정리.

5. **회귀 보호**  
   엣지, 입력 오류, **조합 실패(해 없음 등)** 등을 테스트로 남긴다.

### 2.3 Journey(인지·감정형) — 例2: Magic Square (4×4)

| Stage | Action 요약 | Pain / Opportunity(요지) |
|--------|----------------|-------------------------|
| **1 Awareness** | 문제 확인 | **Pain:** 정의 모호 / **Opp.:** 입출력 계약 |
| **2 Entry** | 4×4, `0`=blank 구조 | **Pain:** 조건 누락 / **Opp.:** Contract-first |
| **3 Action** | 빈칸·누락·조합 | **Pain:** 조합 혼란 / **Opp.:** SRP·메서드 분리 |
| **4 Validation** | 행·열·대각 | **Pain:** 검증 중복 / **Opp.:** Invariant·Validator |
| **5 Outcome** | 결과 반환 | **Pain:** 포맷 어긋남 / **Opp.:** Output schema 고정 |

---

## Level 3: User Stories

### Story 1 — 입력 검증 (Boundary / Contract)

**As a** 학습자  
**I want to** 입력이 4×4·규칙(빈칸 수, 범위, 중복)에 맞는지 **경계에서** 검증되기를  
**So that** 잘못된 데이터가 Domain으로 전달되지 않는다.

**Acceptance Criteria**

- 4×4가 아니면 예외(또는 계약 위반).
- **빈칸 2개**가 아니면 예외.
- 0을 제외한 **중복 숫자**이면 예외.
- 1~16 **범위 위반**이면 예외.

### Story 2 — 빈칸 탐색 (BlankFinder)

**As a** 학습자  
**I want to** `0`인 셀의 **좌표**를 정확히 얻기를  
**So that** 이후 **조합 시도**가 가능하다.

**Acceptance Criteria**

- **row-major** 순서 유지.
- **정확히 2개** 좌표(또는 인덱스) 반환.

### Story 3 — 누락 숫자 탐색 (MissingNumberFinder)

**As a** 학습자  
**I want to** 1~16 중 **격자에 없는 2수**를 알기를  
**So that** 솔버의 **대입 후보**를 Domains 수준에서 확정한다.

**Acceptance Criteria**

- 1~16에서 **누락 2개** (전제: Story 1·입력 규칙과 일치).
- **오름차순** 반환.

### Story 4 — 마방진 판정 (MagicSquareValidator)

**As a** 학습자  
**I want to** **완성** 4×4가 마방진 조건을 만족하는지 판정하길  
**So that** Invariant를 **한곳**에서 검사·테스트로 고정할 수 있다.

**Acceptance Criteria**

- 모든 **행** 합 동일.
- 모든 **열** 합 동일.
- 두 **대각선** 합 동일 (공통 “마방진 합”과 정합).

### Story 5 — 두 조합 시도 (Solver)

**As a** 학습자  
**I want to** (작→큰) 순으로 **small → first blank** 등 **첫 시도** 후, 실패 시 **역순(Reverse)**을 시도하길  
**So that** 시도 **순서**가 스펙으로 남고 회귀에 넣을 수 있다.

**Acceptance Criteria**

- `small → first blank` (팀이 정의한 1차 전략).
- 1차 실패 시 `reverse` (2차 전략).
- **정답 배열 길이 6** (팀이 정의한 `(r1,c1,v1,r2,c2,v2)` 등 1-인덱스 스키마와 정합).

---

## Level 4: 구현 시나리오 — Technical (Gherkin)

> 아래는 BDD/자동화를 위한 **Gherkin 초안**이다. 구현·러너에 맞게 `Feature` / 키워드 언어는 조정 가능하다.

```gherkin
Feature: 4×4 마방진 완성
  Invariant 기반 로직을 검증하기 위해
  TDD를 연습하는 개발자로서
  일부 셀만 비어 있는 4×4 마방진(빈칸 2)을
  팀이 정의한 시도 순서(작은 수·첫 blank 등)에 따라 완성하고
  4×4 “정상” 마방진이 만족하는 공통 합(본 과제: 34)을 맞추고자 한다

  Background:
    Given 4×4 정수 행렬이 주어지고
    And 0은 빈칸을 뜻하며
    And 정확히 2개의 셀만 0이며
    And 0이 아닌 값은 1 이상 16 이하이며
    And 0을 제외한 값끼리는 중복이 없으며
    And 마방진 상수(행·열·대각의 공통 합)는 34이다

  Scenario: 작은 누락 수 → 큰 누락 수, 첫 blank에 작은 수 배치 시 정답
    Given 다음과 같은 격자가 row-major로 주어졌을 때:
      | 16 |  2 |  3 | 13 |
      |  5 | 11 | 10 |  8 |
      |  9 |  7 |  0 | 12 |
      |  4 | 14 | 15 |  0 |
    When 시스템이 0 셀 좌표를 찾고
    And 누락된 두 숫자를 찾은 뒤
    And **작은 수**를 **첫 번째 0(첫 blank)**, **큰 수**를 **두 번째 0(둘째 blank)**에 배치하면
        (그 결과가 마방진(합 34)이 되는 경우)
    Then 모든 행의 합은 34이어야 하고
    And 모든 열의 합은 34이어야 하며
    And 두 대각선의 합도 34이어야 하고
    And 정답은 **길이 6**의 배열(r1, c1, v1, r2, c2, v2)이며
    And (row, col)은 **1-인덱스**이어야 한다

  Scenario: 1차 배치(작→첫)가 틀리고 역순(큰→첫 등)이 맞는 경우
    # 동일 `Given`으로 1·2 시나리오가 둘 다 맞는지, 숫자로 먼저 확인하는 것이 좋다. 필요 시 Given만 변경.
    Given 이전 시나리오와 동일한 4×4 격자일 수 있다
    When (작, 큰)을 (첫 blank, 둘 blank)에 둔 결과가 34를 만족하지 않고
    And (큰, 작) **역배치**로 34를 만족하는 마방진이 되면
    Then **역배치**에 해당하는 길이 6 결과를 반환하고
    And 완성 격자는 마방진 상수 34를 만족해야 한다

  Scenario: 빈칸 개수가 2가 아닌 경우
    Given 4×4이지만 빈칸(0)이 1개만 있을 때(또는 3개 이상)
    When 유효성 검증을 수행하면
    Then Domain으로 넘기기 전 **오류**로 처리한다

  Scenario: 중복 숫자(0 제외)가 있는 경우
    Given 0이 아닌 셀에서 중복이 있는 4×4 격자일 때
    When 유효성 검증을 수행하면
    Then 오류가 발생해야 한다

  Scenario: 값이 1~16 범위를 벗어난 경우
    Given 0이 아닌 셀에 16을 초과하거나 0 미만인 값이 있을 때
    When 유효성 검증을 수행하면
    Then 오류가 발생해야 한다
```

---

## Level 5: 시나리오 검증 및 정리

### 5.1 4레벨 일관성

**Epic → Journey**

- [x] Epic 성공 기준이 Journey(계약·Domain 분리·Dual-Track·회귀)에 반영됨.
- [x] Journey 단계가 Epic 목표(Invariant·TDD·계약·흐름)에 **직접** 기여.
- [x] Pain(모호함·누락·조합 혼란·검증 중복·출력)이 Journey에 **명시**.

**Journey → Story**

- [x] Journey(인식/계약/빈칸·누락/판정/시도)와 Story 1~5 **대응** 가능.
- [x] Story가 **한 번에 검증할 수 있는** 단위.
- [x] Acceptance Criteria가 **측정 가능**(개수, 합, 순서, 배열 길이).

**Story → Technical**

- [x] AC를 Gherkin(Background+Scenario)으로 **지향** 가능.
- [x] Given-When-Then이 **행동·결과**에 가깝게 쓰임.
- [x] pytest/Behave 등 **자동화** 가능(고정 격자·Then 숫자 검증).

**참고:** `역배치` 시나리오는 **퍼즐**마다 1·2가 동시에 성립하는지 **숫자로 검산**·필요 시 `Given` 교체.

### 5.2 Edge case 커버리지(본 프로젝트에 맞춤)

| 구분 | 체크 |
|------|------|
| **정상** | [x] Happy path(34·길이 6·1-인덱스) |
| **정상(대안)** | [ ] 역배치 `Given`이 **실제**로 1차 실패·2차 성립하는지 **문서/테스트**로 입증 |
| **예외** | [x] 4×4·빈칸 2·중복·1~16(0 제외) (Story 1) |
| **경계** | [x] 최·최(1,16), blank 정확히 2, row-major |
| **(비적용)** | “네트워크·권한·QR” 등 **본 TDD/로컬** 범위 **외** 항목은 N/A. |

### 5.3 사용자 중심성(학습/훈련 맥락)

- [x] 例2 Stage에 **Action / Pain / Emotion** 등 정의(선택: 리뷰에 활용).
- [ ] **페어 또는 멘토 1인**— Story ↔ Gherkin **매핑** 리뷰(권장).
- [ ] 리뷰 이후: **“역배치”**·**길이 6** 스키마를 Background 한 줄에 **고정**.

### 5.4 구현 가능성(기술·도메인)

- [x] **순수 Python + pytest** (또는 팀 합의 스택) + ECB 경계.
- [x] `Validator` / Finder / `Solver`가 **이름**으로 식별 가능.
- [x] Entity(격자, 좌표, 6-튜플 등) **문서** 또는 **코드**에 존재.
- [ ] REST가 있다면 요청/응답 JSON 1면(선택).

---

## 부록: 문서 간 정렬(참고)

| 문서(예) | 이 보고서와의 관계 |
|----------|--------------------|
| `01_Magic_Square_Problem_Definition_Report` | “진짜 문제=제약+계약+검증”— Epic·Journey에 위임 |
| `02_Magic_Square_Dual_Track_TDD_Clean_Architecture_Report` | Dual-Track·ECB— Story 1·3·4·5와 `control`·`entity` |
| `03_Magic_Square_CursorRules_Report` | TDD/금지 규칙·커버리지— Level 1 성공 기준·Level 5 구현 점검 |

---

*본 보고서는 사용자 여정·User Story·Gherkin·검증 체크리스트를 **한 궤적**으로 읽을 수 있게 합쳤다. 변경 시 `04_...` 버전만 갱신하거나, “변경일”에 상단 `작성일`에 반영하면 된다.*
