# 사용 예제

이 문서는 Coupang MCP 서버의 다양한 사용 예제를 제공합니다.

## 기본 사용법

### 1. 상품 검색

Claude에게 다음과 같이 요청할 수 있습니다:

#### 예제 1: 기본 검색
```
쿠팡에서 "노트북"을 검색해줘
```

**응답:**
```
Found 10 product(s) for '노트북':

1. LG 그램 17인치 노트북 2024
   Price: 1,899,000원
   ID: 7891234567
   🚀 Rocket Delivery
   📦 Free Shipping
   URL: https://link.coupang.com/...

2. 삼성 갤럭시북4 Pro
   Price: 1,599,000원
   ID: 7891234568
   🚀 Rocket Delivery
   URL: https://link.coupang.com/...

...
```

#### 예제 2: 결과 개수 지정
```
쿠팡에서 "아이폰 15"를 20개 검색해줘
```

#### 예제 3: 영어 검색
```
Search for "coffee maker" on Coupang
```

### 2. 상품 상세 정보 조회

검색 결과에서 받은 상품 ID로 상세 정보를 조회:

```
상품 ID "7891234567"의 상세 정보를 알려줘
```

**응답:**
```
Product Details for ID: 7891234567

Name: LG 그램 17인치 노트북 2024 17Z90S
Price: 1,899,000원
Original Price: 2,299,000원
Discount: 17% (Save 400,000원)
Category: 노트북/PC
Shipping: 🚀 Rocket Delivery, 📦 Free Shipping

Image: https://thumbnail.coupangcdn.com/thumbnails/...
Affiliate URL: https://link.coupang.com/a/...
```

### 3. 카테고리별 베스트 상품 조회

특정 카테고리의 인기 상품을 조회:

#### 예제 1: 가전디지털 베스트 상품
```
쿠팡 가전디지털 카테고리(1016)의 베스트 상품을 보여줘
```

**응답:**
```
Found 20 best product(s) in category '1016':

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

#### 예제 2: 뷰티 카테고리 상위 10개
```
쿠팡 뷰티 카테고리(1010)의 인기 상품 10개만 보여줘
```

#### 사용 가능한 카테고리 코드

| 코드 | 카테고리명 |
|------|-----------|
| 1001 | 여성패션 |
| 1002 | 남성패션 |
| 1010 | 뷰티 |
| 1012 | 식품 |
| 1013 | 주방용품 |
| 1014 | 생활용품 |
| 1015 | 홈인테리어 |
| 1016 | 가전디지털 |
| 1017 | 스포츠/레저 |
| 1018 | 자동차용품 |
| 1019 | 도서/음반/DVD |
| 1020 | 완구/취미 |
| 1021 | 문구/오피스 |
| 1024 | 헬스/건강식품 |
| 1025 | 국내여행 |
| 1026 | 해외여행 |
| 1029 | 반려동물용품 |
| 1030 | 유아동패션 |

### 4. 딥링크 생성

쿠팡 URL을 트래킹 코드가 포함된 단축 URL로 변환:

#### 예제 1: 단일 URL 변환
```
이 쿠팡 URL을 딥링크로 변환해줘:
https://www.coupang.com/vp/products/184614775
```

**응답:**
```
Created 1 deeplink(s):

1. Original: https://www.coupang.com/vp/products/184614775
   Shortened: https://coupa.ng/blE0dT
   Landing: https://link.coupang.com/re/AFFSDP?lptag=AF1234567&pageKey=319834306&itemId=1023216541&vendorItemId=70064597513&traceid=V0-183-5fddb21eaffbb2ef
