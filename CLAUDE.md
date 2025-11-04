# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for Coupang Partners API integration. The project is **PRODUCTION READY** and published on PyPI as `mcp-coupang-server`.

MCP is a protocol that allows AI models to interact with external tools and data sources through standardized server implementations. This server enables Claude Desktop to search products, get category best sellers, and create affiliate deeplinks using Coupang Partners API.

## Project Status

- ✅ **Version**: 1.0.0
- ✅ **Published on PyPI**: `pip install mcp-coupang-server`
- ✅ **All Tests Passing**: 54 tests (unit + integration)
- ✅ **Active Tools**: 3 tools (search_products, get_best_products_by_category, create_deeplinks)
- ✅ **Disabled Tools**: get_product_details (commented out, not in use)

## Development Setup

This project uses `uv` for Python package management (Python 3.13+).

### Install Dependencies
```bash
uv sync
```

### Run the Server
```bash
uv run python main.py
```

### Run Tests
```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/test_client.py

# With coverage
uv run pytest --cov=src --cov-report=html
```

## MCP Server Architecture

MCP servers expose tools, resources, and prompts that AI models can use. This server implements the MCP protocol using the `mcp` package (version >=1.19.0).

### Key Concepts
- **Tools**: Functions that the AI can call to perform actions (e.g., search products, get best products by category, create deeplinks)
- **Resources**: Data sources that can be read (currently not implemented)
- **Prompts**: Pre-defined prompt templates for common tasks (currently not implemented)

### Server Structure
- Server initialization using `mcp.server.Server()` in `src/server.py`
- Tool handlers with `@server.list_tools()` and `@server.call_tool()` decorators
- Server running via stdio transport for Claude Desktop integration
- Asynchronous HTTP client using `aiohttp` in `src/coupang_client.py`

### Active Tools (3)

1. **search_products**: Search Coupang products by keyword
   - Parameters: keyword (required), limit (optional, 1-100, default 10)
   - Handler: `handle_search_products()` in `src/tools/search.py`

2. **get_best_products_by_category**: Get best-selling products by category
   - Parameters: category_id (required, 18 categories supported), limit (optional, 1-100, default 20)
   - Handler: `handle_get_best_products_by_category()` in `src/tools/search.py`
   - Categories defined in `src/utils/categories.py`

3. **create_deeplinks**: Convert Coupang URLs to affiliate tracking URLs
   - Parameters: coupang_urls (required, array), sub_id (optional)
   - Handler: `handle_create_deeplinks()` in `src/tools/details.py`

### Disabled Tools

- **get_product_details**: Currently commented out in `src/server.py` (lines 63-80, 161-162)
  - Reason: Not currently needed per user request
  - Can be re-enabled by uncommenting the tool definition and handler call

## Coupang Integration

### API Authentication
- Uses HMAC-SHA256 authentication with custom timestamp format
- Authorization header: `HMAC-SHA256 accesskey=ACCESS_KEY&expires=TIMESTAMP&signature=SIGNATURE`
- Timestamp format: `yyMMddHHmm` (e.g., 2501041530 for 2025-01-04 15:30)
- Implementation: `src/utils/auth.py`

### API Endpoints
- Base URL: `https://api-gateway.coupang.com`
- Product Search: `/v2/providers/affiliate_open_api/apis/openapi/v1/products/search`
- Category Best: `/v2/providers/affiliate_open_api/apis/openapi/v1/products/bestcategories/{categoryId}`
- Deeplink: `/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink`

### Required Environment Variables
```env
COUPANG_ACCESS_KEY=your_access_key_here
COUPANG_SECRET_KEY=your_secret_key_here
COUPANG_PARTNER_ID=your_partner_id_here
COUPANG_SUB_ID=your_sub_id_here  # Optional: Default tracking ID
```

### Configuration Management
- Environment variables loaded via `python-dotenv`
- Config class: `src/utils/config.py`
- Validates all required credentials on startup

## Project Structure

```
mcp-coupang-server/
├── src/
│   ├── server.py              # MCP server main logic
│   ├── coupang_client.py      # Coupang API client (aiohttp)
│   ├── models/
│   │   └── product.py         # Pydantic data models
│   ├── tools/
│   │   ├── search.py          # Search & category tools
│   │   └── details.py         # Deeplink tool
│   └── utils/
│       ├── config.py          # Environment variables
│       ├── auth.py            # HMAC authentication
│       └── categories.py      # Category definitions (18 categories)
├── playground/                # Test scripts (7 examples)
├── tests/                     # pytest tests (54 tests)
├── docs/                      # Documentation
│   ├── installation-guide.md      # Git clone installation
│   ├── pypi-installation-guide.md # PyPI installation (recommended)
│   └── deployment-guide.md        # Deployment methods
├── main.py                    # Entry point
└── pyproject.toml             # Project metadata & dependencies
```

## Testing

### Test Coverage
- **Unit Tests**: `tests/test_client.py` - API client methods
- **Integration Tests**: `tests/test_integration.py` - End-to-end workflows
- **Playground Scripts**: `playground/*.py` - Manual testing and examples

### Running Playground Scripts
```bash
# Search test
uv run python playground/1_simple_search.py

# Category best products test
uv run python playground/6_category_best.py

# Deeplink creation test
uv run python playground/7_create_deeplinks.py
```

## Deployment

The package is published on PyPI and can be installed with:
```bash
pip install mcp-coupang-server
```

### Entry Point
- Command: `coupang-mcp-server`
- Defined in `pyproject.toml`: `coupang-mcp-server = "src.server:main"`

### Claude Desktop Configuration

**PyPI Installation (Recommended):**
```json
{
  "mcpServers": {
    "coupang": {
      "command": "coupang-mcp-server",
      "env": {
        "COUPANG_ACCESS_KEY": "...",
        "COUPANG_SECRET_KEY": "...",
        "COUPANG_PARTNER_ID": "...",
        "COUPANG_SUB_ID": "..."
      }
    }
  }
}
```

**Git Clone Installation:**
```json
{
  "mcpServers": {
    "coupang": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-coupang-server", "run", "python", "main.py"]
    }
  }
}
```

## Documentation

- **README.md**: Project overview and quick start
- **docs/installation-guide.md**: Detailed Git clone installation guide
- **docs/pypi-installation-guide.md**: PyPI package installation guide (recommended for users)
- **docs/deployment-guide.md**: Distribution methods (GitHub, PyPI, Docker, MCP Registry)

## Code Style

- **Type Hints**: All functions use type annotations
- **Async/Await**: All API calls use async/await with aiohttp
- **Data Validation**: Pydantic V2 models for request/response validation
- **Error Handling**: Comprehensive try/except blocks with informative messages
- **Comments**: Korean comments for better understanding (Korean developer-friendly)

## Important Notes

1. **Korean Language**: This project is designed for Korean developers
   - Documentation primarily in Korean
   - Comments in Korean
   - Error messages can be in Korean for better UX

2. **Disabled Features**:
   - `get_product_details` tool is currently disabled (commented out)
   - Can be re-enabled if needed in the future

3. **Version Management**:
   - Current version: 1.0.0
   - Follow Semantic Versioning (SemVer)
   - Update version in `pyproject.toml` before publishing to PyPI

4. **Publishing to PyPI**:
   ```bash
   # Build
   uv run python -m build

   # Upload
   uv run twine upload dist/*
   ```

## License

MIT License - Copyright (c) 2025 space-cap
