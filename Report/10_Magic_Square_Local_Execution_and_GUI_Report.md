# Magic Square (4×4) 로컬 실행·GUI·pytest 보고서

## 개요

- **문서 목적:** 개발자·학습자가 **로컬에서 저장소를 복제한 뒤** 가상환경·의존성·`pytest`·**PyQt6 GUI 창**을 **같은 절차**로 재현할 수 있게, 루트 [`README.md`](../README.md)의 **「실행·테스트」** 절을 Report에 **독립 수출**한다.
- **대상 독자:** Windows / macOS / Linux에서 첫 온보딩하는 담당자, GUI만 먼저 띄우고 싶은 실습자, CI·에이전트 절차를 문서로 남기는 팀.
- **작성일:** 2026-04-28
- **버전:** 1.3

| 항목 | 값 |
|------|-----|
| 문서 유형 | 내부 보고서(로컬 실행 / GUI / pytest) |
| 제품/프로젝트명 | Magic Square (4×4) — TDD 연습 — [`MagicSquare_02`](../README.md) |
| 동기화 원문 | [`../README.md`](../README.md) — **§실행·테스트** (환경·`pip`·`pytest`·`python -m magicsquare.gui`) |
| 요구·검증 정본 | [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md) §3, §7, §9 (도구·러너) |
| 구현 참고 | [`../pyproject.toml`](../pyproject.toml) — `optional-dependencies.gui` = `PyQt6` |
| Screen 모듈 | [`../src/magicsquare/gui/`](../src/magicsquare/gui/) — `grid_ui.py`, `window.py`, `__main__.py` |

---

## 1. 전제 조건

| 항목 | 요구 |
|------|------|
| Python | **3.10 이상** — `python --version` |
| 작업 디렉터리 | Git clone(또는 압축 해제)한 **저장소 루트** (표준: `pyproject.toml`·`src/`·`tests/`가 보이는 위치) |

---

## 2. (선택) 가상환경

팀·로컬 정책에 따라 `venv`로 격리하는 것을 권장한다.

**PowerShell (Windows):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Bash / macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. 패키지 설치

### 3.1 라이브러리·테스트만 (PyQt 없음)

```bash
pip install -e .
```

Boundary·Domain 단위 테스트와 대부분의 `pytest` 수집은 이 상태로 가능하다.

### 3.2 GUI 및 UI 트랙 테스트 (PyQt6 포함)

[`pyproject.toml`](../pyproject.toml)의 **`[project.optional-dependencies]` → `gui`** extra를 설치한다.

```bash
pip install -e ".[gui]"
```

설치 확인 예:

```bash
pip show PyQt6
```

---

## 4. `pytest` 실행

저장소 루트에서:

```bash
pytest
```

경로를 나누어 돌리는 예:

```bash
pytest tests/domain -v
pytest tests/boundary -v
pytest tests/ui -v
```

### 4.1 UI 테스트와 PyQt 미설치

[`tests/ui/test_ui_magic.py`](../tests/ui/test_ui_magic.py)는 **`pytest.importorskip("PyQt6.QtWidgets")`** 로 보호되어 있다. PyQt6가 없으면 해당 케이스는 **스킵**되고, 나머지 스위트는 계속 실행된다. UI 테스트까지 **실행(통과)** 하려면 §3.2처럼 `pip install -e ".[gui]"` 가 필요하다.

---

## 5. GUI 프로그램 실행 (공식 진입점)

### 5.1 명령 한 줄

```bash
python -m magicsquare.gui
```

- **모듈 경로:** [`src/magicsquare/gui/__main__.py`](../src/magicsquare/gui/__main__.py)
- **의존성:** §3.2와 동일하게 PyQt6가 필요하다.

### 5.2 동작 요약

- [`QMainWindow`](https://doc.qt.io/qt-6/qmainwindow.html)에 [`MagicSquareWindow`](../src/magicsquare/gui/window.py) (내부에 [`GridUI`](../src/magicsquare/gui/grid_ui.py))를 올린 **MVP 창**이 열린다.
- 창 제목 예: `Magic Square 4×4 — Grid (MVP)`.
- 시작 시 [`__main__.py`](../src/magicsquare/gui/__main__.py)에서 **데모 격자**(빈칸 두 칸 `0`, 나머지 칸에 1~14를 각각 한 번씩·**순차 행 나열이 아니라 격자 전체에 섞인 배치**)를 `set_matrix`로 한 번 넣는다. `GridUI` 자체는 셀을 0으로만 만들 뿐이어서, 진입점에서 안 넣으면 화면이 모두 0처럼 보였다.
- MVP는 **4×4 숫자 스핀박스 격자 + 「풀기」 버튼 + 결과 표시**를 제공한다.
  - **정상 경로:** `GridUI.matrix()` → `magicsquare.boundary.validate()` → `magicsquare.magic_square.solve_magic_square()` → 6-튜플을 격자에 적용해 **0이 사라진 상태**로 화면에 반영한다.
  - **실패 경로(UX 개선):** 입력이 검증에 실패하거나 solver가 지원하지 않아도, 팝업으로 이유를 알리고 **데모 정답(골든 완성 격자)**을 격자에 채워 보여준다(입력과 무관하게 “정답 제시” 모드).

### 5.3 종료

창을 닫거나 터미널에서 프로세스를 종료하면 된다.

### 5.4 헤드리스·CI 참고

디스플레이가 없는 Linux 작업자나 일부 CI에서는 Qt가 **오프스크린** 플러그인을 요구할 수 있다. 로컬 Windows 데스크톱에서는 통상 불필요하다. 필요 시 환경 변수 예:

```bash
export QT_QPA_PLATFORM=offscreen   # Bash
```

(운영체제·런너마다 다르므로 CI 템플릿에 맞게 조정한다.)

---

## 6. 다른 Report·README와의 관계

| 문서 | 본 보고서(10)와의 관계 |
|------|-------------------------|
| [`README.md`](../README.md) | **동일 절차**를 유지한다. 갱신 시 README §실행·테스트와 **쌍으로** 수정하는 것을 권장한다. |
| [`07_Magic_Square_README_Repository_Guide_Report.md`](07_Magic_Square_README_Repository_Guide_Report.md) | 저장소 전체 안내 수출본; 본 문서는 **실행·GUI·pytest만** 분리 수출 |
| [`docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md) | 도구·러너·동일 재현 요구의 **정본** |

---

## 7. 변경 이력(본 문서)

| 버전 | 일자 | 내용 |
|------|------|------|
| 1.3 | 2026-04-28 | §5.2 — 「풀기」/결과 표시/0 제거 반영 + 실패 시 데모 정답 제시(UX) |
| 1.2 | 2026-04-28 | §5.2 — 데모 격자를 1~14 순차 배열이 아닌 섞인 배치로 시작 |
| 1.1 | 2026-04-28 | §5.2 — GUI 시작 시 데모 격자 채움(`__main__`), 전부 0처럼 보이던 이유 설명 |
| 1.0 | 2026-04-28 | 초판 — 로컬 환경·`pip`·`pytest`·`python -m magicsquare.gui`·헤드리스 참고 |

---

*제품 기능·납기 판정은 [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md)가 우선한다.*
