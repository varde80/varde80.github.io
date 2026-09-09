# varde80.github.io — AIMAT Lab Site

Vue 3 + TypeScript + Vite로 빌드되는 GitHub Pages 사이트. 데이터는 `src/data/*.json`, 이미지 자산은 `public/images/`에 위치.

## 하네스: GitHub Pages 데이터 갱신

**목표:** rawdata/ 폴더 파일이나 웹 URL에서 정보를 받아 `src/data/*.json`과 `public/images/` 자산을 안전하게 추가·수정·이동·삭제하고 빌드 통과까지 검증한다.

**트리거:** 다음 표현이 보이면 `website-updater` 스킬을 사용하라:
- 멤버 추가/이동(졸업)/수정/삭제
- 연구분야(research area) 추가/수정
- 프로젝트(project) 추가/수정/삭제
- 시설(facility) 추가/수정/삭제
- 논문(publication/journal/conference/preprint) 추가/수정/삭제
- 소프트웨어(software) 추가
- 뉴스(news) 추가
- 후속 작업("다시 실행", "수정", "보완") 포함

단순 코드/디자인 질문은 직접 응답 가능.

**CV 생성:** "CV 만들어", "CV 업데이트", "이력서", "CV 다시", "CV 최신화" 표현이 보이면 `cv-generator` 스킬을 사용하라.

**변경 이력:**

| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-05-11 | 초기 구성 | data-collector / content-editor / schema-guardian / build-validator 에이전트 + website-updater 스킬 + data-schemas 레퍼런스 | 데이터 갱신 워크플로우 자동화 (rawdata/ + 웹 URL 입력 지원, 빌드까지 자동 검증) |
| 2026-05-11 | git-publisher 에이전트 추가 + 오케스트레이터에 Phase 6(자동 게시) 통합 | agents/git-publisher.md, skills/website-updater/SKILL.md | 검증 PASS 시 자동 commit + push로 GitHub Pages 배포까지 완료 (사용자 요청: "github push까지 수행") |
| 2026-05-11 | Korean-only 제목 처리 규칙 추가 — `한글 원문 (English Translation)` 포맷 | agents/data-collector.md, skills/website-updater/references/data-schemas.md | 사용자 피드백: 한글 제목은 영어 번역을 괄호로 병기 |
| 2026-05-12 | conference scope 필드(`domestic`/`international`) 추가 + UI 배지 | src/types/index.ts, src/data/conferences.json, src/pages/AchievementsPage.vue, references/data-schemas.md | 프로젝트의 PI/Co-PI 배지처럼 학회를 국내/국제로 구분 표시 |
| 2026-05-12 | conferences.json에서 `*`(corresponding) 마커 제거 규칙 추가 | agents/data-collector.md, references/data-schemas.md, src/data/conferences.json | 사용자 피드백: "발표는 corresponding을 생략" — journals/preprints는 유지 |
| 2026-05-12 | 운영 학습 일괄 반영 (A+B+C1): 동명이인 차단, 학회명 표지 검증, pdftotext 레시피, 일정집/초록집 구분, Venue null 허용, quasi-lab 명단(Han-Jun Lee), 정식 영문 표기 누적(Seong-Hoon Kang/Se-Jong Kim/Jaimyun Jung/Chi-hun Lee), workspace 아카이브 one-liner | agents/data-collector.md, agents/schema-guardian.md, skills/website-updater/SKILL.md, skills/website-updater/references/data-schemas.md, 메모리 lab_member_canonical_names | 60+ 발표 추가 운영 중 누적된 휴리스틱·표기 결정·실패 사례를 영구 규칙으로 승격 |
| 2026-06-11 | cv-generator 에이전트 + 스킬 추가, website-updater Phase 7(CV 자동 재생성) 연동 | agents/cv-generator.md, skills/cv-generator/SKILL.md, skills/website-updater/SKILL.md | 웹사이트 데이터(professor/journals/projects) 변경 시 CV PDF 자동 재생성; "CV 업데이트" 독립 실행도 지원 |
| 2026-07-15 | auto-news 규칙 추가 — PI 주저자(제1저자 또는 `*`) journal 게재 및 conference 발표 추가 시 news_add 자동 파생 (학회는 이벤트당 1건) | agents/data-collector.md(원칙 11), skills/website-updater/SKILL.md(Phase 2), references/data-schemas.md(news.json 컨벤션) | 사용자 요청: "내가 주저자인 논문 게재되거나 학회 업데이트되면 news 부분도 작성" |
| 2026-07-15 | 동명이인 차단 규칙을 웹 출처로 확장 — 소속(KIMS) 미명시 웹 주장은 PI 근거로 채택 금지 | agents/data-collector.md(원칙 7) | PRESM 2026 plenary speaker "Prof. Lee"(iaicenter 공지)를 PI로 오인 — 사용자 정정 "그거 나 아니야" |
| 2026-07-21 | `*`(corresponding) 마커 PI 전용 규칙 추가 — 교신저자가 PI(Ho Won Lee)가 아니면 `*` 생략, 공동 교신도 PI만 유지. 기존 비-PI `*` 8건(journals.json) 일괄 제거 | agents/data-collector.md(원칙 5), agents/schema-guardian.md(검증 5), references/data-schemas.md, src/data/journals.json | 사용자 피드백: "corresponding author가 내가 아닌 경우에는 *제외 규칙 추가" (pub79의 Dong-Kyu Kim* 계기) |
| 2026-07-24 | 리브랜딩(AIMAT→AIMAP) + 데이터 기반 히어로 생성기 추가 — src/data JSON을 읽어 브랜드 톤 히어로 SVG를 그려 PNG로 렌더링. 논문/데이터 갱신 후 `python3 hero-generator/generate_heroes.py` 재실행 시 히어로 자동 최신화 | hero-generator/generate_heroes.py, public/images/hero/*, src/assets/logo.png, src/style.css | 연구실명 AIMAP 확정(버트 오렌지 테마); 사용자 요청: "hero 그림은 너가 만들어봐. 연구내용이나 논문 기반으로 중요 내용 업데이트 되도록" |
| 2026-07-30 | CV 개인정보 포함 버전(`--personal`) 추가 — 한국어 CV 헤더에 주민등록번호·주소·계좌번호 라인 추가, `*_KR_personal.pdf`로 별도 출력. 값은 gitignore된 `cv-generator/personal_info.json`에서만 읽음(레포 커밋 금지) | cv-generator/generate_cv.py, cv-generator/.gitignore, skills/cv-generator/SKILL.md | 사용자 요청: "주민번호, 주소, 본인 계좌번호 포함 버전 하나 더" (행정용, 평소 미사용) |
| 2026-09-03 | Research Interests 그룹 구조 지원 — `{category, items[]}` 객체 배열(기존 문자열 혼용 가능), CV에서 대분류 굵은 제목 + 서브 항목 들여쓰기 렌더링. professor.json 연구 분야를 기계공학 기반 4개 대분류(전산역학·성형공정 / 멀티스케일 미세조직 / 첨단 제조공정 / 소재·제조 AI)·13개 서브 항목으로 재구성(EN/KO) | src/data/professor.json, src/types/index.ts, cv-generator/generate_cv.py, skills/website-updater/references/data-schemas.md | 사용자 요청: "연구 분야를 기계 전공자답게 수정", "분야별로 합치고 서브로" — 2005~2026 전체 논문 리스트에서 도출 |
| 2026-09-09 | 논문별 사사(Acknowledgments) 과제 번호 표시 — `Publication.grants: string[]` 필드 추가, PublicationCard에 Projects의 PI/Co-PI 배지와 같은 pill 스타일 "GRANT" 배지 렌더링. journals.json 2022~2026 40편에 원문 PDF(`~/Dropbox/1_Projects/Prof/Resources/5_Papers/paper/`)에서 추출한 번호를 원문 표기 그대로 기록. data-collector 원칙 12(사사 추출), schema-guardian 검증 8, data-schemas.md grants 규칙 추가 | src/types/index.ts, src/components/publications/PublicationCard.vue, src/data/journals.json, agents/data-collector.md, agents/schema-guardian.md, references/data-schemas.md | 사용자 요청: "논문 별로 사사의 관련 과제 번호를 넣자", "projects의 pi, co-pi 표시처럼 ui 표현" |
