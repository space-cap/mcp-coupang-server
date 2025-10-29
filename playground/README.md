# Playground - 쿠팡 API 테스트 스크립트

콘솔에서 직접 쿠팡 API를 테스트할 수 있는 스크립트 모음입니다.

## 사용 방법

모든 스크립트는 프로젝트 루트에서 실행하세요:

```bash
uv run python playground/<스크립트명>.py
```

## 스크립트 목록

### 1. 간단한 상품 검색 (`1_simple_search.py`)

기본적인 상품 검색 기능을 테스트합니다.

**실행:**
```bash
uv run python playground/1_simple_search.py
```

**기능:**
- 검색어 입력
- 결과 개수 지정 (1-100)
- 상품 정보 출력 (이름, 가격, ID, 배송 정보)

**예제 출력:**
```
검색어를 입력하세요 (기본값: 노트북): 마우스
결과 개수 (1-100, 기본값: 5): 3

✓ 3개 상품 발견!

[1] 로지텍 무선 마우스
    가격: 29,900원
    ID: 1234567890
    배송: 로켓배송, 무료배송
    ...
```

---

### 2. 상품 상세 정보 (`2_product_details.py`)

특정 상품 ID로 상세 정보를 조회합니다.

**실행:**
```bash
uv run python playground/2_product_details.py
```

**기능:**
- 상품 ID로 상세 정보 조회
- 가격 정보 (현재가, 정가, 할인율)
- 배송 정보
- 이미지 및 구매 링크

**사용 팁:**
1. 먼저 `1_simple_search.py`로 검색
2. 출력된 상품 ID를 복사
3. 이 스크립트로 상세 정보 확인

---

### 3. 여러 키워드 비교 (`3_compare_products.py`)

여러 검색어로 동시에 검색하고 결과를 비교합니다.

**실행:**
```bash
uv run python playground/3_compare_products.py
```

**기능:**
- 쉼표로 구분된 여러 키워드 입력
- 각 키워드별 상위 3개 상품 출력
- 가격 및 배송 정보 비교

**예제 입력:**
```
검색어를 쉼표로 구분하여 입력하세요: 노트북,마우스,키보드
```

---

### 4. 가격 필터링 (`4_price_filter.py`)

특정 가격 범위 내의 상품만 필터링합니다.

**실행:**
```bash
uv run python playground/4_price_filter.py
```

**기능:**
- 최소/최대 가격 범위 설정
- 가격순 정렬
- 통계 정보 (최저가, 최고가, 평균가)

**예제 사용:**
```
검색어를 입력하세요: 무선 이어폰
최소 가격 (원, 엔터시 제한 없음): 50000
최대 가격 (원, 엔터시 제한 없음): 150000
```

---

### 5. 로켓배송 필터링 (`5_rocket_delivery.py`)

로켓배송 가능한 상품만 필터링합니다.

**실행:**
```bash
uv run python playground/5_rocket_delivery.py
```

**기능:**
- 로켓배송 상품만 필터링
- 가격순 정렬
- 통계 (평균가, 무료배송 비율 등)

---

### 6. 카테고리별 베스트 상품 (`6_category_best.py`)

특정 카테고리의 베스트 상품을 조회합니다.

**실행:**
```bash
uv run python playground/6_category_best.py
```

**기능:**
- 카테고리 ID로 베스트 상품 조회
- 가격, 배송, 할인 정보
- 통계 (평균가, 로켓배송 비율 등)

---

### 7. 딥링크 생성 (`7_create_deeplinks.py`)

쿠팡 상품 URL을 트래킹 코드가 포함된 단축 URL로 변환합니다.

**실행:**
```bash
uv run python playground/7_create_deeplinks.py
```

**기능:**
- 쿠팡 URL을 단축 URL로 변환
- 트래킹 코드 자동 포함
- 여러 URL 동시 변환 가능
- Sub ID (트래킹 ID) 선택 가능

**예제 입력:**
```
URL: https://www.coupang.com/vp/products/184614775
Sub ID (엔터시 기본값): mytracker
```

**예제 출력:**
```
[1] Original URL:
    https://www.coupang.com/vp/products/184614775

    >> Shortened URL (단축 URL):
    https://coupa.ng/blE0dT

    >> Landing URL (전체 트래킹 URL):
    https://link.coupang.com/re/AFFSDP?lptag=AF1234567&...

Tracking ID: mytracker
```

**사용 가능한 카테고리 ID:**
- 1001 - 여성패션
- 1002 - 남성패션
- 1010 - 뷰티
- 1012 - 식품
- 1013 - 주방용품
- 1014 - 생활용품
- 1015 - 홈인테리어
- 1016 - 가전디지털
- 1017 - 스포츠/레저
- 1018 - 자동차용품
- 1019 - 도서/음반/DVD
- 1020 - 완구/취미
- 1021 - 문구/오피스
- 1024 - 헬스/건강식품
- 1025 - 국내여행
- 1026 - 해외여행
- 1029 - 반려동물용품
- 1030 - 유아동패션

---

## 요구사항

- Python 3.13+
- UV 패키지 관리자
- `.env` 파일에 쿠팡 API 키 설정

## 환경 변수 확인

스크립트 실행 전 `.env` 파일이 설정되어 있는지 확인하세요:

```env
COUPANG_ACCESS_KEY=your_access_key
COUPANG_SECRET_KEY=your_secret_key
COUPANG_PARTNER_ID=your_partner_id
```

## 문제 해결

### 오류: ModuleNotFoundError

프로젝트 루트에서 실행하세요:
```bash
cd /path/to/mcp-coupang-server
uv run python playground/1_simple_search.py
```

### 오류: API 인증 실패

`.env` 파일의 API 키를 확인하세요.

### 한글 깨짐 (Windows)

Windows 터미널에서 UTF-8 설정:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

또는 Windows Terminal 사용 권장.

## 추가 테스트

더 복잡한 테스트는 직접 코드를 작성하세요:

```python
import asyncio
from src.coupang_client import CoupangClient

async def custom_test():
    async with CoupangClient() as client:
        products = await client.search_products("검색어", limit=10)
        # 원하는 처리...

asyncio.run(custom_test())
```

## 참고

- [프로젝트 README](../README.md)
- [사용 예제 문서](../docs/usage-examples.md)
- [개발 가이드](../docs/development-guide.md)
