# PRD: Magic Square (4×4) — TDD 연습용

| 항목 | 값 |
|------|-----|
| 문서 유형 | Product Requirements Document (PRD) |
| 제품/프로젝트명 | Magic Square (4×4), 빈칸 2개 |
| 버전 | 2.1 (13절: Dual-Track 정교화 + §7.1 MLOps 정렬) |
| 갱신일 | 2026-04-28 |
| 근거 | `Report/01`~`04`, `Report/05` 보고서 형식 사본(동기 권장) |

---

# 1. Executive Summary

이 프로젝트는 4×4 격자에 빈칸(0) 2개와 1~16의 일부가 주어질 때, **고정된 입·출력 계약**과 **이중 시도(정배치·역배치) 규칙**에 따라 `int[6]` 해를 반환하거나, **정의된 오류 코드**로 실패를 보고하는 **순수 도메인** 중심 연습 과제다. 훈련이 지향하는 핵심 역량은 (1) **불변조건(Invariant)**을 한 곳에 모아 판정·검증하는 사고, (2) **경계(Boundary)와 도메인**을 나눈 **입·출력 계약**의 명시·테스트, (3) **Dual-Track TDD**로 RED–GREEN–REFACTOR를 경계/로직에 **병렬**로 적용하는 점이다. 알고리즘의 난이도·최적화는 목표에 포함되지 않는다.

## 1.1 Dual-Track + MLOps (이 문서에서의 뜻)

- **UI 트랙** = **UX Contract / Boundary** 트랙이다. 웹·데스크톱 **화면**이 없을 수 있으며(§4.2), 그때는 **공개 API·`code`·`message`·성공 DTO**가 “**보이는(visible)** / **포함(includes)**” **결과**로 검증된다(§5.1).
- **로직 트랙** = **Logic Rule / Domain** 트랙이다. BR·FR-02~05, FR-04 판정·이중 대입·`Allow`/`Reject`/`Return` 등 **의존성 없는 규칙**으로 RED를 만든다(§5.1, §6).
- **MLOps(비-ML)** = 본 과제는 **학습/추론 모델**이 없다. 대신 **스펙(계약) 버전**·**Golden 픽스처(테스트 격자)**·**CI 품질 게이트**·**결정론·회귀 정책**을 한 세트로 관리하는 **운영 품질** 층으로 둔다(§7.1, §9.2, §9.3).

---

# 2. Problem Statement (문제 정의)

**핵심은 “마방진을 짜맞춘다”가 아니라**, 주어진 제약(4×4, 0은 정확히 2, 0 제외 1~16·중복 없음, row-major로 정의한 첫/둘째 빈칸)을 만족하는 상태에서 **불변조건(행·열·대각 합 34)**을 **검증 가능한 절차**로 완성·판정하는 것이다. **입·출력 계약이 핵심**인 이유: TDD·리팩터링의 통과/실패 기준이 “구현 상세”가 아니라 **스펙**에 있어야 하고, 동일 입력에 **동일한 성공 배열** 또는 **동일한 오류 코드(및 경계에서의 동일 `message`)**가 나와야 하기 때문이다. 계약이 흔들리면 불변조건 테스트와 경계 테스트가 모호해진다.

---

# 3. Target Users

| 대상 | 관점 | 목적·환경 |
|------|------|-----------|
| TDD 학습자 | Red–Green–Refactor, Invariant, 계약 우선 | **콘솔**에서 `pytest`(또는 팀이 택한 동일 러너)로 테스트 실행, 로컬·CI에서 동일 |
| 리뷰어·멘토 | PR·User Story·AC·테스트 대응 | PRD·FR·BR·TC가 1:1로 추적 가능한지 리뷰 |

---

# 4. Scope

## 4.1 In-Scope

- **빈칸 좌표**: row-major **첫 0** = 첫 빈칸, **둘째 0** = 둘째 빈칸(1-index 출력).
- **누락 숫자**: 1~16 중 격자에 없는 2수 \((a,b), a&lt;b\).
- **마방진 판정**: 0이 없는 완성 4×4에 대해 행·열·주·부 대각 합이 **모두 34**.
- **해(solution)**: **시도1**(작→첫 빈칸, 큰→둘) 통과 시 단락; 아니면 **시도2**(큰→첫, 작→둘)만 검사; 둘 다 실패 시 도메인 `E_NO_VALID_ASSIGNMENT`.
- **입력 검증(경계)**: 4×4·0 개수 2·값 범위·0 제외 중복 — 위반 시 FR-05(해 찾기) **미호출**.

