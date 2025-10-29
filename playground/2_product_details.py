"""
상품 상세 정보 조회 테스트

사용법:
    uv run python playground/2_product_details.py
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.coupang_client import CoupangClient


async def main():
    """상품 상세 정보 조회."""
    print("=" * 60)
    print("쿠팡 상품 상세 정보 조회")
    print("=" * 60)
    print()

    # 상품 ID 입력
    product_id = input("상품 ID를 입력하세요: ").strip()

    if not product_id:
        print("상품 ID가 필요합니다.")
        print("\n힌트: 먼저 1_simple_search.py로 검색하여 상품 ID를 확인하세요.")
        return

    print()
    print(f"상품 조회 중: {product_id}...")
    print("-" * 60)
    print()

    # 상세 정보 조회
    async with CoupangClient() as client:
        try:
            product = await client.get_product_details(product_id)

            if not product:
                print(f"상품을 찾을 수 없습니다. (ID: {product_id})")
                return

            # 상세 정보 출력
            print(">> 상품 정보\n")
            print(f"상품명: {product.product_name}")
            print(f"상품 ID: {product.product_id}")
            print()

            # 가격 정보
            print("가격 정보:")
            print(f"  현재가: {product.product_price:,}원")

            if product.original_price and product.discount_rate:
                print(f"  정가: {product.original_price:,}원")
                print(f"  할인율: {product.discount_rate}%")
                savings = product.original_price - product.product_price
                print(f"  절약액: {savings:,}원")

            print()

            # 카테고리
            if product.category_name:
                print(f"카테고리: {product.category_name}")
                print()

            # 배송 정보
            shipping_info = []
            if product.is_rocket:
                shipping_info.append("로켓배송")
            if product.is_free_shipping:
                shipping_info.append("무료배송")

            if shipping_info:
                print(f"배송: {', '.join(shipping_info)}")
                print()

            # 이미지 및 URL
            print(f"이미지: {product.product_image}")
            print(f"구매 링크: {product.product_url}")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
