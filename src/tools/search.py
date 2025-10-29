"""
Product search tool implementation.

Provides functionality for searching Coupang products by keyword.
"""

from typing import List
from src.models.product import Product, SearchParams


def format_search_results(products: List[Product], keyword: str) -> str:
    """
    Format product search results into a readable string.

    Args:
        products: List of Product objects from search
        keyword: The search keyword used

    Returns:
        Formatted string with product information

    Example:
        >>> products = [...]
        >>> formatted = format_search_results(products, "laptop")
        >>> print(formatted)
    """
    if not products:
        return f"No products found for keyword: '{keyword}'"

    lines = [f"Found {len(products)} product(s) for '{keyword}':\n"]

    for i, product in enumerate(products, 1):
        # Format price with thousands separator
        price_formatted = f"{product.product_price:,}원"

        # Add product info
        lines.append(f"{i}. {product.product_name}")
        lines.append(f"   Price: {price_formatted}")
        lines.append(f"   ID: {product.product_id}")

        # Add badges for special features
        badges = []
        if product.is_rocket:
            badges.append("🚀 Rocket Delivery")
        if product.is_free_shipping:
            badges.append("📦 Free Shipping")
        if product.discount_rate:
            badges.append(f"💰 Discount: {product.discount_rate}%")

        for badge in badges:
            lines.append(f"   {badge}")

        # Add affiliate URL
        lines.append(f"   URL: {product.product_url}")
        lines.append("")  # Empty line between products

    return "\n".join(lines)


def validate_search_params(keyword: str, limit: int) -> SearchParams:
    """
    Validate and create SearchParams object.

    Args:
        keyword: Search keyword
        limit: Maximum number of results

    Returns:
        Validated SearchParams object

    Raises:
        ValueError: If parameters are invalid

    Example:
        >>> params = validate_search_params("laptop", 20)
        >>> print(params.keyword, params.limit)
        laptop 20
    """
    return SearchParams(keyword=keyword, limit=limit)


def get_search_summary(products: List[Product]) -> dict:
    """
    Generate summary statistics from search results.

    Args:
        products: List of Product objects

    Returns:
        Dictionary with summary statistics

    Example:
        >>> products = [...]
        >>> summary = get_search_summary(products)
        >>> print(f"Average price: {summary['avg_price']}원")
    """
    if not products:
        return {
            "total_count": 0,
            "avg_price": 0,
            "min_price": 0,
            "max_price": 0,
            "rocket_count": 0,
            "free_shipping_count": 0
        }

    prices = [p.product_price for p in products]
    rocket_count = sum(1 for p in products if p.is_rocket)
    free_shipping_count = sum(1 for p in products if p.is_free_shipping)

    return {
        "total_count": len(products),
        "avg_price": sum(prices) // len(prices),
        "min_price": min(prices),
        "max_price": max(prices),
        "rocket_count": rocket_count,
        "free_shipping_count": free_shipping_count
    }
