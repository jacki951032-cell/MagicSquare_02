# Magic Square (4×4) Git 브랜치·Pull Request 워크플로 보고서

## 개요

- **문서 목적:** TDD 단계명(`red` / `green` / `refactoring`)에 맞춘 브랜치 사용 의도, GitHub에서 Pull Request(PR)를 열 때 **비교할 차이가 없어졌던 사례**의 원인, 그리고 **권장 워크플로**를 Report 폴더에 기록한다.
- **대상 독자:** 저장소 소유자·협업자, Cursor/Git 학습자.
- **작성일:** 2026-04-28
- **버전:** 1.1

| 항목 | 값 |
|------|-----|
| 문서 유형 | 내부 보고서(저장소 운영·Git·PR) |
| 제품/프로젝트명 | Magic Square (4×4) — TDD 연습 — [`MagicSquare_02`](https://github.com/jacki951032-cell/MagicSquare_02) |
| 원격 저장소 | `https://github.com/jacki951032-cell/MagicSquare_02.git` |
| 관련 문서 | [`../docs/TEST_SPEC_Magic_Square_4x4.md`](../docs/TEST_SPEC_Magic_Square_4x4.md)(테스트 명세), [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md)(요구 정본), [`07_Magic_Square_README_Repository_Guide_Report.md`](07_Magic_Square_README_Repository_Guide_Report.md), [`09_Magic_Square_Dual_Track_RED_Test_Design_Report.md`](09_Magic_Square_Dual_Track_RED_Test_Design_Report.md)(Dual-Track RED 설계) |

---

## 1. 브랜치 이름과 TDD 단계

연습 목적으로 **`red` → `green` → `refactoring`(또는 `refactor`)** 순으로 브랜치를 두거나, **한 기능 브랜치 안에서 커밋 메시지로 RED/GREEN/REFACTOR를 구분**할 수 있다. 저장소에 **`red` 브랜치**를 만든 것은 이런 **RED 단계 작업**을 묶기 위함이다.

---

## 2. 발생한 상황(요약)

1. **`red`** 브랜치에서 변경(예: `docs/TEST_SPEC_Magic_Square_4x4.md` 추가)을 커밋했다.
2. 로컬에서 **`main`에 `red`를 fast-forward 머지**해, **`main`과 `red`가 동일 커밋**을 가리키게 되었다.
3. **`main`과 `red`를 모두** 원격(`origin`)에 push했다.

이 결과 GitHub 상에서 **`main`과 `red`의 최신 커밋이 같아져**, **`red` → `main` 방향의 PR**을 만들 때 **서로 다른 커밋이 없어** “비교할 내용이 없음”에 해당하게 된다. 이는 **실수라기보다 작업 순서**(먼저 `main`에 합친 뒤 양쪽을 push)가 **PR을 열기 위한 전형적인 순서**와 어긋난 경우이다.

---

## 3. GitHub에서 `red`가 “안 보이는” 것처럼 느껴질 때

원격에는 **`red` 브랜치가 존재할 수 있다.** 다만 저장소 기본 화면은 **`main`**만 보여 주므로, **브랜치 드롭다운**에서 `red`를 선택하거나  
`https://github.com/jacki951032-cell/MagicSquare_02/tree/red`  
처럼 **브랜치 경로로 직접 열어야** 한다.  
또한 **`main`과 커밋이 같으면** 파일 내용 차이는 없고, **브랜치 목록에서만** 구분된다.

---

## 4. PR을 열고 싶을 때 권장 순서

| 단계 | 내용 |
|------|------|
| 1 | `main`을 최신으로 맞춘 뒤 작업 브랜치 생성(예: `git switch -c red`). |
| 2 | **작업 브랜치에만** 커밋하고 `git push -u origin red`. 이때 **로컬에서 `main`에 머지하지 않는다.** |
| 3 | GitHub에서 **base: `main`**, **compare: `red`** 로 Pull Request 생성. |
| 4 | 리뷰·승인 후 GitHub에서 **Merge**하여 `main` 반영(또는 로컬에서 merge 후 push — 팀 규칙에 따름). |

**로컬에서 먼저 `main`에 merge하고 나서 `main`과 브랜치를 같이 push하면**, 원격 `main`에 이미 변경이 반영되어 **PR로 넣을 diff가 사라진다.**

---

## 5. 이미 `main`에 합쳐진 뒤라면

과거 시점의 **`red` → `main` PR**은 **히스토리를 되돌리지 않는 한** 새로 만들 수 없다. 이후 작업부터 위 **§4** 순서를 적용하면 된다.

---

## 6. 다른 Report와의 관계

| Report | 본 문서(08)와의 관계 |
|--------|----------------------|
| `07` | 저장소·README 안내; 본 문서는 **Git·PR 운영**에 초점. |
| `05` | PRD 내부 보고; 구현·테스트 **요구 정본**은 PRD·[`TEST_SPEC`](../docs/TEST_SPEC_Magic_Square_4x4.md). |
| `09` | Dual-Track **RED** 테스트 설계(UI-T·D-T); 작업 브랜치 예: `feature/dual-track-tdd`. |

---

## 7. Dual-Track TDD에 맞춘 브랜치 전략(요약)

운영 원칙은 **§4**와 동일하다: PR을 열려면 **먼저 로컬에서 `main`에 머지하지 않는다.**

| 방식 | 설명 |
|------|------|
| **한 토픽 브랜치 + 커밋 규약** | `feat/<기능명>` 또는 `feature/<설명>` 하나에서 RED→GREEN→REFACTOR를 **커밋 메시지**로 구분(예: `RED(ui):`, `RED(domain):`, `GREEN:`, `REFACTOR:`). 연습·소규모에 적합하다. |
| **단계별 브랜치(선택)** | `…-red` → `…-green` → `…-refactor`처럼 쪼개려면 **앞 단계가 `main`에 머지된 뒤** 다음 브랜치를 따거나, 한 브랜치에 통합하는 편이 관리 부담이 적다. |

**진행 순서(Dual-Track + TDD):** Dual-Track UI·Logic RED → GREEN(테스트 통과) → Dual-Track Refactoring — 각 단계는 위 브랜치/커밋 규약과 병행하면 된다.

---

## 8. 저장소에 추가된 브랜치(로컬 기준, 2026-04-28)

| 브랜치 | 목적 |
|--------|------|
| **`develop`** | 통합·스테이징용으로 둘 수 있는 장기 브랜치. `main`과 동일 커밋에서 생성 가능하다. 원격 반영: `git push -u origin develop`(네트워크 가능 시). |
| **`feature/dual-track-tdd`** | Dual-Track TDD(RED→GREEN→Refactor) **기능 작업**용 토픽 브랜치. `main`에서 분기해 사용한다. 원격: `git push -u origin feature/dual-track-tdd`. |

팀이 **`develop`을 기본 통합선**으로 쓰는 경우, PR의 base를 `develop`으로 두고 `main`은 릴리스만 받도록 규칙을 정하면 된다.

---

## 9. 변경 이력(본 문서)

| 버전 | 일자 | 내용 |
|------|------|------|
| 1.0 | 2026-04-28 | 초판 — `red`/main PR diff 이슈, 권장 PR 순서 |
| 1.1 | 2026-04-28 | §7 Dual-Track 브랜치 요약, §8 `develop`·`feature/dual-track-tdd`, Report `09` 참조 |

---

*본 보고서는 저장소 운영 경험을 정리한 것이며, 제품 기능·납기 판정은 [`../docs/PRD_Magic_Square_4x4_TDD.md`](../docs/PRD_Magic_Square_4x4_TDD.md)가 우선한다.*
