# Magic Square TDD PRD documentation
_Exported on 4/28/2026 at 08:42:16 GMT+9 from Cursor (3.2.11)_

---

**User**

당신은 시니어 제품/소프트웨어 아키텍트이며 Dual-Track UI + Logic TDD 및 Concept-to-Code Traceability 전문가입니다. 
PRD 본문 골격은 Report/4를 축으로 하고, Report/1로 문제·동기를 보강하며, 기능·계약·성공 정의는 Report/2, 품질·개발 원칙은 Report/3(및 cursor 규칙) 에서 가져오는 방식으로 다음 내용을 고려해 docs 폴더에 PRD를 작성해 주세요.


프로젝트: Magic Square (4x4) — TDD 연습용
목적:
- 알고리즘 난이도보다 TDD 훈련이 목적
- Invariant 기반 설계/검증 사고를 체득
- 입력/출력 계약을 명확히 고정
- UI/DB/Web 의존성 없이 순수 로직 중심으로 구현 가능하게 PRD 작성

⚠️ 중요 규칙
- 구현 코드를 작성하지 마십시오.
- 새로운 기능을 추가하지 마십시오. (요구사항 범위 유지)
- 모호한 표현(“적절히”, “충분히” 등)을 사용하지 마십시오.
- 모든 요구사항은 테스트/검증 가능해야 합니다.
- Dual-Track(경계/도메인) 분리를 문서 구조에 반영하십시오.
- Concept → Rule → Use Case → Contract → Test → Component 추적성을 반드시 포함하십시오.
- 출력은 구조화된 Markdown으로 작성하십시오.

------------------------------------------------------------
[입력/출력 계약(고정)]
------------------------------------------------------------

입력(Input):
- 4x4 정수 행렬 int[][]
- 0은 빈칸
- 빈칸(0)은 정확히 2개
- 값 범위: 0 또는 1~16
- 0을 제외한 중복 숫자 금지
- 첫 번째 빈칸 정의: row-major(행 우선) 스캔 시 먼저 발견되는 0

출력(Output):
- int[6]
- 좌표는 1-index
- 포맷: [r1, c1, n1, r2, c2, n2]
- n1,n2는 누락 숫자 2개
- 시도 1: 작은 수 → 첫 빈칸, 큰 수 → 둘째 빈칸
  - 마방진이면 그 순서 반환
- 시도 2: (시도 1 실패 시) 큰 수 → 첫 빈칸, 작은 수 → 둘째 빈칸
  - 마방진이면 역순 반환
- 두 시도 모두 실패 시 오류 정책에 따라 처리(명시 필수)

마방진 상수(Magic Constant):
- n=4 → 34


---

**Cursor**

Report 1–4와 관련 자료를 읽어 PRD에 반영합니다.



`docs` 폴더를 만들고 Report 1–4와 고정 I/O·오류 정책을 통합한 PRD를 작성합니다.



사용자 규칙에 따라 `§` 기호를 제거하고 읽기 쉬운 참조로 바꿉니다.



`§` 제거 및 92–93행 이스케이프 오류 확인 중.



