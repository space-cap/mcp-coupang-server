# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for Coupang integration. MCP is a protocol that allows AI models to interact with external tools and data sources through standardized server implementations.

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

## MCP Server Architecture

MCP servers expose tools, resources, and prompts that AI models can use. This server should implement the MCP protocol using the `mcp` package (version >=1.19.0).

### Key Concepts
- **Tools**: Functions that the AI can call to perform actions (e.g., search products, check prices)
- **Resources**: Data sources that can be read (e.g., product catalogs, order history)
- **Prompts**: Pre-defined prompt templates for common tasks

### Typical MCP Server Structure
- Server initialization using `mcp.server.Server()`
- Tool handlers decorated with `@server.list_tools()` and `@server.call_tool()`
- Resource handlers for data access
- Server running via stdio transport for local Claude Desktop integration

## Coupang Integration

This server is intended to integrate with Coupang's APIs. Implementation will require:
- Coupang API credentials (API key/secret)
- API endpoint definitions
- Product search, pricing, and order capabilities