## 4.2 Out-of-Scope

- **UI 화면(웹/데스크톱) 앱**을 “제품”으로 **완성**하는 것 — **기본 범위**에서는 **Out**. 본 PRD의 “**UI**”(§8)는 **UX Contract = Boundary**를 뜻하며, `pytest`로 `code`·`message`·6-튜플을 검증해도 **Dual-Track**을 만족한다(§5.1). React 등 **시각 UI**는 **선택**; 도입 시 동일 `UI-T-*`·문구를 **화면 가시성**으로 옮기면 된다.
- **DB** 저장/조회, 파일 영속(확장 시 별도 어댑터·별도 PRD).
- **N×N 일반화**: 본 PRD **기본 범위는 4×4·상수 34**만. 일반화는 “확장 항목”으로만 언급 가능, 본 AC에 넣지 않는다.
- **마방진 “생성”** 알고리즘(임의 n에 대해 마방진을 만드는 전체 생성 문제); 본 과제는 **2칸 대입 + 판정**으로 범위가 한정된다.

---

# 5. Functional Requirements (기능 요구사항)

**공통 기호**: 입력 행렬 `M`은 `int[4][4]`(또는 언어 동치). **Magic constant** = 34.

---

## FR-01 입력 검증 (Boundary)

- **Feature ID**: FR-01  
- **설명**: `M`이 구조·빈칸 수·값·중복 규칙을 만족하는지 **도메인 해 찾기 전**에 검증한다.  
- **입력**: `M`.  
- **처리 규칙(불변조건)**: `M`이 정확히 4행이고 각 행 길이 4(가변 행·빈 행 없음), 모든 셀 정수, 0의 개수=2, 각 값 ∈ {0}∪[1,16], 0이 아닌 값끼리 중복 없음.  
- **출력(성공)**: 검증 통과(도메인에 넘길 수 있는 “유효 격자” 내부 표현; 구현은 PRD 밖).  
- **AC(승인 기준, 검증 가능)**:
  - AC-01-1: 4×4가 아니면 `E_INPUT_SHAPE`이고 FR-05가 호출되지 않는다(테스트에서 스파이/목으로 검증).  
  - AC-01-2: 0이 2개가 아니면 `E_ZERO_COUNT`이고 FR-05가 호출되지 않는다.  
  - AC-01-3: 0·1~16 밖 값이 있으면 `E_VALUE_RANGE`이고 FR-05가 호출되지 않는다.  
  - AC-01-4: 0 제외 중복이 있으면 `E_DUPLICATE_NONZERO`이고 FR-05가 호출되지 않는다.  
- **오류/예외 정책**: `code`는 `E_INPUT_SHAPE` | `E_ZERO_COUNT` | `E_VALUE_RANGE` | `E_DUPLICATE_NONZERO` 중 정확히 하나; `message`는 아래 표와 **문자 그대로** 일치(경계 Contract 테스트로 검증).

**경계 `message` 고정(Contract)**:

| `code` | `message` |
|--------|-----------|
| `E_INPUT_SHAPE` | `matrix must be a 4x4 integer array.` |
| `E_ZERO_COUNT` | `matrix must contain exactly two zeros.` |
| `E_VALUE_RANGE` | `matrix values must be 0 or between 1 and 16.` |
| `E_DUPLICATE_NONZERO` | `non-zero values must be unique.` |

---

## FR-02 빈칸 탐색

- **Feature ID**: FR-02  
- **설명**: 유효 입력에서 row-major로 **첫 0**과 **둘째 0**의 1-index 좌표를 구한다.  
- **입력**: FR-01을 통과한 `M`.  
- **처리 규칙(불변조건)**: 스캔 순서 = 행 1→4, 열 1→4(1-index). 첫으로 만나는 0 = 첫 빈칸, 그 다음 0 = 둘째 빈칸.  
- **출력**: `((r1,c1), (r2,c2))`, 각 \(r,c \in \{1,2,3,4\}\).  
- **AC**:
  - AC-02-1: 0이 정확히 2개일 때, 산출 좌표에 각각 0이 위치한다.  
  - AC-02-2: 첫 좌표가 row-major에서 먼저다(행 작은 쪽 우선, 같으면 열 작은 쪽 우선).  
