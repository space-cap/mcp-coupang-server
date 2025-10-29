# 쿠팡 MCP 서버 개발 가이드

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [개발 환경 설정](#개발-환경-설정)
3. [쿠팡 API 설정](#쿠팡-api-설정)
4. [MCP 서버 구조](#mcp-서버-구조)
5. [구현할 기능](#구현할-기능)
6. [개발 단계](#개발-단계)
7. [테스트 방법](#테스트-방법)
8. [배포 및 사용](#배포-및-사용)

## 프로젝트 개요

쿠팡 MCP 서버는 Claude Desktop이나 다른 MCP 클라이언트에서 쿠팡의 기능을 사용할 수 있게 해주는 서버입니다.

### MCP(Model Context Protocol)란?

MCP는 AI 모델이 외부 도구 및 데이터 소스와 상호작용할 수 있도록 하는 표준 프로토콜입니다.

- **Tools**: AI가 호출할 수 있는 함수 (예: 상품 검색, 가격 조회)
- **Resources**: 읽을 수 있는 데이터 소스 (예: 상품 카탈로그)
- **Prompts**: 사전 정의된 프롬프트 템플릿

## 개발 환경 설정

### 필수 요구사항
- Python 3.13 이상
- uv 패키지 매니저

### 초기 설정

```bash
# 의존성 설치
uv sync

# 개발 의존성 추가 (필요시)
uv add --dev pytest pytest-asyncio
```

### 환경 변수 설정

`.env` 파일을 생성하여 쿠팡 API 자격 증명을 저장합니다:

```env
COUPANG_ACCESS_KEY=your_access_key
COUPANG_SECRET_KEY=your_secret_key
COUPANG_PARTNER_ID=your_partner_id
```

⚠️ **주의**: `.env` 파일은 절대 Git에 커밋하지 마세요!

## 쿠팡 API 설정

### 쿠팡 파트너스 API 신청

1. [쿠팡 파트너스](https://partners.coupang.com/)에 가입
2. API 액세스 키 발급
3. 파트너 ID 확인

### 주요 API 엔드포인트

쿠팡 파트너스 API는 다음과 같은 기능을 제공합니다:

- **상품 검색**: 키워드로 상품 검색
- **딥링크 생성**: 특정 상품에 대한 추천 링크 생성
- **카테고리 조회**: 상품 카테고리 목록

### API 인증

쿠팡 API는 HMAC 서명 기반 인증을 사용합니다:

```python
import hmac
import hashlib
import time

def generate_signature(method, path, secret_key, access_key):
    timestamp = str(int(time.time() * 1000))
    message = timestamp + method + path
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return {
        'Authorization': f'CEA algorithm=HmacSHA256, access-key={access_key}, signed-date={timestamp}, signature={signature}'
    }
```

## MCP 서버 구조

### 기본 서버 템플릿

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 서버 인스턴스 생성
app = Server("coupang-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록 반환"""
    return [
        Tool(
            name="search_products",
            description="쿠팡에서 상품을 검색합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "검색할 키워드"
                    },
                    "limit": {
                        "type": "number",
                        "description": "검색 결과 수 (기본값: 10)"
                    }
                },
                "required": ["keyword"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """도구 실행"""
    if name == "search_products":
        keyword = arguments["keyword"]
        limit = arguments.get("limit", 10)

        # 쿠팡 API 호출
        results = await search_coupang_products(keyword, limit)

        return [TextContent(
            type="text",
            text=f"검색 결과: {results}"
        )]

async def main():
    """서버 실행"""
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 구현할 기능

### 1단계: 기본 기능
- [ ] 상품 검색 (keyword 기반)
- [ ] 상품 상세 정보 조회
- [ ] 딥링크 생성

### 2단계: 고급 기능
- [ ] 카테고리별 상품 검색
- [ ] 가격 비교 (최저가 찾기)
- [ ] 베스트셀러 조회
- [ ] 할인율 높은 상품 찾기

### 3단계: 추가 기능
- [ ] 상품 리뷰 요약
- [ ] 가격 변동 추적
- [ ] 위시리스트 관리

## 개발 단계

### Step 1: 쿠팡 API 클라이언트 구현

`coupang_client.py` 파일 생성:

```python
import aiohttp
import hmac
import hashlib
import time
from typing import Optional

class CoupangClient:
    BASE_URL = "https://api-gateway.coupang.com"

    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.secret_key = secret_key

    def _generate_signature(self, method: str, path: str) -> dict:
        """HMAC 서명 생성"""
        timestamp = str(int(time.time() * 1000))
        message = timestamp + method + path
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return {
            'Authorization': f'CEA algorithm=HmacSHA256, access-key={self.access_key}, signed-date={timestamp}, signature={signature}',
            'Content-Type': 'application/json'
        }

    async def search_products(self, keyword: str, limit: int = 10) -> dict:
        """상품 검색"""
        path = f"/v2/providers/affiliate_open_api/apis/openapi/products/search"
        url = f"{self.BASE_URL}{path}?keyword={keyword}&limit={limit}"

        headers = self._generate_signature("GET", path)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()
```

### Step 2: MCP 서버 구현

`main.py`를 수정하여 MCP 서버 구현

### Step 3: 설정 관리

환경 변수나 설정 파일에서 API 키를 안전하게 로드

### Step 4: 에러 처리

API 호출 실패, 인증 오류 등에 대한 적절한 에러 처리

## 테스트 방법

### 단위 테스트

```bash
# pytest 실행
uv run pytest tests/
```

### 수동 테스트

MCP Inspector를 사용하여 서버 테스트:

```bash
# MCP Inspector 설치
npm install -g @modelcontextprotocol/inspector

# 서버 검사
mcp-inspector uv run python main.py
```

### Claude Desktop에서 테스트

`claude_desktop_config.json` 파일에 서버 추가:

```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": ["run", "python", "C:/workdir/space-cap/mcp-coupang-server/main.py"],
      "env": {
        "COUPANG_ACCESS_KEY": "your_key",
        "COUPANG_SECRET_KEY": "your_secret"
      }
    }
  }
}
```

## 배포 및 사용

### 로컬 사용

Claude Desktop 설정에 서버를 추가하면 자동으로 로드됩니다.

### 패키지 배포

```bash
# PyPI에 배포
uv build
uv publish
```

### 사용 예시

Claude Desktop에서:

```
쿠팡에서 "무선 마우스"를 검색해줘
```

MCP 서버가 자동으로 search_products 도구를 호출하여 결과를 반환합니다.

## 참고 자료

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [쿠팡 파트너스 API 문서](https://developers.coupang.com/)
- [Claude Desktop 설정](https://docs.anthropic.com/claude/docs/claude-desktop)

## 문제 해결

### API 인증 실패
- API 키가 올바른지 확인
- 서명 생성 로직이 정확한지 확인
- 타임스탬프가 올바르게 생성되는지 확인

### 서버 연결 실패
- stdio 통신이 제대로 설정되었는지 확인
- Python 경로와 실행 권한 확인
- 로그를 확인하여 에러 메시지 파악

### 성능 이슈
- API 호출에 캐싱 적용
- 비동기 처리 최적화
- 타임아웃 설정 추가
