"""
Integration tests for Coupang API.

These tests make REAL API calls to Coupang.
Run with: uv run pytest tests/test_integration.py -v -s
"""

import pytest
from src.coupang_client import CoupangClient, CoupangAPIError


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_search_products():
    """Test real product search with Coupang API."""
    print("\n=== Testing Real Coupang API Search ===")

    async with CoupangClient() as client:
        try:
            # Search for a common product
            keyword = "노트북"
            print(f"\nSearching for '{keyword}'...")

            products = await client.search_products(keyword, limit=5)

            print(f"\nFound {len(products)} products")

            if products:
                print("\n--- First 3 Products ---")
                for i, product in enumerate(products[:3], 1):
                    print(f"\n{i}. {product.product_name}")
                    print(f"   ID: {product.product_id}")
                    print(f"   Price: {product.product_price:,}원")

                    if product.is_rocket:
                        print("   🚀 Rocket Delivery")
                    if product.is_free_shipping:
                        print("   📦 Free Shipping")
                    if product.discount_rate:
                        print(f"   💰 Discount: {product.discount_rate}%")

                    print(f"   URL: {product.product_url}")

                # Verify data structure
                assert len(products) > 0
                assert products[0].product_id is not None
                assert products[0].product_name is not None
                assert products[0].product_price > 0

                print("\n✅ Search test PASSED")
            else:
                print("⚠️ No products found - API might not be working correctly")

        except CoupangAPIError as e:
            print(f"\n❌ API Error: {e}")
            pytest.fail(f"Coupang API call failed: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            pytest.fail(f"Unexpected error: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_get_product_details():
    """Test real product details retrieval."""
    print("\n=== Testing Real Product Details Retrieval ===")

    async with CoupangClient() as client:
        try:
            # First, search to get a valid product ID
            print("\nSearching for a product to get ID...")
            products = await client.search_products("노트북", limit=1)

            if not products:
                pytest.skip("No products found to test details")

            product_id = products[0].product_id
            print(f"\nGetting details for product ID: {product_id}")

            # Get product details
            product = await client.get_product_details(product_id)

            if product:
                print(f"\n--- Product Details ---")
                print(f"Name: {product.product_name}")
                print(f"ID: {product.product_id}")
                print(f"Price: {product.product_price:,}원")

                if product.original_price and product.discount_rate:
                    print(f"Original Price: {product.original_price:,}원")
                    print(f"Discount: {product.discount_rate}%")

                if product.category_name:
                    print(f"Category: {product.category_name}")

                if product.is_rocket or product.is_free_shipping:
                    shipping = []
                    if product.is_rocket:
                        shipping.append("🚀 Rocket Delivery")
                    if product.is_free_shipping:
                        shipping.append("📦 Free Shipping")
                    print(f"Shipping: {', '.join(shipping)}")

                print(f"\nImage: {product.product_image}")
                print(f"URL: {product.product_url}")

                # Verify data
                assert product.product_id == product_id
                assert product.product_name is not None
                assert product.product_price > 0

                print("\n✅ Product details test PASSED")
            else:
                print(f"⚠️ Product {product_id} not found")

        except CoupangAPIError as e:
            print(f"\n❌ API Error: {e}")
            pytest.fail(f"Coupang API call failed: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            pytest.fail(f"Unexpected error: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_multiple_searches():
    """Test multiple searches with different keywords."""
    print("\n=== Testing Multiple Searches ===")

    keywords = ["노트북", "마우스", "키보드"]

    async with CoupangClient() as client:
        try:
            for keyword in keywords:
                print(f"\nSearching for '{keyword}'...")
                products = await client.search_products(keyword, limit=3)

                print(f"Found {len(products)} products")

                if products:
                    print(f"  - {products[0].product_name}")
                    assert len(products) > 0
                else:
                    print(f"  ⚠️ No products found for '{keyword}'")

            print("\n✅ Multiple searches test PASSED")

        except CoupangAPIError as e:
            print(f"\n❌ API Error: {e}")
            pytest.fail(f"Coupang API call failed: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_error_handling():
    """Test API error handling with invalid requests."""
    print("\n=== Testing Error Handling ===")

    async with CoupangClient() as client:
        try:
            # Test with invalid limit
            print("\nTesting invalid limit (should fail)...")
            with pytest.raises(ValueError):
                await client.search_products("test", limit=101)

            print("✅ Limit validation works")

            # Test with empty keyword
            print("\nTesting empty keyword...")
            products = await client.search_products("", limit=5)
            print(f"Empty keyword returned {len(products)} products")

            print("\n✅ Error handling test PASSED")

        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            pytest.fail(f"Unexpected error: {e}")


if __name__ == "__main__":
    """Run integration tests directly."""
    import asyncio

    print("=" * 60)
    print("COUPANG API INTEGRATION TESTS")
    print("=" * 60)

    async def run_all_tests():
        """Run all integration tests."""
        await test_real_search_products()
        await test_real_get_product_details()
        await test_multiple_searches()
        await test_api_error_handling()

    try:
        asyncio.run(run_all_tests())
        print("\n" + "=" * 60)
        print("ALL INTEGRATION TESTS COMPLETED")
        print("=" * 60)
    except Exception as e:
        print(f"\n\n❌ Tests failed with error: {e}")
        import traceback
        traceback.print_exc()