- **오류/예외 정책**: FR-01 통과 입력에서는 FR-02가 실패하지 않는다(0=2는 FR-01에서 보장).

---

## FR-03 누락 숫자 탐색

- **Feature ID**: FR-03  
- **설명**: 1~16 중 `M`에 나타나지 않은 **정확히 2개**의 수를 구한다.  
- **입력**: FR-01을 통과한 `M`.  
- **처리 규칙(불변조건)**: 0을 제외한 14칸이 1~16에서 서로 다르므로, 누락 집합 크기=2.  
- **출력**: `(a, b)` where \(a&lt;b\), `a`·`b` ∈ [1,16].  
- **AC**:
  - AC-03-1: 반환 쌍 \((a,b)\)에 대해 `M`의 0이 아닌 셀에 `a`·`b`가 모두 없다.  
  - AC-03-2: `a` &lt; `b`이다.  
- **오류/예외 정책**: FR-01에서 보장되므로 별도 실패 케이스는 본 PRD에 정의하지 않는다.

---

## FR-04 마방진 판정

- **Feature ID**: FR-04  
- **설명**: **0이 없는** 4×4 정수 격자가 마방진(모든 행·열·주·부 대각 합=34)인지 판정한다.  
- **입력**: 4×4, 모든 셀 1~16(완성 격자).  
- **처리 규칙(불변조건)**: 4행·4열·주대각(1,1)~(4,4)·부대각(1,4)~(4,1) 각 **합=34**이면 true, 아니면 false(어느 규칙이 깨졌는지는 테스트/구현이 단위로 분리 가능).  
- **출력**: boolean(또는 동치 판정 결과).  
- **AC**:
  - AC-04-1: 알려진 합=34인 완성 4×4(문서/테스트에 박은 예)는 true.  
  - AC-04-2: 임의 한 행 합을 34가 아닌 값이 되게 바꾼 격자는 false.  
  - AC-04-3: 열·주대각·부대각만 깨뜨린 **최소** 반례 각각 false.  
  - AC-04-4: 입력에 **0이 하나라도** 있으면(완성 격자가 아님) 팀이 **(가)** `false`를 반환하거나 **(나)** 사전조건 **위반(예: assert)으로 중단**하는 **한 가지**로 통일한다. 선택에 맞는 **단위 테스트 1건**이 스위트에 있어야 하며(§11절), 혼용하지 않는다.  
- **오류/예외 정책**: “완성 격자” **사전**조건(0 없음) — 위 AC-04-4, §11.

---

## FR-05 해 찾기 (solution): 두 조합 시도 및 반환

- **Feature ID**: FR-05  
- **설명**: 누락 쌍 \((a,b)\)와 첫/둘 빈칸에 대해 **시도1**을 적용·판정하고, 실패 시 **시도2**를 적용·판정한다.  
- **입력**: FR-01 통과 `M`.  
- **처리 규칙(불변조건)**:
  - **시도1**: 첫 0에 `a`, 둘째 0에 `b` 대입. FR-04로 완성 격자 판정. true이면 **시도2 생략**하고 `int[6] = [r1,c1,a,r2,c2,b]`.  
  - **시도2** (시도1이 false일 때만): 첫 0에 `b`, 둘째 0에 `a` 대입. true이면 `int[6] = [r1,c1,b,r2,c2,a]`.  
  - 둘 다 false: 도메인 `E_NO_VALID_ASSIGNMENT`, 경계에서는 `E_DOMAIN_FAILURE` + `message = failed to resolve a valid magic-square assignment.`
- **출력(성공)**: `int[6]`, 좌표 1-index, `n1`·`n2`는 누락 2수이며 위 순서·대입과 일치.  
- **AC**:
  - AC-05-1: FR-01 실패 시 FR-05는 성공 `int[6]`을 반환하지 않고, `E_INPUT_SHAPE`·`E_ZERO_COUNT`·`E_VALUE_RANGE`·`E_DUPLICATE_NONZERO` 중 **정확히 하나**만 해당한다(FR-01의 `code`·`message` 표).  
  - AC-05-2: FR-01 성공·시도1 true인 입력에 대해, 출력 6-튜플이 `[r1,c1,a,r2,c2,b]`(row-major에서 첫 셀에 `a` 등)이고, 완성 격자가 FR-04 true.  
  - AC-05-3: FR-01 성공·시도1 false·시도2 true인 입력에 대해, 출력이 `[r1,c1,b,r2,c2,a]`이고 완성 격자가 FR-04 true.  
  - AC-05-4: FR-01 성공·시도1·2 모두 false이면 `E_NO_VALID_ASSIGNMENT` (경계: `E_DOMAIN_FAILURE` + 위 `message`).  