```

#### 예제 2: 여러 URL 동시 변환
```
다음 쿠팡 URL들을 딥링크로 변환하고, Sub ID는 "campaign2024"로 설정해줘:
- https://www.coupang.com/vp/products/184614775
- https://www.coupang.com/vp/products/123456789
```

## 실전 활용 예제

### 1. 가격 비교

```
쿠팡에서 "무선 이어폰"을 검색해서 가장 저렴한 제품 3개를 추천해줘
```

Claude가 자동으로:
1. 상품 검색 도구 호출
2. 결과 분석 및 가격 비교
3. 상위 3개 추천

### 2. 특정 조건으로 필터링

```
쿠팡에서 "커피머신"을 검색해서 로켓배송이 가능한 제품만 보여줘
```

Claude가:
1. 상품 검색
2. isRocket=True 필터링
3. 결과 제시

### 3. 카테고리별 베스트 상품 비교

```
쿠팡에서 가전디지털(1016)과 뷰티(1010) 카테고리의 베스트 상품을 비교해줘
```

Claude가 여러 번 카테고리 베스트 도구를 호출하여 각 카테고리의 인기 상품 제공

### 4. 할인 상품 찾기

```
쿠팡에서 "스마트폰"을 검색해서 할인율이 높은 상품들을 추천해줘
```

Claude가:
1. 상품 검색
2. discountRate 필드 확인
3. 높은 할인율 순으로 정렬 및 추천

### 5. 카테고리 기반 쇼핑 추천

```
주방용품(1013) 카테고리에서 베스트 상품 중 10만원 이하 제품을 추천해줘
```

Claude가:
1. 주방용품 카테고리 베스트 상품 조회
2. 가격 필터링 (10만원 이하)
3. 추천 목록 제공

### 6. 상세 비교

```
쿠팡에서 "갤럭시 버즈"와 "에어팟"을 각각 검색하고 비교해줘
```

Claude가:
1. 두 제품 각각 검색
2. 가격, 배송 옵션, 할인율 비교
3. 종합 비교 결과 제공

## 고급 사용 예제

### 1. 쇼핑 리스트 작성

```
다음 물품들을 쿠팡에서 찾아서 총 가격을 계산해줘:
- 노트북 마우스
- USB-C 허브
- 노트북 거치대
```

### 2. 예산 내 쇼핑

```
50만원 예산으로 쿠팡에서 홈오피스 세팅을 구성해줘.
필요한 것: 모니터, 키보드, 마우스
```

### 3. 리뷰 기반 추천 요청

```
쿠팡에서 "블루투스 스피커"를 검색하고,
로켓배송 가능하고 가격이 10만원 이하인 제품을 추천해줘
```

### 4. 선물 찾기

```
30대 남성을 위한 생일 선물을 쿠팡에서 찾아줘.
예산은 5만원 정도야.
```

### 5. 카테고리별 트렌드 분석

```
여성패션(1001)과 남성패션(1002) 카테고리의 베스트 상품을 조회하고
평균 가격과 로켓배송 비율을 비교해줘
```

### 6. 검색 후 딥링크 생성

```
쿠팡에서 "무선 이어폰"을 검색한 후,
상위 3개 상품의 URL을 딥링크로 변환해줘
```

Claude가:
1. search_products로 "무선 이어폰" 검색
2. 상위 3개 상품의 productUrl 추출
3. create_deeplinks로 단축 URL 생성
4. 결과 제공

## API 직접 사용 (개발자용)

Python 코드에서 직접 사용하는 예제:

### 기본 사용

```python
import asyncio
from src.coupang_client import CoupangClient

async def main():
    # 클라이언트 생성
    async with CoupangClient() as client:
        # 상품 검색
        products = await client.search_products("노트북", limit=10)

        for product in products:
            print(f"{product.product_name}: {product.product_price:,}원")
            if product.is_rocket:
                print("  🚀 Rocket Delivery")

asyncio.run(main())
```

### 상세 정보 조회

```python
import asyncio
from src.coupang_client import CoupangClient

async def main():
    async with CoupangClient() as client:
        # 상품 상세 조회
        product = await client.get_product_details("1234567890")

        if product:
            print(f"Name: {product.product_name}")
            print(f"Price: {product.product_price:,}원")

            if product.discount_rate:
                print(f"Discount: {product.discount_rate}%")

            print(f"URL: {product.product_url}")

asyncio.run(main())
```

### 에러 처리

```python
import asyncio
from src.coupang_client import CoupangClient, CoupangAPIError

async def main():
    async with CoupangClient() as client:
        try:
            products = await client.search_products("laptop", limit=20)
            print(f"Found {len(products)} products")

        except CoupangAPIError as e:
            print(f"API Error: {e}")
        except ValueError as e:
            print(f"Validation Error: {e}")

asyncio.run(main())
```

### 여러 검색 동시 실행

```python
import asyncio
from src.coupang_client import CoupangClient

async def search_multiple(keywords):
    async with CoupangClient() as client:
        # 여러 검색을 동시에 실행
        tasks = [
            client.search_products(keyword, limit=5)
            for keyword in keywords
        ]

        results = await asyncio.gather(*tasks)

        for keyword, products in zip(keywords, results):
            print(f"\n{keyword}: {len(products)} products found")
            for product in products[:3]:  # 상위 3개만
                print(f"  - {product.product_name}")

