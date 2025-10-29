"""Debug script to see actual Coupang API response."""

import asyncio
import json
from src.coupang_client import CoupangClient

async def main():
    """Check real API response structure."""
    print("=== Coupang API Response Debug ===\n")

    async with CoupangClient() as client:
        try:
            # Make raw request
            path = "/v2/providers/affiliate_open_api/apis/openapi/products/search"
            params = {"keyword": "laptop", "limit": 2}

            print(f"Making request to: {path}")
            print(f"Parameters: {params}\n")

            response_data = await client._make_request("GET", path, params)

            print("=== RAW API RESPONSE ===")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
