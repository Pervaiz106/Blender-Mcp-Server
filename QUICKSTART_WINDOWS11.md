# 🚀 Quick Start Guide - Windows 11 Complete Setup

## Overview

This Blender MCP system has **two parts** that work together:

1. **External MCP Server** (Python script) - Connects to AI assistants
2. **Blender Addon** (runs inside Blender) - Executes commands

Both must be running for AI-controlled Blender to work!

---

## 📋 Complete Setup (10 Minutes)

### Part 1: Prerequisites

#### A. Install Python
1. Download from [python.org](https://www.python.org/downloads/)
2. ✅ **Check "Add Python to PATH"** during installation
3. Verify: Open Command Prompt and run:
   ```cmd
   python --version
   ```

#### B. Install Blender
1. Download from [blender.org](https://www.blender.org/download/)
2. Install with default settings
3. Launch Blender once to verify it works

### Part 2: Install Python Dependencies

1. **Open Command Prompt** (press `Win + R`, type `cmd`)

2. **Navigate to project folder**:
   ```cmd
   cd C:\path\to\blender-mcp-comprehensive
   ```

3. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Test installation**:
   ```cmd
   test-windows-setup.bat
   ```

### Part 3: Install Blender Addon

1. **Open Blender**

2. **Go to**: Edit → Preferences (or press `Ctrl + Alt + U`)

3. **Click**: Add-ons → Install...

4. **Browse to**: `blender-mcp-comprehensive\blender_addon\__init__.py`

5. **Click**: "Install Add-on"

6. **Enable**: Search "MCP" and check the box next to "Blender MCP Bridge"

7. **Configure**:
   - Expand the addon (click arrow)
   - Host: `localhost`
   - Port: `9876`

8. **Save Preferences**

### Part 4: Start Everything

#### Terminal 1 - Start Blender with Addon
1. **Open Blender**
2. **Press `N`** to show sidebar
3. **Click "MCP" tab**
4. **Click "Start MCP Server"**
5. ✅ Status should show "Server Running ✓"
6. **Keep Blender open!**

#### Terminal 2 - Start External MCP Server
1. **Open new Command Prompt**
2. **Navigate to project**:
   ```cmd
   cd C:\path\to\blender-mcp-comprehensive
   ```
3. **Run**:
   ```cmd
   start-windows.bat
   ```
4. ✅ Should connect without errors

---

## 🎯 How to Use with AI

### Configure Claude Desktop (Example)

1. **Open Claude Desktop config**:
   ```
   C:\Users\YourUsername\AppData\Roaming\Claude\claude_desktop_config.json
   ```

2. **Add MCP server**:
   ```json
   {
     "mcpServers": {
       "blender": {
         "command": "python",
         "args": [
           "-m",
           "src.blender_mcp_server.server",
           "--transport",
           "stdio"
         ],
         "cwd": "C:\\path\\to\\blender-mcp-comprehensive"
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test with commands**:
   - "Add a cube to the Blender scene"
   - "Create 5 spheres in a circle"
   - "Render the current scene"

---

## 📁 File Structure

```
blender-mcp-comprehensive/
├── src/
│   └── blender_mcp_server/
│       ├── server.py              # Main MCP server
│       └── simple_server.py       # Alternative server
├── blender_addon/
│   └── __init__.py                # Blender addon (install in Blender)
├── start-windows.bat              # Quick start (double-click)
├── test-windows-setup.bat         # Test everything
├── requirements.txt               # Python dependencies
├── WINDOWS11_SETUP_GUIDE.md       # Detailed Windows guide
└── BLENDER_ADDON_INSTALL.md       # Addon installation guide
```

---

## 🔧 Troubleshooting

### "No module named 'bpy'" - NORMAL!
- The external server shows this when Blender isn't connected
- This is expected - the addon runs **inside** Blender with bpy access
- As long as Blender addon is running, commands will work

### Connection Refused
1. ✅ Start **Blender addon server first** (in Blender: MCP tab → Start)
2. ✅ Then start **external MCP server** (start-windows.bat)
3. Check port 9876 isn't blocked by firewall

### Addon Not Found
- Make sure you installed `blender_addon\__init__.py` (not the whole folder)
- Try manual installation: Copy to Blender's addons folder
- See: BLENDER_ADDON_INSTALL.md for detailed steps

### Windows Firewall Prompt
- **Click "Allow"** when prompted for Python.exe
- This lets the MCP server communicate with Blender

---

## ✅ Quick Test Checklist

- [ ] Python 3.8+ installed and in PATH
- [ ] Blender 3.0+ installed and working
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Blender addon installed and enabled
- [ ] Blender addon server started (shows "Server Running ✓")
- [ ] External MCP server running (start-windows.bat)
- [ ] AI client configured with MCP server

---

## 🎨 Example Commands

Once everything is running, try these with your AI assistant:

```
"Add a red cube at the origin"
"Create a blue sphere above the cube"
"Add a camera pointing at the objects"
"Set up lighting for the scene"
"Render and save the image"
```

---

## 📚 Documentation

- **WINDOWS11_SETUP_GUIDE.md** - Complete Windows installation
- **BLENDER_ADDON_INSTALL.md** - Addon installation details
- **README.md** - Full project documentation
- **api_reference.md** - All 47+ available tools

---

## 🆘 Need Help?

1. Run `test-windows-setup.bat` to check your setup
2. Check documentation in the project folder
3. Verify both servers are running:
   - Blender addon: "Server Running ✓"
   - External MCP: Command window shows no errors

---

## 🎉 You're Ready!

Both servers running? Addon enabled? You can now control Blender with AI commands!

Start with simple commands and gradually explore all 47+ MCP tools for creating complex 3D scenes.