asyncio.run(search_multiple(["노트북", "마우스", "키보드"]))
```

### 카테고리 베스트 상품 조회

```python
import asyncio
from src.coupang_client import CoupangClient
from src.utils.categories import get_category_name

async def main():
    async with CoupangClient() as client:
        # 가전디지털 카테고리 베스트 상품 조회
        category_id = "1016"
        products = await client.get_best_products_by_category(
            category_id=category_id,
            limit=10
        )

        category_name = get_category_name(category_id)
        print(f"\n{category_name} 카테고리 베스트 {len(products)}개:")

        for i, product in enumerate(products, 1):
            print(f"\n{i}. {product.product_name}")
            print(f"   가격: {product.product_price:,}원")
            if product.is_rocket:
                print("   로켓배송 가능")

asyncio.run(main())
```

### 딥링크 생성

```python
import asyncio
from src.coupang_client import CoupangClient

async def main():
    async with CoupangClient() as client:
        # 쿠팡 URL을 딥링크로 변환
        urls = [
            "https://www.coupang.com/vp/products/184614775",
            "https://www.coupang.com/vp/products/123456789"
        ]

        deeplinks = await client.create_deeplinks(
            coupang_urls=urls,
            sub_id="campaign2024"  # Optional
        )

        for link in deeplinks:
            print(f"원본: {link.original_url}")
            print(f"단축: {link.shorten_url}")
            print(f"랜딩: {link.landing_url}")
            print()

asyncio.run(main())
```

### 검색 후 딥링크 생성 (통합 예제)

```python
import asyncio
from src.coupang_client import CoupangClient

async def search_and_create_deeplinks(keyword: str, count: int = 3):
    """상품 검색 후 상위 결과의 딥링크 생성"""
    async with CoupangClient() as client:
        # 1. 상품 검색
        products = await client.search_products(keyword, limit=count)
        print(f"\n'{keyword}' 검색 결과 {len(products)}개:")

        # 2. 상품 URL 추출
        product_urls = [p.product_url for p in products]

        # 3. 딥링크 생성
        deeplinks = await client.create_deeplinks(
            coupang_urls=product_urls,
            sub_id="auto_search"
        )

        # 4. 결과 출력
        for i, (product, deeplink) in enumerate(zip(products, deeplinks), 1):
            print(f"\n[{i}] {product.product_name}")
            print(f"    가격: {product.product_price:,}원")
            print(f"    단축 URL: {deeplink.shorten_url}")

asyncio.run(search_and_create_deeplinks("무선 이어폰", 5))
```

## 응답 데이터 활용

### 상품 정보 추출

검색 결과에서 다음 정보를 활용할 수 있습니다:

- `product_id`: 상품 고유 ID
- `product_name`: 상품명
- `product_price`: 현재 가격
- `original_price`: 원래 가격 (할인 전)
- `discount_rate`: 할인율 (%)
- `product_url`: 제휴 링크
- `product_image`: 이미지 URL
- `category_name`: 카테고리
- `is_rocket`: 로켓배송 가능 여부
- `is_free_shipping`: 무료배송 가능 여부

### 제휴 링크 사용

모든 `product_url`은 쿠팡 파트너스 제휴 링크입니다:
- 사용자가 이 링크를 통해 구매하면 수수료 발생
- 링크는 자동으로 파트너 ID가 포함됨

## 팁과 요령

### 1. 정확한 검색어 사용

```
❌ "좋은 노트북"
✅ "LG 그램 17인치"
```

### 2. 구체적인 요청

```
❌ "무언가 찾아줘"
✅ "50만원 이하 게이밍 노트북을 찾아줘"
```

### 3. 필터 활용

```
✅ "쿠팡에서 '무선 이어폰'을 검색해서 로켓배송 가능한 제품만 보여줘"
```

### 4. 비교 요청

```
✅ "쿠팡에서 '갤럭시 버즈 2'와 '에어팟 프로 2'의 가격을 비교해줘"
```

## 제한사항

1. **검색 결과 제한**: 한 번에 최대 100개 상품
2. **API 속도 제한**: 쿠팡 API의 rate limit 적용
3. **실시간 재고**: 재고 정보는 실시간이 아닐 수 있음
4. **가격 변동**: 가격은 실시간으로 변경될 수 있음

## 추가 리소스

- [README.md](../README.md): 설치 및 기본 설정
- [Claude Desktop 설정](claude-desktop-setup.md): Claude Desktop 연동
- [개발 가이드](development-guide.md): 개발자 문서
