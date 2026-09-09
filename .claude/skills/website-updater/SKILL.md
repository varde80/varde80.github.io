---
name: website-updater
description: AIMAT Lab GitHub Pages 사이트(varde80.github.io)의 데이터·이미지를 안전하게 갱신하고 검증 PASS 시 main 브랜치에 자동 push까지 수행하는 오케스트레이터. rawdata/ 폴더 파일이나 웹 URL에서 정보를 받아 멤버 추가/이동(졸업)/삭제/수정, research area 업데이트, 프로젝트 추가/수정/삭제, 시설(facilities) 추가/수정/삭제, 논문(publication/journal/conference/preprint) 추가/수정/삭제, 소프트웨어 추가, 뉴스 추가를 수행하고, npm 빌드 통과 + 스키마 검증 통과 시 git commit + push로 GitHub Pages를 배포한다. "멤버 추가", "졸업으로 이동", "논문 추가", "프로젝트 수정", "시설 삭제", "뉴스 추가", "research 영역 업데이트", "다시 실행", "재실행", "보완", "수정", "사이트 업데이트", "배포", "push" 같은 표현이 보이면 반드시 이 스킬을 사용하라. 단순 코드 질문이나 디자인 질문에는 사용하지 않는다.
---

# website-updater — AIMAT Lab Site 갱신 오케스트레이터

## 목적

`src/data/*.json`과 `public/images/` 자산을 사용자 입력(rawdata/ 또는 웹 URL)으로부터 안전하게 갱신하고, `npm run build` 통과 + schema 검증 통과까지 보장한 뒤, **검증 PASS 시 자동으로 main 브랜치에 commit + push하여 GitHub Pages를 배포한다.**

## 실행 모드: 에이전트 팀 (하이브리드 폴백)

기본은 에이전트 팀 모드. 단순 수정(파일 1개, 1~2 필드만 변경) 시 서브 에이전트 모드로 폴백하여 오버헤드를 줄인다.

**팀원:**
- `data-collector` — 입력 추출/정규화
- `content-editor` — JSON·이미지 수정
- `schema-guardian` — 정적 시멘틱 검증 (read-only)
- `build-validator` — npm run build 실행
- `git-publisher` — staging + commit + push (PASS 게이트 통과 시에만)

모든 Agent 호출에 `model: "opus"` 명시.

## Phase 0: 컨텍스트 확인

워크플로우 시작 시 가장 먼저 다음을 확인하고 실행 모드를 결정한다:

1. `_workspace/` 존재 여부 확인 (`ls _workspace/` via Bash)
2. 분기:
   - **초기 실행**: `_workspace/`가 없음 → `mkdir -p _workspace/images _workspace/_prev` 후 전체 파이프라인 실행.
   - **부분 재실행**: `_workspace/`가 있고 사용자가 특정 부분 수정 요청 (예: "방금 추가한 pub42의 doi 수정") → 해당 operation만 재처리 (collector 건너뛰고 editor부터).
   - **새 실행**: `_workspace/`가 있고 사용자가 새 입력 제공 → 기존을 `_workspace/_prev/{timestamp}/`로 이동, 전체 재실행. 표준 명령:
     ```bash
     TS=$(date +%Y%m%d-%H%M%S) && mkdir -p _workspace/_prev/$TS && \
       for f in 01_collected.json 01_collected_notes.md 02_changes.{md,json} 03_qa.{md,json} 04_build.{md,json}; do \
         [ -f _workspace/$f ] && mv _workspace/$f _workspace/_prev/$TS/; \
       done
     ```
   - **빌드만**: 사용자가 "빌드만 다시" 요청 → build-validator만 호출.

판별이 모호하면 사용자에게 한 번 묻고 결정.

## Phase 1: 입력 검증 및 의도 명확화

1. 사용자가 제공한 입력 경로/URL/텍스트 확인.
   - rawdata/ 경로면 파일 존재 확인.
   - URL이면 도메인 reasonability 확인 (사내 미접근 도메인 등은 사용자에게 사전 양해).
2. 의도 분류:
   - 명시적 의도가 있으면 그대로 사용.
   - 모호하면 입력 일부를 빠르게 읽어 의도 추론 후, 1회 확인 질문.
3. 팀 구성:
   - 단순 케이스(파일 1개, 필드 1~2개): 서브 에이전트 모드 (Agent 도구 직접 호출).
   - 일반 케이스: `TeamCreate` 호출하여 4명 팀 구성.

## Phase 2: 데이터 수집 (data-collector)

**실행 모드:** 단일 에이전트 (팀 모드에서도 이 단계는 순차).

`TaskCreate`로 작업 등록 후 data-collector 호출:
- 입력: 경로/URL 목록 + 의도 힌트.
- 출력: `_workspace/01_collected.json`, `_workspace/01_collected_notes.md`.

