# Magic Square (4×4) RED 테스트 스켈레톤·개발 환경·저장소 반영 보고서

## 개요

- **문서 목적:** [`TEST_SPEC`](../docs/TEST_SPEC_Magic_Square_4x4.md)에 맞춘 **pytest RED 스켈레톤**, **픽스처**, **로컬 실행(가상환경)** 절차, **`origin` 원격 반영** 내역을 Report에 남긴다.
- **대상 독자:** 실습자, 리뷰어, CI·협업 환경을 맞추는 담당자.
- **작성일:** 2026-04-28
- **버전:** 1.0

| 항목 | 값 |
|------|-----|
| 문서 유형 | 내부 보고서(산출물 기록 · 운영 메모) |
| 제품/프로젝트명 | Magic Square (4×4) — [`MagicSquare_02`](https://github.com/jacki951032-cell/MagicSquare_02) |
| 요구·테스트 정본 | [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md), [`../docs/TEST_SPEC_Magic_Square_4x4.md`](../docs/TEST_SPEC_Magic_Square_4x4.md) |
| 관련 Report | [`09_Magic_Square_Dual_Track_RED_Test_Design_Report.md`](09_Magic_Square_Dual_Track_RED_Test_Design_Report.md), [`08_Magic_Square_Git_Branch_PR_Workflow_Report.md`](08_Magic_Square_Git_Branch_PR_Workflow_Report.md), [`07_Magic_Square_README_Repository_Guide_Report.md`](07_Magic_Square_README_Repository_Guide_Report.md) |

---

## 1. 본 보고서의 범위

| 구분 | 내용 |
|------|------|
| **포함** | 레포에 추가된 테스트·설정 파일 목록, RED 단계 기대 동작(실패), 가상환경에서의 `pytest` 실행 방법, Git 브랜치·원격 URL |
| **제외** | 도메인·경계 **구현 본문(GREEN)**, PR 머지 완료 여부(변동 가능) |

---

## 2. 저장소에 반영된 산출물(요약)

| 구분 | 경로·파일 | 설명 |
|------|-----------|------|
| 테스트 명세(갱신) | [`docs/TEST_SPEC_Magic_Square_4x4.md`](../docs/TEST_SPEC_Magic_Square_4x4.md) | 계약 상수, Golden 예 A 검산, pytest/JUnit RED 스켈레톤 예시 |
| Pytest 설정 | [`pytest.ini`](../pytest.ini) | `testpaths = tests`, `pythonpath = src` |
| 개발 의존성 | [`requirements-dev.txt`](../requirements-dev.txt) | `pytest>=7.0` |
| 무시 규칙 | [`.gitignore`](../.gitignore) | `.venv/`, `__pycache__/`, `.pytest_cache/` 등 |
| 패키지 루트 | [`src/magic_square/__init__.py`](../src/magic_square/__init__.py) | 이후 구현 모듈 배치용 |
| 경계 RED | [`tests/boundary/test_solve_magic_square.py`](../tests/boundary/test_solve_magic_square.py) | TC-MS-A·UI-T·T-S-02/03 등 **9**건, 본문 `assert False` |
| 도메인 RED | [`tests/domain/test_*.py`](../tests/domain/) | Blank / Missing / Judge / Resolver **7**건 |
| 통합 RED | [`tests/integration/test_scenarios_ts01_ts03.py`](../tests/integration/test_scenarios_ts01_ts03.py) | **2**건 |
| 픽스처 | [`tests/fixtures/golden_example_a.py`](../tests/fixtures/golden_example_a.py) | `M_EXAMPLE_A` (PRD §9.3) |
| 픽스처 | [`tests/fixtures/boundary_invalid_inputs.py`](../tests/fixtures/boundary_invalid_inputs.py) | FR-01 경계용 샘플 행렬 |
| 픽스처 | [`tests/fixtures/no_solution_matrix.py`](../tests/fixtures/no_solution_matrix.py) | `T-S-03`용 `M_NO_SOLUTION` 플레이스홀더 |
| 공통 | [`tests/conftest.py`](../tests/conftest.py) | 확장용 |

**RED 기대:** 구현 전에는 위 단위 테스트가 **`AssertionError`(assert False)** 로 **전부 실패**한다(현재 설계 의도).

---

## 3. 로컬 실행 방법(가상환경, Windows PowerShell 기준)

### 3.1 가상환경 생성(프로젝트 루트에서 1회)

```powershell
cd c:\DEV\MagicSquare_02
python -m venv .venv
```

Python **3.10+** 권장(PRD·명세와 정합).

### 3.2 가상환경 활성화(세션마다)

```powershell
.\.venv\Scripts\Activate.ps1
```

프롬프트 앞에 `(.venv)`가 보이면 활성화된 상태다.

스크립트 실행이 차단되면(ExecutionPolicy), 사용자 범위에서 예외를 허용하거나, 활성화 없이  
`.\.venv\Scripts\python.exe -m pytest ...` 로 실행한다.

### 3.3 의존성 설치

```powershell
pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 3.4 테스트 실행

```powershell
python -m pytest tests -q
```

상세 로그:

```powershell
python -m pytest tests -v
```

### 3.5 가상환경 종료

```powershell
deactivate
```

---

## 4. Git 원격·브랜치 기록

| 항목 | 값 |
|------|-----|
| 원격 `origin` | `https://github.com/jacki951032-cell/MagicSquare_02.git` |
| 작업 브랜치(예시) | `feature/dual-track-tdd` |
| PR 생성 URL(브랜치 푸시 후) | `https://github.com/jacki951032-cell/MagicSquare_02/pull/new/feature/dual-track-tdd` |

`main`에 반영하려면 GitHub에서 Pull Request를 열어 머지하거나, 팀 워크플로([`08`](08_Magic_Square_Git_Branch_PR_Workflow_Report.md))에 따른다.

---

## 5. 문서·추적 매핑

| 본 보고서 내용 | 대응 문서 |
|----------------|-----------|
| RED 함수명·디렉터리 | [`TEST_SPEC` §5·§8](../docs/TEST_SPEC_Magic_Square_4x4.md), [`09`](09_Magic_Square_Dual_Track_RED_Test_Design_Report.md) |
| 계약 문자열·Golden | [`TEST_SPEC` §2·§3](../docs/TEST_SPEC_Magic_Square_4x4.md), PRD FR-01·§9.3 |
| 브랜치·PR 습관 | [`08`](08_Magic_Square_Git_Branch_PR_Workflow_Report.md) |

---

## 6. 후속 권장 작업

1. **GREEN:** [`src/magic_square/`](../src/magic_square/)에 도메인·경계 구현 후 테스트를 하나씩 통과시킨다.
2. **`M_NO_SOLUTION`:** [`no_solution_matrix.py`](../tests/fixtures/no_solution_matrix.py)에 검산된 `T-S-03` 전용 격자를 채운다(PR [`TEST_SPEC` §3](../docs/TEST_SPEC_Magic_Square_4x4.md)).
3. **CI:** 동일 커맨드(`pytest`)를 파이프라인에 고정한다(PR [`PRD` §7.1](../docs/PRD_Magic_Square_4x4_TDD.md)).

---

*납기·기능 판정은 [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md)가 우선한다.*
