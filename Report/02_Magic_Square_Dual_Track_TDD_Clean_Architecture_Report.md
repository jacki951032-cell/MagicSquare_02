# Magic Square (4x4) Dual-Track UI + Logic TDD 및 Clean Architecture 설계 보고서

## 프로젝트 목적
- 알고리즘 난이도보다 `레이어 분리`, `계약 기반 테스트`, `리팩토링 안정성` 훈련을 목표로 한다.
- 구현 코드는 작성하지 않고 설계/계약/테스트/통합 계획만 정의한다.

## 고정 입력/출력 계약
- 입력 계약
  - 타입: `4x4 int[][]`
  - 빈칸은 `0`, 개수는 정확히 2개
  - 값 범위: `0` 또는 `1~16`
  - `0` 제외 중복 금지
- 출력 계약
  - 타입: `int[6]`
  - 형식: `[r1,c1,n1,r2,c2,n2]`
  - 좌표는 `1-index`
  - 순서 규칙:
    - `(작은수 -> 첫빈칸, 큰수 -> 둘째빈칸)` 조합이 마방진이면 그 순서
    - 아니면 반대 순서

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념
- Entities / Value Objects / Domain Services 목록과 책임(SRP)

| 분류 | 이름 | 책임(SRP) | 검증 가능 조건 |
|---|---|---|---|
| Entity | `Matrix4x4` | 4x4 행렬 상태 보관 및 구조 불변성 유지 | 항상 4행 4열 |
| Value Object | `CellPosition` | 빈칸 좌표 표현(1-index) | row,col이 1~4 |
| Value Object | `MissingPair` | 누락 숫자 2개 표현 (`small < large`) | 범위 1~16, 정렬 유지 |
| Domain Service | `InputMatrixValidator` | 입력 계약 검증 | 크기/0개수/범위/중복 검사 |
| Domain Service | `BlankCellLocator` | 빈칸 2개 찾기 | 정확히 2개 좌표 |
| Domain Service | `MissingNumberFinder` | 누락 숫자 2개 찾기 | 정확히 2개 숫자 |
| Domain Service | `MagicSquareJudge` | 마방진 여부 판정 | 행/열/대각선 합 검사 |
| Domain Service | `DualAssignmentResolver` | 두 조합 시도 후 정답 순서 결정 | 출력 형식/순서 규칙 보장 |

## 1.2 도메인 불변조건(Invariants)
- 행/열/대각선 합 일치, Magic Constant 등

| ID | Invariant | Rule | 검증 테스트 |
|---|---|---|---|
| INV-D-01 | Magic Constant | 4x4에서 상수 34 | 상수 비교 테스트 |
| INV-D-02 | 행 합 일치 | 모든 행 합=34 | 행별 합 테스트 |
| INV-D-03 | 열 합 일치 | 모든 열 합=34 | 열별 합 테스트 |
| INV-D-04 | 주대각선 합 | (1,1)+(2,2)+(3,3)+(4,4)=34 | 주대각선 테스트 |
| INV-D-05 | 부대각선 합 | (1,4)+(2,3)+(3,2)+(4,1)=34 | 부대각선 테스트 |
| INV-D-06 | 빈칸 개수 | 0의 개수=정확히 2 | 입력 검증 테스트 |
| INV-D-07 | 값 범위 | 값은 0 또는 1~16 | 입력 검증 테스트 |
| INV-D-08 | 중복 제한 | 0 제외 중복 없음 | 입력 검증 테스트 |
| INV-D-09 | 좌표 규칙 | 출력 좌표는 1-index | 출력 계약 테스트 |
| INV-D-10 | 출력 포맷 | 길이 6, 순서 고정 | 출력 계약 테스트 |

## 1.3 핵심 유스케이스(도메인 관점)
- 빈칸 찾기, 누락 숫자 찾기, 마방진 판정, 두 조합 시도

| UC ID | 유스케이스 | 입력 | 출력 | 실패조건 |
|---|---|---|---|---|
| UC-D-01 | 빈칸 찾기 | `Matrix4x4` | `CellPosition[2]` | 0 개수 2 아님 |
| UC-D-02 | 누락 숫자 찾기 | `Matrix4x4` | `MissingPair` | 범위/중복 위반 |
| UC-D-03 | 마방진 판정 | 완성 행렬(0 없음) | `isMagic`, `failedRuleId` | 없음(판정 반환) |
| UC-D-04 | 두 조합 시도 | 빈칸2 + 누락숫자2 | `int[6]` | 두 조합 모두 실패 |

