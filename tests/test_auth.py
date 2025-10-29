"""
Tests for authentication module.

Tests HMAC signature generation and header creation.
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch

from src.utils.auth import CoupangAuth


class TestCoupangAuth:
    """Test cases for CoupangAuth class."""

    @pytest.fixture
    def auth(self):
        """Create CoupangAuth instance for testing."""
        return CoupangAuth(
            access_key="test_access_key",
            secret_key="test_secret_key"
        )

    def test_auth_initialization(self, auth):
        """Test that CoupangAuth initializes correctly."""
        assert auth.access_key == "test_access_key"
        assert auth.secret_key == "test_secret_key"
        assert auth.ALGORITHM == "HmacSHA256"

    def test_generate_signature_basic(self, auth):
        """Test signature generation with basic parameters."""
        signature = auth.generate_signature(
            method="GET",
            path="/v2/providers/affiliate_open_api/apis/openapi/products/search",
            query="keyword=laptop",
            timestamp="241015T120000Z"
        )

        # Signature should be a hex string
        assert isinstance(signature, str)
        assert len(signature) == 64  # SHA256 produces 64 hex characters
        # Should only contain hex characters
        assert all(c in "0123456789abcdef" for c in signature)

    def test_generate_signature_consistency(self, auth):
        """Test that same input produces same signature."""
        timestamp = "241015T120000Z"

        sig1 = auth.generate_signature(
            method="GET",
            path="/v2/test",
            query="param=value",
            timestamp=timestamp
        )

        sig2 = auth.generate_signature(
            method="GET",
            path="/v2/test",
            query="param=value",
            timestamp=timestamp
        )

        assert sig1 == sig2

    def test_generate_signature_different_inputs(self, auth):
        """Test that different inputs produce different signatures."""
        timestamp = "241015T120000Z"

        sig1 = auth.generate_signature(
            method="GET",
            path="/v2/test1",
            timestamp=timestamp
        )

        sig2 = auth.generate_signature(
            method="GET",
            path="/v2/test2",
            timestamp=timestamp
        )

        assert sig1 != sig2

    def test_generate_signature_without_query(self, auth):
        """Test signature generation without query parameters."""
        signature = auth.generate_signature(
            method="GET",
            path="/v2/test",
            timestamp="241015T120000Z"
        )

        assert isinstance(signature, str)
        assert len(signature) == 64

    def test_generate_signature_auto_timestamp(self, auth):
        """Test that signature generation creates timestamp if not provided."""
        signature = auth.generate_signature(
            method="GET",
            path="/v2/test"
        )

        # Should successfully generate signature with auto timestamp
        assert isinstance(signature, str)
        assert len(signature) == 64

    def test_generate_headers(self, auth):
        """Test authentication header generation."""
        headers = auth.generate_headers(
            method="GET",
            path="/v2/test",
            query="param=value"
        )

        # Check required headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json;charset=UTF-8"

        assert "Authorization" in headers
        auth_header = headers["Authorization"]

        # Check authorization header format
        assert auth_header.startswith("CEA algorithm=")
        assert "HmacSHA256" in auth_header
        assert "access-key=test_access_key" in auth_header
        assert "signed-date=" in auth_header
        assert "signature=" in auth_header

    def test_generate_headers_without_query(self, auth):
        """Test header generation without query parameters."""
        headers = auth.generate_headers(
            method="POST",
            path="/v2/test"
        )

        assert "Authorization" in headers
        assert "Content-Type" in headers

    def test_timestamp_format(self):
        """Test that _get_timestamp returns correct Coupang API format."""
        timestamp = CoupangAuth._get_timestamp()

        # Should match format: 251029T173045Z (yymmddTHHMMSSZ)
        assert len(timestamp) == 14
        assert timestamp.endswith("Z")
        assert "T" in timestamp
        assert timestamp[6] == "T"

        # Should be valid datetime
        try:
            dt = datetime.strptime(timestamp, "%y%m%dT%H%M%SZ")
            assert dt is not None
        except ValueError:
            pytest.fail("Timestamp format is invalid")

    def test_signature_with_different_methods(self, auth):
        """Test that different HTTP methods produce different signatures."""
        timestamp = "241015T120000Z"
        path = "/v2/test"

        sig_get = auth.generate_signature("GET", path, timestamp=timestamp)
        sig_post = auth.generate_signature("POST", path, timestamp=timestamp)

        assert sig_get != sig_post

    def test_signature_with_special_characters_in_query(self, auth):
        """Test signature generation with special characters in query string."""
        signature = auth.generate_signature(
            method="GET",
            path="/v2/search",
            query="keyword=laptop+bag&price=100%2C000",
            timestamp="241015T120000Z"
        )

        # Should handle special characters without error
        assert isinstance(signature, str)
        assert len(signature) == 64

    def test_empty_secret_key(self):
        """Test behavior with empty secret key."""
        auth = CoupangAuth(
            access_key="test_key",
            secret_key=""
        )

        # Should still generate signature (even if not valid for API)
        signature = auth.generate_signature(
            method="GET",
            path="/v2/test",
            timestamp="241015T120000Z"
        )

        assert isinstance(signature, str)
