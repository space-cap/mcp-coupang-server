"""
Authentication utilities for Coupang API.

Implements HMAC-SHA256 signature generation for API requests.
"""

import hmac
import hashlib
from datetime import datetime, timezone
from typing import Optional


class CoupangAuth:
    """Handles authentication for Coupang API requests."""

    ALGORITHM = "HmacSHA256"

    def __init__(self, access_key: str, secret_key: str):
        """
        Initialize authentication handler.

        Args:
            access_key: Coupang API access key
            secret_key: Coupang API secret key
        """
        self.access_key = access_key
        self.secret_key = secret_key

    def generate_signature(
        self,
        method: str,
        path: str,
        query: str = "",
        timestamp: Optional[str] = None
    ) -> str:
        """
        Generate HMAC-SHA256 signature for API request.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            query: URL query string (without leading '?')
            timestamp: ISO 8601 timestamp (generated if not provided)

        Returns:
            Hexadecimal HMAC signature string

        Example:
            >>> auth = CoupangAuth("access_key", "secret_key")
            >>> signature = auth.generate_signature("GET", "/v2/providers/affiliate_open_api/apis/openapi/products/search", "keyword=laptop")
        """
        if timestamp is None:
            timestamp = self._get_timestamp()

        # Construct message to sign
        message = f"{timestamp}{method}{path}"
        if query:
            message += f"{query}"

        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return signature

    def generate_headers(
        self,
        method: str,
        path: str,
        query: str = ""
    ) -> dict:
        """
        Generate authentication headers for API request.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            query: URL query string (without leading '?')

        Returns:
            Dictionary of headers including authorization

        Example:
            >>> auth = CoupangAuth("access_key", "secret_key")
            >>> headers = auth.generate_headers("GET", "/v2/providers/affiliate_open_api/apis/openapi/products/search", "keyword=laptop")
        """
        timestamp = self._get_timestamp()
        signature = self.generate_signature(method, path, query, timestamp)

        return {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"CEA algorithm={self.ALGORITHM}, access-key={self.access_key}, signed-date={timestamp}, signature={signature}"
        }

    @staticmethod
    def _get_timestamp() -> str:
        """
        Get current timestamp in Coupang API format.

        Returns:
            Coupang formatted timestamp string (e.g., "251029T173045Z")
            Format: yymmddTHHMMSSZ
        """
        return datetime.now(timezone.utc).strftime("%y%m%dT%H%M%SZ")
