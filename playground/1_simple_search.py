"""
간단한 상품 검색 테스트

사용법:
    uv run python playground/1_simple_search.py
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.coupang_client import CoupangClient


async def main():
    """간단한 상품 검색."""
    print("=" * 60)
    print("쿠팡 상품 검색 테스트")
    print("=" * 60)
    print()

    # 검색어 입력
    keyword = input("검색어를 입력하세요 (기본값: 노트북): ").strip()
    if not keyword:
        keyword = "노트북"

    # 결과 개수 입력
    limit_input = input("결과 개수 (1-100, 기본값: 5): ").strip()
    if limit_input:
        try:
            limit = int(limit_input)
            if limit < 1 or limit > 100:
                print("1-100 사이 값을 입력하세요. 기본값 5 사용.")
                limit = 5
        except ValueError:
            print("숫자를 입력하세요. 기본값 5 사용.")
            limit = 5
    else:
        limit = 5

    print()
    print(f"검색 중: '{keyword}' (최대 {limit}개)...")
    print("-" * 60)
    print()

    # 검색 실행
    async with CoupangClient() as client:
        try:
            products = await client.search_products(keyword, limit=limit)

            if not products:
                print("검색 결과가 없습니다.")
                return

            print(f">> {len(products)}개 상품 발견!\n")

            # 결과 출력
            for i, product in enumerate(products, 1):
                print(f"[{i}] {product.product_name}")
                print(f"    가격: {product.product_price:,}원")
                print(f"    ID: {product.product_id}")

                # 배송 정보
                features = []
                if product.is_rocket:
                    features.append("로켓배송")
                if product.is_free_shipping:
                    features.append("무료배송")
                if features:
                    print(f"    배송: {', '.join(features)}")

                if product.category_name:
                    print(f"    카테고리: {product.category_name}")

                print(f"    URL: {product.product_url}")
                print(f"    Image: {product.product_image}")
                print()

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