## 1.4 Domain API(내부 계약)
- 메서드 시그니처 수준(코드 X) + 입력/출력/실패조건

| API | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `validateInput(matrix)` | `int[][]` | `ValidatedMatrix4x4` | `E_INPUT_SHAPE`, `E_ZERO_COUNT`, `E_VALUE_RANGE`, `E_DUPLICATE_NONZERO` |
| `locateBlanks(validMatrix)` | `ValidatedMatrix4x4` | `CellPosition[2]` | `E_ZERO_COUNT` |
| `findMissingPair(validMatrix)` | `ValidatedMatrix4x4` | `MissingPair` | `E_VALUE_RANGE`, `E_DUPLICATE_NONZERO` |
| `judgeMagicSquare(filledMatrix)` | `int[4][4]` | `MagicJudgeResult` | 없음 |
| `resolveDualAssignment(validMatrix)` | `ValidatedMatrix4x4` | `int[6]` | `E_NO_VALID_ASSIGNMENT` |

## 1.5 Domain 단위 테스트 설계(RED 우선)
- 테스트 케이스 목록(정상/비정상/엣지)
- 각 테스트가 보호하는 invariant 명시

| Test ID | 유형 | 시나리오 | 기대 결과 | 보호 Invariant |
|---|---|---|---|---|
| D-T-VAL-01 | 정상 | 유효 4x4 입력 | 검증 통과 | INV-D-06~08 |
| D-T-VAL-02 | 비정상 | 0 개수 1개/3개 | `E_ZERO_COUNT` | INV-D-06 |
| D-T-VAL-03 | 비정상 | -1 또는 17 포함 | `E_VALUE_RANGE` | INV-D-07 |
| D-T-VAL-04 | 비정상 | non-zero 중복 | `E_DUPLICATE_NONZERO` | INV-D-08 |
| D-T-JDG-01 | 정상 | 유효 마방진 | `isMagic=true` | INV-D-01~05 |
| D-T-JDG-02 | 엣지 | 특정 행 합 불일치 | `isMagic=false` | INV-D-02 |
| D-T-JDG-03 | 엣지 | 특정 열 합 불일치 | `isMagic=false` | INV-D-03 |
| D-T-JDG-04 | 엣지 | 주대각선 불일치 | `isMagic=false` | INV-D-04 |
| D-T-JDG-05 | 엣지 | 부대각선 불일치 | `isMagic=false` | INV-D-05 |
| D-T-ASG-01 | 정상 | 정순 조합 유효 | 정순 출력 | INV-D-09, INV-D-10 |
| D-T-ASG-02 | 정상 | 역순 조합 유효 | 역순 출력 | INV-D-09, INV-D-10 |
| D-T-ASG-03 | 비정상 | 두 조합 모두 실패 | `E_NO_VALID_ASSIGNMENT` | INV-D-02~05 |

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 관점 시나리오
- “행렬 입력 -> 검증 -> 결과 출력” 흐름

체크리스트:
- [ ] 입력 payload에서 `matrix` 수신
- [ ] UI Boundary 계약 검증 수행
- [ ] 실패 시 에러 스키마 반환, 도메인 호출 금지
- [ ] 성공 시 Domain/App Service 호출
- [ ] 출력 스키마로 직렬화 후 반환

## 2.2 UI 계약(외부 계약)
- Input schema / Output schema / Error schema

| 스키마 | 구조 | 규칙 |
|---|---|---|
| Input | `{ matrix: int[4][4] }` | 크기/0개수/범위/중복 규칙 강제 |
| Output | `{ result: int[6] }` | `[r1,c1,n1,r2,c2,n2]`, 좌표 1-index |
| Error | `{ code, message, details? }` | code-message 고정 매핑 |

## 2.3 UI 레벨 테스트(Contract-first, RED 우선)
- 잘못된 크기, 빈칸 개수 오류, 값 범위 오류, 중복 오류, 반환 포맷 검증
- Domain은 Mock으로 가정

