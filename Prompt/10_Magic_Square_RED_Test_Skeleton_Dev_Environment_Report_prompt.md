# Test specification for magic square
_Exported on 4/28/2026 at 14:10:30 GMT+9 from Cursor (3.2.11)_

---

**User**

@docs/TEST_SPEC_Magic_Square_4x4.md 를 참조해 테스트해 볼 수 있도록 자세하게 다시 작성해줘 테스트 프레임워크 이름(JUnit 5, pytest 등)에 맞춰 파일/클래스 이름만 적은 테스트 스켈레톤(메서드 빈 본문, fail 또는 assertTrue(false) 한 줄)도 같은 RED 원칙으로만 적어봅니다.


---

**Cursor**

참조 문서와 프로젝트 구조를 확인합니다.



PRD에서 FR-01 메시지, §9.3 Golden 격자, AC-05 문구를 확인합니다.



예 A 격자를 검산해 §9.3과의 정합성을 확인했습니다. 시도1은 실패·시도2만 성공하는 케이스입니다. 문서에 검산 결과와 실행 가능한 명세·RED 스켈레톤을 반영합니다.



`docs/TEST_SPEC_Magic_Square_4x4.md`를 실행 가능한 수준으로 다시 정리했습니다. 요약만 말씀드립니다.

### 바뀐 점

1. **실행 방법** — 프로젝트 루트에서 `python -m pytest tests/ -q` 등 복붙용 명령.
2. **계약 상수** — FR-01 표 전체 + `E_DOMAIN_FAILURE` / 해 없음 한 줄 문구를 §2로 따로 두어 assertion에 그대로 넣을 수 있게 함.
3. **§9.3 예 A 검산** — 격자를 그대로 두고, 누락 수 \(a=1, b=6\), 빈칸 `(3,3)`·`(4,4)`에서 **시도1은 실패·시도2만 성공**임을 적었습니다. 그래서 기대 튜플은 AC-05-3 기준 **`[3, 3, 6, 4, 4, 1]`**이며, **`T-S-02`에 맞고 `T-S-01`용 Golden은 별도 검산이 필요**하다고 명시했습니다(PRD의 “시도1·Gherkin” 라벨과 수학적 결과가 어긋나면 혼동이 나므로).
4. **경계 TC용 예시 리터럴** — `M_INVALID_RANGE` 등 최소 샘플.
5. **권장 디렉터리** — `tests/boundary/`, `tests/domain/`, `tests/fixtures/` 예시 트리.
6. **TC 표** — §7에서 Given/When/Then과 기대 코드·메시지를 한 표에 묶음.
7. **RED 스켈레톤**
   - **pytest**: §8에 파일별 함수 이름과 `assert False  # RED` 한 줄만 있는 블록.
   - **JUnit 5**: §9에 `SolveMagicSquareTest` 클래스와 `{ fail("RED"); }` 한 줄 패턴, 도메인은 클래스명만 예시.

원하시면 `tests/` 아래에 위 스켈레톤을 실제 빈 파일로 추가하는 작업도 이어서 할 수 있습니다.

---

**User**

그렇게 해주세요

---

**Cursor**

테스트 스켈레톤 파일을 생성합니다. 프로젝트 루트 구조를 확인합니다.



픽스처 모듈과 `pytest.ini`를 추가하고, 문서에 맞는 테스트 스켈레톤을 생성합니다.



중복 테스트용 격자에 `0`이 두 개 있도록 수정합니다.



사용하지 않는 `import pytest` 제거 후 `pytest` 실행으로 확인합니다.



의존성을 명시하기 위해 `requirements-dev.txt`를 추가합니다.



작업 반영했습니다. 추가·수정된 내용만 정리합니다.

### 생성된 레이아웃

