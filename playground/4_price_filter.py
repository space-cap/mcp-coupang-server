"""
가격 필터링 테스트

사용법:
    uv run python playground/4_price_filter.py
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.coupang_client import CoupangClient


async def main():
    """가격 범위로 상품 필터링."""
    print("=" * 60)
    print("쿠팡 상품 가격 필터링")
    print("=" * 60)
    print()

    # 검색어 입력
    keyword = input("검색어를 입력하세요: ").strip()
    if not keyword:
        keyword = "노트북"
        print(f"기본 검색어 사용: {keyword}")

    # 최소 가격
    min_price_input = input("최소 가격 (원, 엔터시 제한 없음): ").strip()
    min_price = int(min_price_input) if min_price_input else 0

    # 최대 가격
    max_price_input = input("최대 가격 (원, 엔터시 제한 없음): ").strip()
    max_price = int(max_price_input) if max_price_input else float('inf')

    print()
    print(f"검색 중: '{keyword}'")
    print(f"가격 범위: {min_price:,}원 ~ {max_price:,}원" if max_price != float('inf') else f"가격 범위: {min_price:,}원 이상")
    print("-" * 60)
    print()

    # 검색 및 필터링
    async with CoupangClient() as client:
        try:
            products = await client.search_products(keyword, limit=50)

            if not products:
                print("검색 결과가 없습니다.")
                return

            # 가격 필터링
            filtered = [
                p for p in products
                if min_price <= p.product_price <= max_price
            ]

            if not filtered:
                print(f"가격 범위 내 상품이 없습니다.")
                print(f"\n전체 검색 결과: {len(products)}개")
                print(f"최저가: {min(p.product_price for p in products):,}원")
                print(f"최고가: {max(p.product_price for p in products):,}원")
                return

            print(f">> {len(filtered)}개 상품 발견! (전체 {len(products)}개 중)\n")

            # 가격순 정렬
            filtered.sort(key=lambda p: p.product_price)

            for i, product in enumerate(filtered[:10], 1):  # 상위 10개만
                print(f"[{i}] {product.product_name}")
                print(f"    가격: {product.product_price:,}원")

                features = []
                if product.is_rocket:
                    features.append("로켓배송")
                if product.is_free_shipping:
                    features.append("무료배송")
                if product.discount_rate:
                    features.append(f"할인 {product.discount_rate}%")

                if features:
                    print(f"    특징: {', '.join(features)}")

                print()

            if len(filtered) > 10:
                print(f"... 외 {len(filtered) - 10}개 더 있음")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