91행의 잘못된 `\(b\)\` 를 수정하고, 모든 `§` 참조를 정리합니다.



I-06의 '3.3' 참조를 '3.3절'로 바로잡고, 남은 `§`·오타(빈침)를 일괄 수정합니다.



작업을 반영했습니다. `docs/PRD_Magic_Square_4x4_TDD.md`에 PRD를 두었습니다.

## 요약

- **골격**: `Report/04` — Epic, Journey, User Story(S-1~5), Gherkin·검증 흐름.
- **문제·동기**: `Report/01` — 표면 vs 본질, TDD·Invariant·결정성(2절).
- **계약·Dual-Track·매트릭스 ID**: `Report/02` — I/O, 도메인/경계, `E_*`, 테스트 ID·커버리지 목표.
- **품질·TDD·ECB**: `Report/03` — RED/GREEN/REFACTOR, pytest·커버리지, 금지 규칙(7~8절).

**고정해 둔 사항(요청 반영)**  
- 입력: 4×4 `int[][]`, 0=빈칸 2곳, 0 또는 1~16, 0 제외 중복 없음, **첫 0 = row-major 첫 0**.  
- 출력: `int[6]`, 1-index, 시도1(작→첫, 큰→둘) 통과 시 단락, 아니면 시도2(큰→첫, 작→둘) → `[r1,c1,b,r2,c2,a]`, 둘 다 실패 시 **`E_NO_VALID_ASSIGNMENT` / `E_DOMAIN_FAILURE` + 고정 `message`**.  
- **구현 코드 없음**, 범위 밖 기능 추가 없음, `§` 기호는 UI 가독성을 위해 `3절`·`3.3절` 등으로 치환함.

**Concept → Rule → Use Case → Contract → Test → Component**는 9절 표로 정리했고, **Dual-Track**은 6절에서 Logic vs Boundary(선택)로 나눴습니다. **순수 로직**은 1.3·6절에서 “핵심 납품”으로, DB/웹/선택 Data는 비핵심으로 구분했습니다.

---

**User**


------------------------------------------------------------
[PRD 작성 지시]
------------------------------------------------------------

아래 구조를 반드시 지켜 PRD를 작성하십시오.

# 1. Executive Summary
- 한 문단 요약
- 프로젝트가 훈련하려는 핵심 역량(불변조건/계약/TDD)

# 2. Problem Statement (문제 정의)
- “마방진을 만든다”가 아니라 “불변조건을 검증 가능한 형태로 완성한다” 관점으로 정의
- 왜 입력/출력 계약이 핵심인지 설명

# 3. Target Users
- TDD 학습자/리뷰어 관점
- 사용 목적/사용 환경(콘솔/테스트 실행)

# 4. Scope
## 4.1 In-Scope
- 빈칸 좌표 찾기
- 누락 숫자 찾기
- 마방진 판정
- 두 조합 시도 후 결과 반환
- 입력 검증(경계 레이어)
## 4.2 Out-of-Scope
- UI 화면 개발
- DB 저장/조회
- N×N 일반화(기본 PRD 범위 제외, 확장 항목으로만)
- 마방진 “생성” 알고리즘(완전 생성 문제)

# 5. Functional Requirements (기능 요구사항)
각 기능마다 아래 템플릿을 반복해서 작성하십시오:
- Feature ID
- 설명(1~2문장)
- 입력
- 처리 규칙(불변조건 포함)
- 출력
- 승인 기준(AC) — 반드시 테스트 가능 문장으로
- 관련 오류/예외 정책

필수 기능 목록:
- FR-01 입력 검증 (Boundary)
- FR-02 빈칸 탐색
- FR-03 누락 숫자 탐색
- FR-04 마방진 판정
- FR-05 해 찾기(solution): 두 조합 시도 및 반환

# 6. Business Rules (도메인 규칙)
- BR-01 ~ 형태로 나열
- “항상 참이어야 하는 규칙”으로 서술
- 예: 중복 금지, 합 규칙, 좌표 인덱스 규칙, row-major 규칙 등

# 7. Non-Functional Requirements
- 테스트 커버리지 목표:
  - Domain Logic 95%+
  - Boundary Validation 85%+
- 결정론적 실행(동일 입력 → 동일 출력)
- 부작용 금지(입력 행렬 변경 정책 명시)
- 성능 기준(선택): 4x4 기준 즉시 처리(예: 50ms 내)

# 8. Dual-Track TDD Strategy
## 8.1 Track A — Boundary(UI) TDD
- Contract-first 테스트 항목 목록
- 실패 정책(예외 타입/메시지 표준)
## 8.2 Track B — Domain(Logic) TDD
- 메서드 단위 테스트 목록
- 불변조건 테스트 목록
## 8.3 병렬 진행 규칙
- UI RED & Logic RED → UI GREEN & Logic GREEN → REFACTOR
- “도메인 먼저 다 구현 후 경계 추가” 금지

# 9. Test Plan (QA)
- 시나리오 기반 테스트 목록(정상/역순 성공/실패/입력오류)
- 회귀 테스트 정책
- 테스트 데이터(대표 4x4 예시 행렬) 포함
- Property/Invariant 기반 체크 항목

# 10. Architecture Overview (High-Level)
- 레이어 정의:
  - Boundary Layer(입력검증/출력형식)
  - Domain Layer(순수 로직)
- 책임 분리(SRP)와 확장(OCP) 전략
- 의존성 방향(도메인이 경계를 모르게)

# 11. Risks & Ambiguities
- 모호한 부분을 “결정 항목”으로 명시(예: 두 시도 모두 실패 시 정책)
- 자주 실수하는 포인트(1-index, row-major, 입력 변경 여부 등)

# 12. Traceability Matrix (필수)
다음 형식으로 표를 제공하십시오:
Concept/Invariant → Business Rule → Feature(FR) → Acceptance Criteria → Test Case → Component

------------------------------------------------------------
출력 요구사항
------------------------------------------------------------
- 전체를 Markdown으로 출력
- 번호/ID 체계 일관성 유지
- 구현 코드 작성 금지
- 모든 요구사항은 검증 가능 문장으로

---

**Cursor**

기존 PRD의 고정 계약·오류 정책을 유지하며, 요청하신 12절 구조로 문서를 작성합니다.



12절 구조로 `docs/PRD_Magic_Square_4x4_TDD.md`를 전면 재작성합니다.



문서가 길어 `Write`로 핵심을 담은 전체 PRD를 작성한 뒤, 필요 시 보강합니다.



요청하신 **1~12절 구조**로 `docs/PRD_Magic_Square_4x4_TDD.md`를 **버전 2.0**으로 다시 썼습니다. 구현 코드는 넣지 않았고, AC·BR·오류는 **검증 가능한 문장**으로 맞춰 두었습니다.

**포함된 절목**  
1 Executive Summary — 2 Problem Statement — 3 Target Users — 4 Scope (4.1 In / 4.2 Out) — 5 Functional (FR-01~05, 템플릿·AC·오류) — 6 Business Rules (BR-01~10) — 7 NFR (커버리지 95/85%, 결정론, 입력 불변, 50ms 선택) — 8 Dual-Track (8.1~8.3) — 9 Test Plan (시나리오, 회귀, 예시 격자, property) — 10 Architecture — 11 Risks & 결정 — 12 Traceability Matrix (요청 형식).

**일관 ID**  
- `FR-01`~`FR-05`, `BR-01`~`BR-10`, `AC-xx-yy`, `E_*` + 고정 `message`, `INV-D-*`·테스트 ID·논리 컴포넌트를 12절 표로 연결했습니다.

전문은 워크스페이스의 [`docs/PRD_Magic_Square_4x4_TDD.md`](c:\DEV\Magic_Square_XXX\docs\PRD_Magic_Square_4x4_TDD.md)에서 확인하시면 됩니다.

---

**User**

Report 폴더에 보고서 형식으로 올려주세요

---

**Cursor**

Report 폴더의 기존 보고서 명명·형식을 확인한 뒤 PRD를 보고서 형식으로 추가합니다.



`docs`의 PRD 전체를 복사한 뒤, Report 폴더 보고서 양식(제목·개요·문서 메타)을 앞에 붙이고 제목 수준을 정리합니다.



문서를 복사한 뒤 보고서 전용 머리말을 붙이고, 제목 단계(`#` → `##`, `##` → `###`)를 정리합니다.



