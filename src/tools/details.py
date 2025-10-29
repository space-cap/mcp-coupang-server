"""
Product details tool implementation.

Provides functionality for retrieving detailed product information.
"""

from typing import Optional
from src.models.product import Product


def format_product_details(product: Product) -> str:
    """
    Format product details into a readable string.

    Args:
        product: Product object with detailed information

    Returns:
        Formatted string with product details

    Example:
        >>> product = Product(...)
        >>> formatted = format_product_details(product)
        >>> print(formatted)
    """
    # Format price with thousands separator
    price_formatted = f"{product.product_price:,}원"

    lines = [
        f"Product Details for ID: {product.product_id}\n",
        f"Name: {product.product_name}",
        f"Price: {price_formatted}",
    ]

    # Add discount information
    if product.original_price and product.discount_rate:
        original_formatted = f"{product.original_price:,}원"
        savings = product.original_price - product.product_price
        savings_formatted = f"{savings:,}원"

        lines.append(f"Original Price: {original_formatted}")
        lines.append(f"Discount: {product.discount_rate}% (Save {savings_formatted})")

    # Add category
    if product.category_name:
        lines.append(f"Category: {product.category_name}")

    # Add shipping information
    shipping_features = []
    if product.is_rocket:
        shipping_features.append("🚀 Rocket Delivery")
    if product.is_free_shipping:
        shipping_features.append("📦 Free Shipping")

    if shipping_features:
        lines.append("Shipping: " + ", ".join(shipping_features))

    # Add URLs
    lines.append(f"\nImage: {product.product_image}")
    lines.append(f"Affiliate URL: {product.product_url}")

    return "\n".join(lines)


def get_product_summary(product: Product) -> dict:
    """
    Generate a summary dictionary from product details.

    Args:
        product: Product object

    Returns:
        Dictionary with key product information

    Example:
        >>> product = Product(...)
        >>> summary = get_product_summary(product)
        >>> print(summary['name'], summary['price'])
    """
    summary = {
        "product_id": product.product_id,
        "name": product.product_name,
        "price": product.product_price,
        "has_discount": bool(product.discount_rate),
        "is_rocket": product.is_rocket or False,
        "is_free_shipping": product.is_free_shipping or False,
    }

    if product.discount_rate:
        summary["discount_rate"] = product.discount_rate
        summary["original_price"] = product.original_price

    if product.category_name:
        summary["category"] = product.category_name

    return summary


def compare_products(product1: Product, product2: Product) -> dict:
    """
    Compare two products and return comparison results.

    Args:
        product1: First product
        product2: Second product

    Returns:
        Dictionary with comparison information

    Example:
        >>> comparison = compare_products(product1, product2)
        >>> print(f"Cheaper: {comparison['cheaper_product']}")
    """
    comparison = {
        "product1_id": product1.product_id,
        "product2_id": product2.product_id,
        "price_difference": abs(product1.product_price - product2.product_price),
        "cheaper_product": product1.product_id if product1.product_price < product2.product_price else product2.product_id,
    }

    # Compare shipping
    p1_shipping_score = (
        (1 if product1.is_rocket else 0) +
        (1 if product1.is_free_shipping else 0)
    )
    p2_shipping_score = (
        (1 if product2.is_rocket else 0) +
        (1 if product2.is_free_shipping else 0)
    )

    comparison["better_shipping"] = (
        product1.product_id if p1_shipping_score > p2_shipping_score
        else product2.product_id if p2_shipping_score > p1_shipping_score
        else "equal"
    )

    # Compare discounts
    p1_discount = product1.discount_rate or 0
    p2_discount = product2.discount_rate or 0

    comparison["better_discount"] = (
        product1.product_id if p1_discount > p2_discount
        else product2.product_id if p2_discount > p1_discount
        else "equal"
    )

    return comparison


def validate_product_id(product_id: str) -> bool:
    """
    Validate product ID format.

    Args:
        product_id: Product ID to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> is_valid = validate_product_id("1234567890")
        >>> print(is_valid)
        True
    """
    if not product_id:
        return False

    # Product ID should be a non-empty string
    # Add more specific validation if needed based on Coupang's format
    return isinstance(product_id, str) and len(product_id) > 0
