# PowerShell startup script for Blender MCP Server on Windows 11

Write-Host "🚀 Starting Blender MCP Server (Windows 11 - PowerShell)..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "src\blender_mcp_server\server.py")) {
    Write-Host "❌ Error: Please run this from the blender-mcp-comprehensive directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Set default environment variables
$env:BLENDER_HOST = if ($env:BLENDER_HOST) { $env:BLENDER_HOST } else { "localhost" }
$env:BLENDER_PORT = if ($env:BLENDER_PORT) { $env:BLENDER_PORT } else { "9876" }

Write-Host "📡 Connection settings:" -ForegroundColor Yellow
Write-Host "   Host: $($env:BLENDER_HOST)" -ForegroundColor Cyan
Write-Host "   Port: $($env:BLENDER_PORT)" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔧 Starting MCP Server..." -ForegroundColor Yellow
Write-Host ""

# Start the server
try {
    python -m src.blender_mcp_server.server --transport stdio
} catch {
    Write-Host ""
    Write-Host "❌ Server stopped with error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
}
