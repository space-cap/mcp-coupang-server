"""
Tests for data models.

Tests Pydantic models for products and search parameters.
"""

import pytest
from pydantic import ValidationError

from src.models.product import Product, ProductSearchResponse, SearchParams


class TestProduct:
    """Test cases for Product model."""

    def test_product_creation_with_required_fields(self):
        """Test creating a product with only required fields."""
        product = Product(
            productId="123456",
            productName="Test Product",
            productPrice=50000,
            productImage="https://example.com/image.jpg",
            productUrl="https://example.com/product"
        )

        assert product.product_id == "123456"
        assert product.product_name == "Test Product"
        assert product.product_price == 50000
        assert product.product_image == "https://example.com/image.jpg"
        assert product.product_url == "https://example.com/product"

    def test_product_creation_with_all_fields(self):
        """Test creating a product with all optional fields."""
        product = Product(
            productId="123456",
            productName="Test Product",
            productPrice=50000,
            productImage="https://example.com/image.jpg",
            productUrl="https://example.com/product",
            categoryName="Electronics",
            isRocket=True,
            isFreeShipping=True,
            discountRate=15,
            originalPrice=60000
        )

        assert product.category_name == "Electronics"
        assert product.is_rocket is True
        assert product.is_free_shipping is True
        assert product.discount_rate == 15
        assert product.original_price == 60000

    def test_product_field_aliases(self):
        """Test that field aliases work correctly."""
        # Using camelCase (API format)
        product = Product(
            productId="123",
            productName="Test",
            productPrice=10000,
            productImage="https://example.com/img.jpg",
            productUrl="https://example.com/url"
        )

        # Should be accessible via snake_case
        assert product.product_id == "123"
        assert product.product_name == "Test"

    def test_product_missing_required_field(self):
        """Test that validation fails when required fields are missing."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                productName="Test",
                productPrice=10000
                # Missing productId, productImage, productUrl
            )

        errors = exc_info.value.errors()
        assert len(errors) >= 3  # At least 3 missing fields

    def test_product_optional_fields_default_to_none(self):
        """Test that optional fields default to None."""
        product = Product(
            productId="123",
            productName="Test",
            productPrice=10000,
            productImage="https://example.com/img.jpg",
            productUrl="https://example.com/url"
        )

        assert product.category_name is None
        assert product.is_rocket is None
        assert product.is_free_shipping is None
        assert product.discount_rate is None
        assert product.original_price is None


class TestProductSearchResponse:
    """Test cases for ProductSearchResponse model."""

    def test_search_response_with_products(self):
        """Test creating search response with product list."""
        products = [
            Product(
                productId="1",
                productName="Product 1",
                productPrice=10000,
                productImage="https://example.com/1.jpg",
                productUrl="https://example.com/1"
            ),
            Product(
                productId="2",
                productName="Product 2",
                productPrice=20000,
                productImage="https://example.com/2.jpg",
                productUrl="https://example.com/2"
            )
        ]

        response = ProductSearchResponse(
            data=products,
            totalCount=2
        )

        assert len(response.data) == 2
        assert response.total_count == 2
        assert response.data[0].product_id == "1"
        assert response.data[1].product_id == "2"

    def test_search_response_empty_list(self):
        """Test creating search response with empty product list."""
        response = ProductSearchResponse(data=[], totalCount=0)

        assert response.data == []
        assert response.total_count == 0

    def test_search_response_defaults(self):
        """Test search response with default values."""
        response = ProductSearchResponse()

        assert response.data == []
        assert response.total_count is None


class TestSearchParams:
    """Test cases for SearchParams model."""

    def test_search_params_with_defaults(self):
        """Test creating search params with default limit."""
        params = SearchParams(keyword="laptop")

        assert params.keyword == "laptop"
        assert params.limit == 10  # Default value

    def test_search_params_with_custom_limit(self):
        """Test creating search params with custom limit."""
        params = SearchParams(keyword="laptop", limit=50)

        assert params.keyword == "laptop"
        assert params.limit == 50

    def test_search_params_limit_validation_min(self):
        """Test that limit validation fails for values below 1."""
        with pytest.raises(ValidationError) as exc_info:
            SearchParams(keyword="laptop", limit=0)

        errors = exc_info.value.errors()
        assert any("greater_than_equal" in str(error) for error in errors)

    def test_search_params_limit_validation_max(self):
        """Test that limit validation fails for values above 100."""
        with pytest.raises(ValidationError) as exc_info:
            SearchParams(keyword="laptop", limit=101)

        errors = exc_info.value.errors()
        assert any("less_than_equal" in str(error) for error in errors)

    def test_search_params_missing_keyword(self):
        """Test that validation fails when keyword is missing."""
        with pytest.raises(ValidationError) as exc_info:
            SearchParams(limit=10)

        errors = exc_info.value.errors()
        assert any("keyword" in str(error) for error in errors)

    def test_search_params_empty_keyword(self):
        """Test behavior with empty keyword string."""
        # Empty string should be allowed (API will handle it)
        params = SearchParams(keyword="", limit=10)
        assert params.keyword == ""

    def test_search_params_valid_limits(self):
        """Test that valid limit values work correctly."""
        # Test boundary values
        params1 = SearchParams(keyword="test", limit=1)
        assert params1.limit == 1

        params2 = SearchParams(keyword="test", limit=100)
        assert params2.limit == 100

        params3 = SearchParams(keyword="test", limit=50)
        assert params3.limit == 50

    def test_search_params_keyword_with_special_chars(self):
        """Test that keywords with special characters are accepted."""
        params = SearchParams(keyword="laptop + bag", limit=10)
        assert params.keyword == "laptop + bag"

        params2 = SearchParams(keyword="iPhone 15 Pro", limit=10)
        assert params2.keyword == "iPhone 15 Pro"
