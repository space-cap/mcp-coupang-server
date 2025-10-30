"""
MCP Server for Coupang integration.

Provides tools for searching products and retrieving product details.
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent

from src.coupang_client import CoupangClient, CoupangAPIError
from src.models.product import SearchParams, DeepLinkRequest
from src.utils.categories import get_category_list_text, is_valid_category

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("coupang-mcp-server")

# Initialize MCP server
app = Server("coupang-mcp-server")

# Global client instance
client: CoupangClient = None


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools.

    Returns:
        List of Tool objects that can be called by the AI.
    """
    return [
        Tool(
            name="search_products",
            description=(
                "Search for products on Coupang by keyword. "
                "Returns a list of products with names, prices, images, and affiliate URLs. "
                "Useful for finding products, comparing prices, or discovering items."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Search query keyword (e.g., 'laptop', 'iPhone 15', 'coffee maker')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (1-100, default: 10)",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 10
                    }
                },
                "required": ["keyword"]
            }
        ),
        # Tool(
        #     name="get_product_details",
        #     description=(
        #         "Get detailed information about a specific Coupang product by ID. "
        #         "Returns product name, price, images, category, shipping info, and affiliate URL. "
        #         "Use this after searching to get more details about a particular product."
        #     ),
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "product_id": {
        #                 "type": "string",
        #                 "description": "Coupang product ID (obtained from search results)"
        #             }
        #         },
        #         "required": ["product_id"]
        #     }
        # ),
        Tool(
            name="get_best_products_by_category",
            description=(
                "Get best-selling products in a specific Coupang category. "
                "Returns a list of top products in the category with names, prices, and affiliate URLs. "
                "Useful for finding popular items in specific categories.\n\n"
                "Available categories:\n"
                "1001-여성패션, 1002-남성패션, 1010-뷰티, 1012-식품, 1013-주방용품, "
                "1014-생활용품, 1015-홈인테리어, 1016-가전디지털, 1017-스포츠/레저, "
                "1018-자동차용품, 1019-도서/음반/DVD, 1020-완구/취미, 1021-문구/오피스, "
                "1024-헬스/건강식품, 1025-국내여행, 1026-해외여행, 1029-반려동물용품, 1030-유아동패션"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "category_id": {
                        "type": "string",
                        "description": "Coupang category ID (e.g., '1016' for 가전디지털)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (1-100, default: 20)",
                        "minimum": 1,
                        "maximum": 100,
                        "default": 20
                    }
                },
                "required": ["category_id"]
            }
        ),
        Tool(
            name="create_deeplinks",
            description=(
                "Convert Coupang product URLs to affiliate tracking deeplinks. "
                "Takes regular Coupang URLs and converts them to shortened tracking URLs with your affiliate code. "
                "Useful for creating trackable links from search results or specific product pages."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "coupang_urls": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of Coupang product URLs to convert (e.g., ['https://www.coupang.com/vp/products/184614775'])"
                    },
                    "sub_id": {
                        "type": "string",
                        "description": "Optional tracking/sub ID for analytics (uses environment default if not provided)"
                    }
                },
                "required": ["coupang_urls"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool calls from the AI.

    Args:
        name: Name of the tool to call
        arguments: Dictionary of arguments for the tool

    Returns:
        List of TextContent responses

    Raises:
        ValueError: If tool name is unknown
    """
    global client

    # Ensure client is initialized
    if client is None:
        client = CoupangClient()

    try:
        if name == "search_products":
            return await handle_search_products(arguments)
        # elif name == "get_product_details":
        #     return await handle_get_product_details(arguments)
        elif name == "get_best_products_by_category":
            return await handle_get_best_products_by_category(arguments)
        elif name == "create_deeplinks":
            return await handle_create_deeplinks(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

    except CoupangAPIError as e:
        logger.error(f"Coupang API error in {name}: {e}")
        return [TextContent(
            type="text",
            text=f"Error: Failed to fetch data from Coupang API. {str(e)}"
        )]
    except Exception as e:
        logger.error(f"Unexpected error in {name}: {e}")
        return [TextContent(
            type="text",
            text=f"Error: An unexpected error occurred. {str(e)}"
        )]


async def handle_search_products(arguments: dict) -> list[TextContent]:
    """
    Handle search_products tool call.

    Args:
        arguments: Dictionary with 'keyword' and optional 'limit'

    Returns:
        List of TextContent with search results
    """
    # Validate and extract arguments
    keyword = arguments.get("keyword")
    limit = arguments.get("limit", 10)

    if not keyword:
        return [TextContent(
            type="text",
            text="Error: 'keyword' parameter is required"
        )]

    # Validate parameters using Pydantic model
    try:
        params = SearchParams(keyword=keyword, limit=limit)
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: Invalid parameters. {str(e)}"
        )]

    logger.info(f"Searching products: keyword='{params.keyword}', limit={params.limit}")

    # Search products
    products = await client.search_products(
        keyword=params.keyword,
        limit=params.limit
    )

    # Format response
    if not products:
        return [TextContent(
            type="text",
            text=f"No products found for keyword: '{params.keyword}'"
        )]

    # Build response text
    response_lines = [
        f"Found {len(products)} product(s) for '{params.keyword}':\n"
    ]

    for i, product in enumerate(products, 1):
        # Format price
        price_formatted = f"{product.product_price:,}원"

        # Add product info
        response_lines.append(f"{i}. {product.product_name}")
        response_lines.append(f"   Price: {price_formatted}")
        response_lines.append(f"   ID: {product.product_id}")

        # Add optional fields
        if product.is_rocket:
            response_lines.append("   🚀 Rocket Delivery")
        if product.is_free_shipping:
            response_lines.append("   📦 Free Shipping")
        if product.discount_rate:
            response_lines.append(f"   💰 Discount: {product.discount_rate}%")

        response_lines.append(f"   URL: {product.product_url}")
        response_lines.append("")  # Empty line between products

    return [TextContent(
        type="text",
        text="\n".join(response_lines)
    )]


async def handle_get_product_details(arguments: dict) -> list[TextContent]:
    """
    Handle get_product_details tool call.

    Args:
        arguments: Dictionary with 'product_id'

    Returns:
        List of TextContent with product details
    """
    # Extract product_id
    product_id = arguments.get("product_id")

    if not product_id:
        return [TextContent(
            type="text",
            text="Error: 'product_id' parameter is required"
        )]

    logger.info(f"Fetching product details: product_id='{product_id}'")

    # Get product details
    product = await client.get_product_details(product_id)

    # Check if product was found
    if not product:
        return [TextContent(
            type="text",
            text=f"Product not found: ID '{product_id}'"
        )]

    # Format response
    price_formatted = f"{product.product_price:,}원"

    response_lines = [
        f"Product Details for ID: {product.product_id}\n",
        f"Name: {product.product_name}",
        f"Price: {price_formatted}",
    ]

    # Add optional fields
    if product.original_price and product.discount_rate:
        original_formatted = f"{product.original_price:,}원"
        response_lines.append(f"Original Price: {original_formatted}")
        response_lines.append(f"Discount: {product.discount_rate}%")

    if product.category_name:
        response_lines.append(f"Category: {product.category_name}")

    # Shipping info
    shipping_info = []
    if product.is_rocket:
        shipping_info.append("🚀 Rocket Delivery")
    if product.is_free_shipping:
        shipping_info.append("📦 Free Shipping")

    if shipping_info:
        response_lines.append("Shipping: " + ", ".join(shipping_info))

    response_lines.append(f"\nImage: {product.product_image}")
    response_lines.append(f"Affiliate URL: {product.product_url}")

    return [TextContent(
        type="text",
        text="\n".join(response_lines)
    )]


async def handle_get_best_products_by_category(arguments: dict) -> list[TextContent]:
    """
    Handle get_best_products_by_category tool call.

    Args:
        arguments: Dictionary with 'category_id' and optional 'limit'

    Returns:
        List of TextContent with category best products
    """
    # Extract arguments
    category_id = arguments.get("category_id")
    limit = arguments.get("limit", 20)

    if not category_id:
        return [TextContent(
            type="text",
            text="Error: 'category_id' parameter is required"
        )]

    logger.info(f"Fetching best products for category: category_id='{category_id}', limit={limit}")

    # Get best products
    products = await client.get_best_products_by_category(
        category_id=category_id,
        limit=limit
    )

    # Format response
    if not products:
        return [TextContent(
            type="text",
            text=f"No products found for category: '{category_id}'"
        )]

    # Build response text
    response_lines = [
        f"Found {len(products)} best product(s) in category '{category_id}':\n"
    ]

    for i, product in enumerate(products, 1):
        # Format price
        price_formatted = f"{product.product_price:,}원"

        # Add product info
        response_lines.append(f"{i}. {product.product_name}")
        response_lines.append(f"   Price: {price_formatted}")
        response_lines.append(f"   ID: {product.product_id}")

        # Add optional fields
        if product.category_name:
            response_lines.append(f"   Category: {product.category_name}")
        if product.is_rocket:
            response_lines.append("   🚀 Rocket Delivery")
        if product.is_free_shipping:
            response_lines.append("   📦 Free Shipping")
        if product.discount_rate:
            response_lines.append(f"   💰 Discount: {product.discount_rate}%")

        response_lines.append(f"   URL: {product.product_url}")
        response_lines.append("")  # Empty line between products

    return [TextContent(
        type="text",
        text="\n".join(response_lines)
    )]


async def handle_create_deeplinks(arguments: dict) -> list[TextContent]:
    """
    Handle create_deeplinks tool call.

    Args:
        arguments: Dictionary with 'coupang_urls' and optional 'sub_id'

    Returns:
        List of TextContent with deeplink results
    """
    # Extract arguments
    coupang_urls = arguments.get("coupang_urls")
    sub_id = arguments.get("sub_id")

    if not coupang_urls:
        return [TextContent(
            type="text",
            text="Error: 'coupang_urls' parameter is required"
        )]

    if not isinstance(coupang_urls, list) or len(coupang_urls) == 0:
        return [TextContent(
            type="text",
            text="Error: 'coupang_urls' must be a non-empty list of URLs"
        )]

    logger.info(f"Creating deeplinks for {len(coupang_urls)} URL(s), sub_id={sub_id or 'default'}")

    # Create deeplinks
    deeplinks = await client.create_deeplinks(
        coupang_urls=coupang_urls,
        sub_id=sub_id
    )

    # Format response
    if not deeplinks:
        return [TextContent(
            type="text",
            text=f"No deeplinks created for provided URLs"
        )]

    # Build response text
    response_lines = [
        f"Created {len(deeplinks)} deeplink(s):\n"
    ]

    for i, link in enumerate(deeplinks, 1):
        response_lines.append(f"{i}. Original: {link.original_url}")
        response_lines.append(f"   Shortened: {link.shorten_url}")
        response_lines.append(f"   Landing: {link.landing_url}")
        response_lines.append("")  # Empty line between links

    if sub_id:
        response_lines.append(f"Tracking ID: {sub_id}")

    return [TextContent(
        type="text",
        text="\n".join(response_lines)
    )]


async def cleanup():
    """Cleanup resources on server shutdown."""
    global client
    if client:
        await client.close()
        logger.info("Coupang client closed")


def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Coupang MCP Server...")
    
    # Run server
    async def run():
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")


if __name__ == "__main__":
    main()
