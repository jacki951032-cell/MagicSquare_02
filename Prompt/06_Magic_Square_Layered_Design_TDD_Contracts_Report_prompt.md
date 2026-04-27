# Magic square project design and testing
_Exported on 4/28/2026 at 08:47:06 GMT+9 from Cursor (3.2.11)_

---

**User**


프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련
제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만
- 입력/출력은 명확히 고정

입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지
출력 계약:
- int[6]
- 좌표는 1-index
- 반환 형식: [r1,c1,n1,r2,c2,n2]
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

------------------------------------------------------------
출력 형식 (반드시 이 구조로)
------------------------------------------------------------

# 1) Logic Layer (Domain Layer) 설계
## 1.1 도메인 개념
- Entities / Value Objects / Domain Services 목록과 책임(SRP)
## 1.2 도메인 불변조건(Invariants)
- 행/열/대각선 합 일치, Magic Constant 등
## 1.3 핵심 유스케이스(도메인 관점)
- 빈칸 찾기, 누락 숫자 찾기, 마방진 판정, 두 조합 시도
## 1.4 Domain API(내부 계약)
- 메서드 시그니처 수준(코드 X) + 입력/출력/실패조건
## 1.5 Domain 단위 테스트 설계(RED 우선)
- 테스트 케이스 목록(정상/비정상/엣지)
- 각 테스트가 보호하는 invariant 명시

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)
## 2.1 사용자/호출자 관점 시나리오
- “행렬 입력 → 검증 → 결과 출력” 흐름
## 2.2 UI 계약(외부 계약)
- Input schema / Output schema / Error schema
## 2.3 UI 레벨 테스트(Contract-first, RED 우선)
- 잘못된 크기, 빈칸 개수 오류, 값 범위 오류, 중복 오류, 반환 포맷 검증
- Domain은 Mock으로 가정
## 2.4 UX/출력 규칙
- 에러 메시지 표준(정확한 문구 규칙까지)

# 3) Data Layer 설계 (Data Layer)
## 3.1 목적 정의
- “저장/로드”의 필요성과 범위(학습용)
## 3.2 인터페이스 계약
- 예: MatrixRepository.save/load (메서드 수준, 코드 X)
- 저장 대상: 입력 행렬, 실행 결과(선택)
## 3.3 구현 옵션 비교(메모리/파일)
- 옵션 A: InMemory / 옵션 B: File(JSON/CSV)
- 추천안 1개 선택 + 이유
## 3.4 Data 레이어 테스트
- 저장/로드 정합성, 예외(파일 없음/형식 오류), 불변조건(4x4 유지)

# 4) Integration & Verification (통합 및 검증)
## 4.1 통합 경로 정의
- UI → Application(선택) → Domain → Data 흐름(의존성 방향 포함)
## 4.2 통합 테스트 시나리오
- 정상 시나리오 2개 이상
- 실패 시나리오 3개 이상(입력 오류, 도메인 실패, 데이터 실패)
## 4.3 회귀 보호 규칙
- 기존 테스트 유지 정책
- 변경 금지 규칙(계약/출력 포맷)
## 4.4 커버리지 목표
- Domain Logic 95%+
- UI Boundary 85%+
- Data 80%+
## 4.5 Traceability Matrix (필수)
- Concept(Invariant) → Rule → Use Case → Contract → Test → Component

------------------------------------------------------------
추가 조건
------------------------------------------------------------
- 모호한 표현 금지(“적절히/충분히” 금지)
- 모든 규칙은 검증 가능해야 함(테스트로 확인 가능)
- 구현 코드 작성 금지
- 표/체크리스트를 적극 사용

---

**Cursor**

구현 코드 없이, 요청하신 섹션·제약(입·출력 계약, TDD, 레이어, 표/트레이서빌리티)에 맞춰 정리합니다.

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

