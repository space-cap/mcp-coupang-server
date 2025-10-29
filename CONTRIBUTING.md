# 기여 가이드

Coupang MCP Server 프로젝트에 기여해주셔서 감사합니다! 이 문서는 프로젝트 기여 방법을 안내합니다.

## 기여 방법

### 1. 버그 리포트

버그를 발견하셨나요? 다음 정보를 포함하여 [이슈](../../issues)를 생성해주세요:

- **버그 설명**: 무엇이 잘못되었나요?
- **재현 방법**: 단계별 재현 과정
- **예상 동작**: 어떻게 동작해야 하나요?
- **실제 동작**: 실제로 어떻게 동작하나요?
- **환경 정보**:
  - OS (Windows/macOS/Linux)
  - Python 버전
  - UV 버전
  - 관련 의존성 버전

**예제:**
```markdown
## 버그 설명
상품 검색 시 한글 키워드가 제대로 인코딩되지 않음

## 재현 방법
1. `search_products("노트북")` 호출
2. API 요청 확인

## 예상 동작
한글이 URL 인코딩되어 전송되어야 함

## 실제 동작
인코딩 없이 전송되어 400 에러 발생

## 환경
- OS: Windows 11
- Python: 3.13.8
- UV: 0.5.0
```

### 2. 기능 제안

새로운 기능을 제안하고 싶으신가요?

1. [이슈](../../issues)를 생성
2. `enhancement` 라벨 추가
3. 다음 정보 포함:
   - 기능 설명
   - 사용 사례
   - 구현 아이디어 (선택사항)

### 3. 코드 기여

#### 시작하기

1. **저장소 포크**
   ```bash
   # GitHub에서 Fork 버튼 클릭
   ```

2. **로컬에 클론**
   ```bash
   git clone https://github.com/your-username/mcp-coupang-server.git
   cd mcp-coupang-server
   ```

3. **개발 환경 설정**
   ```bash
   # 의존성 설치
   uv sync

   # 환경 변수 설정
   cp .env.example .env
   # .env 파일 편집
   ```

4. **새 브랜치 생성**
   ```bash
   git checkout -b feature/your-feature-name
   # 또는
   git checkout -b fix/bug-description
   ```

#### 개발 가이드라인

**코드 스타일:**
- PEP 8 준수
- Type hints 사용
- Docstring 작성 (Google 스타일)

**예제:**
```python
def search_products(keyword: str, limit: int = 10) -> List[Product]:
    """
    Search for products by keyword.

    Args:
        keyword: Search query keyword
        limit: Maximum number of results (1-100)

    Returns:
        List of Product objects

    Raises:
        ValueError: If limit is out of range
        CoupangAPIError: If API request fails

    Example:
        >>> products = search_products("laptop", limit=20)
        >>> len(products)
        20
    """
    pass
```

**테스트 작성:**
- 모든 새 기능에 테스트 추가
- 기존 테스트가 통과하는지 확인

```bash
# 테스트 실행
uv run pytest

# 특정 테스트만 실행
uv run pytest tests/test_client.py::TestCoupangClient::test_search_products

# 커버리지 확인
uv run pytest --cov=src
```

**커밋 메시지:**
- 명확하고 설명적인 메시지 작성
- 현재형 사용 ("Add feature" not "Added feature")
- 첫 줄은 50자 이내
- 본문은 72자마다 줄바꿈

```
Add product comparison feature

- Implement compare_products function
- Add tests for comparison logic
- Update documentation

Fixes #123
```

#### Pull Request 생성

1. **변경사항 커밋**
   ```bash
   git add .
   git commit -m "Add feature: product comparison"
   ```

2. **푸시**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Pull Request 생성**
   - GitHub에서 "New Pull Request" 클릭
   - 변경사항 설명
   - 관련 이슈 번호 참조 (#123)

4. **PR 체크리스트**
   - [ ] 코드가 PEP 8을 준수하는가?
   - [ ] Type hints가 추가되었는가?
   - [ ] Docstring이 작성되었는가?
   - [ ] 테스트가 추가/업데이트되었는가?
   - [ ] 모든 테스트가 통과하는가?
   - [ ] 문서가 업데이트되었는가?

## 개발 워크플로우

### 브랜치 전략

- `main`: 안정 버전
- `feature/*`: 새 기능
- `fix/*`: 버그 수정
- `docs/*`: 문서 개선
- `refactor/*`: 리팩토링

### 릴리스 프로세스

1. 기능 개발 및 테스트
2. Pull Request 생성 및 리뷰
3. `main` 브랜치에 병합
4. 버전 태그 생성 (Semantic Versioning)

## 코드 리뷰

모든 Pull Request는 리뷰를 거칩니다:

1. **자동 검사**
   - 테스트 통과
   - 코드 스타일 검사

2. **수동 리뷰**
   - 코드 품질
   - 설계 패턴
   - 문서화

3. **피드백 처리**
   - 리뷰 코멘트 확인
   - 필요한 수정 반영
   - 토론 및 개선

## 프로젝트 구조

```
mcp-coupang-server/
├── src/              # 소스 코드
│   ├── server.py     # MCP 서버
│   ├── coupang_client.py  # API 클라이언트
│   ├── models/       # 데이터 모델
│   ├── tools/        # 도구 유틸리티
│   └── utils/        # 유틸리티 함수
├── tests/            # 테스트
├── docs/             # 문서
└── main.py           # 진입점
```

## 테스트 작성 가이드

### 단위 테스트

```python
import pytest
from src.coupang_client import CoupangClient

class TestCoupangClient:
    """Test cases for CoupangClient."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return CoupangClient(
            access_key="test_key",
            secret_key="test_secret",
            partner_id="test_partner"
        )

    def test_initialization(self, client):
        """Test client initialization."""
        assert client.access_key == "test_key"
        assert client.secret_key == "test_secret"

    @pytest.mark.asyncio
    async def test_search_products(self, client):
        """Test product search."""
        # Mock API response
        with patch.object(client, '_make_request') as mock_request:
            mock_request.return_value = {"data": []}

            products = await client.search_products("laptop")
            assert isinstance(products, list)
```

### 통합 테스트

```python
@pytest.mark.asyncio
async def test_full_search_workflow():
    """Test complete search workflow."""
    async with CoupangClient() as client:
        # Search
        products = await client.search_products("test", limit=5)

        # Get details
        if products:
            product = await client.get_product_details(products[0].product_id)
            assert product is not None
```

## 문서화

### 코드 문서화

모든 public 함수/클래스에 docstring 작성:

```python
class Product(BaseModel):
    """
    Coupang product model.

    Represents a product from Coupang's affiliate API.

    Attributes:
        product_id: Unique product identifier
        product_name: Product name
        product_price: Current price in KRW
        ...

    Example:
        >>> product = Product(
        ...     productId="123",
        ...     productName="Test",
        ...     productPrice=10000,
        ...     ...
        ... )
    """
    pass
```

### 문서 파일 업데이트

코드 변경 시 관련 문서 업데이트:
- README.md
- docs/*.md
- CONTRIBUTING.md (이 파일)

## 도움이 필요하신가요?

- [이슈](../../issues)에서 질문하기
- [Discussion](../../discussions)에서 토론하기
- 기존 코드와 테스트 참고하기

## 라이선스

기여하신 코드는 프로젝트의 MIT 라이선스 하에 배포됩니다.

## 감사합니다!

여러분의 기여가 이 프로젝트를 더 좋게 만듭니다. 감사합니다!
