# Magic Square (4×4) 리팩토링 분석·계획 보고서 (Domain/Boundary/GUI)

## 개요

- **문서 목적:** `Domain/Boundary/GUI(Screen)` 3개 축에서 **테스트 현황**, **코드 스멜**, **ECB/SRP 관점**을 정리하고, **테스트 선행 기반 리팩토링 계획**을 제시한다.
- **대상 독자:** 리팩토링 착수 전(특히 `refactoring` 브랜치) 안전장치를 마련하려는 구현자/리뷰어.
- **작성일:** 2026-04-28
- **버전:** 1.0

| 항목 | 값 |
|------|-----|
| 문서 유형 | 내부 보고서(리팩토링 분석/계획) |
| 제품/프로젝트명 | Magic Square (4×4) — TDD 연습 — [`MagicSquare_02`](../README.md) |
| 분석 대상(코드) | [`../src/magicsquare/domain.py`](../src/magicsquare/domain.py), [`../src/magicsquare/boundary.py`](../src/magicsquare/boundary.py), GUI 창 로직 = [`../src/magicsquare/gui/window.py`](../src/magicsquare/gui/window.py) |
| 참고(실행/GUI) | [`10_Magic_Square_Local_Execution_and_GUI_Report.md`](10_Magic_Square_Local_Execution_and_GUI_Report.md) |
| 요구·검증 정본 | [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md) |

> 참고: 요청 경로에 `gui/main_window.py`가 있었으나, 본 저장소에서는 동일 역할이 `src/magicsquare/gui/window.py`에 구현되어 있다.

---

## 1. 현재 테스트 파일 존재 여부 및 커버 범위(요약)

### 1.1 `test_*.py` 존재 여부

현재 `tests/` 아래에 `test_*.py`가 **존재**한다.

### 1.2 발견된 테스트 목록(요약)

| 테스트 파일 | 주요 대상(의도) |
|---|---|
| [`../tests/domain/test_l_red_01_find_blank_coords.py`](../tests/domain/test_l_red_01_find_blank_coords.py) | `domain.find_blank_coords`(빈칸 2개 좌표, row-major, 1-index) |
| [`../tests/domain/test_l_red_02_find_missing_pair.py`](../tests/domain/test_l_red_02_find_missing_pair.py) | `domain.find_missing_pair`(1..VALUE_MAX에서 누락 2수, 정렬) |
| [`../tests/boundary/test_u_red_01_validate_shape.py`](../tests/boundary/test_u_red_01_validate_shape.py) | `boundary.validate`(shape 계약) |
| [`../tests/boundary/test_u_red_02_zero_count.py`](../tests/boundary/test_u_red_02_zero_count.py) | `boundary.validate`(0 개수 계약) |
| [`../tests/domain/test_logic_magic.py`](../tests/domain/test_logic_magic.py) | `magic_square.solve_magic_square`(골든/거부 케이스) |
| [`../tests/ui/test_ui_magic.py`](../tests/ui/test_ui_magic.py) | `GridUI` 조립 결과가 `boundary.validate`를 통과하는지(UI 조립 레벨) |

### 1.3 테스트 보강이 필요한 영역(핵심)

- GUI 창(`MagicSquareWindow`)의 클릭 플로우(`_on_solve_clicked`)는 현재 테스트가 직접 커버하지 않는다.
  - **성공 경로:** `validate` 통과 → `solve_magic_square` 반환(6-튜플) → grid 반영/라벨 출력
  - **실패 경로:** `ValueError` → `demo_solution()` 사용 → 메시지 박스 표시 → grid 채움/라벨 출력

---

## 2. 코드 스멜(Code Smell) 점검 결과(문제 항목만)

점검 항목(요약): 이해하기 힘든 이름, 중복 코드, 긴 함수(20줄 초과), 매직 넘버, 긴 매개변수 목록(>3), 불필요한 주석, 사용하지 않는 변수·함수.

| 파일명 | 줄번호 | 스멜 종류 | 문제 설명 | 우선순위 |
|---|---:|---|---|---|
| `src/magicsquare/boundary.py` | 6-20 | 중복 코드 | shape 불일치 시 같은 메시지 생성/raise 로직이 2곳(행 수/열 수 체크)에서 반복되어 변경 시 누락 위험 | 중 |
| `src/magicsquare/gui/window.py` | 44-67 | 긴 함수(20줄 초과) | `_on_solve_clicked`가 입력 수집→검증→솔버 호출→예외 UX→grid 반영→결과 표시까지 수행(책임 과다, 수정 위험) | 상 |
| `src/magicsquare/gui/window.py` | 49-66 | 이해하기 힘든 이름 | `answer`가 “정답 6-튜플/데모 정답”으로 의미가 상황에 따라 달라져 추론 비용 증가 | 중 |
| `src/magicsquare/gui/window.py` | 50, 60-63 | 불필요한 변수/흐름 | `solved_matrix=None`을 두고 분기하는 흐름이 복잡도를 올림(성공 케이스에서 실질적으로 항상 `None`) | 중 |
| `src/magicsquare/domain.py` | 11, 24 | 매직 넘버(도메인 규칙 하드코딩) | 빈칸 규칙이 `0`으로 직접 박혀 있어(==0/!=0) 규칙이 산재, 의미 공유가 약함 | 하 |
| `src/magicsquare/domain.py` | 12 | 매직 넘버(표현 규칙 하드코딩) | 좌표를 1-index로 반환하기 위한 `+1`이 코드에 직접 존재(의도가 코드 구조로 드러나지 않음) | 하 |
| `src/magicsquare/domain.py` | 26 | 매직 넘버(규칙의 암묵성) | universe를 `range(1, VALUE_MAX+1)`로 구성하며 최소값 `1`이 암묵적으로 박힘 | 하 |
| `src/magicsquare/gui/window.py` | 63-66 | 하드코딩된 결과 형식 | solver 결과를 6개로 고정 언패킹(반환 형식 변경에 취약, UI가 도메인 결과 구조에 강결합) | 중 |