| 구분 | 이름 | 단일 책임(SRP) |
|------|------|----------------|
| **Value Object** | `CellPosition` (또는 좌표 VO) | 행·열(1~4) 유효성, 동등성 |
| **Value Object** | `PuzzleState` (또는 `PartialGrid`) | 4×4 정수 그리드 스냅샷(0=빈칸)과 읽기 전용 조회 |
| **Entity / Aggregate root** | `UniqueAssignmentPuzzle` (4×4, 빈 2, 중복·범위 규칙) | “이 입력이 도메인에서 허용되는지”에 대한 식별 가능한 퍼즐 인스턴스(식별자는 선택) |
| **Domain Service** | `MagicSquareSpecification` (또는 `Order4MagicPropertyChecker`) | 행/열/대각선 합·매직 상수(34) 만족 여부 판정(순수 판정만) |
| **Domain Service** | `EmptyCellResolver` | 빈칸 정확히 2개인지, 좌표(행·열) 나열(도메인 내부 표현은 0~3 또는 1~4로 고정) |
| **Domain Service** | `MissingNumberResolver` | 1~16 집합 대비 “그리드에 이미 있음/없음”으로 누락 2수 산출 |
| **Domain Service** | `CompletionStrategy` (이름은 예시) | (빈1,빈2) × (n_small, n_large) 두 배치를 시도해 `MagicSquareSpecification`이 참이 되는 조합 선택 |

*참고:* “누락 숫자 (작→첫빈, 큰→둘째)가 맞으면 그 순서, 아니면 반대”는 **응용 규칙**이면서 도메인 불변(유일한 해법 순서)과 겹칩니다. Domain API는 **최종 [r1,c1,n1,r2,c2,n2]를 1-인덱스로 내보내는 책임**을 한 곳에 모으는 것이 SRP에 유리합니다(아래 1.4).

## 1.2 도메인 불변조건 (Invariants)

| ID | 불변 | 검증 대상(진술) |
|----|------|----------------|
| I1 | **크기** | 격자는 4×4 |
| I2 | **빈칸 개수** | 값이 0인 셀은 정확히 2개 |
| I3 | **값 집합** | 각 셀은 0이거나 1~16 |
| I4 | **비영 중복** | 0이 아닌 값들은 서로 중복 없음 |
| I5 | **완성 격자(후보)** | 빈칸이 채워진 4×4는 1~16이 각 1회씩 등장 |
| I6 | **4차 일반(정상) 마방진** | 4행·4열 각 합 = 34, 주대각 2개 각 합 = 34(매직 상수 MC = 34) |

*정의 고정:* **Magic Constant(4×4, 1~16 완성)** = **34** (검증 가능, 단일 값).

## 1.3 핵심 유스케이스(도메인 관점)

| # | 유스케이스 | 사전조건(요약) | 사후조건(요약) |
|---|------------|----------------|----------------|
| UC1 | **빈칸 식별** | I1~I4 충족(입력 DTO/VO 수준) | “빈 2곳” 좌표 결정(내부 표기 일관) |
| UC2 | **누락 숫자 식별** | I1~I4 | {1..16} 중 그리드에 없는 정확히 2개 |
| UC3 | **마방진 판정** | I1, I3, I5(완성 가정) | I6을 만족하는지 bool |
| UC4 | **두 조합 시도(순서 결정)** | UC1·UC2 결과, I5 가능성 | n_small→첫빈·n_large→둘째빈을 먼저 시도, 성공 시 그 순서; 실패 시 반대 순서만이 성공해야 함(해 존재 시) |

*실패 유스케이스(도메인):* 입력 I1~I4 위반 시 **ValidationFailure**; 유효 입력인데 **어느 배치로도 I6·I5 불가**면 **UnsatisfiablePuzzle** (또는 동일 의미의 실패).

## 1.4 Domain API(내부 계약)

*코드 없이 시그니처 수준(의사·타입名만).*

