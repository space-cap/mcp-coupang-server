"""
카테고리별 베스트 상품 조회 테스트

사용법:
    uv run python playground/6_category_best.py
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.coupang_client import CoupangClient


async def main():
    """카테고리별 베스트 상품 조회."""
    print("=" * 60)
    print("쿠팡 카테고리별 베스트 상품 조회")
    print("=" * 60)
    print()
    print("사용 가능한 카테고리 ID:")
    print("  1001 - 여성패션")
    print("  1002 - 남성패션")
    print("  1010 - 뷰티")
    print("  1012 - 식품")
    print("  1013 - 주방용품")
    print("  1014 - 생활용품")
    print("  1015 - 홈인테리어")
    print("  1016 - 가전디지털")
    print("  1017 - 스포츠/레저")
    print("  1018 - 자동차용품")
    print("  1019 - 도서/음반/DVD")
    print("  1020 - 완구/취미")
    print("  1021 - 문구/오피스")
    print("  1024 - 헬스/건강식품")
    print("  1025 - 국내여행")
    print("  1026 - 해외여행")
    print("  1029 - 반려동물용품")
    print("  1030 - 유아동패션")
    print()

    # 카테고리 ID 입력
    category_id = input("카테고리 ID를 입력하세요 (기본값: 1001): ").strip()
    if not category_id:
        category_id = "1001"

    # 결과 개수 입력
    limit_input = input("결과 개수 (1-100, 기본값: 10): ").strip()
    if limit_input:
        try:
            limit = int(limit_input)
            if limit < 1 or limit > 100:
                print("1-100 사이 값을 입력하세요. 기본값 10 사용.")
                limit = 10
        except ValueError:
            print("숫자를 입력하세요. 기본값 10 사용.")
            limit = 10
    else:
        limit = 10

    print()
    print(f"카테고리 {category_id}의 베스트 상품 조회 중... (최대 {limit}개)")
    print("-" * 60)
    print()

    # 베스트 상품 조회
    async with CoupangClient() as client:
        try:
            products = await client.get_best_products_by_category(
                category_id=category_id,
                limit=limit
            )

            if not products:
                print("베스트 상품을 찾을 수 없습니다.")
                return

            print(f">> {len(products)}개 베스트 상품 발견!\n")

            # 결과 출력
            for i, product in enumerate(products, 1):
                print(f"[{i}] {product.product_name}")
                print(f"    가격: {product.product_price:,}원")
                print(f"    ID: {product.product_id}")

                # 카테고리
                if product.category_name:
                    print(f"    카테고리: {product.category_name}")

                # 배송 정보
                features = []
                if product.is_rocket:
                    features.append("로켓배송")
                if product.is_free_shipping:
                    features.append("무료배송")
                if features:
                    print(f"    배송: {', '.join(features)}")

                # 할인 정보
                if product.discount_rate:
                    print(f"    할인: {product.discount_rate}%")
                    if product.original_price:
                        savings = product.original_price - product.product_price
                        print(f"    절약: {savings:,}원")

                print(f"    URL: {product.product_url}")
                print()

            # 통계
            print("-" * 60)
            print("통계:")
            avg_price = sum(p.product_price for p in products) // len(products)
            print(f"  평균 가격: {avg_price:,}원")
            print(f"  최저 가격: {min(p.product_price for p in products):,}원")
            print(f"  최고 가격: {max(p.product_price for p in products):,}원")

            rocket_count = sum(1 for p in products if p.is_rocket)
            if rocket_count > 0:
                print(f"  로켓배송: {rocket_count}개 ({rocket_count/len(products)*100:.1f}%)")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
