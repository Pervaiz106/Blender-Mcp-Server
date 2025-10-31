# Windows 11 Setup Guide for Blender MCP Server

## Prerequisites

### 1. Python Installation
- **Download Python 3.8+** from [python.org](https://www.python.org/downloads/)
- **During installation**, check "Add Python to PATH"
- **Verify installation**: Open Command Prompt or PowerShell and run:
  ```cmd
  python --version
  pip --version
  ```

### 2. Blender Installation (Required)
- **Download Blender 3.0+** from [blender.org](https://www.blender.org/download/)
- **Install Blender** with default settings
- **Note the installation path** (usually `C:\Program Files\Blender Foundation\Blender 4.x\`)

### 3. Project Setup
1. **Extract the downloaded package** to a folder like `C:\blender-mcp\`
2. **Open Command Prompt or PowerShell** in the extracted directory
3. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

## Quick Start (Windows 11)

### Method 1: Using Batch File (Recommended)
1. **Double-click** `start-windows.bat`
2. **Server will start** in a new command window

### Method 2: Using PowerShell
1. **Right-click** on `start-windows-ps1.ps1`
2. **Select "Run with PowerShell"**
3. **If blocked**, run PowerShell as Administrator and execute:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Method 3: Manual Command Line
1. **Open Command Prompt or PowerShell** in the project directory
2. **Run**:
   ```cmd
   python -m src.blender_mcp_server.server --transport stdio
   ```

## Windows 11 Specific Notes

### File Paths and Backslashes
- Windows uses backslashes (`\`) in file paths
- All scripts automatically handle Windows paths
- Environment variables work the same as Linux/Mac

### PowerShell vs Command Prompt
- **PowerShell**: More modern, better error handling
- **Command Prompt**: Simpler, more compatible
- Both work equally well for the MCP server

### Windows Firewall
- **First run** may prompt Windows Firewall
- **Allow the connection** for Python.exe
- This enables the MCP server to communicate properly

### Python Environment
- **No virtual environment required** on Windows
- **System Python** works perfectly
- **All dependencies** are installed globally via pip

## Configuration (Optional)

### Environment Variables
Set these before starting the server:
```cmd
set BLENDER_HOST=localhost
set BLENDER_PORT=9876
python -m src.blender_mcp_server.server --transport stdio
```

### Custom Blender Path
If Blender is installed in a custom location:
```cmd
set BLENDER_PATH=C:\Path\To\Your\Blender\blender.exe
python -m src.blender_mcp_server.server --transport stdio
```

## Testing the Installation

### 1. Check Python Installation
```cmd
python --version
```
Should show Python 3.8 or higher.

### 2. Check Dependencies
```cmd
pip list | findstr fastmcp
```
Should show FastMCP 2.13.0.2 or similar.

### 3. Test Server Startup
```cmd
python -m src.blender_mcp_server.server --transport stdio
```
Should start without errors (will show bpy module error if Blender not installed - this is normal).

### 4. Check Available Tools
The server provides **47+ Blender tools** including:
- Scene management (create_scene, set_scene_frame, etc.)
- Object operations (add_cube, add_sphere, move_object, etc.) 
- Materials (create_material, set_material_property, etc.)
- Animation (create_keyframe, set_animation_data, etc.)
- Rendering (render_scene, set_render_settings, etc.)

## Troubleshooting Windows 11

### "python is not recognized"
- **Reinstall Python** with "Add to PATH" checked
- **Or use full path**: `C:\Python39\python.exe` (adjust version)

### "No module named 'bpy'"
- **Install Blender** first (required dependency)
- **Restart Command Prompt** after Blender installation

### "Permission denied"
- **Run as Administrator**
- **Or install to user directory** (not Program Files)

### Firewall prompts
- **Allow Python.exe** through Windows Firewall
- **This is normal** for network applications

### Import errors
```cmd
pip install --upgrade -r requirements.txt
```

## Next Steps

1. **Start the MCP server** using one of the methods above
2. **Configure your AI client** (Claude Desktop, etc.) to connect
3. **Begin using Blender tools** through AI commands

## Support

If you encounter issues:
1. **Check Windows 11 compatibility** (Windows 10+ required)
2. **Verify Python installation** with `python --version`
3. **Ensure Blender 3.0+ is installed**
4. **Run as Administrator** if permission issues occur

The MCP server is fully compatible with Windows 11 and provides the same 47+ Blender tools as on Linux/Mac systems.