| API | 입력 | 출력 | 실패조건(명시) |
|-----|------|------|----------------|
| `parseAndValidatePuzzle(int[][] g)` | 외부와 동일 형태(4×4) | `ValidPartialGrid` 또는 Failure | I1(행·열 수), I2(빈칸 수≠2), I3(범위), I4(중복) — 각각 **구분 가능**한 실패 |
| `findEmptyCells(ValidPartialGrid)` | - | `[(r,c),(r',c')]` 내부(0-인덱스 **또는** 1-인덱스 둘 중 **프로젝트 전역 하나로만** 고정) | 빈칸 2가 아닌 경우는 `parse` 단계에서 제거 |
| `findMissingTwoNumbers(ValidPartialGrid)` | - | `(n_a, n_b)` 오름차순 `n_a ≤ n_b` | 2개가 아닌 경우(논리 오류)는 **프로그래밍 오류**로 분류할지, 별도 실패로 둘지 **팀 규칙 1문장으로 고정** |
| `isCompletedMagicSquare(int[][] full)` | 4×4, I3·I5 | `boolean` | I3·I5 위반 시 false(또는 `validateFullGrid`로 선행) |
| `tryAssignmentOrder(empties, n_small, n_large)` | 빈칸 [첫, 둘], (n1,n2) | **성공 시** 1-인덱스 `[r1,c1,n1,r2,c2,n2]` | 양 배치 모두 I6 false → **Unsatisfiable** |
| `solveToOutput6(ValidPartialGrid)` (파사드) | - | `int[6]` **1-인덱스**, 출력 계약 | 위 실패 + **둘 다 실패** |

*고정 규칙(출력 계약과 합치기):*  
- `n1, n2` = 두 누락 수(출력에 실제로 넣는 **숫자**).  
- (작은 수 → 첫 번째 빈칸, 큰 수 → 두 번째 빈칸)이 마방진이면 **배치 순이 그것**; 그렇지 않으면 **첫/둘째 빈칸에 수를 바꾼 배치**가 유일한 해.

*“첫/둘째 빈칸” 정렬 고정(검증 가능):* 예) **행 우선(행↑, 열↑)**로 빈 셀을 읽은 순서 = 첫 번째, 두 번째. (문서·테스트·구현 **삼자 동일**.)

## 1.5 Domain 단위 테스트 설계(RED 우선)

### 테스트 케이스 목록

| ID | 구분 | 내용 | 보호하는 Invariant / 규칙 |
|----|------|------|---------------------------|
| D-V-01 | 비정상 | 3×3 또는 4×5 | I1 |
| D-V-02 | 비정상 | 빈칸 0, 1, 3개 | I2 |
| D-V-03 | 비정상 | -1, 17, 99 | I3 |
| D-V-04 | 비정상 | 5가 두 번(0 제외) | I4 |
| D-V-05 | 엣지 | 0 둘 + 14개 1~16, 중복 없음, 형식만 **합법** (해는 별도) | I1~I4 |
| D-H-01 | 정상 | **알려진 4×4 완성 마방진**에서 **임의 2칸**을 0으로 바꾼 뒤 `solve` → 복원과 동일 | I5, I6, 출력 순서 규칙 |
| D-H-02 | 정상 | n_small→첫빈·n_large→둘째빈이 **성공**인 인스턴스(픽스쳐) | UC4(첫 순서 선택) |
| D-H-03 | 정상 | **반대**만 되는 인스턴스(픽스쳐) | UC4(스왑) |
| D-F-01 | 실패(도메인) | 합법 입력이나 **어느 배치로도 MC·합 불가** | Unsatisfiable(정의한 이름) |
| D-P-01 | 단위 | `isCompletedMagicSquare`만: 합=34 **위반** 한 행 | I6 |
| D-P-02 | 단위 | 대각선만 틀린 4×4(숫자는 1~16) | I6 |
| D-E-01 | 엣지 | “첫/둘째 빈칸” **행·열** 정렬 규칙이 (r1,c1) < (r2,c2) lex | 출력 좌표 일관(문서 1.4) |

*체크리스트(RED):*  
- [ ] 위 표의 실패 케이스는 **서로 다른 실패 타입/코드**로 식별 가능(경계: 외부 계약과 맞출지는 §2.2).  
- [ ] 도메인 테스트는 **I/O 1-인덱스**는 “파사드 1곳” 테스트로 묶는다(중복 억제).

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 시나리오

