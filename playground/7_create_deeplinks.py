"""
딥링크 생성 테스트

사용법:
    uv run python playground/7_create_deeplinks.py
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.coupang_client import CoupangClient


async def main():
    """딥링크 생성 테스트."""
    print("=" * 60)
    print("쿠팡 딥링크 생성 테스트")
    print("=" * 60)
    print()
    print("쿠팡 상품 URL을 트래킹 코드가 포함된 단축 URL로 변환합니다.")
    print()

    # URL 입력
    print("변환할 쿠팡 URL을 입력하세요.")
    print("(여러 개인 경우 쉼표로 구분)")
    print("예: https://www.coupang.com/vp/products/184614775")
    print()

    url_input = input("URL: ").strip()
    if not url_input:
        print("URL이 입력되지 않았습니다.")
        return

    # URL 파싱 (쉼표로 구분)
    urls = [url.strip() for url in url_input.split(",") if url.strip()]

    if not urls:
        print("유효한 URL이 없습니다.")
        return

    # Sub ID 입력 (선택사항)
    sub_id_input = input("\nSub ID (트래킹 ID, 선택사항, 엔터시 기본값): ").strip()
    sub_id = sub_id_input if sub_id_input else None

    print()
    print(f"{len(urls)}개 URL을 딥링크로 변환 중...")
    print("-" * 60)
    print()

    # 딥링크 생성
    async with CoupangClient() as client:
        try:
            deeplinks = await client.create_deeplinks(
                coupang_urls=urls,
                sub_id=sub_id
            )

            if not deeplinks:
                print("딥링크를 생성할 수 없습니다.")
                return

            print(f">> {len(deeplinks)}개 딥링크 생성 완료!\n")

            # 결과 출력
            for i, link in enumerate(deeplinks, 1):
                print(f"[{i}] Original URL:")
                print(f"    {link.original_url}")
                print(f"\n    >> Shortened URL (단축 URL):")
                print(f"    {link.shorten_url}")
                print(f"\n    >> Landing URL (전체 트래킹 URL):")
                print(f"    {link.landing_url}")
                print()

            # Sub ID 표시
            if sub_id:
                print("-" * 60)
                print(f"Tracking ID: {sub_id}")

        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
