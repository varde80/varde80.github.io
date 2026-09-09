---
name: cv-generator
description: AIMAT Lab 홈페이지 데이터(professor.json, journals.json, projects.json)로 영문·한국어 PDF CV를 생성하는 오케스트레이터. "CV 생성", "CV 업데이트", "이력서 만들어", "CV 다시", "curriculum vitae", "CV 만들어줘", "CV 최신화" 같은 표현이 보이면 반드시 이 스킬을 사용하라. website-updater와 달리 홈페이지 데이터를 변경하지 않고 오직 PDF 출력만 담당한다.
---

# cv-generator — CV PDF 생성 오케스트레이터

## 목적

`cv-generator/generate_cv.py`를 실행하여 `src/data/*.json`의 최신 데이터를 PDF CV로 변환한다.
홈페이지 데이터를 수정하지 않으며, 생성된 PDF는 `cv-generator/output/`에 로컬 저장만 한다 (git 커밋 제외).

## 실행 모드: 단일 서브에이전트

CV 생성은 단일 에이전트 작업이므로 서브에이전트 모드로 실행한다.

```
cv-generator 에이전트 호출 (Agent 도구, model: "opus")
```

## Phase 0: 컨텍스트 확인

1. `_workspace/` 존재 확인 — 있으면 website-updater 실행 직후임을 감지
2. 최근 변경 맥락 파악:
   - `_workspace/02_changes.json`이 있으면 읽어서 CV 관련 데이터 변경 여부 확인
   - 없으면 "명시적 요청으로 실행" 모드

## Phase 1: CV 생성

cv-generator 에이전트를 호출한다:

```
Agent(
  subagent_type: "cv-generator",
  model: "opus",
  prompt: "cv-generator/generate_cv.py를 실행하여 PDF CV를 생성하라.
           프로젝트 루트: /Users/varde/Dropbox/claude/varde80.github.io"
)
```

## Phase 2: 결과 보고

생성 성공 시:

```
✅ CV 생성 완료

생성된 파일:
- cv-generator/output/YYYYMMDD_CV_HLee.pdf (영문)
- cv-generator/output/YYYYMMDD_CV_HLee_KR.pdf (한국어)
```

## 개인정보 포함 버전 (--personal)

"주민번호/주소/계좌번호 포함", "개인정보 버전", "행정용 이력서" 류의 요청 시:

```
python3 cv-generator/generate_cv.py --personal
```

- 헤더(전화·이메일 아래)에 주민등록번호·주소·계좌번호를 추가한 **한국어 CV만** 생성
- 출력: `cv-generator/output/YYYYMMDD_CV_HLee_KR_personal.pdf` (기본 PDF는 덮어쓰지 않음)
- 값 출처: `cv-generator/personal_info.json` (키: `rrn`, `address`, `bank`, `account_number`)
- **이 파일은 gitignore 대상** — 절대 커밋하지 말 것. 값이 비어 있으면 스크립트가 에러로 중단하므로, 비어 있을 때는 사용자에게 값을 요청한다. 개인정보 값은 CLAUDE.md·메모리·커밋 메시지 등 어디에도 기록 금지.

실패 시: 에러 내용과 함께 `_workspace/06_cv.md` 경로 안내.

## 에러 핸들링

- venv/의존성 문제 → cv-generator 에이전트가 자동 처리
- 스크립트 오류 → 에러 메시지 사용자에게 전달, `cv-generator/generate_cv.py` 수정 제안

## 트리거 구분 (website-updater와의 경계)

| 요청 | 사용 스킬 |
|------|----------|
| "논문 추가해줘" | website-updater |
| "CV 업데이트해줘" | cv-generator (이 스킬) |
| "논문 추가하고 CV도 업데이트" | website-updater (Phase 7에서 자동 CV 재생성) |
| "CV만 다시 만들어줘" | cv-generator (이 스킬) |

## 테스트 시나리오

### 정상: 명시적 요청
입력: "CV 업데이트해줘"
- Phase 0: _workspace 없음 → 명시적 요청 모드
- Phase 1: cv-generator 에이전트 실행
- Phase 2: 오늘 날짜 PDF 2개 경로 보고

### 정상: website-updater 직후 자동 트리거
입력: website-updater Phase 7에서 자동 호출
- Phase 0: _workspace/02_changes.json 읽어 journals.json 변경 감지
- Phase 1: cv-generator 에이전트 실행
- Phase 2: PDF 경로 보고 (website-updater의 Phase 8 최종 보고에 포함)

### 에러: 스크립트 오류
- 에이전트가 stderr 기록 → _workspace/06_cv.md
- 사용자에게 오류 내용 전달
