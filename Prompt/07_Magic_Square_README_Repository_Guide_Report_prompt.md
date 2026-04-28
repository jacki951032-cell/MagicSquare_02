# To-do list creation references
_Exported on 4/28/2026 at 10:57:34 GMT+9 from Cursor (3.2.11)_

---

**User**

Ｔｏ－Ｄｏ　리스트를 작성하고 싶습니다. 작성한 문서 중 무엇을 참조해서 만들어야 할까요?

---

**Cursor**

프로젝트 문서를 확인해 To-Do 리스트 작성에 참고할 자료를 파악합니다.



PRD 나머지 구조(테스트·섹션 번호)를 간단히 확인합니다.



To-Do 리스트를 **무엇을 할지(기능·검증 기준·테스트 ID)** 기준으로 잡으려면, 아래처럼 참고하면 됩니다.

## 1순위: `docs/PRD_Magic_Square_4x4_TDD.md`

이게 **한 통으로 쓰기 가장 좋은 문서**입니다. PRD 안에 이미 “할 일”을 나누는 뼈대가 들어 있습니다.

| 참고 섹션 | To-Do에 쓰는 방식 |
|-----------|------------------|
| **FR-01~FR-05** + 각 **AC-*** | 기능 단위 작업(입력검증 → 빈칸·누락수 → 판정 → 해찾기) |
| **§6 BR-01~BR-10** | 도메인 규칙·불변조건 체크리스트(구현/리뷰) |
| **§7 NFR-*** | 커버리지, 결정론, `M` 불변, (선택) 50ms 등 **품질 항목** |
| **§8** (Dual-Track) | “경계(UX·Contract) 테스트”와 “도메인(로직) 테스트”를 **같이** 진행할 일의 구분 |
| **§9** (`UI-T-*`, `D-T-*`, `T-S-01`~`05` 등) | **테스트/시나리오** 단위 To-Do로 바로 옮기기 좋음 |

PRD itself also says that **PRD·FR·BR·TC** should be traceable together — that is exactly the structure you want for a backlog.

## 보조(배경·맥락): `Report/01` ~ `06`

PRD 앞몸말에 **Report/01~04, Report/05**를 근거로 쓰라고 되어 있지만, 이 보고서들은 **문제 정의, Dual-Track, Cursor 규칙, 사용자 여정·추적성** 같은 **맥락·근거**용입니다. “오늘 무엇을 코딩·테스트할지” 목록의 **1차 출처**는 PRD이고, Report는 PRD의 어떤 FR/AC가 **왜** 그런지 더 보고 싶을 때 쓰면 됩니다.

---

**정리:** To-Do는 **`docs/PRD_Magic_Square_4x4_TDD.md`의 FR·AC·(원하면) BR·§9 테스트 ID**를 끊어서 쓰는 것이 맞고, `Report/*`는 필요할 때만 참고하면 됩니다.  
원하시면 PRD의 FR 순서(예: FR-04/05 전에 FR-01~03)에 맞춰 **To-Do 템플릿(체크리스트) 초안**도 여기에 바로 써 드리겠습니다.

---

**User**

