# Installing Blender MCP Addon on Windows 11

## What is the Blender MCP Addon?

The **Blender MCP Addon** is a small plugin that runs **inside Blender** and allows the external MCP server to control Blender through AI commands.

Think of it as:
- **MCP Server** (external) = The "brain" that receives AI commands
- **Blender Addon** (internal) = The "hands" that execute commands in Blender

## Installation Steps (Windows 11)

### Step 1: Locate the Addon File
The addon file is located at:
```
blender-mcp-comprehensive\blender_addon\__init__.py
```

### Step 2: Install in Blender (Method 1 - Recommended)

1. **Open Blender** on your Windows 11 PC

2. **Go to Edit → Preferences** (or press `Ctrl + Alt + U`)

3. **Click on "Add-ons"** in the left sidebar

4. **Click "Install..."** button at the top

5. **Navigate** to the addon folder:
   ```
   C:\path\to\blender-mcp-comprehensive\blender_addon\
   ```

6. **Select** the `__init__.py` file

7. **Click "Install Add-on"**

8. **Enable the addon**:
   - Search for "MCP" in the add-ons list
   - Check the checkbox next to "System: Blender MCP Bridge"

9. **Click "Save Preferences"**

### Step 3: Configure the Addon

1. **Expand the addon** in the preferences by clicking the arrow

2. **Set connection settings**:
   - **Host**: `localhost` (default)
   - **Port**: `9876` (default)

3. **Save Preferences** again

### Step 4: Access the MCP Panel

1. **Open the 3D Viewport** (default view)

2. **Press `N`** to open the sidebar (if not visible)

3. **Click on the "MCP" tab** in the sidebar

4. You should see:
   - Connection settings
   - Start/Stop server buttons
   - Server status

### Step 5: Start the MCP Server in Blender

1. **Click "Start MCP Server"** button

2. **Status should show**: "Server Running ✓"

3. **Blender is now ready** to receive commands from the external MCP server!

## Alternative Installation Method (Manual)

If the above doesn't work, manually copy the addon:

1. **Find Blender's addons folder**:
   ```
   C:\Users\YourUsername\AppData\Roaming\Blender Foundation\Blender\4.x\scripts\addons\
   ```
   (Replace `4.x` with your Blender version, e.g., `4.0`, `3.6`, etc.)

2. **Create a folder** named `blender_mcp_bridge`

3. **Copy** the `__init__.py` file into this folder

4. **Restart Blender**

5. **Enable the addon** in Edit → Preferences → Add-ons

## How It Works

```
┌─────────────────────┐         ┌──────────────────────┐
│   AI Assistant      │         │      Blender         │
│   (Claude, etc.)    │         │                      │
└──────────┬──────────┘         └──────────┬───────────┘
           │                               │
           │  Commands                     │
           ▼                               │
┌─────────────────────┐                   │
│   MCP Server        │                   │
│   (External Python) │◄──────────────────┤
│   Port: stdio       │   Socket          │
└─────────────────────┘   Connection      │
                          Port 9876       │
                                          │
                          ┌───────────────▼────────┐
                          │  Blender MCP Addon     │
                          │  (Inside Blender)      │
                          │  Executes bpy commands │
                          └────────────────────────┘
```

## Testing the Setup

### Test 1: Start the Addon Server
1. Open Blender
2. Press `N` → Click "MCP" tab
3. Click "Start MCP Server"
4. Should see "Server Running ✓"

### Test 2: External MCP Server Connection
1. Keep Blender open with addon server running
2. Open Command Prompt in another window
3. Navigate to: `cd C:\path\to\blender-mcp-comprehensive`
4. Run: `python -m src.blender_mcp_server.server --transport stdio`
5. The external server should connect to Blender

### Test 3: Send a Command via AI
Once both servers are running, use your AI assistant (Claude Desktop configured with MCP) to send commands like:
- "Add a cube to the Blender scene"
- "Create a sphere at location (0, 0, 5)"
- "Render the current scene"

## Troubleshooting

### "No module named 'bpy'" Error
- **This is NORMAL** when running the external MCP server without Blender
- The addon runs **inside** Blender, so it has access to `bpy`
- The external server just needs to **connect** to Blender

### Addon Not Showing Up
1. Check Blender version compatibility (requires Blender 3.0+)
2. Make sure `__init__.py` is in the correct location
3. Try the manual installation method above

### "Server Running" but No Connection
1. Check Windows Firewall isn't blocking port 9876
2. Verify both addon and external server use same port (9876)
3. Make sure Blender addon server is started first

### Port Already in Use
- Change the port in addon preferences (e.g., 9877)
- Also update `BLENDER_PORT` environment variable for external server:
  ```cmd
  set BLENDER_PORT=9877
  python -m src.blender_mcp_server.server --transport stdio
  ```

## What the Addon Does

The addon provides a **socket server inside Blender** that:
- ✅ Listens on port 9876 (configurable)
- ✅ Receives JSON commands from external MCP server
- ✅ Executes Blender Python (bpy) operations
- ✅ Returns success/error results
- ✅ Handles multiple connections
- ✅ Runs in background thread (doesn't freeze Blender)

## Supported Operations

The addon can execute all 47+ MCP tools including:
- Add objects (cube, sphere, cylinder, etc.)
- Delete/move/rotate objects
- Create materials and apply properties
- Set up animations and keyframes
- Configure rendering settings
- Save/load Blender files
- Execute custom Python code

## Security Note

The addon executes Python code inside Blender. Only use it with:
- ✅ Trusted AI assistants
- ✅ Local connections (localhost)
- ✅ Secured networks

❌ **Do NOT expose port 9876 to the internet** without proper security measures.

## Next Steps

After installing the addon:
1. ✅ **Enable and start** the addon server in Blender
2. ✅ **Run the external MCP server** (start-windows.bat)
3. ✅ **Configure your AI client** to use the MCP server
4. 🎨 **Start creating** 3D content with AI commands!

Your Blender MCP setup is now complete on Windows 11!
