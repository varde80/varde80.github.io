# Data Schemas & Conventions

AIMAT Lab 사이트의 `src/data/*.json` 파일별 스키마와 프로젝트 컨벤션. content-editor와 schema-guardian이 참조한다.

## 목차
- [파일 인벤토리](#파일-인벤토리)
- [공통 컨벤션](#공통-컨벤션)
- [members.json](#membersjson)
- [professor.json](#professorjson)
- [research.json](#researchjson)
- [projects.json](#projectsjson)
- [facilities.json](#facilitiesjson)
- [journals.json / conferences.json / preprints.json](#journalsjson--conferencesjson--preprintsjson)
- [IF.json](#ifjson)
- [software.json](#softwarejson)
- [news.json](#newsjson)
- [contact.json](#contactjson)

## 파일 인벤토리

| 파일 | 역할 | id 형식 | 이미지 폴더 |
|------|------|--------|------------|
| `members.json` | 연구원/학생/인턴/동문 | `r{N}`/`phd{N}`/`ms{N}`/`int{N}` | `public/images/members/` |
| `professor.json` | 교수 1인 (object) | — | `public/images/members/` |
| `research.json` | 5개 연구분야 (array) | `research{N}` | `public/images/research/` |
| `projects.json` | 펀딩 프로젝트 | `proj{N}` | — |
| `facilities.json` | 장비/시설 | `f{N}` | `public/images/facilities/` |
| `journals.json` | 저널 논문 | `pub{N}` | `public/images/publications/` |
| `conferences.json` | 학회 논문 | `conf{N}` | `public/images/publications/` |
| `preprints.json` | preprint/submitted | `prep{N}` | `public/images/publications/` |
| `IF.json` | journal name → IF dict | — (object) | — |
| `software.json` | 오픈소스 SW | `sw{N}` | `public/images/software/` |
| `news.json` | 뉴스/갤러리 | `g{N}` | `public/images/news/` |
| `contact.json` | 연락처 (object) | — | — |

## 공통 컨벤션

### id 발급
- 같은 종류 파일 내에서 가장 큰 숫자 + 1.
- members.json의 각 카테고리는 독립 카운터 (phdStudents의 phd3 다음은 phd4, msStudents와 무관).
- 동문(alumni)으로 이동 시 원래 id 유지 — 새 id 발급 금지.

### 이미지 경로
- JSON 필드 값: `/images/{category}/{filename}` (앞에 `/` 필수, `public` 포함하지 않음).
- 실제 파일: `public/images/{category}/{filename}`.
- 파일명 컨벤션: 대소문자 혼합 허용. 공백·한글은 피하고 영문 소문자/숫자/`_`/`-` 권장.

### 다국어 필드 (projects.json 전용)
- `title`, `role`: `{ ko: string, en: string }`. 두 키 모두 필수, 빈 문자열 허용.
- `period`, `fundingAgency`, `fundingAmount`: `string | { ko, en }`. 보통 string으로 단일 표기.

### 저자 표기 (publications)
- `^` (이름 뒤): lab 멤버 강조 (예: `"Ho Won Lee^"`).
- `*`: 교신저자 (예: `"Ho Won Lee^*"`). **PI 전용 — 아래 규칙 참조.**
- `+`: 제1저자/공동제1 (예: `"Hoang Hai Nam Nguyen^+"`).
- 마커는 의무 아님. 같은 인물 표기는 파일 간 일관성 유지.

**중요 — 학회 발표(conferences.json)는 `*` 마커 생략:** 학회 발표 항목에서는 교신저자 `*`를 사용하지 않는다. lab 멤버 `^`와 공동제1 `+`만 표기한다 (예: `"Ho Won Lee^"`, `"Hoang Hai Nam Nguyen^+"`). 이는 발표 형식에서는 교신저자 개념이 약하기 때문이다. journals.json·preprints.json에서는 `*` 표기를 유지하되 아래 PI 전용 규칙을 따른다.

**중요 — `*` 마커는 PI 전용 (2026-07-21):** journals.json·preprints.json에서 `*`는 PI(Ho Won Lee, 축약형 `H.W. Lee` 포함)가 교신저자인 경우에만 표기한다. 교신저자가 PI가 아니면(외부 협력자든 lab 멤버든) `*`를 붙이지 않으며, 공동 교신인 경우에도 PI만 `*`를 유지한다. 사유: 사용자 피드백 "corresponding author가 내가 아닌 경우에는 * 제외" — 기존 비-PI `*` 8건은 2026-07-21에 일괄 제거됨.

### Quasi-lab 명단 (members.json에 없어도 `^` 적용)

다음 인물은 lab roster에 등재돼 있지 않지만, 과거 협력·졸업 등으로 lab과 강하게 결합돼 있어 publications에서 `^` 마커를 유지한다:

- **Han-Jun Lee** — conf4 등 다수 기존 entry에서 `^` 사용. 새 entry 추가 시 동일 처리.

새 quasi-lab 인물을 추가하려면 이 섹션과 schema-guardian의 검증 로직을 함께 갱신한다.

### Venue 필드 허용 값

- `Venue?: string` — 미인쇄 시 필드 생략 또는 `null` 허용. 빌드(`vue-tsc`)와 런타임 모두 통과 확인됨. content-editor는 가능한 한 null 대신 필드 생략을 선호.

### 다국어 제목 (publications)
원본 입력의 제목이 한국어인 경우, `title` 필드는 다음 형식을 사용한다:

`"<한국어 원문> (<English Translation>)"`

예시:
- 원문 "딥러닝을 이용한 철강 소재 열처리 공정–미세조직–기계적 물성 연계 모델링 기법 개발"
- 저장 형식: `"딥러닝을 이용한 철강 소재 열처리 공정–미세조직–기계적 물성 연계 모델링 기법 개발 (Development of Deep Learning-Based Modeling Methodology Linking Heat Treatment Process–Microstructure–Mechanical Properties for Steel Materials)"`

규칙:
- 원본이 영어 제목이면 영어만 저장 (한국어 추가 금지).
- 원본이 한국어인데 영어 번역이 학회 자료에 함께 표기돼 있으면 그 번역을 사용 (공식 영문명 우선).
- 그 외에는 collector가 학술 직역.
- 한국어 부분은 원문 그대로 (맞춤법·띄어쓰기 보존).

### date / period 포맷
- date: ISO `YYYY-MM-DD` (예: `"2025-11-26"`).
- year: 4자리 정수 (예: `2025`, not `"2025"`).
- period: `YYYY.MM - YYYY.MM` 또는 `YYYY.MM-YYYY.MM` 또는 `YYYY.MM-Present`.

## members.json

```typescript
interface MembersData {
  researchers: Member[]   // postdoc
  phdStudents: Member[]
  integratedStudents: Member[]   // 석박사통합과정, id ip{N}
  msStudents: Member[]
  Intern: Member[]        // 대문자 I 주의
  alumni: Member[]
}
interface Member {
  id: string
  name: string
  position: string
  email: string           // 빈 문자열 허용
  image: string           // /images/members/...
  research?: string       // 자유 텍스트
  year?: number           // 입학/시작 연도
}
```

### 멤버 졸업(이동) 절차
1. 원본 카테고리(phdStudents 등)에서 항목 pop.
2. `alumni`에 push. id 유지.
3. `position` 변경: e.g. `"Ph.D. Candidate"` → `"Ph.D. (YYYY)"`.
4. `research` 필드: 졸업 후 직장이 주어졌으면 그 값, 아니면 빈 문자열.
5. `year`: 졸업 연도로 갱신 (선택).

### 멤버 추가 시 필수
- id, name, position, image, year (학생/인턴의 경우).
- email은 빈 문자열로 둘 수 있음.
- image는 placeholder 사용 불가 — 사진이 없으면 사용자에게 요청 또는 `_workspace`에 보류.

## professor.json

단일 객체 (배열 아님). 필드: `name`, `title`, `email`, `phone`, `image`, `education[]`, `experience[]`, `Research Interests[]`(문자열 또는 `{category, items[]}` 그룹 객체 혼용 가능 — CV에서 대분류 굵은 제목 + 서브 항목 들여쓰기로 렌더링, `ko` 블록도 동일 구조), `Honors and Awards[]`, `Professional Activities/Memberships[]`. 추가/수정 시 기존 키 이름(대소문자 포함)을 그대로 유지.

## research.json

5개 연구분야 고정 (research1~research5). 새 분야 추가/삭제는 사이트 네비게이션·홈페이지에도 영향 — 사용자 명시 확인 후에만.

```typescript
interface ResearchArea {
  id: string              // research{N}
  title: string
  description: string
  image: string           // /images/research/...
  details: string[]       // 3~5개 권장
}
```

## projects.json

```typescript
interface Project {
  id: string              // proj{N}
  title: { ko: string, en: string }
  period: string | { ko, en }
  role: { ko: string, en: string }
  fundingAgency: string | { ko, en }
  fundingAmount?: string | { ko, en }   // 미공개 가능
  status: 'ongoing' | 'completed'
}
```

`fundingAmount` 표기: `"30.5B KRW"` (billion), `"0.97B KRW"`, `"89M KRW"` (million). 단위 일관성 유지.

`role.en` 표준 값: `PI`, `Co-PI`, `Co-Investigator`, `Participant`.

## facilities.json

```typescript
interface Facility {
  id: string              // f{N}
  name: string
  description: string
  image: string           // /images/facilities/...
  manufacturer?: string
  model?: string
  specifications?: string[]
}
```

## journals.json / conferences.json / preprints.json

세 파일 모두 `Publication[]` 형태이지만 일부 필드가 다름.

```typescript
interface Publication {
  id: string                          // pub{N}/conf{N}/prep{N}
  type?: 'journal' | 'conference'     // preprints.json은 보통 'journal'
  title: string
  authors: string[]                   // 마커 포함 ("Name^*")
  year: number
  featured?: boolean                  // default false
  highlightImage?: string             // /images/publications/... (선택)

  // journals/preprints 전용
  journal?: string
  volume?: string
  pages?: string
  doi?: string
  status?: string                     // preprints: "Preprint" | "Submitted" | "Accepted"

  // conferences 전용
  "Conference Name"?: string          // 따옴표 키 (공백 포함)
  "start date"?: string               // "YYYY.M.D"
  "end date"?: string
  Venue?: string
  scope?: 'domestic' | 'international'  // KIM·KSTP·KSME 등 국내 학회 = "domestic", TMS·ICCV 등 = "international"
}
```

### Grant 번호 (`grants`) 규칙 (2026-09-09)

- 논문 원문의 **Acknowledgments / Funding / 감사의 글** 문단에 적힌 과제 번호를 **원문 표기 그대로** 배열로 기록한다. 예: `["RS-2024-00451579", "PNKB300"]`, `["2022R1C1C1012700", "P0022331"]`.
- 번호만 기록한다. "Project No.", "Grant No.", "(", ")" 같은 접두어·괄호는 제거하고, 하이픈·대소문자는 원문 그대로 둔다 (`RS-2024-00451579`, `2021RIS-001`, `PNKA640`).
- 사사에 적힌 모든 번호를 순서대로 넣는다 (PI 과제가 아니어도, 해외 기관 과제여도 포함). 기관명만 있고 번호가 없는 사사(예: "supported by Konkuk University")는 항목을 만들지 않고 필드를 생략한다.
- 원문 오타는 사용자 확인 후 정정한다. 확정된 정정: `P00223311` → `P0022331` (2026-09-09, 사용자 확인 "P0022331 맞아"). 새 오타 의심은 notes에 남기고 사용자에게 묻는다.
- 원문 PDF가 없어 사사를 확인할 수 없으면 필드를 생략한다 (추측 금지). 논문 원문 아카이브: `~/Dropbox/1_Projects/Prof/Resources/5_Papers/paper/`.
- UI: PublicationCard가 Projects 페이지의 PI/Co-PI 배지와 같은 pill 스타일로 "GRANT" 라벨 옆에 번호를 나열한다.

### Conference scope 분류 규칙

새 학회 항목 추가 시 `scope` 필드를 반드시 지정한다:
- **domestic** — 대한금속·재료학회(KIM), 한국소성가공학회(KSTP), 한국기계학회(KSME) 등 한국에서 주최되는 학회. Venue가 한국 국내인 경우.
- **international** — TMS, ICCV, NeurIPS, ICME 등 국제 학회. Venue가 해외이거나 영문 공식명을 가진 다국적 학회.

판별이 모호하면 (예: 한국에서 열리지만 영어 공식 학회) `Venue`의 국가 표기를 1차 기준으로 사용한다.

### Featured publication
- `featured: true`로 표시하면 홈페이지 highlight 섹션에 노출.
- `highlightImage` 함께 지정 권장.

### Preprint → published 전환
- `preprints.json`에서 제거 → `journals.json`에 추가.
- id는 새로 발급(`pub{N}`). 기존 prep id는 재사용 금지(과거 링크 보존).
- `status` 필드 제거.

## IF.json

```typescript
type IFData = Record<string /* journal name */, string /* "IF X.X, JCR Y%" */>
```

새 저널 추가 시 `IF X.X, JCR Y%` 또는 `IF X.X, JCR Qn` 형식 유지.

## software.json

```typescript
interface Software {
  id: string              // sw{N}
  name: string
  description: string
  year: string            // "2025" — 문자열 주의
  github: string          // 전체 URL
  image?: string          // /images/software/...
  tags?: string[]
  developers?: string[]
  hidden?: boolean        // true면 페이지에서 숨김
}
```

## news.json

```typescript
interface GalleryImage {
  id: string              // g{N}
  images: string[]        // ["/images/news/...", ...]
  title: string
  description?: string
  date?: string           // YYYY-MM-DD
  category?: string       // "Conferences" | "Paper Alerts" | "Awards" | ...
}
```

여러 장의 이미지는 `images` 배열에 순서대로. 갤러리 슬라이드로 표시됨.

**auto-news 컨벤션 (2026-07-15 도입):** PI 주저자(제1저자 또는 `*`) journal 추가와 conference 발표 추가 시 collector가 news_add를 자동 파생한다.
- **Paper Alerts**: title은 `"New Paper Alert, {저널 약칭} by {호칭}. {성}"` 스타일, description은 `"Congratulations! {호칭} {성}'s paper, '{제목}', has been accepted by {저널 약칭}."` 스타일. 이미지는 해당 논문 highlightImage 재사용 가능 (별도 이미지 없으면).
- **Conferences**: 학회 이벤트당 1건 (발표당 1건 아님). title은 `"{학회 약칭} {연도} in {도시}, {국가}"` 스타일, description은 참석자·발표 내용 요약 1~2문장. 이미지는 현장 사진 1~4장 (`/images/news/` 배치, 파일명 `{학회약칭}{연도}_{n}.jpg` 또는 `{YYYYMMDD}_{약칭}.jpg` 패턴).
- date: Paper Alerts는 게재/억셉 확인일, Conferences는 학회 종료일. id는 기존 `g{N}` 최대값 +1.

## contact.json

```typescript
interface ContactInfo {
  address: string         // \n으로 줄바꿈
  phone: string
  email: string
  fax?: string
  mapCoordinates?: { lat: number, lng: number }
}
```

변경 시 mapCoordinates는 사용자 명시 좌표만 사용 (geocoding 추측 금지).