당신은 시니어 소프트웨어 아키텍트이자 TDD 코치입니다. 할 일 목록의 항목과 완료 조건은 docs/PRD_Magic_Square_4x4_TDD.md를 주 소스로 두고, 스토리 단위 분해는 Report/*는 필요할 때만 참고해서 
다음 방법론을 적용하여
"Magic Square 4x4 완성 시스템"의 구현용 To-Do 구조를 작성하세요.

적용 방법론:
- Concept-to-Code Traceability
- Dual-Track UI + Logic TDD
- To-Do → Scenario → Test → Code 구조
- ECB(Entity / Control / Boundary) 모델
- RED → GREEN → REFACTOR

반드시 한국어로 작성하세요.

---

**Cursor**

PRD 전체를 확인해 To-Do 구조를 정확히 잡습니다.



PRD §12 추적성 매트릭스와 §8~10을 반영해 구현용 To-Do 구조를 작성합니다. `docs`에 보관용 파일을 추가합니다.



`docs/IMPLEMENTATION_TODO_Magic_Square_4x4.md`에 **구현용 To-Do 구조**를 정리해 두었습니다. 핵심만 요약합니다.

---

## 1. 주 소스와 추적 (Concept-to-Code)

- **할 일·완료 조건**은 PRD `docs/PRD_Magic_Square_4x4_TDD.md`만 **법적 기준**으로 둡니다.  
- PRD **§12 Traceability Matrix**를 “개념 → BR → FR → AC → Test → 논리 컴포넌트”의 **한 뷰**로 쓰고, 문서 안 **§3 표**로 T1~T7(입력~품질)로 압축해 두었습니다.  
- **Report/** 는 INV-D 전문·Gherkin 출처 등 **막힐 때만** 열도록 썼습니다.

## 2. To-Do → Scenario → Test → Code

- 각 본문 To-Do는 **동일 템플릿**으로 반복: Concept/Trace, **Scenario(§9.1 `T-S-*`)**, Track A·B **Test ID**, **ECB**, **RGR**, **PRD 완료 조건**.  
- **Code**는 ECB(아래)에 맞는 컴포넌트·최소 구현으로 채웁니다.

## 3. Dual-Track + RGR

- **트랙 A (Boundary)**: `UI-T-01`~`07` 등 — `code` / 고정 `message` / 6-튜플(§8.1, §4.2).  
- **트랙 B (Domain)**: `D-T-VAL*`, `D-T-JDG*`, `D-T-ASG*` — FR-02~05, BR(§8.2).  
- PRD **§8.3**대로, 스프린트(또는 일일)마다 A·B **둘 다** RED가 있어야 합니다. 순서는 **RED → GREEN → REFACTOR**.

## 4. ECB (PRD §10과 정합)

- **Entity**: 격자·좌표·`a,b` 등 순수 구조.  
- **Control**: FR-01 통과 후에만 FR-02→05, 시도1→2, **FR-05 미호출** 보장(스파이).  
- **Boundary**: `InputMatrixValidator` + **Presenter/Facade**, `E_NO_VALID_ASSIGNMENT` → `E_DOMAIN_FAILURE`+문구(§5.1).

## 5. Phase 구성 (스토리 절단)

- **P0**: 도구/CI, §9.3 Golden 격자.  
- **Phase 1~4**: **T1→T2·T3→T4→T5+T6** (FR-01뿐 → 좌표·누락 → FR-04 → FR-05·경계).  
- **Phase 5**: NFR(커버리지 등), (선택) §9.4.

자세한 항목 번호, AC 대응, `T-S-*` 연결은 **저장한 마크다운**을 열면 그대로 따라갈 수 있습니다.

---

**User**


[시스템 목표]
부분적으로 비어 있는 4x4 Magic Square를 완성하는 시스템의 개발 To-Do를 작성합니다.

[도메인 규칙]
- 보드는 4x4이다.
- 숫자는 1~16만 사용한다.
- 0은 빈칸이다.
- 정확히 2칸이 비어 있다.
- 0을 제외한 중복 숫자는 허용되지 않는다.
- 모든 행, 열, 대각선의 합은 34여야 한다.
- 해결 가능한 경우 빈칸 값을 찾아 채운다.
- 유효하지 않은 보드는 거부한다.

[출력 형식]
다음 구조를 반드시 지켜서 작성하세요.

1. Epic
2. User Story
3. Phase별 Task 목록
4. 각 Task에는 반드시 아래 정보를 포함하세요.
   - Task ID
   - RED / GREEN / REFACTOR 여부
   - 작업 제목
   - Scenario Level (L0/L1/L2/L3)
   - 연결되는 Test 이름
   - 연결되는 Code 대상
   - ECB 스테레오타입 (Entity / Control / Boundary)
   - 필요 시 체크포인트

[표현 스타일]
- Markdown 사용
- 체크박스 형식 사용
- 실제 Cursor.AI 실습용 개발 보드처럼 작성
- 식별자는 Epic-001, US-001, TASK-001 형식 사용
- 유효한 케이스와 실패 케이스를 모두 포함
- 최소한 다음 작업을 포함
  - 보드 생성
  - 보드 유효성 검사
  - 빈칸 탐지
  - 후보값 필터링
  - 완성 로직
  - 잘못된 입력 처리
  - 테스트 커버리지 체크포인트

[Scenario Level 정의]
- L0: 기능 개요
- L1: 정상 흐름
- L2: 경계 상황
- L3: 실패 상황

[추가 제약]
- Logic 책임은 명확히 분리할 것
- UI/Boundary에는 비즈니스 규칙을 넣지 말 것
- Control은 검증과 해결 흐름을 조율할 것
- Entity는 보드 상태를 표현할 것
- 모든 To-Do는 Scenario, Test, Code로 추적 가능해야 함

이제
"Magic Square 4x4 완성 시스템"의 To-Do 구조를 생성하세요.

---

**Cursor**

PRD의 FR·테스트 ID와 정합되도록 To-Do 구조 문서를 작성합니다.



PRD( FR-01~05, UI-T-*, D-T-*, T-S-* )와 맞추어 `docs`에 실습용 보드 형식의 To-Do를 작성합니다.



다음 문서에 요청하신 구조( Epic → User Story → Phase별 Task, 각 Task에 RGR·L0~L3·Test·Code·ECB·체크포인트, 체크박스, 식별자 형식, 성공/실패·최소 작업 포함 )로 정리해 두었습니다.

**파일:** `docs/TODO_Cursor_Practicum_Magic_Square_4x4.md`

---

## 요지

| 섹션 | 내용 |
|--------|------|
| **Epic-001** | 4×4·빈칸 2·합 34·PRD `FR-01`~`FR-05`·NFR·`T-S-*` 충족 |
| **US-001~003** | (1) 유효 격자 → 6-튜플/도메인 실패 (2) 잘못된 입력 → 4종 `E_*` + `message` (3) 흐름/결정론/커버·CI |
| **Phase** | **0** 보드·Factory·골든 픽스처 / **1** 유효성+잘못된 입력 / **2** 빈칸+누락(후보)쌍 / **3** `MagicSquareJudge`+`DualAssignmentResolver`+Present / **4** 커버·회귀·(선택) 50ms |

- **“후보값 필터링”** = PRD **FR-03** — 1~16 중 격자에 **없는 2수** (a,b), a&lt;b (`MissingNumberFinder`). 전수 탐색 CSP는 범위 밖이며, 문서에도 명시했습니다.
- **RGR**는 Task마다 **RED / GREEN / REFACTOR** 체크, 부분 카드(§4)에도 동일.
- **ECB:** Boundary=검증·`code`/`message`/DTO, Control=`DualAssignment`·`Judge`·`Locator` 등 조율/순수 도메인 로직, **Entity=보드(상태)**. Boundary에 34/대입 규칙 넣지 않는다고 적어 두었습니다.
- **TASK-040**이 **테스트 커버리지 체크포인트**(NFR-01, `T-S-05`)입니다.

PRD `UI-T-*`, `D-T-*`, `T-S-*`와 `FR-01`~`FR-05`에 맞춰 두었고, **상세·표·복붙용 Task 카드**는 위 마크다운을 열어 쓰면 됩니다.

---

**User**

Ｔｏ－Ｄｏ　리스트를  포함해 READMD.md 파일을 만들고 싶습니다. 무슨 문서를 참조하면 좋을까요?

---

**Cursor**

프로젝트에 있는 문서를 확인한 뒤 README 작성 시 참고할 자료를 정리합니다.



`README`는 아직 없고, `docs`에는 아래 네 가지가 있습니다. **README에 넣을 To-Do**를 정하려면 아래 순서로 참고하면 됩니다.

## 1. 꼭 넣는 문서(정본)

| 문서 | 역할 |
|------|------|
| [**`docs/PRD_Magic_Square_4x4_TDD.md`**](docs/PRD_Magic_Square_4x4_TDD.md) | **기능·완료 조건·`FR` / `AC` / 테스트 ID**의 1차 근거. README의 “이 프로젝트가 뭔지” `Executive Summary`·`Scope`도 여기서 요약하면 됨. |

README의 To-Do는 “무엇을 **다 했는지**”의 기준을 **PRD에 있는 AC / `T-S-*` 등**에 맞추는 것이 맞습니다.

## 2. To-Do 리스트 본문용(이미 만든 구현 보드)

| 문서 | 역할 |
|------|------|
| [**`docs/IMPLEMENTATION_TODO_Magic_Square_4x4.md`**](docs/IMPLEMENTATION_TODO_Magic_Square_4x4.md) | PRD 기반 **Phase / 방법론(Dual-Track, RGR, ECB)**·추적 표. **README에 “로드맵/Phase” 한두 단락**을 쓰거나 **링크만** 걸 때. |
| [**`docs/TODO_Cursor_Practicum_Magic_Square_4x4.md`**](docs/TODO_Cursor_Practicum_Magic_Square_4x4.md) | **Epic-001, US-001~003, TASK-0xx** 체크리스트. **README에 “체크박스 To-Do”**를 **복붙·요약**할 때 쓰기 좋음(길면 링크만 권장). |

보통 **README**에는 **짧은 소개 + 설치/실행 + `docs/PRD_...` 링크**를 두고, **긴 To-Do는 `TODO_Cursor_...` 또는 `IMPLEMENTATION_TODO_...`로 링크**하는 방식이 유지보수에 유리합니다.

## 3. 필요할 때만(보조)

| 위치 | 참고 |
|------|------|
| **`Report/*.md`** | 사용자 시나·추적성, `INV-D-*` 전문 등. README 필수는 아님. |
| **`src/.cursor/rules/.cursorrules`** (있다면) | 에이전트/코딩 룰. README “개발 시 규칙”에 한 줄로 링크할 수는 있음. |

---

**정리:** **요구·완료 기준 = PRD**, **실제 To-Do 항목·체크 = `TODO_Cursor_Practicum_...` 또는 `IMPLEMENTATION_TODO_...`** 를 참고하면 README와 잘 맞습니다.  
참고: 파일 이름은 **`README.md`** 이 맞고, `READMD.md`는 흔한 오타입니다.

원하시면 이 참조 구조(링크 + 짧은 To-Do)만 담은 `README.md` 초안을 저장소 루트에 만들어 드리겠습니다.

---

**User**

@c:\DEV\MagicSquare _02\ 에 있는 README 본문·To-Do·검증 기준은 docs/PRD_Magic_Square_4x4_TDD.md 를 중심에 두고, 스토리 표현은 ,오류·계약 요약, 실행·ECB·TDD, 문서 관계 한 줄 등은 Report/*를 참조해서 To-Do 리스트를 포함한 MagicSquare를 만들기 위한 README.md 파일을 만들어줘.


---

**Cursor**

PRD와 Report 문서를 읽어 README.md를 작성합니다.



README.md 작성 중입니다.



`c:\DEV\MagicSquare_02\README.md`를 추가해 두었습니다.

## 구성 요약

| 섹션 | 출처 |
|--------|------|
| **한 줄 요약·문제의 본질** | PRD Executive Summary, §2 |
| **문서 관계(표 + 한 줄)** | Report/05 “문서 간 정렬” + 01~06, `docs/PRD*`, `docs/TODO*` |
| **User Story(3개, 요지)** | Report/04 (입력 검증·빈칸·누락+해) |
| **오류·계약** | PRD FR-01 표, §5.1 도메인/경계, 성공 `int[6]` |
| **ECB** | PRD §10, Report/04 “Domain 분리” |
| **실행·pytest·coverage·T-S·9.3** | PRD §3, §7, §9, Report/04 성공 기준(참고) |
| **Dual-Track TDD** | PRD §1.1, §8 |
| **To-Do 체크리스트** | PRD `FR-01`~`FR-05` + P0 + NFR, 상세는 `docs/TODO_Cursor_Practicum_...`로 링크 |
| **검증 기준(마지막 문장)** | PRD AC, NFR, T-S, INV-D는 Report/02·§6·§12 동기 |

**판정 우선순위**는 README 끝에 “**법적/납기는 PRD 우선**”으로 적어 두었습니다.  
파일 경로: `README.md` (저장소 루트).

---

**User**

Report 폴더에 보고서로 내보내주세요

---

**Cursor**

README를 Report 폴더 보고서 형식으로 맞춰 내보냅니다.



Report/07에 README 내용을 보고서 형식(개요·동기·본문)으로 내보냅니다. `Report` 기준 상대 링크로 정리합니다.



README의 ‘문서 관계’ 표에 `Report/07` 링크를 한 줄 추가해 동기화합니다.



작업 반영했습니다.

## 내보낸 보고서

- **경로:** [`Report/07_Magic_Square_README_Repository_Guide_Report.md`](c:\DEV\MagicSquare_02\Report\07_Magic_Square_README_Repository_Guide_Report.md)
- **내용:** `README.md`와 같은 본문(요약, 문서 지도, User Story, 오류·계약, ECB, 실행·테스트, TDD, To-Do) + **보고서 머리**  
  - 문서 목적, 대상 독자, 작성일, 버전, `README`와 **동기 권장** 안내  
  - `07`과 `01`~`06`·`README` 관계 **부록 표**  
  - `Report` 폴더 기준으로 **상대 링크**(`../docs/...`, `../README.md`, 동일 폴더 `01_`~`06_` 파일)  
  - **Document change log** (1.0)

루트 [`README.md`](c:\DEV\MagicSquare_02\README.md)의 **“문서 관계”** 표에 **07 수출본** 링크 한 행을 넣어, README ↔ Report가 서로 가리키도록 맞춰 두었습니다.

---

**User**

이걸 참고해서@README.md 파일 내용 중 To-Do list를 작성해주세요. 자세하게 생각해서 이해하기 쉽게..(sequence thinking)

---

**Cursor**

README.md의 To-Do 섹션을 이미지의 Epic→US→TASK·RGR·C2C 추적 형식으로 상세화합니다. 현재 README를 확인합니다.



To-Do 섹션을 이미지의 Epic→US→TASK·RGR·시나리오·C2C 매트릭스 형식으로 대체·확장합니다.



`README.md`의 **To-Do** 구간을 이미지에 맞춰 **① 단계·의존 설명( sequence )** ② **Epic-001 → US-000~006 → TASK-0xx** ③ **TASK-010-1/2/3 (RED / GREEN / REFACTOR) 예시** ④ **Checkpoint** ⑤ **C2C 요약 표(Task·Req·L·Test·상태)** 로 바꿔 두었습니다.

## 반영한 구조(요지)

| 요소 | README 안에서의 쓰임 |
|------|------------------------|
| **Sequence** | FR-01 → Control(미호출) → FR-02·03 → FR-04 → FR-05 → NFR 순 **왜** 그런지 6줄. §8.3(경계만 뒤로 미루기 금지) 한 줄. |
| **Epic / US / TASK** | `Epic-001` 아래 `US-000`~`006`으로 **FR**과 1:1에 가깝게 쪼갬. |
| **RGR** | `TASK-010`에 **-1 RED / -2 GREEN / -3 REFACTOR**; `US-006`·`TASK-060`에 REF 예시. |
| **L0~L3 + UI** | 표·Task 줄에 *L0/L1/L2/L3 / UI·계약*로 표기(이미지의 Happy/Edge/Fail·UI). |
| **C2C** | “Task → Req( **FR-01** ) → 시나 L → 테스트( Track ) → 코드” + **Traceability 요약 테이블** + 마지막 “C2C 한 문장”. |
| **Checkpoint** | `> [Checkpoint] ...` 형식( TASK-001~002, US-001, US-002, US-005 ). |
| **오타** | `인프RA` → `인프라`. PRD 앵커는 깨질 수 있어 **파일 링크**만 쓰도록 정리. |

이제 **보드(ENTITY)**·**검사기**·**RGR 3스텝**·**트레이싱 테이블**이 한 덩어리로 읽히게 맞춰 두었고, **세부 Epic/TASK 번호(예: TASK-101~)** 는 [`docs/TODO_Cursor_Practicum_Magic_Square_4x4.md`](docs/TODO_Cursor_Practicum_Magic_Square_4x4.md)와 **어긋날 수 있으니** (README는 010·020·030… 축) 동기 점검은 원하면 그 문서와 맞출 수 있습니다.  
`Report/07` **수동 동기**가 필요하면 말해 주세요.

---

**User**

해주세요

---

**Cursor**

README의 최신 본문(특히 To-Do)을 `Report/07`에 동기화합니다.



Report/07을 README의 §1.3 To-Do 전체로 동기화하고, `Report` 기준 링크를 조정하며, README의 표 오타(인프RA)를 수정합니다.



작업 반영했습니다.

## 한 일

1. **[`Report/07_Magic_Square_README_Repository_Guide_Report.md`](c:\DEV\MagicSquare_02\Report\07_Magic_Square_README_Repository_Guide_Report.md)**  
   - 옛 **짧은 To-Do**를 [`README.md`](c:\DEV\MagicSquare_02\README.md) **§1.3**과 동일한 본문으로 바꿨습니다.  
   - **Epic-001 / US-000~006 / TASK-0xx / RGR / Checkpoint / C2C 표 / sequence** 전부 포함.  
   - 링크는 `Report` 기준으로 정리: `../docs/...`, `../docs/TODO_...`, Report/02는 동일 폴더 `02_Magic_Square_...`  
   - **“문서 관계”** 표에 **07(본 문서)** 한 행 추가.  
   - 메타: **v1.1**, 개요·선행·참고·각주에 **README §1.3** 동기 명시.  
   - **Document change log**에 **1.1** 항목 추가.

2. **[`README.md`](c:\DEV\MagicSquare_02\README.md)**  
   - C2C 표 **TASK-001** 행 오타 `인프RA` → **`인프라`** 수정(07과 맞춤).

이제 **루트 README**와 **Report/07**의 To-Do·트레이싱은 같은 내용이며, 07만 열어도 C2C 구조를 그대로 쓸 수 있습니다. 앞으로 README의 §1.3을 고칠 때 **07도 같이** 맞추면 됩니다.