- **부작용**: **입력 `M`은 읽기 전용**; 해를 만들 때는 **사본**에 대입하거나, 호출자가 `M`이 변하지 않음을 자동화 테스트로 검증한다(NFR-03).  
- **오류/예외 정책**: 입력 오류 4종 + `E_NO_VALID_ASSIGNMENT` / `E_DOMAIN_FAILURE`; `message`는 결정론(동일 이유·동일 문자열).

---

## 5.1 Dual-Track vocabulary & Domain vs Boundary errors

팀·테스트·이슈/PR에서 **같은 말**로 말하도록, 슬라이드 수준 **동사**로만 **결정(Decision)**이 있는 항목을 TDD에 태운다(할 일 “정리”만의 작업은 테스트로 승격하지 않음).

**① UX Contract (Track A, Boundary — 화면이 있으면 그걸, 없으면 DTO/문자열이 그 역할)**  

| 권장 동사(영문) | 의미 | 본 PRD에 대응하는 예 |
|-----------------|------|----------------------|
| Visible / Not visible | 메시지·필드가 노출됨/아님 | `E_INPUT_SHAPE`일 때 `message`가 **정확히** FR-01 표와 일치(보임/다른 문구 **미포함**). |
| Includes / Does not include | 본문에 부분문자열 포함 | `E_DOMAIN_FAILURE` + `message` **한 줄** = `failed to resolve...` **includes** 검사. |
| Possible / Impossible (경로) | 해를 찾는 쪽 호출 가능 여부 | FR-01 실패 시 `DualAssignment` **impossible** — FR-05 미호출(스파이). |
| Enabled / Disabled | (시각 UI 시) 제출/재시도 | 선택 UI 확장 시. |

**② Logic Rule (Track B, Domain — 외부 I/O 없음)**  

| 권장 동사(영문) | 의미 | 본 PRD에 대응하는 예 |
|-----------------|------|----------------------|
| Reject / Allow | 합=34·구조·대입 | `MagicSquareJudge` true/false, 입력 검사 실패. |
| Return / Block | 해 또는 실패 | 성공 `int[6]`, `E_NO_VALID_ASSIGNMENT` 내부. |
| Calculate / Maintain | 좌표·(a,b)·34 | FR-02~04, M 사본 `Maintain`(원본 NFR-03). |

**③ 도메인 `code` vs 경계(사용자/응답) 표현**  

| 내부(도메인) | 경계(멀리 보이는 쪽) | 메모 |
|-------------|----------------------|------|
| `E_NO_VALID_ASSIGNMENT` (시도1·2 모두 실패) | `E_DOMAIN_FAILURE` + `message` = `failed to resolve a valid magic-square assignment.` (FR-05) | **Presenter/Boundary**가 매핑; `UI-T-06`. |
| FR-01 실패(4종) | 동일 `code`+표의 `message` (중간 `E_NO_VALID_…` 변환 **금지**) | AC-05-1, `UI-T-01`~`04`. |

---

# 6. Business Rules (도메인 규칙)

아래는 **성공/실패를 판단하는 동안 항상 참**이어야 한다는 절(유효 입력·정의된 대입/출력에 한함).

| ID | 규칙 |
|----|------|
| BR-01 | `M`의 행 수=4, 각 행의 열 수=4(총 16칸). |
| BR-02 | 0이 아닌 셀의 값 ∈ [1,16]이고, 0이 아닌 셀끼리 값이 중복되지 않는다. |
| BR-03 | 0의 개수=2이다. |
| BR-04 | 1-index에서 첫 0 = row-major 스캔 시 가장 먼저 만나는 0, 둘째 0 = 그 다음 0(유일). |
| BR-05 | 누락 숫자는 {1,…,16}에서 0이 아닌 14칸에 등장한 수의 여집합(크기 2)이다. |
| BR-06 | 누락 쌍 \((a,b)\)는 항상 \(a&lt;b\)로 정해진다(시도1에서 작은 수를 첫 빈칸에). |
| BR-07 | 완성 4×4가 마방진이면, 모든 행 합=모든 열 합=주 대각 합=부 대각 합=**34**이다. |
| BR-08 | 성공 출력 `int[6]`의 \(r_1,c_1,r_2,c_2\)는 각각 1~4, 좌표는 (BR-04)의 첫/둘 0과 같다. |
| BR-09 | 성공 출력의 \(n_1,n_2\)는 (BR-05)의 \((a,b)\)이며, 시도1/시도2 중 성립한 대입(FR-05)과 **동일 순서**이어야 한다. |
| BR-10 | FR-01 실패가 아닌 **입력**에도 시도1·2가 모두 false이면, 성공 `int[6]`이 존재하지 **않고** `E_NO_VALID_ASSIGNMENT`만 적법하다. |

