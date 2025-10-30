# Coupang MCP Server

MCP (Model Context Protocol) 서버로 Claude AI가 쿠팡 제휴 API를 사용하여 상품 검색 및 정보 조회를 할 수 있도록 합니다.

## 기능

- **상품 검색**: 키워드로 쿠팡 상품 검색
- **상품 상세 조회**: 상품 ID로 상세 정보 확인
- **카테고리별 베스트 상품**: 카테고리별 인기 상품 조회 (18개 카테고리 지원)
- **딥링크 생성**: 쿠팡 URL을 트래킹 코드가 포함된 단축 URL로 변환
- **제휴 링크 제공**: 쿠팡 파트너스 제휴 링크 생성
- **비동기 처리**: aiohttp를 사용한 효율적인 API 호출

## 요구사항

- Python 3.13+
- UV (Python 패키지 관리자)
- 쿠팡 파트너스 API 자격증명

## 설치

### 빠른 시작

```bash
# 1. 저장소 클론
git clone https://github.com/space-cap/mcp-coupang-server.git
cd mcp-coupang-server

# 2. 의존성 설치
uv sync

# 3. 환경 변수 설정
# .env 파일을 생성하고 쿠팡 API 키를 입력하세요
```

### 상세 설치 가이드

처음 설치하시나요? **[📖 설치 및 설정 가이드](docs/installation-guide.md)**를 참조하세요.

이 가이드는 다음 내용을 포함합니다:
- Python 및 UV 설치 방법
- 쿠팡 파트너스 API 키 발급 절차
- Claude Desktop 설정 방법 (Windows/macOS/Linux)
- 문제 해결 및 테스트 방법

### 환경 변수

`.env` 파일 예제:

```env
COUPANG_ACCESS_KEY=your_access_key_here
COUPANG_SECRET_KEY=your_secret_key_here
COUPANG_PARTNER_ID=your_partner_id_here
COUPANG_SUB_ID=your_sub_id_here  # Optional: Default tracking ID for deeplinks
```

## 사용 방법

### 로컬 테스트

MCP 서버를 직접 실행:

```bash
uv run python main.py
```

### Claude Desktop과 연동

Claude Desktop 설정 파일(`claude_desktop_config.json`)에 다음을 추가:

**Windows:**
```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-coupang-server",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

자세한 설정 방법은 [docs/claude-desktop-setup.md](docs/claude-desktop-setup.md)를 참조하세요.

## 제공되는 도구

### 1. search_products

키워드로 쿠팡 상품을 검색합니다.

**매개변수:**
- `keyword` (string, 필수): 검색어 (예: "laptop", "iPhone 15")
- `limit` (integer, 선택): 결과 개수 (1-100, 기본값: 10)

**예제:**
```
검색어 "노트북"으로 상품 20개 검색
```

**응답:**
```
Found 20 product(s) for '노트북':

1. LG 그램 17인치 노트북
   Price: 1,899,000원
   ID: 1234567890
   🚀 Rocket Delivery
   📦 Free Shipping
   URL: https://link.coupang.com/...

2. 삼성 갤럭시북 Pro
   Price: 1,499,000원
   ...
```

### 2. get_product_details

상품 ID로 상세 정보를 조회합니다.

**매개변수:**
- `product_id` (string, 필수): 쿠팡 상품 ID

**예제:**
```
상품 ID "1234567890"의 상세 정보 조회
```

**응답:**
```
Product Details for ID: 1234567890

Name: LG 그램 17인치 노트북
Price: 1,899,000원
Original Price: 2,299,000원
Discount: 17% (Save 400,000원)
Category: Electronics
Shipping: 🚀 Rocket Delivery, 📦 Free Shipping

Image: https://thumbnail.coupangcdn.com/...
Affiliate URL: https://link.coupang.com/...
```

### 3. get_best_products_by_category

특정 카테고리의 베스트 상품을 조회합니다.

**매개변수:**
- `category_id` (string, 필수): 쿠팡 카테고리 ID
- `limit` (integer, 선택): 결과 개수 (1-100, 기본값: 20)

**사용 가능한 카테고리:**
- `1001` - 여성패션
- `1002` - 남성패션
- `1010` - 뷰티
- `1012` - 식품
- `1013` - 주방용품
- `1014` - 생활용품
- `1015` - 홈인테리어
- `1016` - 가전디지털
- `1017` - 스포츠/레저
- `1018` - 자동차용품
- `1019` - 도서/음반/DVD
- `1020` - 완구/취미
- `1021` - 문구/오피스
- `1024` - 헬스/건강식품
- `1025` - 국내여행
- `1026` - 해외여행
- `1029` - 반려동물용품
- `1030` - 유아동패션

**예제:**
```
가전디지털 카테고리(1016)의 베스트 상품 10개 조회
```

**응답:**
```
Found 10 best product(s) in category '1016':

