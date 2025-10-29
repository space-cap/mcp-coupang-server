"""Simple test for product search."""

import asyncio
from src.coupang_client import CoupangClient

async def main():
    """Test product search."""
    print("=== Testing Product Search ===\n")

    async with CoupangClient() as client:
        try:
            # Search for products
            keyword = "laptop"
            limit = 3

            print(f"Searching for '{keyword}' (limit: {limit})...\n")

            products = await client.search_products(keyword, limit=limit)

            print(f"Found {len(products)} products:\n")

            for i, product in enumerate(products, 1):
                print(f"{i}. {product.product_name}")
                print(f"   ID: {product.product_id}")
                print(f"   Price: {product.product_price:,} won")

                if product.is_rocket:
                    print("   [Rocket Delivery]")
                if product.is_free_shipping:
                    print("   [Free Shipping]")
                if product.category_name:
                    print(f"   Category: {product.category_name}")

                print(f"   URL: {product.product_url}")
                print()

            if products:
                print("SUCCESS! Product search is working correctly.")
            else:
                print("No products found.")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
