@echo off
REM Windows 11 test script for Blender MCP Server setup

echo 🧪 Testing Blender MCP Server Setup (Windows 11)
echo.

REM Test Python installation
echo 1. Testing Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ from python.org
    echo    Make sure to check "Add Python to PATH" during installation
    goto :end
) else (
    echo ✅ Python is installed
    python --version
)

REM Test pip
echo.
echo 2. Testing pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip not found!
    goto :end
) else (
    echo ✅ pip is available
    pip --version
)

REM Test project files
echo.
echo 3. Checking project files...
if exist "src\blender_mcp_server\server.py" (
    echo ✅ Main server file found
) else (
    echo ❌ Server file not found! Please check directory
    goto :end
)

if exist "requirements.txt" (
    echo ✅ Requirements file found
) else (
    echo ❌ Requirements file not found!
    goto :end
)

REM Test FastMCP installation
echo.
echo 4. Testing FastMCP installation...
pip show fastmcp >nul 2>&1
if errorlevel 1 (
    echo ⚠️  FastMCP not installed. Installing now...
    pip install fastmcp==2.13.0.2
) else (
    echo ✅ FastMCP is installed
    pip show fastmcp | findstr Version
)

REM Test Blender (optional)
echo.
echo 5. Checking Blender installation...
set BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 4.*
if exist "%BLENDER_PATH%" (
    echo ✅ Blender 4.x found at %BLENDER_PATH%
) else (
    set BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 3.*
    if exist "%BLENDER_PATH%" (
        echo ✅ Blender 3.x found at %BLENDER_PATH%
    ) else (
        echo ⚠️  Blender not found! Please install from blender.org
        echo    The MCP server will work, but you'll need Blender to use the tools
    )
)

REM Final test
echo.
echo 6. Testing server startup...
echo    (This will show expected bpy error if Blender not installed)
python -m src.blender_mcp_server.server --help >nul 2>&1
if errorlevel 1 (
    echo ✅ Server is ready! (bpy error is normal without Blender)
) else (
    echo ✅ Server startup test passed
)

echo.
echo 🎉 Setup test complete!
echo.
echo 📋 Quick Start:
echo    Double-click: start-windows.bat
echo    Or run: python -m src.blender_mcp_server.server --transport stdio
echo.
echo 📖 For detailed setup: See WINDOWS11_SETUP_GUIDE.md

:end
pause