1. 삼성전자 갤럭시 버즈3 Pro
   Price: 289,000원
   ID: 8123456789
   Category: 가전디지털
   🚀 Rocket Delivery
   📦 Free Shipping
   💰 Discount: 10%
   URL: https://link.coupang.com/...

2. LG전자 그램 스타일 노트북
   Price: 1,790,000원
   ...
```

### 4. create_deeplinks

쿠팡 상품 URL을 트래킹 코드가 포함된 단축 URL로 변환합니다.

**매개변수:**
- `coupang_urls` (array, 필수): 변환할 쿠팡 URL 목록
- `sub_id` (string, 선택): 트래킹/Sub ID (환경 변수 기본값 사용 가능)

**예제:**
```
다음 쿠팡 URL을 딥링크로 변환해줘:
https://www.coupang.com/vp/products/184614775
```

**응답:**
```
Created 1 deeplink(s):

1. Original: https://www.coupang.com/vp/products/184614775
   Shortened: https://coupa.ng/blE0dT
   Landing: https://link.coupang.com/re/AFFSDP?lptag=AF1234567&pageKey=319834306&itemId=1023216541&vendorItemId=70064597513&traceid=V0-183-5fddb21eaffbb2ef
```

**활용 사례:**
- 검색 결과에서 얻은 상품 URL을 추적 가능한 링크로 변환
- 여러 상품의 URL을 한 번에 변환하여 링크 관리
- Sub ID를 사용하여 다양한 트래픽 소스 추적

## 프로젝트 구조

```
mcp-coupang-server/
├── src/
│   ├── __init__.py
│   ├── server.py              # MCP 서버 메인 로직
│   ├── coupang_client.py      # 쿠팡 API 클라이언트
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py         # 상품 데이터 모델
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search.py          # 검색 도구 유틸리티
│   │   └── details.py         # 상세정보 도구 유틸리티
│   └── utils/
│       ├── __init__.py
│       ├── config.py          # 환경 변수 관리
│       ├── auth.py            # HMAC 인증
│       └── categories.py      # 카테고리 코드 정의
├── playground/                # 테스트 스크립트 (콘솔)
│   ├── 1_simple_search.py
│   ├── 2_product_details.py
│   ├── 3_compare_products.py
│   ├── 4_price_filter.py
│   ├── 5_rocket_delivery.py
│   ├── 6_category_best.py
│   ├── 7_create_deeplinks.py
│   └── README.md
├── tests/                     # 테스트 파일
├── docs/                      # 문서
├── main.py                    # 진입점
├── pyproject.toml             # 프로젝트 설정
└── pytest.ini                 # 테스트 설정
```

## 배포

다른 사람들이 사용할 수 있도록 배포하고 싶으신가요? **[🚀 배포 가이드](docs/deployment-guide.md)**를 참조하세요.

배포 방법:
- GitHub 공개 저장소 (가장 쉬움, 권장)
- PyPI 패키지 배포
- Docker 컨테이너
- MCP Registry 등록

## 개발

### 테스트 실행

```bash
# 모든 테스트 실행
uv run pytest

# 상세 출력과 함께 실행
uv run pytest -v

# 특정 테스트 파일만 실행
uv run pytest tests/test_client.py

# 커버리지와 함께 실행 (pytest-cov 설치 필요)
uv run pytest --cov=src --cov-report=html
```

### 코드 품질

프로젝트는 다음을 준수합니다:
- Type hints 사용
- Pydantic을 통한 데이터 검증
- 비동기 프로그래밍 (asyncio/aiohttp)
- 포괄적인 단위 테스트 및 통합 테스트

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

```
MIT License - Copyright (c) 2025 space-cap
```

## 기여하기

기여를 환영합니다! [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

## 문제 보고

버그를 발견하거나 기능 요청이 있으시면 [이슈](../../issues)를 생성해주세요.

## 관련 링크

- [쿠팡 파트너스](https://partners.coupang.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Claude Desktop](https://claude.ai/desktop)

## 참고사항

> 이 서비스는 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다 