| # | 시나리오 | 단계 |
|---|----------|------|
| S1 | **정상 해** | 4×4 정수 전달(경계) → **형식/제약 검증** → Domain 호출 → 6-튜플 출력 |
| S2 | **검증 실패** | 잘못된 그리드 → **고정된 에러 코드+메시지** → Domain 미호출 |
| S3 | **합법이나 풀 수 없음** | 검증 통과 → Domain `Unsatisfiable` → 고정 응답(§2.4) |
| S4 | (선택) **저장** | 성공/실패 후 `Data.save` (경로는 §3) |

## 2.2 UI 계약(외부 계약)

### Input schema (고정)

| 필드 | 타입 | 제약 | 위반 시 |
|------|------|------|--------|
| `grid` | 2D 4×4 int | 4행, 4열, `length`·`[i].length` | `ERR_GRID_SHAPE` |
| `grid[i][j]` | int | 0 또는 1~16 | `ERR_VALUE_RANGE` |
| 0의 개수 | 2 | 정확히 2 | `ERR_EMPTY_COUNT` |
| 1~16 (0 제외) | 집합 | 중복 없음 | `ERR_DUPLICATE` |

*교차 검증 가능성:* 0이 2개 + 비0 14개의 중복 없음 → 남는 집합 크기 **정확히 2**이면 누락 2수는 **논리적으로** 결정됨(UI가 미리 넣을 필요 없음, Domain이 책임).

### Output schema (성공, 고정)

| 필드 | 조건 | 형식 |
|------|------|------|
| 성공 | 6정수 | `[r1,c1,n1,r2,c2,n2]` 1-인덱스, 1≤r/c≤4, n1·n2 ∈1~16, 도메인 순서(문서 1) |

### Error schema (권장 공통)

| 키 | 설명 | 예시(문자열은 2.4에서 **문구 고정**) |
|----|------|----------------------------------------|
| `code` | 기계 읽기 코드(위 `ERR_*`) | `ERR_DUPLICATE` |
| `message` | 인간이 읽는 문장 1개 | 2.4 |
| (선택) `details` | { expected: "2 zeros", found: 3 } — **초기 버전은 생략 가능**, 생략 시 `message`만으로 검증 |

## 2.3 UI 레벨 테스트(Contract-first, Domain Mock)

*Domain은 Mock: `solve` 성공/실패만 스텁 가능.*

| ID | 케이스 | 기대(검증) |
|----|--------|------------|
| B-01 | 3×4 그리드 | `ERR_GRID_SHAPE`, Domain 0호출 |
| B-02 | 4×4, 0이 1개 | `ERR_EMPTY_COUNT` |
| B-03 | 값 17 | `ERR_VALUE_RANGE` |
| B-04 | 7 중복 | `ERR_DUPLICATE` |
| B-05 | Mock 성공 [1,2,3,4,5,6] | 출력 배열 **동일**, Mock 입력이 **parse된 그리드**로 전달됨 |
| B-06 | Mock `Unsatisfiable` | **고정 코드+문구(2.4)** |
| B-07 | (선택) `save` 이후 | Data Mock `save` 1회(성공 흐름) |

*체크리스트:*  
- [ ] “잘못된 입력”은 **절대** Real Domain에 가지 않음(호출 횟수 0).  
- [ ] 성공 응답 **배열 길이=6, 타입=int** (언어별로 동등 검증).

## 2.4 UX/출력 규칙(에러 메시지 **문구 고정**)

*아래 **문자열은 구현에서 동일**해야 UI 테스트가 `equals`로 검증 가능합니다.*