*(해당 없음으로 관찰된 항목: 긴 매개변수 목록(>3), 명백한 unused 함수/변수.)*

---

## 3. ECB(Entity-Control-Boundary) 관점 분석(요약)

### 3.1 각 파일의 현재 역할

- `src/magicsquare/domain.py`
  - **Control 중심**: 입력(matrix)을 해석하여 규칙에 따라 결과를 계산(`find_blank_coords`, `find_missing_pair`).
  - **Entity(데이터 보관)** 역할은 현재 명시적 형태(클래스/값 객체)로는 거의 없다.

- `src/magicsquare/boundary.py`
  - **Boundary 역할**: 외부/상위 레이어에서 넘어오는 입력 계약(형태, 0 개수)을 강제(`validate`).
  - 현재 계약 범위는 **shape + zero count**에 집중되어 있으며, 범위/중복/타입 등 확장 여부는 정책 결정 포인트다.

- `src/magicsquare/gui/window.py` (Screen/UI)
  - UI 이벤트 처리 외에 **Control 성격의 정책/조합 책임**이 섞여 있음.
    - 실패 시에도 데모 정답을 채우는 정책 선택(`demo_solution()`)
    - solver 결과(6-튜플) 해석 및 적용(도메인 결과 구조에 결합)

### 3.2 “잘못된 위치”로 보이는 코드와 이동 제안(개념)

- GUI(`window.py`) 내부의 “무엇을 보여줄지(성공/실패 정책)”와 “도메인 결과(6-튜플) 해석”은
  - **Use-case / Controller 계층**(예: `controller.py`)로 이동해 “결과 모델”을 반환하고,
  - GUI는 반환된 모델을 **그리기만** 하는 구조가 ECB에 더 부합한다.

---

## 4. SRP(단일 책임 원칙) 관점 위반(요약, 문제 항목만)

- `src/magicsquare/boundary.py:6-20`
  - `validate()`가 **shape 검증**과 **zero count 검증**을 동시에 수행(2가지 책임).

- `src/magicsquare/gui/window.py:44-66`
  - `_on_solve_clicked()`가 UI 이벤트 처리 외에 **정책 결정(데모 정답 제시)** 및 **도메인 결과 해석/적용**까지 수행.

---

## 5. 리팩토링 계획(테스트 선행 기반)

## 5.1 리팩토링 대상 목록 (우선순위 순)

| 순번 | 대상 파일 | 문제 | 적용 기법 | 우선순위 |
|---:|---|---|---|---|
| 1 | `src/magicsquare/gui/window.py` | 클릭 핸들러가 UI+정책+조합 책임을 동시에 가짐(긴 함수, 강결합) | Extract Method, Introduce Controller(Use-case), 결과 모델(성공/실패/메시지/적용값)로 UI 단순화 | 상 |
| 2 | `src/magicsquare/boundary.py` | `validate`의 복합 책임 + 메시지 중복 | Extract Function(`validate_shape`, `validate_zero_count`), DRY(에러 생성 통합) | 중 |
| 3 | `src/magicsquare/domain.py` | 도메인 규칙/표현 규칙(0, 1-index, 최소값)이 암묵적 | Introduce Constants/Helpers(의도 명시), 필요 시 Value Object(Entity) 도입 검토 | 하~중 |
| 4 | (연관) `src/magicsquare/magic_square.py` | GUI가 solver 결과(6-튜플) 구조에 결합 | Encapsulate Return Type 또는 Controller에서 UI 친화 형태로 변환 | 중 |

## 5.2 테스트 선행 필요 항목

- 리팩토링 전에 먼저 테스트를 추가해야 할 함수/플로우:
  - `src/magicsquare/gui/window.py`의 `MagicSquareWindow._on_solve_clicked`
    - **성공 경로** 고정(6-튜플 적용, 결과 라벨)
    - **실패(ValueError) 경로** 고정(데모 정답 채움, 안내 메시지)

> `tests/ui/test_ui_magic.py`는 `GridUI` 조립 수준까지만 커버하므로, “창 이벤트”를 고정하려면 별도 테스트가 필요하다.

## 5.3 리팩토링 후 검증 방법

### 회귀 테스트(Regression Test) 실행 명령어

저장소 루트에서:

```bash
pytest -q
```

UI 테스트까지 포함(환경에 PyQt6가 설치되어 있어야 함):

```bash
pytest -q tests/ui
```

### 외부 동작(기능)이 바뀌지 않았음을 확인하는 방법

- **테스트 스위트 전부 통과**(Domain/Boundary/Logic/UI).
- GUI 수동 시나리오 2개를 리팩토링 전/후 비교:
  - 정상 입력(4×4, 0 두 개) → “풀기” 후 결과 표시 및 빈칸 채움이 동일
  - 잘못된 입력(0 개수 오류 등) → 오류 안내 및 데모 정답 표시 동작이 동일
- (선택) 커버리지 리포트가 이미 존재한다면(`htmlcov/`) 핵심 분기(성공/실패 경로) 커버 유지 여부를 확인.

---

## 6. 변경 이력(본 문서)

| 버전 | 일자 | 내용 |
|------|------|------|
| 1.0 | 2026-04-28 | Domain/Boundary/GUI 분석 요약 + 테스트 선행 기반 리팩토링 계획서 초판 |

---

*본 보고서는 리팩토링 착수 전 “안전장치(테스트)” 확보를 우선한다. 제품 요구·승인 기준은 [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md)가 우선한다.*

