"""
로켓배송 상품 필터링 테스트

사용법:
    uv run python playground/5_rocket_delivery.py
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.coupang_client import CoupangClient


async def main():
    """로켓배송 가능 상품만 필터링."""
    print("=" * 60)
    print("쿠팡 로켓배송 상품 검색")
    print("=" * 60)
    print()

    # 검색어 입력
    keyword = input("검색어를 입력하세요: ").strip()
    if not keyword:
        keyword = "노트북"
        print(f"기본 검색어 사용: {keyword}")

    print()
    print(f"로켓배송 상품 검색 중: '{keyword}'...")
    print("-" * 60)
    print()

    # 검색
    async with CoupangClient() as client:
        try:
            products = await client.search_products(keyword, limit=50)

            if not products:
                print("검색 결과가 없습니다.")
                return

            # 로켓배송 필터링
            rocket_products = [p for p in products if p.is_rocket]

            print(f"전체 상품: {len(products)}개")
            print(f"로켓배송: {len(rocket_products)}개")
            print()

            if not rocket_products:
                print("로켓배송 가능한 상품이 없습니다.")
                return

            print("로켓배송 상품 목록:\n")

            # 가격순 정렬
            rocket_products.sort(key=lambda p: p.product_price)

            for i, product in enumerate(rocket_products[:15], 1):
                print(f"[{i}] {product.product_name}")
                print(f"    가격: {product.product_price:,}원")

                if product.is_free_shipping:
                    print(f"    무료배송 ✓")

                if product.discount_rate:
                    print(f"    할인: {product.discount_rate}%")
                    if product.original_price:
                        savings = product.original_price - product.product_price
                        print(f"    절약: {savings:,}원")

                print()

            if len(rocket_products) > 15:
                print(f"... 외 {len(rocket_products) - 15}개 더 있음")

            # 통계
            print("-" * 60)
            print("통계:")
            avg_price = sum(p.product_price for p in rocket_products) // len(rocket_products)
            print(f"  평균 가격: {avg_price:,}원")
            print(f"  최저 가격: {min(p.product_price for p in rocket_products):,}원")
            print(f"  최고 가격: {max(p.product_price for p in rocket_products):,}원")

            free_shipping_count = sum(1 for p in rocket_products if p.is_free_shipping)
            print(f"  무료배송: {free_shipping_count}개 ({free_shipping_count/len(rocket_products)*100:.1f}%)")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
