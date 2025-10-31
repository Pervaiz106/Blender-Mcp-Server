#!/bin/sh
# STDIO mode startup script - suitable for local tool integration
set -e

# Change to script directory
cd "$(dirname "$0")"

# Check necessary environment variables
if [ -z "$BLENDER_HOST" ]; then
    echo "Warning: BLENDER_HOST environment variable not set (using default: localhost)" >&2
fi

if [ -z "$BLENDER_PORT" ]; then
    echo "Warning: BLENDER_PORT environment variable not set (using default: 9876)" >&2
fi

# Create independent virtual environment (if it doesn't exist)
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..." >&2
    uv venv
    echo "Installing dependencies..." >&2
    echo "Note: Dependency installation may take several minutes. Please wait..." >&2
    uv sync
fi

# Start STDIO mode MCP server
uv run python src/blender_mcp_server/simple_server.py --transport stdio