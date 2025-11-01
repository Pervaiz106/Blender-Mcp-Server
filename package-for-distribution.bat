@echo off
echo 📦 Creating distribution package for Blender MCP Server...
echo.

REM Create dist folder
if not exist "dist" mkdir dist

REM Create zip file name with date
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
set ZIPNAME=blender-mcp-windows11-%mydate%.zip

echo Creating: %ZIPNAME%
echo.

REM Check if 7-Zip or WinRAR is available
where 7z >nul 2>&1
if %errorlevel% equ 0 (
    echo Using 7-Zip...
    7z a -tzip "dist\%ZIPNAME%" ^
        src\ ^
        blender_addon\ ^
        *.bat ^
        *.ps1 ^
        *.md ^
        requirements.txt ^
        LICENSE ^
        -xr!__pycache__ ^
        -xr!.venv ^
        -xr!*.pyc ^
        -xr!.git
    goto :success
)

where winrar >nul 2>&1
if %errorlevel% equ 0 (
    echo Using WinRAR...
    winrar a -afzip -ep1 -r "dist\%ZIPNAME%" ^
        src ^
        blender_addon ^
        *.bat ^
        *.ps1 ^
        *.md ^
        requirements.txt ^
        LICENSE ^
        -x*__pycache__ ^
        -x*.venv ^
        -x*.pyc ^
        -x*.git
    goto :success
)

REM If no archiver found, use PowerShell
echo Using PowerShell Compress-Archive...
powershell -command "Compress-Archive -Path src,blender_addon,*.bat,*.ps1,*.md,requirements.txt,LICENSE -DestinationPath dist\%ZIPNAME% -Force"

:success
echo.
echo ✅ Package created successfully!
echo 📁 Location: dist\%ZIPNAME%
echo.
echo 📋 Package includes:
echo    - MCP Server (src/)
echo    - Blender Addon (blender_addon/)
echo    - Windows scripts (*.bat, *.ps1)
echo    - Documentation (*.md)
echo    - Requirements (requirements.txt)
echo.
echo 🚀 Ready to share or install on another Windows 11 PC!
echo.
pause