| 경로 | 역할 |
|------|------|
| `pytest.ini` | `testpaths = tests`, `pythonpath = src` |
| `requirements-dev.txt` | `pytest>=7.0` |
| `src/magic_square/__init__.py` | 이후 구현용 패키지 루트 |
| `tests/conftest.py` | 공통 설정 (현재는 docstring만) |
| `tests/fixtures/golden_example_a.py` | `M_EXAMPLE_A` (§9.3 예 A) |
| `tests/fixtures/boundary_invalid_inputs.py` | UI-T-01~04용 샘플 행렬 (`M_INPUT_SHAPE_NOT_4X4`, `M_ZERO_COUNT_ONE`, `M_INVALID_RANGE`, `M_DUPLICATE_NONZERO`) |
| `tests/fixtures/no_solution_matrix.py` | `T-S-03`용 `M_NO_SOLUTION` 플레이스홀더 (`None`) |
| `tests/boundary/test_solve_magic_square.py` | 경계 9개 테스트 |
| `tests/domain/test_*.py` | 도메인 단위 테스트 7개 |
| `tests/integration/test_scenarios_ts01_ts03.py` | 통합 2개 |

각 테스트는 **`assert False  # RED`** 한 줄만 있으며, 로컬에서 `pip install -r requirements-dev.txt` 후 `python -m pytest tests -q` 실행 시 **19건 실패**로 확인했습니다.

경계 TC용 **`M_DUPLICATE_NONZERO`**는 FR-01 의미에 맞게 **빈칸 `0` 두 칸 + 비영역 중복**으로 맞춰 두었습니다.

---

**User**

실행방법을 상세하게 알려주세요 (가상환경에서 수행가능하도록)

---

**Cursor**

가상환경을 쓰는 전제로, **Windows(PowerShell)** 기준 실행 절차만 정리합니다.

---

## 1. 한 번만: 가상환경 만들기

프로젝트 루트(`c:\DEV\MagicSquare_02`)에서:

```powershell
cd c:\DEV\MagicSquare_02
python -m venv .venv
```

- `python`이 3.10+인지 확인: `python --version`  
- 여러 버전이 있으면 `py -3.10 -m venv .venv` 처럼 지정해도 됩니다.

---

## 2. 가상환경 켜기(매 작업 세션)

**PowerShell:**

```powershell
cd c:\DEV\MagicSquare_02
.\.venv\Scripts\Activate.ps1
```

활성화되면 프롬프트 앞에 `(.venv)`가 붙습니다.

**스크립트 실행이 막힐 때(ExecutionPolicy):**  
현재 세션에서만 허용하려면:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

또는 활성화 없이 매번:

```powershell
c:\DEV\MagicSquare_02\.venv\Scripts\python.exe -m pytest ...
```

---

## 3. 의존성 설치(가상환경 활성화된 상태)

```powershell
pip install --upgrade pip
pip install -r requirements-dev.txt
```

`requirements-dev.txt`에는 `pytest`가 들어 있습니다.

---

## 4. 테스트 실행

**전체 스위트(요약만):**

```powershell
python -m pytest tests -q
```

**어느 테스트가 실패하는지 보기(RED 확인):**

```powershell
python -m pytest tests -v
```

**한 모듈만:**

```powershell
python -m pytest tests\boundary\test_solve_magic_square.py -v
```

**짧은 트레이스백:**

```powershell
python -m pytest tests --tb=short
```

---

## 5. 가상환경 끄기

```powershell
deactivate
```

---

## 6. 요약 체크리스트

| 순서 | 명령 |
|------|------|
| 1 | `cd c:\DEV\MagicSquare_02` |
| 2 | `.\.venv\Scripts\Activate.ps1` (또는 이미 만든 venv 사용) |
| 3 | `pip install -r requirements-dev.txt` (최초 1회 또는 의존성 바뀐 뒤) |
| 4 | `python -m pytest tests -q` |

`.venv`는 보통 **Git에 올리지 않고** 로컬에만 둡니다(`.gitignore`에 `/.venv/` 있으면 그대로 두면 됩니다).

원하시면 이 내용을 `README.md`에 “로컬 실행” 절로 붙여 넣는 문구도 맞춰 드리겠습니다.

---

**User**

