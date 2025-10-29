# 쿠팡 MCP 서버 구현 단계

## 개요

이 문서는 쿠팡 MCP 서버를 처음부터 완성까지 구현하는 단계별 가이드입니다.

## 전체 로드맵

```
Phase 1: 프로젝트 기초 설정 (30분)
  ↓
Phase 2: 쿠팡 API 클라이언트 구현 (1-2시간)
  ↓
Phase 3: MCP 서버 기본 구조 (1시간)
  ↓
Phase 4: 첫 번째 도구 구현 (1시간)
  ↓
Phase 5: 테스트 및 디버깅 (30분-1시간)
  ↓
Phase 6: 추가 기능 확장 (선택사항)
```

---

## Phase 1: 프로젝트 기초 설정

### 1.1 폴더 구조 생성

```bash
# 필요한 폴더 및 파일 생성
mkdir -p src/tools src/utils src/models tests/test_tools logs
touch src/__init__.py src/server.py src/coupang_client.py
touch src/tools/__init__.py src/utils/__init__.py src/models/__init__.py
touch tests/__init__.py
```

### 1.2 필수 의존성 설치

필요한 패키지들:
- `aiohttp`: 비동기 HTTP 클라이언트 (쿠팡 API 호출)
- `python-dotenv`: 환경 변수 로드
- `pydantic`: 데이터 검증 및 모델링

개발 의존성:
- `pytest`: 테스트 프레임워크
- `pytest-asyncio`: 비동기 테스트 지원

### 1.3 환경 변수 설정

`.env` 파일에 쿠팡 API 자격 증명 추가:
```env
COUPANG_ACCESS_KEY=your_access_key_here
COUPANG_SECRET_KEY=your_secret_key_here
COUPANG_PARTNER_ID=your_partner_id_here
```

**체크포인트**: `.env` 파일이 `.gitignore`에 포함되어 있는지 확인

---

## Phase 2: 쿠팡 API 클라이언트 구현

### 2.1 설정 관리 구현

**파일**: `src/utils/config.py`

**기능**:
- 환경 변수 로드
- 필수 설정 검증
- 설정 객체 제공

**우선순위**: ⭐⭐⭐ (가장 먼저 구현)

### 2.2 인증 모듈 구현

**파일**: `src/utils/auth.py`

**기능**:
- HMAC SHA256 서명 생성
- 쿠팡 API 인증 헤더 생성
- 타임스탬프 생성

**우선순위**: ⭐⭐⭐ (필수)

**참고**: 쿠팡 API는 다음 형식의 서명이 필요합니다:
```
Authorization: CEA algorithm=HmacSHA256, access-key={key}, signed-date={timestamp}, signature={signature}
```

### 2.3 데이터 모델 정의

**파일**: `src/models/product.py`

**기능**:
- 상품 데이터 클래스 정의 (Pydantic 모델 사용)
- API 응답을 구조화된 데이터로 변환

**우선순위**: ⭐⭐

### 2.4 쿠팡 API 클라이언트 구현

**파일**: `src/coupang_client.py`

**기능**:
- API 기본 URL 및 엔드포인트 정의
- HTTP 요청 메서드 (GET, POST)
- 상품 검색 메서드
- 상품 상세 조회 메서드
- 딥링크 생성 메서드
- 에러 핸들링

**우선순위**: ⭐⭐⭐

**주요 메서드**:
```python
class CoupangClient:
    async def search_products(keyword: str, limit: int) -> dict
    async def get_product_details(product_id: str) -> dict
    async def generate_deeplink(product_url: str) -> str
```

**체크포인트**: 간단한 스크립트로 API 호출이 정상 작동하는지 테스트

---

## Phase 3: MCP 서버 기본 구조

### 3.1 서버 초기화

**파일**: `src/server.py`

**기능**:
- MCP Server 인스턴스 생성
- CoupangClient 초기화
- 서버 설정

**우선순위**: ⭐⭐⭐

### 3.2 도구 목록 핸들러

**기능**:
- `@app.list_tools()` 데코레이터 구현
- 사용 가능한 도구 목록 반환
- 각 도구의 스키마 정의

**우선순위**: ⭐⭐⭐

### 3.3 도구 호출 핸들러

**기능**:
- `@app.call_tool()` 데코레이터 구현
- 도구 이름에 따라 적절한 함수 라우팅
- 결과를 MCP 형식으로 반환

**우선순위**: ⭐⭐⭐

### 3.4 메인 진입점

**파일**: `main.py`

**기능**:
- 서버 실행 로직
- stdio 통신 설정
- asyncio 이벤트 루프 실행

**우선순위**: ⭐⭐⭐

**체크포인트**: MCP Inspector로 서버가 시작되는지 확인

---

## Phase 4: 첫 번째 도구 구현

### 4.1 상품 검색 도구

**파일**: `src/tools/search.py`

**기능**:
- 키워드로 상품 검색
- 검색 결과 포맷팅
- 에러 처리

**입력 파라미터**:
- `keyword` (필수): 검색 키워드
- `limit` (선택): 결과 개수 (기본값: 10)

**출력**:
```
검색 결과: {keyword}

1. [상품명]
   - 가격: {price}원
   - 로켓배송: {available}
   - 링크: {url}

2. [상품명]
   ...
```