| Test ID | Given | Domain Mock | Expected |
|---|---|---|---|
| UI-T-01 | 4x4가 아닌 크기 | 호출 안 함 | `E_INPUT_SHAPE` |
| UI-T-02 | 0 개수 != 2 | 호출 안 함 | `E_ZERO_COUNT` |
| UI-T-03 | 범위 밖 값 포함 | 호출 안 함 | `E_VALUE_RANGE` |
| UI-T-04 | non-zero 중복 값 포함 | 호출 안 함 | `E_DUPLICATE_NONZERO` |
| UI-T-05 | 유효 입력 | 고정 `int[6]` 반환 | 출력 형식 일치 |
| UI-T-06 | 유효 입력 | 도메인 실패 응답 | `E_DOMAIN_FAILURE` |
| UI-T-07 | 유효 입력 | 임의 `int[6]` 반환 | 좌표 1-index 검증 |

## 2.4 UX/출력 규칙
- 에러 메시지 표준(정확한 문구 규칙까지)

| 코드 | 표준 메시지 |
|---|---|
| `E_INPUT_SHAPE` | `matrix must be a 4x4 integer array.` |
| `E_ZERO_COUNT` | `matrix must contain exactly two zeros.` |
| `E_VALUE_RANGE` | `matrix values must be 0 or between 1 and 16.` |
| `E_DUPLICATE_NONZERO` | `non-zero values must be unique.` |
| `E_DOMAIN_FAILURE` | `failed to resolve a valid magic-square assignment.` |
| `E_DATA_FAILURE` | `failed to load or save matrix data.` |

문구 규칙:
- [ ] 코드별 메시지는 1개로 고정
- [ ] 문장은 마침표(`.`)로 종료
- [ ] 동일 원인에 다른 문구 사용 금지
- [ ] 메시지 변경 시 계약 변경으로 간주하고 테스트 동시 수정

---

# 3) Data Layer 설계 (Data Layer)

## 3.1 목적 정의
- “저장/로드”의 필요성과 범위(학습용)

정의:
- [ ] 입력 행렬 저장/로드를 통해 재현 가능한 테스트 데이터 확보
- [ ] 실행 결과 저장/로드는 선택 기능으로 분리
- [ ] 비즈니스 판정 로직은 Data Layer에 두지 않음

## 3.2 인터페이스 계약
- 예: MatrixRepository.save/load (메서드 수준, 코드 X)
- 저장 대상: 입력 행렬, 실행 결과(선택)

| 메서드 | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `saveInput(matrix)` | `int[4][4]` | `recordId:string` | `E_DATA_IO` |
| `loadInput(recordId)` | `string` | `int[4][4]` | `E_DATA_NOT_FOUND`, `E_DATA_FORMAT` |
| `saveResult(result)` | `int[6]` | `recordId:string` | `E_DATA_IO` |
| `loadResult(recordId)` | `string` | `int[6]` | `E_DATA_NOT_FOUND`, `E_DATA_FORMAT` |

## 3.3 구현 옵션 비교(메모리/파일)
- 옵션 A: InMemory / 옵션 B: File(JSON/CSV)
- 추천안 1개 선택 + 이유

| 옵션 | 장점 | 단점 | 추천 여부 |
|---|---|---|---|
| 옵션 A: InMemory | 빠른 테스트, 결정적 실행, 설정 단순 | 프로세스 종료 시 데이터 소실 | **추천 (초기)** |
| 옵션 B: File(JSON/CSV) | 영속성 확보, 수동 검토 가능 | I/O 예외 및 형식 오류 처리 필요 | 후속 어댑터 |

추천안:
- **옵션 A(InMemory) 우선**
  - 이유 1: TDD 초기 사이클에서 실패 원인 분리 용이
  - 이유 2: 계약 안정화 이후 옵션 B를 어댑터로 확장 가능
  - 이유 3: 포트/어댑터 학습 효과가 명확함

## 3.4 Data 레이어 테스트
- 저장/로드 정합성, 예외(파일 없음/형식 오류), 불변조건(4x4 유지)

| Test ID | 시나리오 | 기대 결과 |
|---|---|---|
| DATA-T-01 | 입력 저장 후 즉시 로드 | 동일한 4x4 반환 |
| DATA-T-02 | 결과 저장 후 즉시 로드 | 동일한 int[6] 반환 |
| DATA-T-03 | 존재하지 않는 키/파일 로드 | `E_DATA_NOT_FOUND` |
| DATA-T-04 | 형식 손상 데이터 로드 | `E_DATA_FORMAT` |
| DATA-T-05 | 로드 결과가 4x4 아님 | 불변조건 위반 처리 |
| DATA-T-06 | 로드 값이 범위/중복 위반 | 상위 검증기에서 차단 |