@https://github.com/jacki951032-cell/MagicSquare_02.git 에 작업한 모든 내용을 업로드해주세요

---

**Cursor**

Git 상태와 원격 저장소 설정을 확인한 뒤 커밋하고 푸시합니다.



원격이 이미 올바릅니다. Python 프로젝트용 `.gitignore`를 추가한 뒤 전체 변경을 커밋하고 푸시합니다.



작업 반영해 두었습니다.

### 수행한 작업

1. **`.gitignore` 추가** — `.venv/`, `__pycache__/`, `.pytest_cache/` 등이 커밋되지 않도록 했습니다.
2. **변경·신규 파일 전부 스테이징** 후 **커밋** (`8580a18`).
3. **`origin`**(`https://github.com/jacki951032-cell/MagicSquare_02.git`)에 **`feature/dual-track-tdd`** 브랜치로 **푸시** (원격에 해당 브랜치가 없어 새로 생성됨).

### 원격에 포함된 내용(요약)

- `README.md`, `docs/TEST_SPEC_Magic_Square_4x4.md` 수정
- `Report/07` 수정, `Report/08`, `09` 및 대응 `Prompt` 추가
- `pytest.ini`, `requirements-dev.txt`, `src/magic_square/`, `tests/` 전부
- 기타 위 커밋 메시지에 적힌 파일

### 다음에 하실 수 있는 것

- **PR 열기:**  
  https://github.com/jacki951032-cell/MagicSquare_02/pull/new/feature/dual-track-tdd  
- **`main`에 합치려면** 위 PR에서 머지하거나, 로컬에서 `main`으로 머지 후 `git push origin main` 하시면 됩니다.

현재 로컬은 **`feature/dual-track-tdd`**이며 `origin/feature/dual-track-tdd`와 동기화된 상태입니다.

---

**User**

Report 폴더에 보고서로 업로드해주세요

---

**Cursor**

기존 Report 파일 형식을 확인한 뒤, 최근 작업(테스트 스켈레톤·실행 방법·Git 업로드)을 정리한 보고서를 `Report` 폴더에 추가합니다.



연번 `10`으로 개발 산출물·실행 방법·원격 반영을 정리한 보고서를 작성합니다.



보고서를 추가했습니다. Git에 커밋하고 원격에 푸시합니다.



다음 작업을 반영했습니다.

### 추가한 보고서

**`Report/10_Magic_Square_RED_Test_Square_RED_Test_Skeleton_Dev_Environment_Report.md`**

아래를 한 문서로 정리했습니다.

| 절 | 내용 |
|----|------|
| 개요·메타 표 | 목적, 독자, 정본 문서, 관련 Report 07·08·09 링크 |
| 범위 | 포함/제외 |
| 산출물 표 | `pytest.ini`, `requirements-dev.txt`, `tests/**`, `src/magic_square/`, 픽스처 등 |
| 로컬 실행 | 가상환경 생성·활성화( PowerShell ), `pip install`, `pytest` 명령 |
| Git | `origin` URL, `feature/dual-track-tdd`, PR 링크 패턴 |
| 추적 | TEST_SPEC·09·08와의 대응 |
| 후속 | GREEN, `M_NO_SOLUTION` 검산, CI |

### Git 상태

- 로컬에는 **커밋까지 완료**되었습니다 (`56a60d4`: Report 10 추가).
- **`git push`는 네트워크 오류로 실패**했습니다. 연결 가능할 때 프로젝트 루트에서 다음만 실행하면 원격에 올라갑니다.

```powershell
cd c:\DEV\MagicSquare_02
git push origin feature/dual-track-tdd
```

파일명에 오타가 있었습니다: 제목은 `10_Magic_Square_RED_Test_Skeleton_Dev_Environment_Report.md`로 저장했는데, 위에서 한 번 잘못 적었습니다. 실제 파일명을 확인합니다.



실제 파일명은 **`Report/10_Magic_Square_RED_Test_Skeleton_Dev_Environment_Report.md`** 입니다.