`Report` 폴더에 **보고서 형식**으로 PRD를 올려 두었습니다.

**파일:** `Report/05_Magic_Square_PRD_Report.md`

**적용한 보고서 형식**
- **H1** 보고서 제목: *Magic Square (4×4) 제품 요구사항(PRD) 보고서*
- **개요**: 문서 목적, 대상 독자, 작성일, 버전, `docs`와의 동기화 안내
- **메타 표**: 문서 유형(내부 보고서)·프로젝트명·선행 Report 참조
- **부록: 문서 간 정렬**: `01`~`04`와 05번 본문 절(2·4~6·7~8·3~5·9~12 등) 매핑
- 본문: **1~12절**은 `##`로, **4.1/4.2, FR-01~05, 8.x, 9.x**는 `###`으로 단계를 내려, 상위 01~04 보고서와 맞는 계층으로 정리
- **FR-05** 부작용 주석: `(7.3)` → `(7절 NFR-03)`으로 절 번호에 맞게 수정
- 말미에 짧은 **“문서 끝”** 구분

**동기화:** `docs/PRD_Magic_Square_4x4_TDD.md` 메타 `근거`에 `Report/05` 를 넣어 두었고, 05 `개요`에도 `docs` 경로를 적어 두었으니, 수정 시 **둘 다 같이** 고치는 편이 좋습니다.