---

# 7. Non-Functional Requirements

- **NFR-01(커버리지)**: Domain(Logic) 코드 분기/라인 **≥95%**; Boundary(Validation) **≥85%** (팀 툴에서 `coverage`로 측정, CI에서 게이트 가능).  
- **NFR-02(결정론)**: 동일 입력(동일 `M` 바이트/값 동치) → 동일 성공 배열 **또는** 동일 `code`(+경계 `message`)이다.  
- **NFR-03(부작용)**: `M` **원본을 직접 변형하지 않는다**; 단위/통합 테스트로 “호출 전후 `M` 동일(깊은 동등)”을 검증할 수 있다(프로젝트가 `copy`를 쓰면 식별·동등 기준을 팀이 한 가지로 고정).  
- **NFR-04(성능, 선택)**: 4×4 1건만의 해 탐지·검증은 **50ms** 이내(동일 머신, 테스트에서 상한 `timeout`로 측정); 초과 시 성능 이슈로 기록(기본 납은 통과).  
- **NFR-05(관찰가능성)**: 구현이 `print`로 표준출력에 의존하지 않는다(학습 룰: `logging` 또는 검증 캡).

## 7.1 MLOps로 읽는 운영 품질 (비-ML, 본 PRD의 범위)

본 제품에 **학습/추론 모델**은 없다. 그래도 아래는 **MLOps와 같은 자리**에서 “**깨지지 않게**” 관리한다.

- **스펙·스키마(artifact)**: `code`·`message`·6-튜플 형식은 **API/데이터 스키마**에 준한 **버전 대상**이다(§9.2, CHANGELOG).
- **데이터(테스트)**: 9.3 **Golden 격자**·T-S-02/03 **전용 M**·Report/04 **출처** = **검산된 평가 세트**; 변경은 **PR + 검산 기록** 권장.
- **CI 파이프라인**: `pytest` 전부 + (선택) 커버리지 게이트 NFR-01, (선택) 50ms T-S-05. **PR마다** 동일 러너(§3).
- **재현성**: NFR-02(결정론); (선택) `uv.lock` / `poetry.lock` / `pip-tools` 등 **의존성 락**을 팀 표준에 두면 “동일 머신/이미지” **재빌드**가 쉬움(본 PRD는 툴을 **강제하지 않음**).
- **감시·알람(경량)**: 통과하던 테스트가 **빨간색**이면 회귀; 9.2 “삭제 금지”와 연결(프로덕 **모델 모니터링**은 범위 밖).

---

# 8. Dual-Track TDD Strategy

**용어(§1.1, §5.1)**: “**UI**” = **UX Contract / Boundary**; **“Logic”** = **Domain**.

## 8.0 Track A vs B (한 줄씩)

| Track | 뭐로 RED? | 뭐로 GREEN/REF? |
|-------|------------|------------------|
| **A (Boundary / UX Contract)** | 설계/계약: `message`·`code`·6-튜플 DTO(또는 **화면**이 있으면 `queryByText` 류) | `UI-T-*`, **§5.1** 동사 **Includes/Visible/Impossible** |
| **B (Domain / Logic Rule)** | 규칙: 34, 좌표, (a,b), 이중 대입 | `D-T-JDG`·`D-T-ASG`·BR, **Allow/Reject/Return** |

## 8.1 Track A — Boundary (UX Contract / “UI”) TDD

