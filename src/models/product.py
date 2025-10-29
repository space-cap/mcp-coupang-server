"""
Data models for Coupang products.

Defines Pydantic models for product search results and product details.
"""

from typing import Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ProductImage(BaseModel):
    """Product image information."""
    url: str = Field(description="Image URL")


class Product(BaseModel):
    """
    Coupang product model.

    Represents a product from Coupang's affiliate API.
    """
    product_id: Union[str, int] = Field(alias="productId", description="Unique product ID")
    product_name: str = Field(alias="productName", description="Product name")
    product_price: int = Field(alias="productPrice", description="Product price in KRW")
    product_image: str = Field(alias="productImage", description="Main product image URL")
    product_url: str = Field(alias="productUrl", description="Affiliate product URL")

    @field_validator('product_id', mode='before')
    @classmethod
    def convert_product_id_to_str(cls, v):
        """Convert product_id to string if it's an integer."""
        return str(v) if v is not None else v

    # Optional fields
    category_name: Optional[str] = Field(None, alias="categoryName", description="Product category")
    is_rocket: Optional[bool] = Field(None, alias="isRocket", description="Rocket delivery available")
    is_free_shipping: Optional[bool] = Field(None, alias="isFreeShipping", description="Free shipping available")
    discount_rate: Optional[int] = Field(None, alias="discountRate", description="Discount rate percentage")
    original_price: Optional[int] = Field(None, alias="originalPrice", description="Original price before discount")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "productId": "1234567890",
                "productName": "Samsung Galaxy S24",
                "productPrice": 999000,
                "productImage": "https://thumbnail.coupangcdn.com/...",
                "productUrl": "https://link.coupang.com/...",
                "categoryName": "Electronics",
                "isRocket": True,
                "isFreeShipping": True,
                "discountRate": 15,
                "originalPrice": 1175000
            }
        }
    )


class ProductSearchResponse(BaseModel):
    """
    Response from product search API.

    Contains list of products and pagination information.
    """
    data: List[Product] = Field(default_factory=list, description="List of products")
    total_count: Optional[int] = Field(None, alias="totalCount", description="Total number of results")

    model_config = ConfigDict(populate_by_name=True)


class SearchParams(BaseModel):
    """
    Parameters for product search.

    Used to validate and structure search queries.
    """
    keyword: str = Field(description="Search keyword")
    limit: int = Field(default=10, ge=1, le=100, description="Number of results (1-100)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "keyword": "laptop",
                "limit": 20
            }
        }
    )


class DeepLink(BaseModel):
    """
    Deeplink conversion result.

    Represents a single URL conversion with tracking information.
    """
    original_url: str = Field(alias="originalUrl", description="Original Coupang URL")
    shorten_url: str = Field(alias="shortenUrl", description="Shortened tracking URL")
    landing_url: str = Field(alias="landingUrl", description="Full landing URL with tracking parameters")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "originalUrl": "https://www.coupang.com/vp/products/184614775",
                "shortenUrl": "https://coupa.ng/blE0dT",
                "landingUrl": "https://link.coupang.com/re/AFFSDP?lptag=AF1234567&pageKey=319834306&itemId=1023216541&vendorItemId=70064597513&traceid=V0-183-5fddb21eaffbb2ef"
            }
        }
    )


class DeepLinkRequest(BaseModel):
    """
    Request parameters for deeplink creation.

    Used to validate deeplink conversion requests.
    """
    coupang_urls: List[str] = Field(description="List of Coupang URLs to convert")
    sub_id: Optional[str] = Field(None, description="Optional tracking/sub ID")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "coupang_urls": ["https://www.coupang.com/vp/products/184614775"],
                "sub_id": "publicMCP"
            }
        }
    )