**우선순위**: ⭐⭐⭐ (첫 번째 구현)

### 4.2 서버에 도구 통합

`src/server.py`에서:
1. 도구 목록에 "search_products" 추가
2. 도구 호출 핸들러에서 search.py 함수 호출
3. 결과를 TextContent로 반환

**체크포인트**: Claude Desktop 또는 MCP Inspector에서 상품 검색 테스트

---

## Phase 5: 테스트 및 디버깅

### 5.1 단위 테스트 작성

**파일**: `tests/test_coupang_client.py`

**테스트 항목**:
- API 서명 생성 테스트
- API 호출 모킹 테스트
- 에러 처리 테스트

### 5.2 통합 테스트

**파일**: `tests/test_server.py`

**테스트 항목**:
- 도구 목록 조회 테스트
- 도구 호출 테스트
- 잘못된 입력 처리 테스트

### 5.3 수동 테스트

#### MCP Inspector 사용
```bash
npx @modelcontextprotocol/inspector uv run python main.py
```

#### Claude Desktop 설정
`claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": ["run", "python", "C:/workdir/space-cap/mcp-coupang-server/main.py"],
      "env": {
        "COUPANG_ACCESS_KEY": "your_key",
        "COUPANG_SECRET_KEY": "your_secret",
        "COUPANG_PARTNER_ID": "your_id"
      }
    }
  }
}
```

**체크포인트**:
- ✅ 서버가 정상적으로 시작됨
- ✅ 도구 목록이 표시됨
- ✅ 상품 검색이 작동함
- ✅ 에러가 적절하게 처리됨

---

## Phase 6: 추가 기능 확장 (선택사항)

### 6.1 상품 상세 정보 도구

**파일**: `src/tools/product.py`

**기능**: 특정 상품의 상세 정보 조회

### 6.2 딥링크 생성 도구

**파일**: `src/tools/link.py`

**기능**: 제휴 링크 생성

### 6.3 카테고리 검색

**기능**: 카테고리별 상품 검색

### 6.4 가격 비교

**기능**: 여러 상품의 가격 비교

### 6.5 베스트셀러 조회

**기능**: 인기 상품 목록 조회

---

## 실제 작업 순서 요약

### 최소 기능 구현 (MVP)

1. ✅ **폴더 구조 생성**
2. ✅ **필수 패키지 설치** (aiohttp, python-dotenv, pydantic)
3. ✅ **환경 변수 설정** (.env 파일)
4. 🔧 **config.py 구현** (환경 변수 로드)
5. 🔧 **auth.py 구현** (HMAC 서명)
6. 🔧 **coupang_client.py 구현** (API 클라이언트 기본)
7. 🔧 **product.py 모델 구현** (데이터 구조)
8. 🔧 **search.py 도구 구현** (상품 검색)
9. 🔧 **server.py 구현** (MCP 서버)
10. 🔧 **main.py 구현** (서버 실행)
11. 🧪 **테스트** (MCP Inspector 또는 Claude Desktop)

### 완전한 기능 구현

12. 📝 **단위 테스트 작성**
13. ➕ **추가 도구 구현** (상품 상세, 딥링크 등)
14. 🎨 **출력 포맷 개선**
15. ⚡ **성능 최적화** (캐싱 등)
16. 📚 **문서 업데이트**

---

## 각 단계별 예상 시간

| 단계 | 작업 | 예상 시간 |
|------|------|-----------|
| 1 | 프로젝트 설정 | 30분 |
| 2 | API 클라이언트 구현 | 1-2시간 |
| 3 | MCP 서버 기본 구조 | 1시간 |
| 4 | 첫 번째 도구 구현 | 1시간 |
| 5 | 테스트 및 디버깅 | 30분-1시간 |
| **합계 (MVP)** | | **4-5.5시간** |
| 6 | 추가 기능 확장 | 2-4시간 |
| **합계 (전체)** | | **6-9.5시간** |

---

## 중요 체크리스트

### 보안
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있음
- [ ] API 키가 코드에 하드코딩되지 않음
- [ ] HMAC 서명이 올바르게 생성됨

### 기능
- [ ] 서버가 정상적으로 시작됨
- [ ] 도구 목록이 올바르게 반환됨
- [ ] 상품 검색이 작동함
- [ ] 결과가 읽기 쉬운 형식으로 출력됨

### 에러 처리
- [ ] API 호출 실패 시 적절한 에러 메시지
- [ ] 잘못된 입력 처리
- [ ] 네트워크 타임아웃 처리

### 테스트
- [ ] MCP Inspector에서 테스트 완료
- [ ] Claude Desktop에서 테스트 완료
- [ ] 단위 테스트 작성 (선택)

---

## 다음 단계

이 문서를 읽었다면:

1. **Phase 1부터 시작**: 폴더 구조를 생성하고 필수 패키지를 설치
2. **순차적으로 진행**: 각 Phase를 완료한 후 다음 단계로
3. **체크포인트 확인**: 각 단계의 체크포인트에서 작동 여부 확인
4. **문제 발생 시**: `docs/development-guide.md`의 "문제 해결" 섹션 참조

준비되었다면 "Phase 1 시작"이라고 말씀해주세요!