- **UI가 “픽셀”일 필요는 없다**(§4.2). `pytest`가 **최종 응답**의 `code`·`message`·6-튜플을 assert하면 **Track A**다. React 등을 쓰면 **동일** AC를 **Visible / not visible**로 번역(§5.1).
- **Contract-first** 테스트 항목(예시 ID): `UI-T-01`~`UI-T-04` = FR-01·AC와 1:1(형태·0개수·범위·중복), `UI-T-05` = FR-01 통과+도메인 고정 `int[6]` 성공, `UI-T-06` = `E_NO_VALID_ASSIGNMENT`→`E_DOMAIN_FAILURE` 매핑(§5.1 표), `UI-T-07` = 1-index 좌표.  
- **실패 정책**: 위 FR-01 표의 `code`·`message`; `E_DOMAIN_FAILURE`는 `failed to resolve a valid magic-square assignment.` **한 줄**이어야 한다.

## 8.2 Track B — Domain (Logic) TDD

- **단위(메서드/책임) 예시 ID**: `D-T-VAL-*`(입력), `D-T-JDG-*`(FR-04), `D-T-ASG-*`(FR-05).  
- **불변조건 매핑**: `INV-D-01`~`10`(문서/Report/02) ↔ BR-01~10 ↔ 단위 실패/성공 케이스(행·열·대각 각각 34, 실패 반례).

## 8.3 병렬 진행 규칙

- **Boundary(UX) RED** & **Domain(Logic) RED** (동시에 실패하는 테스트 1개씩) → **Boundary GREEN** & **Domain GREEN** (각각 최소 통과) → **REFACTOR** (전체 스위트, 계약·경계 위반 없음, §7.1 CI).  
- **도메인 전부를 먼저 구현한 뒤 경계만 뒤에 붙이는** 순서는 **금지**; 매 스프린트/과제 루프마다 **양 트랙**에 테스트가 **존재**한다(한쪽 0이면 REFACTOR 단계에서 **운영/품질 누락**과 동일(§7.1)).

---

# 9. Test Plan (QA)

## 9.1 시나리오(검증 가능)

| ID | 시나리오 | 기대 |
|----|----------|------|
| T-S-01 | **정상(시도1)**: 임의 유효 `M`에서 시도1이 마방진 | `int[6] = [r1,c1,a,r2,c2,b]`, FR-04(완성) true |
| T-S-02 | **정상(시도2)**: 시도1 false, 시도2 true | `int[6] = [r1,c1,b,r2,c2,a]`, FR-04 true |
| T-S-03 | **도메인 실패**: 둘 다 false | `E_NO_VALID_ASSIGNMENT` / `E_DOMAIN_FAILURE` |
| T-S-04 | **입력 오류** 4종 각각 | 해당 `E_*` **단일**, FR-05 미호출 |
| T-S-05 | **콘솔/CI** | `pytest` 전부 통과, (선택) 50ms 상한 1건만 측정 |

## 9.2 회귀 정책

- 통과한 테스트 **삭제 금지**; 계약 변경은 **RED 선반영** 후 GREEN.  
- `code`·`message`·6-튜플 **형식** 변경 = **계약 변경** (버전/CHANGELOG).

## 9.3 테스트 데이터(고정 4×4, Report/04와 동일 출처)

**예 A (시도1·Gherkin):**

| 16 | 2  | 3  | 13 |
| 5  | 11 | 10 | 8  |
| 9  | 7  | 0  | 12 |
| 4  | 14 | 15 | 0  |

- `a`,`b`는 1~16·누락 집합으로 **계산**해 기대 6-튜플·완성 격자=34에 맞는지 **자동 검산**.  
- **T-S-02**·**T-S-03** 전용 `M`은 “시도1 실패/시도2 성공”·“둘 다 실패”를 **수로 검산한 뒤** 저장(동일 `Given`이 두 케이스에 동시 성립하는지 **문서상** 확인).

## 9.4 Property / Invariant 머지

- 임의 **FR-01 합법** `M`에 대해(생성기 또는 셋에서 샘플): (1) 누락 집합 크기=2, (2) 좌표가 BR-04, (3) FR-04에 넣는 완성 격자는 0이 없다. (선택) **Hypothesis** 등.  
- 성공 `int[6]`에 대해: 인덱스/값으로 복원한 `M` 사본+대입 = FR-04 true.

---

# 10. Architecture Overview (High-Level)

| 레이어 | 책임 | 예시 논리 컴포넌트명(구현 아님) |
|--------|------|----------------------------------|
| **Boundary** | 외부 입력 스키마 검사, `code`/`message`, 성공 DTO | Validator Facade, Presenter |
| **Domain** | FR-02~05, `E_NO_VALID_ASSIGNMENT` | `BlankCellLocator`, `MissingNumberFinder`, `MagicSquareJudge`, `DualAssignmentResolver` |