| `code` | `message` (한글, 고정) |
|--------|------------------------|
| `ERR_GRID_SHAPE` | `입력은 4행 4열의 정수 배열이어야 합니다.` |
| `ERR_EMPTY_COUNT` | `빈 칸(0)은 정확히 두 개여야 합니다.` |
| `ERR_VALUE_RANGE` | `각 값은 0이거나 1 이상 16 이하여야 합니다.` |
| `ERR_DUPLICATE` | `0을 제외한 값은 중복될 수 없습니다.` |
| `ERR_UNSATISFIABLE` | `주어진 빈 칸에 두 수를 넣어 마방진을 완성할 수 없습니다.` |
| (내부) `ERR_INTERNAL` | (선택) `처리 중 오류가 발생했습니다.` — Data/예상 밖; **통합/계약에 포함할지** 팀 합의 |

*성공 시(선택):* 메시지 없이 **수 배열만** 반환하거나, ` result: { values: int[6] }` — **둘 중 하나만** API 문서에 고정.

---

# 3) Data Layer 설계

## 3.1 목적·범위(학습용)

| 목적 | 범위 |
|------|------|
| “같은 유스케이스”에 **Repository 구현을 바꿔**도 Domain/UI 테스트가 동작 | **저장/로드**만(쿼리/트랜잭션/마이그레이션 **제외**). |
| 저장 **대상** | (A) 마지막 **입력 그리드** (B) 마지막 **출력 6-튜플** + 타임스탬프(선택) — 둘 다 DTO(직렬화 가능 구조) |

*불필요 작업 **명시:** DB 스키마, ORM, 동시성 튜닝 **범위 밖.**

## 3.2 인터페이스 계약(예)

| 메서드 | 입출력(개념) | 실패 |
|--------|-------------|------|
| `void save(Snapshot s)` | `Snapshot = { int[][] input4x4, int[]? output6, long? savedAt }` (필드 최소) | `StorageWriteException` (원인: 디스크 권한 등) |
| `Optional<Snapshot> load(String id)` **또는** `loadLatest()` | 최근 1건(학습) | `NotFound` / `loadLatest` → empty |
| (선택) `void clear()` | - | - |

*식별자 `id`는 학습용: `"last"` **단일 키**로 단순화해도 contract 상 문제 없음.

## 3.3 구현 옵션 비교

| 옵션 | 장점 | 단점 |
|------|------|------|
| **A. InMemory** | 테스트 빠름, 파일 없이 통합. **I/O 실패** 시나리오는 Mock/별도. | 프로세스 종료 시 데이터 소실(학습용으로 **허용 명시** 가능) |
| **B. File(JSON 권장)** | 프로세스 간 유지, “불리니스 스토리” 재현. | 경로, UTF-8, **깨진 JSON** 예외. CSV는 4×4·이스케이프 엣지 **규칙 추가** 부담 |

**추천: B (JSON, 단일 파일, 예: `~/.magicsquare/last.json`)**  
*이유:* (1) Data 레이어 “파일/형식 오류” **실패 시나리오(§4.2)** 를 **실제 코드 경로**로 돌릴 수 있고, (2) 스냅샷에 `input`+`output` **중첩**이 1~2줄이면 **불변조건 검증(I1)**이 재로드에서 재검수 가능. InMemory는 **필수 보조(테스트 더블).**

## 3.4 Data 레이어 테스트

| ID | 항목 | 기대 |
|----|------|------|
| DS-01 | save→load | 동일 4×4(값 동등) |
| DS-02 | 파일 없음/키 없음 | `NotFound` 또는 empty |
| DS-03 | 훼손된 JSON(구문) | `CorruptDataException` (이름은 고정) |
| DS-04 | 3×3으로 저장하려는 시도 | `save` 전 **I1** 검사 실패(Repository가 아니라 **Adapter에서 DTO 검증**—어느 층이 검증하는지 1문장: **Data Adapter가 직렬화 직전**에 I1) |
| DS-05 | 4×4 + output6 | 로드 후 output 길이 6 |

---

# 4) Integration & Verification

## 4.1 통합 경로(의존성 방향)

```mermaid
flowchart LR
  B[UI Boundary] --> A[Application Optional]
  A --> D[Domain]
  B --> D
  A --> R[Data Repository]
  A -. optional .-> B
  D ... Domain pure ... D
```