**auto-news 규칙 (2026-07-15):** 다음 두 경우 collector는 사용자가 뉴스를 요청하지 않아도 `news_add` operation을 자동 파생한다 (사용자가 명시적으로 거부하면 생략). 오케스트레이터는 collector 호출 prompt에 이 규칙을 상기시킨다:
- PI(Ho Won Lee)가 **주저자(제1저자 또는 corresponding `*`)** 인 journal 논문 추가 → "Paper Alerts" 뉴스 1건
- conference 발표 추가 → **학회 이벤트당** "Conferences" 뉴스 1건 (발표 N건을 1건으로 묶음)

세부 기준(주저자 판정, 톤, 이미지 선택)은 `agents/data-collector.md` 원칙 11과 `references/data-schemas.md`의 news.json 섹션 참조.

빈 결과(operations이 0개)면 사용자에게 "추출 가능한 데이터 없음" 보고 후 종료.

## Phase 3: 변경 적용 (content-editor)

`TaskCreate` (blockedBy: Phase 2 task) 후 content-editor 호출:
- 입력: `_workspace/01_collected.json`.
- 출력: 수정된 `src/data/*.json`, 새 `public/images/...`, `_workspace/02_changes.md`, `_workspace/02_changes.json`.

Phase 2의 notes에서 사용자 결정이 필요한 항목(예: 졸업생의 현재 직장)이 있으면 여기서 한 번 사용자 확인.

## Phase 4: 병렬 검증 (schema-guardian + build-validator)

**실행 모드:** 두 에이전트 병렬 (`run_in_background: true`로 동시 실행).

두 작업 모두 Phase 3 task에 `blockedBy`로 의존, 서로는 독립.

- schema-guardian: 정적 시멘틱 검증 → `_workspace/03_qa.{md,json}`.
- build-validator: `npm run build` → `_workspace/04_build.{md,json}`.

둘 다 완료를 기다린 후 결과 평가.

## Phase 5: 결과 평가 및 루프

평가 매트릭스:

| schema-guardian | build-validator | 다음 행동 |
|----------------|----------------|----------|
| PASS | PASS | Phase 6 (자동 게시) |
| PASS | FAIL | content-editor 재호출 (build-validator의 fix_hint 기반) |
| FAIL | PASS | content-editor 재호출 (schema-guardian의 errors 기반) |
| FAIL | FAIL | content-editor 재호출, 두 보고서 모두 전달 |

재호출은 최대 2회. 그 후에도 실패면 사용자에게 escalate하고 `_workspace/`의 상태를 보존한 채 중단 (Phase 6은 건너뜀).

## Phase 6: 자동 게시 (git-publisher)

**전제 조건:** schema-guardian + build-validator 둘 다 PASS.

`TaskCreate` (blockedBy: Phase 4 두 task)로 작업 등록 후 git-publisher 호출:
- 입력: `_workspace/02_changes.json`, `_workspace/03_qa.json`, `_workspace/04_build.json`.
- 행동: PASS 게이트 재확인 → .gitignore 안전성 확인 → 변경 파일만 staging → 단일 커밋 생성 → `git push origin <current-branch>`.
- 출력: `_workspace/05_publish.{md,json}` — 커밋 SHA, 푸시 결과.

**중요 정책:**
- 한 실행 = 한 커밋. 모든 operation을 묶어 의미 있는 한 줄 요약 + 변경 본문.
- `--force`, `--amend`, `--no-verify`, `--no-gpg-sign` 모두 금지.
- staging은 `02_changes.json`의 `files_modified` + `images_added` 경로만. `git add .`나 `git add -A` 금지.
- push 거부·인증 실패·hook 실패 시 자동 재시도하지 않고 사용자에게 보고.

Why 자동 push: 사용자가 명시적으로 "검증 PASS면 확인 없이 push"를 결정함. PASS 게이트(QA + build 둘 다 통과)가 안전망 역할을 하며, push 자체가 GitHub Pages 배포를 트리거한다.

## Phase 7: CV 자동 재생성 (조건부)

**전제 조건:** Phase 6 (git-publisher) 완료 후.

`_workspace/02_changes.json`의 `files_modified` 목록을 읽어 CV 관련 데이터 파일이 변경됐는지 확인한다:

- `src/data/professor.json`
- `src/data/journals.json`
- `src/data/projects.json`

셋 중 하나라도 변경됐으면 cv-generator 에이전트를 호출한다:

```
Agent(
  subagent_type: "cv-generator",
  model: "opus",
  prompt: "cv-generator/generate_cv.py를 실행하여 PDF CV를 생성하라.
           프로젝트 루트: /Users/varde/Dropbox/claude/varde80.github.io"
)
```

변경된 파일이 CV와 무관하면 (예: members.json, facilities.json만 변경) 이 Phase를 건너뛰고 "CV 관련 데이터 변경 없음 — CV 재생성 건너뜀"을 Phase 8 보고에 포함한다.

