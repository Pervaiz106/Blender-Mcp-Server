@echo off
REM Windows 11 startup script for Blender MCP Server

echo 🚀 Starting Blender MCP Server (Windows 11)...

REM Check if we're in the right directory
if not exist "src\blender_mcp_server\server.py" (
    echo ❌ Error: Please run this from the blender-mcp-comprehensive directory
    pause
    exit /b 1
)

REM Set default environment variables
if "%BLENDER_HOST%"=="" set BLENDER_HOST=localhost
if "%BLENDER_PORT%"=="" set BLENDER_PORT=9876

echo 📡 Connection settings:
echo    Host: %BLENDER_HOST%
echo    Port: %BLENDER_PORT%
echo.

echo 🔧 Starting MCP Server...
echo.

REM Start the server using python
python -m src.blender_mcp_server.server --transport stdio

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Server stopped. Press any key to close...
    pause >nul
)