| 방향 | 규칙 |
|------|------|
| **의존** | `UI, Application, Data(구현) → Domain 인터페이스` / `UI → Application(선택)` / `Application → Data 인터페이스` |
| **금지** | Domain **의존** InMemory, 파일, `System.*` **직접** |
| **선택 Application** | `SolveMagicSquare` 유스케이스: (입력) → domain.solve → (선택) `repository.save` |

*호출 2가지 학습용 구성:*  
- **슬림:** `UI → Domain` (저장 제외)  
- **풀:** `UI → App → Domain + Data`

## 4.2 통합 테스트 시나리오

| # | 구분 | 시나리오 (요지) | 기대 |
|---|------|----------------|------|
| I1 | 정상 | `valid4x4` + Mock 없음(진짜 Domain) + JsonRepo save/load | end-to-end와 동일한 `int[6]` (도메인 단위검사와 **동일 픽스쳐**) |
| I2 | 정상 | InMemory로만 App 경로(파일 I/O 제외) | I1과 동일 결과(결과 **결정적**) |
| I3 | 실패(입력) | `ERR_DUPLICATE` | Domain/App 미실행(라이브 **경량 spy**) |
| I4 | 실패(도메인) | Unsatisfiable **합법** 입력 | `ERR_UNSATISFIABLE` (문구 고정) |
| I5 | 실패(데이터) | 손상 파일 로드(또는 read-only dir에 save) | Data 예외 **또는** `ERR_INTERNAL` 1가지로만 문서화 |

*최소: 정상 2, 실패 3 — 위 표로 충족.*

## 4.3 회귀 보호 규칙

| 항목 | 정책 |
|------|------|
| 계약凍結 | `int[6]`, 1-인덱스, n의 의미(§입력/출력), 에러 `code` 5종 **변경 = 메이저 버전** + 변경 로그 |
| 기존 테스트 | **Red로 추가된** 테스트 **삭제 금지**; 시그니처 변경 시 **이전 케이스**를 새 래퍼에 **이동(리네임 링)** |
| 리팩터 | **Domain I6(34)**, I2(빈 2) **절대 완화 금지**(테스트가 먼저) |

## 4.4 커버리지 목표(팀/CI)