## Phase 8: 최종 보고

사용자에게 다음을 보고:

```
✅ varde80.github.io 갱신 + 배포 완료

변경:
- journals.json: +1 (pub42)
- public/images/publications/pub42.png 추가
- members.json: phd2 → alumni (Mooyoung Joo 졸업)

검증:
- Schema QA: PASS (warning 1건 — IF.json에 'X' 추가 권장)
- Build: PASS (47s)

배포:
- Commit: a1b2c3d (data: ...)
- Pushed: main → origin/main
- Live: https://varde80.github.io/ (1~2분 후 반영)

CV 재생성:
- cv-generator/output/20260611_CV_HLee.pdf ✅
- cv-generator/output/20260611_CV_HLee_KR.pdf ✅
(또는: CV 관련 데이터 변경 없음 — 재생성 건너뜀)

개선 피드백 있으면 알려주세요 (해당 부분만 재실행).
```

push가 BLOCKED/SKIPPED인 경우 사유와 함께 보고하고 사용자가 수동으로 처리할 수 있도록 git 상태 안내.

## 데이터 스키마 및 컨벤션

세부 JSON 스키마, id 규칙, 이미지 경로 규칙, 저자 표기 컨벤션은 `references/data-schemas.md`에 정리. content-editor와 schema-guardian이 이 파일을 참조한다.

## 에러 핸들링 (오케스트레이터 레벨)

- 에이전트 1회 실패 → 재호출.
- 에이전트 2회 실패 → 사용자에게 보고 후 중단, `_workspace/` 보존.
- 사용자 인터럽트("취소") → 즉시 정지, `_workspace/` 보존, 적용된 변경은 그대로 둠 (롤백은 사용자의 git 결정).
- 상충 데이터(예: collector가 동일 항목을 2번 추출) → 삭제하지 않고 사용자에게 어느 것을 채택할지 질문.

## 테스트 시나리오

### 정상 시나리오 1: 학술논문 추가 + 자동 배포
입력: `rawdata/2026_AdvEngInf.pdf` (Phan의 AEI 논문)
- data-collector: PDF에서 제목/저자/저널명/DOI/년도/이미지 추출.
- content-editor: `src/data/journals.json`에 새 항목 추가, 이미지를 `public/images/publications/`에 복사.
- schema-guardian: 타입·이미지 경로·저자 마커 검증 → PASS.
- build-validator: `npm run build` → PASS.
- git-publisher: `src/data/journals.json` + 이미지만 staging → commit "data: add AEI 2025 publication (Phan)" → push.
- 보고: 변경 1건, 검증 PASS, commit SHA + GitHub Pages URL 안내.

### 정상 시나리오 2: 멤버 졸업 처리
입력: "Mooyoung Joo가 졸업해서 alumni로 옮겨주고, 현재는 KIMS 연구원"
- data-collector: 의도 `member_move`, target id `phd2`, alumni position 추론.
- content-editor: phdStudents에서 phd2 제거, alumni 배열에 추가, position 보정.
- 검증·빌드 PASS.

### 에러 시나리오 1: 빌드 실패
입력: 사용자가 잘못된 image 경로 제공 → 이미지 누락 빌드 실패.
- build-validator: FAIL, fix_hint = "public/images/publications/pub42.png 누락".
- 오케스트레이터: content-editor 재호출, JSON의 image 필드를 빈 문자열로 변경 (이미지 없이도 빌드 통과하도록).
- 재검증 PASS → git-publisher 호출되어 push까지 진행.
- 사용자에게 "이미지 파일이 없어 image 필드를 비웠습니다. 나중에 파일이 준비되면 다시 알려주세요" 보고.

### 에러 시나리오 2: push 거부 (원격이 앞섬)
- 모든 검증 PASS, git-publisher가 push 시도.
- 응답: `! [rejected] main -> main (fetch first)`.
- git-publisher: BLOCKED, 자동 rebase하지 않고 사용자에게 보고.
- 사용자 안내: "원격 main이 앞서 있습니다. `git pull --rebase` 후 다시 `/website-updater 빌드만 다시 push`로 재시도해 주세요." 변경은 로컬에 commit된 상태로 보존.

### 후속 시나리오: 직전 변경 수정
입력: "방금 추가한 pub42의 제목 오타 수정해줘 — 'Microstructur' → 'Microstructure'"
- Phase 0에서 부분 재실행으로 판단.
- data-collector 건너뜀.
- content-editor 직접 호출: pub42의 title 필드만 수정.
- 검증·빌드 PASS.

## 진화 (Phase 8)

매 실행 후 사용자에게 "결과 만족하시나요? 개선할 부분 있나요?" 1회 질문. 피드백은 CLAUDE.md 변경 이력에 기록하고, 반복되는 피드백은 본 스킬이나 에이전트 정의에 반영.