- **SRP**: 판정(FR-04)과 대입·시퀀스(FR-05)를 **다른** 테스트/모듈로 쪼갤 수 있어야 한다.  
- **OCP**: N×N, 저장소는 **새 어댑터**; 도메인 **인터페이스** 뒤에 확장(본 PRD 4.2 범위 밖).  
- **의존**: Boundary → (Application 선택) → Domain. **Domain은** Boundary/DB/HTTP **모름** (도메인 단위테스트 **외곽 0**).

---

# 11. Risks & Ambiguities

| 결정 항목 | 고정(본 PRD) |
|----------|----------------|
| 두 시도 모두 실패 | `E_NO_VALID_ASSIGNMENT` (경계 `E_DOMAIN_FAILURE`+고정 `message`); 6-원 **부재** |
| 1-index vs 0-index | **출력 1-index**; 스캔 = row-major(행→열) |
| 입력 `M` 변경 | NFR-03: **읽기 전용**; 테스트로 동일성 |
| 0이 있는 `M`에 FR-04? | **AC-04-4**: `false` **또는** `assert` 중 **한 가지**; 혼용 금지, **단위 테스트 1건** |

| 자주 흡수하는 실수 | 완화 |
|--------------------|------|
| “큰/작” 순서 **출력 6-튜플**과 혼동 | **시도1/2** 정의를 AC와 나란히 **복붙**해 쓴다 |
| Gherkin 격자만 보고 1·2 동시 기대 | `Given` **검산** (Report/04) |
| `message` **마침표/대소** 오타 | **문자 그대로** AC |

---

# 12. Traceability Matrix (필수)

**`INV-D-01`~`10` 전문**: 본 PRD **본문**에는 `INV-D-06`~`08` 등 **참조만** 둔다(§6~§12). **정의·문장 전체**는 `Report/02` 등 **동기 문서**와 **일치**시킬 것.

| Concept/Invariant | Business Rule | Feature (FR) | Acceptance Criteria | Test Case | Component(논리) |
|-------------------|---------------|--------------|---------------------|-----------|-----------------|
| INV-D-06~08 (입력 구조) | BR-01~04 | FR-01 | AC-01-1~4 | D-T-VAL, UI-T-01~04 | `InputMatrixValidator` |
| INV-D-06+첫/둘 0 (순서) | BR-04 | FR-02 | AC-02-1,2 | 단위(고정 M) | `BlankCellLocator` |
| 누락 집합 | BR-05,06 | FR-03 | AC-03-1,2 | 단위 | `MissingNumberFinder` |
| INV-D-01~05 (34) | BR-07 | FR-04 | AC-04-1~4 | D-T-JDG-01~05, AC-04-4 | `MagicSquareJudge` |
| INV-D-09~10 (6-튜플) | BR-08,09 | FR-05 | AC-05-1~4 | D-T-ASG, UI-T-05~07, INT | `DualAssignmentResolver` |
| 해 없음 (일관) | BR-10 | FR-05 | AC-05-4 | D-T-ASG-03, INT-T-05, §5.1 | `DualAssignmentResolver`+ 경계 |
| `message` / 도메인→경계 | — | FR-01, FR-05, §5.1 | 5.1, 5절, 11절 | UI-T / Contract | Boundary Presenter |
| CI·회귀·Golden 데이터 | NFR-01,02, §7.1 | §9.2, §9.3 | 9.2, T-S-05 | CI job, 9.3 | (인프라/레포) |

---

# 13. Document change log (문서)

| 버전 | 날짜 | 요약 |
|------|------|------|
| 2.0 | 2026-04-28 | 12절 PRD(초기). |
| 2.1 | 2026-04-28 | **§1.1** Dual-Track+MLOps 정의, **§4.2** UI=Boundary 정리, **§5.1** UX/Logic 어휘·도메인/경계 오류 표, **AC-04-4** FR-04(0 있음) 통일, **§7.1** 비-ML MLOps(스키마·CI·락·데이터), **§8.0~8.1** Boundary(UX) 명시, **§12** `INV` 출처·TR 행 보강. |

---

*구현 소스/함수 본문은 이 PRD에 포함하지 않는다.*
