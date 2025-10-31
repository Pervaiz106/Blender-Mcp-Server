#!/bin/bash
# Simple startup script for Blender MCP Server (no UV required)

echo "🚀 Starting Blender MCP Server..."

# Check if we're in the right directory
if [ ! -f "src/blender_mcp_server/server.py" ]; then
    echo "❌ Error: Please run this from the blender-mcp-comprehensive directory"
    exit 1
fi

# Set environment variables (defaults)
export BLENDER_HOST="${BLENDER_HOST:-localhost}"
export BLENDER_PORT="${BLENDER_PORT:-9876}"

echo "📡 Connection settings:"
echo "   Host: $BLENDER_HOST"
echo "   Port: $BLENDER_PORT"
echo ""

# Start the server
echo "🔧 Starting MCP Server..."
python3 -m src.blender_mcp_server.server --transport stdio