# BizTone Converter 프로젝트 컨텍스트

## 프로젝트 개요

**BizTone Converter**는 평범한 말투를 전문적인 비즈니스 언어로 변환해 주는 AI 기반 웹 도구입니다. 신입사원, 주니어 직원 등 비즈니스 커뮤니케이션에 어려움을 겪는 사용자들을 위해 설계되었습니다.

*   **목표:** 텍스트를 "상사(보고/격식)", "동료(요청/존중)", "고객(응대/극존칭)" 톤으로 변환합니다.
*   **핵심 기술:**
    *   **프론트엔드:** HTML5, Tailwind CSS (Play CDN), Vanilla JavaScript.
    *   **백엔드:** Python (Flask), AI 모델 API 게이트웨이 역할.
    *   **AI 엔진:** Groq API (`llama-3.3-70b-versatile` 사용).
    *   **배포:** Vercel (Serverless Functions).

## 아키텍처 및 디렉토리 구조

이 프로젝트는 API와 정적 자산을 함께 제공하는 Vercel 친화적인 구조를 따릅니다.

```text
C:\vibecoding\biztalk_python\
├── api/                  # 백엔드 로직 (Serverless Functions)
│   ├── index.py          # 메인 Flask 애플리케이션 진입점
│   ├── services.py       # Groq AI 연동 및 프롬프트 엔지니어링
│   └── requirements.txt  # Python 의존성 목록
├── public/               # 프론트엔드 정적 자산
│   ├── index.html        # 메인 SPA 진입점 (Tailwind CSS 포함)
│   └── js/
│       └── script.js     # 프론트엔드 로직 (DOM, Fetch API)
├── .venv/                # 로컬 Python 가상 환경
├── vercel.json           # Vercel 배포 설정
├── PRD.md                # 제품 요구사항 문서
└── 프로그램개요서.md       # 초기 기획안
```

## 주요 파일

*   **`api/index.py`**: Flask 앱입니다. 루트 경로 `/`에서 정적 `index.html`을 서빙하고, `/api/convert` 엔드포인트를 제공합니다.
*   **`api/services.py`**: Groq API와 상호작용하는 `convert_text` 함수가 포함되어 있습니다. 각 대상(상사, 동료, 고객)에 맞는 시스템 프롬프트가 정의되어 있습니다.
*   **`public/index.html`**: 사용자 인터페이스입니다. Tailwind CSS v4 (Play CDN)로 스타일링되었습니다. 반응형 상하 배치(Top-Down) 레이아웃(입력 -> 설정 -> 결과)을 사용합니다.
*   **`public/js/script.js`**: 사용자 입력을 처리하고, 백엔드로 비동기 요청을 보내고, 결과를 UI에 업데이트하며, 알림(토스트) 메시지를 관리합니다.
*   **`vercel.json`**: Vercel이 `api/index.py`를 서버리스 함수로 처리하고 API 트래픽을 올바르게 라우팅하도록 설정합니다.

## 설정 및 개발

### 필수 조건
*   Python 3.11 이상
*   Node.js (선택 사항, Vercel CLI 사용 시 필요)
*   Groq API Key

### 로컬 개발
1.  **환경:** `.venv` 가상 환경이 활성화되어 있는지 확인합니다.
2.  **의존성 설치:** `api/requirements.txt`를 사용하여 설치합니다.
    ```bash
    pip install -r api/requirements.txt
    ```
3.  **환경 변수:** `.env` 파일을 생성하거나 시스템 변수를 설정합니다:
    ```
    GROQ_API_KEY=your_groq_api_key_here
    ```
4.  **서버 실행:** 
    ```bash
    python api/index.py
    ```
    서버는 보통 `http://localhost:5000`에서 실행됩니다.

### 배포 (Vercel)
이 프로젝트는 Vercel 배포를 위해 구성되었습니다.
*   **명령어:** `vercel` (배포) 또는 `vercel dev` (로컬 시뮬레이션).
*   **설정:** Vercel 프로젝트 설정(Settings) > 환경 변수(Environment Variables)에 `GROQ_API_KEY`를 추가해야 합니다.

## 현재 상태 및 컨벤션

*   **스타일링:** 최근 사용자 정의 CSS에서 **Tailwind CSS**로 마이그레이션했습니다. 모든 스타일은 HTML 내 유틸리티 클래스로 처리됩니다. 레이아웃은 **상하(Top-Down)** 구조입니다.
*   **반응형:** UI는 `min-w-0`과 `w-full`을 사용하여 작은 화면에서도 텍스트 영역이 올바르게 축소되도록 반응형으로 제작되었습니다.
*   **백엔드 로직:** "Sprint 3" 로직(AI 연동)이 `api/services.py`에 완전히 구현되어 있습니다.
*   **언어:** 코드베이스(변수명, 주석)는 영어를 사용하지만, 애플리케이션 인터페이스와 프롬프트는 **한국어** 사용자를 대상으로 합니다.

## 다음 단계
*   **배포:** Vercel에 푸시하고 프로덕션 동작을 확인합니다.
*   **테스트:** 라이브 URL에서 E2E(End-to-End) 테스트를 수행합니다.
*   **피드백:** 변환 품질에 대한 사용자 피드백을 수집하여 프롬프트를 튜닝합니다.
