"""
여러 키워드로 상품 비교 테스트

사용법:
    uv run python playground/3_compare_products.py
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.coupang_client import CoupangClient


async def main():
    """여러 키워드로 상품 검색 및 비교."""
    print("=" * 60)
    print("쿠팡 상품 비교 검색")
    print("=" * 60)
    print()

    # 키워드 입력
    keywords_input = input("검색어를 쉼표로 구분하여 입력하세요 (예: 노트북,마우스,키보드): ").strip()

    if not keywords_input:
        print("기본 검색어 사용: 노트북, 마우스, 키보드")
        keywords = ["노트북", "마우스", "키보드"]
    else:
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

    if not keywords:
        print("검색어를 입력해주세요.")
        return

    print()
    print(f"검색할 키워드: {', '.join(keywords)}")
    print("-" * 60)
    print()

    # 각 키워드로 검색
    async with CoupangClient() as client:
        try:
            for keyword in keywords:
                print(f"\n[{keyword}] 검색 중...")
                products = await client.search_products(keyword, limit=3)

                if not products:
                    print(f"  결과 없음")
                    continue

                print(f"  {len(products)}개 상품 발견:")

                for i, product in enumerate(products, 1):
                    print(f"    {i}. {product.product_name}")
                    print(f"       {product.product_price:,}원", end="")

                    if product.is_rocket:
                        print(" [로켓배송]", end="")
                    if product.discount_rate:
                        print(f" [할인 {product.discount_rate}%]", end="")

                    print()

            print()
            print("-" * 60)
            print("검색 완료!")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
