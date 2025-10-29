# 프로젝트 폴더 구조

## 기본 구조

```
mcp-coupang-server/
├── .gitignore                 # Git 무시 파일
├── .env                       # 환경 변수 (API 키 등)
├── .python-version            # Python 버전 명시
├── README.md                  # 프로젝트 소개
├── CLAUDE.md                  # Claude Code 가이드
├── pyproject.toml             # 프로젝트 설정 및 의존성
├── uv.lock                    # 의존성 잠금 파일
│
├── docs/                      # 문서 폴더
│   ├── development-guide.md   # 개발 가이드
│   └── project-structure.md   # 프로젝트 구조 (이 파일)
│
├── src/                       # 소스 코드 폴더
│   ├── __init__.py
│   ├── server.py              # MCP 서버 메인 로직
│   ├── coupang_client.py      # 쿠팡 API 클라이언트
│   ├── tools/                 # MCP 도구 정의
│   │   ├── __init__.py
│   │   ├── search.py          # 상품 검색 도구
│   │   ├── product.py         # 상품 상세 정보 도구
│   │   └── link.py            # 딥링크 생성 도구
│   ├── utils/                 # 유틸리티 함수
│   │   ├── __init__.py
│   │   ├── auth.py            # 인증 관련 (HMAC 서명)
│   │   └── config.py          # 설정 로드
│   └── models/                # 데이터 모델
│       ├── __init__.py
│       └── product.py         # 상품 데이터 모델
│
├── tests/                     # 테스트 폴더
│   ├── __init__.py
│   ├── test_server.py         # 서버 테스트
│   ├── test_coupang_client.py # API 클라이언트 테스트
│   └── test_tools/            # 도구별 테스트
│       ├── __init__.py
│       ├── test_search.py
│       └── test_product.py
│
├── main.py                    # 서버 진입점
└── logs/                      # 로그 파일 (gitignore)
```

## 폴더 및 파일 설명

### 루트 디렉토리

- **`.env`**: API 키, 시크릿 키 등 환경 변수 저장 (절대 커밋하지 말것!)
- **`main.py`**: 서버 실행 진입점
- **`pyproject.toml`**: 프로젝트 메타데이터, 의존성, 빌드 설정

### `src/` - 소스 코드

핵심 애플리케이션 로직이 위치하는 폴더

#### 주요 파일
- **`server.py`**: MCP 서버 초기화 및 실행 로직
  - `Server` 인스턴스 생성
  - `@app.list_tools()`, `@app.call_tool()` 데코레이터 정의
  - stdio 통신 설정

- **`coupang_client.py`**: 쿠팡 API와 통신하는 클라이언트
  - HTTP 요청 처리
  - API 엔드포인트 호출
  - 응답 파싱

#### `src/tools/` - MCP 도구 모듈

각 도구를 독립적인 모듈로 분리하여 관리

- **`search.py`**: 상품 검색 기능
- **`product.py`**: 상품 상세 정보 조회
- **`link.py`**: 딥링크/제휴 링크 생성

#### `src/utils/` - 유틸리티

공통으로 사용되는 헬퍼 함수들

- **`auth.py`**: HMAC SHA256 서명 생성, 인증 헤더 생성
- **`config.py`**: 환경 변수 로드, 설정 검증

#### `src/models/` - 데이터 모델

API 응답을 파싱하여 구조화된 데이터로 변환

- **`product.py`**: 상품 정보 데이터 클래스 (Pydantic 모델 권장)

### `tests/` - 테스트

각 모듈에 대응하는 테스트 코드

- 단위 테스트 (pytest 사용)
- API 모킹 (aioresponses 사용 권장)
- 통합 테스트

### `docs/` - 문서

프로젝트 관련 문서 저장

- 개발 가이드
- API 사용법
- 아키텍처 설명

## 추천 개발 순서

1. **`src/utils/config.py`**: 환경 변수 로드 구현
2. **`src/utils/auth.py`**: HMAC 서명 생성 구현
3. **`src/coupang_client.py`**: API 클라이언트 기본 구조
4. **`src/models/product.py`**: 데이터 모델 정의
5. **`src/tools/search.py`**: 첫 번째 도구 구현
6. **`src/server.py`**: MCP 서버 통합
7. **`main.py`**: 서버 실행 로직
8. **`tests/`**: 테스트 작성

## 파일 생성 명령어

```bash
# src 폴더 구조 생성
mkdir -p src/tools src/utils src/models
touch src/__init__.py
touch src/server.py
touch src/coupang_client.py
touch src/tools/__init__.py src/tools/search.py src/tools/product.py src/tools/link.py
touch src/utils/__init__.py src/utils/auth.py src/utils/config.py
touch src/models/__init__.py src/models/product.py

# tests 폴더 구조 생성
mkdir -p tests/test_tools
touch tests/__init__.py
touch tests/test_server.py
touch tests/test_coupang_client.py
touch tests/test_tools/__init__.py tests/test_tools/test_search.py tests/test_tools/test_product.py

# logs 폴더 생성
mkdir logs
```

## 모듈 임포트 예시

```python
# main.py에서
from src.server import app, main

# server.py에서
from src.coupang_client import CoupangClient
from src.tools.search import search_products_tool
from src.tools.product import get_product_details_tool
from src.utils.config import load_config

# search.py에서
from src.models.product import Product
from src.utils.auth import generate_signature
```

## 주의사항

- **`src/` 폴더 사용**: 코드와 설정 파일을 명확히 분리
- **모듈화**: 각 기능을 독립적인 파일로 분리하여 유지보수 용이
- **테스트**: 각 모듈에 대응하는 테스트 작성
- **환경 변수**: `.env` 파일은 절대 Git에 커밋하지 말것
- **`__init__.py`**: Python 패키지로 인식되도록 각 폴더에 포함
