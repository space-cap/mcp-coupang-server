"""
Debug script to test Coupang API authentication.
"""

import asyncio
from src.utils.config import config
from src.utils.auth import CoupangAuth

async def main():
    """Debug API request."""
    print("=== Coupang API Debug ===\n")

    # Show config
    print("Configuration:")
    print(f"  Access Key: {config.access_key[:10]}..." if config.access_key else "  Access Key: None")
    print(f"  Secret Key: {config.secret_key[:10]}..." if config.secret_key else "  Secret Key: None")
    print(f"  Partner ID: {config.partner_id}")
    print(f"  Base URL: {config.api_base_url}\n")

    # Create auth
    auth = CoupangAuth(config.access_key, config.secret_key)

    # Test signature generation
    method = "GET"
    path = "/v2/providers/affiliate_open_api/apis/openapi/products/search"
    query = "keyword=laptop&limit=10"

    print("Request Details:")
    print(f"  Method: {method}")
    print(f"  Path: {path}")
    print(f"  Query: {query}\n")

    # Generate headers
    headers = auth.generate_headers(method, path, query)

    print("Generated Headers:")
    for key, value in headers.items():
        if key == "Authorization":
            print(f"  {key}: {value[:100]}...")
        else:
            print(f"  {key}: {value}")

    print("\n" + "="*60)
    print("Note: 쿠팡 파트너스 API 문서를 확인하여")
    print("HMAC 서명 생성 방식이 정확한지 검증이 필요합니다.")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
