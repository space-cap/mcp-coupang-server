"""
Coupang API client implementation.

Provides async methods for interacting with Coupang's affiliate API.
"""

import aiohttp
from typing import List, Optional
from urllib.parse import urlencode

from src.utils.config import config
from src.utils.auth import CoupangAuth
from src.models.product import Product, ProductSearchResponse, DeepLink


class CoupangAPIError(Exception):
    """Base exception for Coupang API errors."""
    pass


class CoupangClient:
    """
    Async client for Coupang Affiliate API.

    Handles product search and detail retrieval with proper authentication.
    """

    def __init__(
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        partner_id: Optional[str] = None
    ):
        """
        Initialize Coupang API client.

        Args:
            access_key: Coupang API access key (uses config if not provided)
            secret_key: Coupang API secret key (uses config if not provided)
            partner_id: Coupang partner ID (uses config if not provided)
        """
        self.access_key = access_key or config.access_key
        self.secret_key = secret_key or config.secret_key
        self.partner_id = partner_id or config.partner_id
        self.base_url = config.api_base_url

        if not all([self.access_key, self.secret_key, self.partner_id]):
            raise ValueError("Missing required Coupang API credentials")

        self.auth = CoupangAuth(self.access_key, self.secret_key)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def _ensure_session(self):
        """Ensure aiohttp session exists."""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """Close the HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json_body: Optional[dict] = None
    ) -> dict:
        """
        Make authenticated request to Coupang API.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            params: Query parameters
            json_body: JSON request body for POST requests

        Returns:
            JSON response as dictionary

        Raises:
            CoupangAPIError: If request fails
        """
        await self._ensure_session()

        # Build query string
        query = urlencode(params) if params else ""

        # Generate authentication headers
        headers = self.auth.generate_headers(method, path, query)

        # Add Content-Type header for JSON requests
        if json_body is not None:
            headers["Content-Type"] = "application/json;charset=UTF-8"

        # Build full URL
        url = f"{self.base_url}{path}"
        if query:
            url += f"?{query}"

        # Make request
        try:
            async with self.session.request(
                method, url, headers=headers, json=json_body
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise CoupangAPIError(
                        f"API request failed with status {response.status}: {error_text}"
                    )

                return await response.json()

        except aiohttp.ClientError as e:
            raise CoupangAPIError(f"HTTP request failed: {str(e)}")

    async def search_products(
        self,
        keyword: str,
        limit: int = 10
    ) -> List[Product]:
        """
        Search for products by keyword.
        검색 키워드에 대한 쿠팡 검색 결과와 상세 상품 정보를 생성합니다 (1 분당 최대 50번 호출 가능합니다.)

        Args:
            keyword: Search query keyword
            limit: Maximum number of results (1-100, default: 10)

        Returns:
            List of Product objects

        Raises:
            CoupangAPIError: If search fails

        Example:
            >>> async with CoupangClient() as client:
            ...     products = await client.search_products("laptop", limit=20)
            ...     for product in products:
            ...         print(f"{product.product_name}: {product.product_price}원")
        """
        # Validate limit
        if not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100")

        # API endpoint for product search
        path = "/v2/providers/affiliate_open_api/apis/openapi/products/search"

        # Query parameters
        params = {
            "keyword": keyword,
            "limit": limit
        }

        # Make request
        response_data = await self._make_request("GET", path, params)

        # Parse response
        try:
            # Extract product list from response
            # Coupang API response structure: {"rCode": "0", "data": {"productData": [...]}}
            if "data" in response_data and "productData" in response_data["data"]:
                products_data = response_data["data"]["productData"]
            elif "data" in response_data:
                # Fallback for different response structure
                products_data = response_data["data"]
            else:
                products_data = []

            # Convert to Product objects
            products = []
            for item in products_data:
                try:
                    product = Product(**item)
                    products.append(product)
                except Exception as e:
                    # Skip invalid products but log the error
                    print(f"Warning: Failed to parse product: {e}")
                    continue

            return products

        except Exception as e:
            raise CoupangAPIError(f"Failed to parse search response: {str(e)}")

    async def get_product_details(self, product_id: str) -> Optional[Product]:
        """
        Get detailed information for a specific product.

        Args:
            product_id: Coupang product ID

        Returns:
            Product object or None if not found

        Raises:
            CoupangAPIError: If request fails

        Example:
            >>> async with CoupangClient() as client:
            ...     product = await client.get_product_details("1234567890")
            ...     if product:
            ...         print(f"{product.product_name}: {product.product_price}원")
        """
        # API endpoint for product details
        path = f"/v2/providers/affiliate_open_api/apis/openapi/products/{product_id}"

        try:
            response_data = await self._make_request("GET", path)

            # Parse response
            if "data" in response_data:
                product_data = response_data["data"]
            else:
                product_data = response_data

            return Product(**product_data)

        except CoupangAPIError as e:
            if "404" in str(e):
                return None
            raise

    async def get_best_products_by_category(
        self,
        category_id: str,
        limit: int = 20
    ) -> List[Product]:
        """
        Get best products by category.
        카테고리 별 베스트 상품에 대한 상세 상품 정보를 생성합니다.

        Args:
            category_id: Coupang category ID (예: "1001")
            limit: Maximum number of results (1-100, default: 20)

        Returns:
            List of Product objects

        Raises:
            CoupangAPIError: If request fails

        Example:
            >>> async with CoupangClient() as client:
            ...     products = await client.get_best_products_by_category("1001", limit=50)
            ...     for product in products:
            ...         print(f"{product.product_name}: {product.product_price}원")
        """
        # Validate limit
        if not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100")

        # API endpoint for category best products
        path = f"/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/{category_id}"

        # Query parameters
        params = {
            "limit": limit
        }

        # Make request
        response_data = await self._make_request("GET", path, params)

        # Parse response
        try:
            # Extract product list from response
            # Response structure: {"rCode": "0", "rMessage": "", "data": [...]}
            if "data" in response_data:
                products_data = response_data["data"]
            else:
                products_data = []

            # Convert to Product objects
            products = []
            for item in products_data:
                try:
                    product = Product(**item)
                    products.append(product)
                except Exception as e:
                    # Skip invalid products but log the error
                    print(f"Warning: Failed to parse product: {e}")
                    continue

            return products

        except Exception as e:
            raise CoupangAPIError(f"Failed to parse category best products response: {str(e)}")

    async def create_deeplinks(
        self,
        coupang_urls: List[str],
        sub_id: Optional[str] = None
    ) -> List[DeepLink]:
        """
        Convert Coupang URLs to tracking deeplinks.
        쿠팡 URL을 회원 트래킹 코드가 포함된 단축 URL로 변환합니다.

        Args:
            coupang_urls: List of Coupang product URLs to convert
            sub_id: Optional tracking/sub ID (uses config default if not provided)

        Returns:
            List of DeepLink objects with shortened and landing URLs

        Raises:
            CoupangAPIError: If deeplink creation fails

        Example:
            >>> async with CoupangClient() as client:
            ...     urls = ["https://www.coupang.com/vp/products/184614775"]
            ...     deeplinks = await client.create_deeplinks(urls, sub_id="mytracker")
            ...     for link in deeplinks:
            ...         print(f"Short: {link.shorten_url}")
        """
        # Use provided sub_id or fall back to config
        effective_sub_id = sub_id or config.sub_id

        # API endpoint for deeplink creation
        path = "/v2/providers/affiliate_open_api/apis/openapi/deeplink"

        # Request body
        request_body = {
            "coupangUrls": coupang_urls
        }

        # Add subId if provided
        if effective_sub_id:
            request_body["subId"] = effective_sub_id

        # Make request
        response_data = await self._make_request("POST", path, json_body=request_body)

        # Parse response
        try:
            # Extract deeplink list from response
            # Response structure: {"rCode": "0", "rMessage": "", "data": [...]}
            if "data" in response_data:
                deeplinks_data = response_data["data"]
            else:
                deeplinks_data = []

            # Convert to DeepLink objects
            deeplinks = []
            for item in deeplinks_data:
                try:
                    deeplink = DeepLink(**item)
                    deeplinks.append(deeplink)
                except Exception as e:
                    # Skip invalid deeplinks but log the error
                    print(f"Warning: Failed to parse deeplink: {e}")
                    continue

            return deeplinks

        except Exception as e:
            raise CoupangAPIError(f"Failed to parse deeplink response: {str(e)}")

    def __repr__(self) -> str:
        """String representation."""
        return f"CoupangClient(partner_id={self.partner_id})"