| 층 | 목표(라인 또는 브랜치) | 비고 |
|----|-------------------------|------|
| Domain | **95%+** (브랜치 포함 권장) | 판정·빈칸·2조합·실패 **모든 분기** |
| UI Boundary | **85%+** | Mock Domain으로 오류/성공 **모든 ERR_*` |
| Data | **80%+** | **happy + corrupt + not found** |

*계측 도구(예: JaCoCo, Istanbul 등)는 언어 확정 후 1가지만 문서에 고정.*

## 4.5 Traceability Matrix (필수)

| Concept (Invariant) | Rule (검증 가능) | Use Case | Contract (§) | Test IDs | Component |
|---------------------|------------------|----------|--------------|----------|------------|
| I1 4×4 | `rows==4 && all row len==4` | UC-입력 | Input `grid` (2.2) | B-01, D-V-01, DS-04 | UI Validator |
| I2 빈 2 | `count(0)==2` | UC-입력 | `ERR_EMPTY_COUNT` | B-02, D-V-02 | UI Validator |
| I3 0∪1..16 | per-cell | UC-입력 | `ERR_VALUE_RANGE` | B-03, D-V-03 | UI Validator |
| I4 중복(0除外) | multiset | UC-입력 | `ERR_DUPLICATE` | B-04, D-V-04 | UI Validator |
| I5 완성 시 1~16 | placement | UC2, UC3 | Domain internal | D-H-01, D-P-01 | Domain |
| I6 MC=34 | 4+4+2 lines | UC3, UC4 | `solve` 성공 | D-P-01, I1 | Domain |
| 출력 순(작/큰·빈 순서) | Lex 빈칸, 시도1→2 | UC4 | Output int[6] (상단) | D-H-02, D-H-03, I1, I2 | Domain Facade |
| 저장 무결 I1 | reload same shape | (선택) | Snapshot (3.2) | DS-01, I1 | Data Adapter |
| Unsatisfiable | 둘 다 false | — | `ERR_UNSATISFIABLE` (2.4) | B-06, D-F-01, I4 | App or UI + Domain |

---

**요약:** 도메인은 **I1~I6**과 “빈칸 2 + 누락 2 + 두 배치”로 **완전히** 규정하고, **첫/둘째 빈칸**은 **행·열 lex 정렬**로 1문장 고정하세요. **경계**는 5가지 `ERR_*` + `ERR_UNSATISFIABLE` 문구로 **UI 테스트를 equals-검증** 가능하게 했고, **Data**는 **JSON+InMemory** 조합이 학습/통합(오류 경로)에 **검증 가능**합니다. **구현 코드**는 이 문서 범위에 포함하지 않았습니다.

---

**User**

Report 폴더에 보고서 형식으로 올려주세요

---

**Cursor**

Report 폴더의 기존 보고서 형식을 확인한 뒤 동일한 톤으로 문서를 작성합니다.



`06` 번으로 기존 보고서 메타·표지 형식에 맞춰 레이어 설계 보고서를 작성합니다.



다음 파일로 정리해 두었습니다.

**`c:\DEV\Magic_Square_XXX\Report\06_Magic_Square_Layered_Design_TDD_Contracts_Report.md`**

- 기존 `05_Magic_Square_PRD_Report.md`와 같은 **보고서 메타**(제목, 개요 표, 작성일, 버전, `01`·`02`·`04`·`05`와의 **정합** 문단).
- **§0**에 입·출력·row-major 빈칸 규칙을 `05` PRD와 **명시적 정합**.
- **§1~4**에 이전에 드린 Logic / Boundary / Data / 통합·Traceability·커버리지·**Traceability matrix**·체크리스트.
- `05`의 `E_*`와 2.4 `ERR_*` **명칭·문구**가 다를 수 있으므로, **PRD를 단일 사실원**으로 두고 `code` 매핑 1행을 둔다는 **주의**를 넣음.
- **Revision History** 1.0 1행.

`PRD` 쪽 `E_*` 메시지와 2.4에 적은 `ERR_*` **문자열**을 1:1로 맞추고 싶으면, `05`에 있는 `E_*` **정확 문구**를 주시면 `06` §2.4을 그에 맞게 **문구만** 바꾸는 게 좋습니다(구현·코드 없이 문서 정합).

---

**User**

바꿔주세요

---

**Cursor**

PRD(05)의 `E_*` 코드와 메시지를 확인한 뒤 보고서 06을 맞춥니다.



PRD `05`의 `E_*` 코드·영어 `message`·도메인 `E_NO_VALID_ASSIGNMENT` / 경계 `E_DOMAIN_FAILURE`에 맞춰 `06` 전체를 갱신합니다.



§2.4의 도메인 `E_NO_VALID_ASSIGNMENT` 설명을 PRD와 맞게 단순화합니다.



적용해 두었습니다. `Report/06_Magic_Square_Layered_Design_TDD_Contracts_Report.md`를 **PRD `05`의 `E_*`·영문 `message`**와 맞췄습니다.

**바꾼 요지**
- **FR-01:** `E_INPUT_SHAPE`, `E_ZERO_COUNT`, `E_VALUE_RANGE`, `E_DUPLICATE_NONZERO` + `05`와 **동일한 4문장** `message`
- **FR-05:** 도메인 `E_NO_VALID_ASSIGNMENT` / 경계 `E_DOMAIN_FAILURE` + `failed to resolve a valid magic-square assignment.` (한 줄)
- `ERR_*`, 한글 고정 문구(구버전) **삭제**
- 시나리오·2.2·2.3·4.2·4.4·Traceability·Revision **1.1** 기록 **전반 정리**

`05` `FR-01` 표에 있는 `message` 문자열은 **그대로** 넣었습니다.