---

# 4) Integration & Verification (통합 및 검증)

## 4.1 통합 경로 정의
- UI -> Application(선택) -> Domain -> Data 흐름(의존성 방향 포함)

정의:
- [ ] UI는 Application/Domain 인터페이스에만 의존
- [ ] Domain은 Data 구현체가 아닌 Repository 포트에 의존
- [ ] Data 어댑터는 외곽 계층에서 포트 구현
- [ ] 의존성 방향은 항상 바깥 -> 안쪽

## 4.2 통합 테스트 시나리오
- 정상 시나리오 2개 이상
- 실패 시나리오 3개 이상(입력 오류, 도메인 실패, 데이터 실패)

| Test ID | 유형 | 시나리오 | 기대 결과 |
|---|---|---|---|
| INT-T-01 | 정상 | 정순 조합 유효 케이스 | 정순 `int[6]` 반환 |
| INT-T-02 | 정상 | 역순 조합 유효 케이스 | 역순 `int[6]` 반환 |
| INT-T-03 | 실패(입력) | 4x4 크기 위반 | `E_INPUT_SHAPE` |
| INT-T-04 | 실패(입력) | 값 범위/중복 위반 | `E_VALUE_RANGE` 또는 `E_DUPLICATE_NONZERO` |
| INT-T-05 | 실패(도메인) | 두 조합 모두 마방진 실패 | `E_DOMAIN_FAILURE` |
| INT-T-06 | 실패(데이터) | 저장/로드 실패 | `E_DATA_FAILURE` |

## 4.3 회귀 보호 규칙
- 기존 테스트 유지 정책
- 변경 금지 규칙(계약/출력 포맷)

체크리스트:
- [ ] 통과 중인 기존 테스트 삭제 금지
- [ ] 계약 수정 전 RED 테스트 선반영
- [ ] 입력 계약(4x4/0 두 개/범위/중복) 변경 금지
- [ ] 출력 포맷 `[r1,c1,n1,r2,c2,n2]` 변경 금지
- [ ] 좌표 1-index 규칙 변경 금지
- [ ] 에러 코드 문자열 변경 금지

## 4.4 커버리지 목표
- Domain Logic 95%+
- UI Boundary 85%+
- Data 80%+

품질 게이트:
- [ ] Domain 미달 시 빌드 실패
- [ ] UI Boundary 미달 시 빌드 실패
- [ ] Data 미달 시 빌드 실패

## 4.5 Traceability Matrix (필수)
- Concept(Invariant) -> Rule -> Use Case -> Contract -> Test -> Component

| Concept(Invariant) | Rule | Use Case | Contract | Test | Component |
|---|---|---|---|---|---|
| INV-D-06 | 0 개수=2 | UC-D-01 | Input zero count | D-T-VAL-02, UI-T-02, INT-T-03 | `InputMatrixValidator`, `BlankCellLocator` |
| INV-D-07 | 값 범위 0 or 1~16 | UC-D-02 | Input value range | D-T-VAL-03, UI-T-03, INT-T-04 | `InputMatrixValidator`, `MissingNumberFinder` |
| INV-D-08 | non-zero 중복 없음 | UC-D-02 | Input duplicate rule | D-T-VAL-04, UI-T-04, INT-T-04 | `InputMatrixValidator` |
| INV-D-02/03/04/05 | 행/열/대각선 합=34 | UC-D-03 | Domain judge contract | D-T-JDG-01~05 | `MagicSquareJudge` |
| INV-D-09/10 | 출력 1-index + int[6] | UC-D-04 | Output schema | D-T-ASG-01~03, UI-T-05~07, INT-T-01~02 | `DualAssignmentResolver`, `UI Boundary Presenter` |

---

## 최종 검증 체크리스트
- [ ] 문서 내 모호 표현(`적절히`, `충분히`) 사용 없음
- [ ] 모든 규칙은 테스트 케이스로 검증 가능
- [ ] 구현 코드 없음
- [ ] 레이어별 책임과 계약 경계가 분리됨
