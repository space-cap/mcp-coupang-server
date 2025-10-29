"""
Tests for Coupang API client.

Tests API client functionality with mocked HTTP responses.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiohttp import ClientError

from src.coupang_client import CoupangClient, CoupangAPIError
from src.models.product import Product


class TestCoupangClient:
    """Test cases for CoupangClient class."""

    @pytest.fixture
    def client(self):
        """Create CoupangClient instance for testing."""
        return CoupangClient(
            access_key="test_access_key",
            secret_key="test_secret_key",
            partner_id="test_partner_id"
        )

    def test_client_initialization(self, client):
        """Test that CoupangClient initializes correctly."""
        assert client.access_key == "test_access_key"
        assert client.secret_key == "test_secret_key"
        assert client.partner_id == "test_partner_id"
        assert client.base_url == "https://api-gateway.coupang.com"
        assert client.auth is not None

    def test_client_initialization_with_defaults(self):
        """Test that CoupangClient uses config defaults."""
        # This assumes .env has valid credentials
        client = CoupangClient()

        assert client.access_key is not None
        assert client.secret_key is not None
        assert client.partner_id is not None

    def test_client_initialization_missing_credentials(self):
        """Test that CoupangClient fails without credentials."""
        # Mock config to prevent loading from .env
        with patch('src.coupang_client.config') as mock_config:
            mock_config.access_key = None
            mock_config.secret_key = None
            mock_config.partner_id = None

            with pytest.raises(ValueError) as exc_info:
                CoupangClient(
                    access_key=None,
                    secret_key=None,
                    partner_id=None
                )

            assert "Missing required Coupang API credentials" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test that CoupangClient works as async context manager."""
        client = CoupangClient(
            access_key="test_key",
            secret_key="test_secret",
            partner_id="test_partner"
        )

        async with client:
            assert client.session is not None

        # Session should be closed after exiting context
        # Note: We can't easily test if session is closed, but it should be

    @pytest.mark.asyncio
    async def test_close_method(self):
        """Test that close method works correctly."""
        client = CoupangClient(
            access_key="test_key",
            secret_key="test_secret",
            partner_id="test_partner"
        )

        await client._ensure_session()
        assert client.session is not None

        await client.close()
        assert client.session is None

    @pytest.mark.asyncio
    async def test_make_request_success(self, client):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"data": "test"})

        with patch.object(client, 'session') as mock_session:
            mock_session.request = MagicMock(return_value=mock_response)
            mock_session.request.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.request.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await client._make_request("GET", "/v2/test", {"param": "value"})

            assert result == {"data": "test"}

    @pytest.mark.asyncio
    async def test_make_request_api_error(self, client):
        """Test API request with error response."""
        mock_response = MagicMock()
        mock_response.status = 400
        mock_response.text = AsyncMock(return_value="Bad Request")

        with patch.object(client, 'session') as mock_session:
            mock_session.request = MagicMock(return_value=mock_response)
            mock_session.request.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.request.return_value.__aexit__ = AsyncMock(return_value=None)

            with pytest.raises(CoupangAPIError) as exc_info:
                await client._make_request("GET", "/v2/test")

            assert "400" in str(exc_info.value)
            assert "Bad Request" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_make_request_network_error(self, client):
        """Test API request with network error."""
        with patch.object(client, 'session') as mock_session:
            mock_session.request = MagicMock(side_effect=ClientError("Network error"))

            with pytest.raises(CoupangAPIError) as exc_info:
                await client._make_request("GET", "/v2/test")

            assert "HTTP request failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_search_products_success(self, client):
        """Test successful product search."""
        mock_products = [
            {
                "productId": "1",
                "productName": "Product 1",
                "productPrice": 10000,
                "productImage": "https://example.com/1.jpg",
                "productUrl": "https://example.com/1"
            },
            {
                "productId": "2",
                "productName": "Product 2",
                "productPrice": 20000,
                "productImage": "https://example.com/2.jpg",
                "productUrl": "https://example.com/2"
            }
        ]

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"data": mock_products}

            products = await client.search_products("laptop", limit=10)

            assert len(products) == 2
            assert products[0].product_id == "1"
            assert products[1].product_name == "Product 2"
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_products_empty_results(self, client):
        """Test product search with no results."""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"data": []}

            products = await client.search_products("nonexistent", limit=10)

            assert products == []

    @pytest.mark.asyncio
    async def test_search_products_limit_validation(self, client):
        """Test that search_products validates limit parameter."""
        with pytest.raises(ValueError) as exc_info:
            await client.search_products("laptop", limit=0)

        assert "between 1 and 100" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            await client.search_products("laptop", limit=101)

        assert "between 1 and 100" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_search_products_invalid_response(self, client):
        """Test search_products with invalid API response."""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            # Return invalid data that can't be parsed as Product
            mock_request.return_value = {"data": [{"invalid": "data"}]}

            # Should skip invalid products but not raise error
            products = await client.search_products("laptop", limit=10)

            assert products == []

    @pytest.mark.asyncio
    async def test_get_product_details_success(self, client):
        """Test successful product details retrieval."""
        mock_product = {
            "productId": "123",
            "productName": "Test Product",
            "productPrice": 50000,
            "productImage": "https://example.com/img.jpg",
            "productUrl": "https://example.com/url"
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"data": mock_product}

            product = await client.get_product_details("123")

            assert product is not None
            assert product.product_id == "123"
            assert product.product_name == "Test Product"

    @pytest.mark.asyncio
    async def test_get_product_details_not_found(self, client):
        """Test product details retrieval for non-existent product."""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = CoupangAPIError("API request failed with status 404")

            product = await client.get_product_details("nonexistent")

            assert product is None

    @pytest.mark.asyncio
    async def test_get_product_details_api_error(self, client):
        """Test product details retrieval with API error."""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = CoupangAPIError("API request failed with status 500")

            with pytest.raises(CoupangAPIError):
                await client.get_product_details("123")

    def test_client_repr(self, client):
        """Test string representation of client."""
        repr_str = repr(client)

        assert "CoupangClient" in repr_str
        assert "test_partner_id" in repr_str
