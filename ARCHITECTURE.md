# Blender MCP System Architecture

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                                                                     │
│  ┌──────────────────┐        ┌──────────────────┐                 │
│  │  Claude Desktop  │   OR   │  Other AI Client │                 │
│  │  (with MCP)      │        │  (Gemini, GPT)   │                 │
│  └────────┬─────────┘        └────────┬─────────┘                 │
│           │                           │                            │
│           └───────────┬───────────────┘                            │
│                       │                                            │
│                  AI Commands                                       │
│              "Add a cube at (0,0,0)"                               │
│                       │                                            │
└───────────────────────┼────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL MCP SERVER                              │
│                   (Python Process - stdio)                          │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  src/blender_mcp_server/server.py                            │  │
│  │                                                               │  │
│  │  - Receives AI commands via MCP protocol                     │  │
│  │  - Translates to Blender operations                          │  │
│  │  - Connects to Blender via socket (port 9876)                │  │
│  │  - Returns results to AI                                     │  │
│  │                                                               │  │
│  │  47+ Tools Available:                                        │  │
│  │    • Scene Management                                        │  │
│  │    • Object Operations                                       │  │
│  │    • Materials & Textures                                    │  │
│  │    • Animation & Keyframes                                   │  │
│  │    • Rendering & Camera                                      │  │
│  │    • File I/O                                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                     Socket Connection
                        localhost:9876
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         BLENDER                                     │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Blender MCP Addon (blender_addon/__init__.py)              │  │
│  │                                                               │  │
│  │  - Runs inside Blender as plugin                            │  │
│  │  - Opens socket server on port 9876                         │  │
│  │  - Receives JSON commands                                   │  │
│  │  - Executes bpy (Blender Python) operations                │  │
│  │  - Returns success/error results                            │  │
│  │                                                               │  │
│  │  UI Panel (View3D Sidebar → MCP Tab):                       │  │
│  │    • Start/Stop Server                                       │  │
│  │    • Connection Settings                                     │  │
│  │    • Server Status                                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Blender Python API (bpy)                                    │  │
│  │                                                               │  │
│  │  - bpy.ops.mesh.primitive_cube_add()                        │  │
│  │  - bpy.data.objects["Cube"].location = (0, 0, 0)           │  │
│  │  - bpy.ops.render.render()                                  │  │
│  │  - And many more...                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  3D Viewport - Visual Output                                 │  │
│  │                                                               │  │
│  │     [Your 3D Scene Created by AI]                           │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Example: "Add a red cube at position (2, 3, 5)"

```
1. USER COMMAND
   │
   │  "Add a red cube at position (2, 3, 5)"
   │
   ▼
2. AI ASSISTANT (Claude/Gemini)
   │
   │  Interprets command → Selects MCP tool
   │
   ▼
3. MCP SERVER (External Python)
   │
   │  Receives: tool_name="add_cube", params={location:(2,3,5), color:"red"}
   │  Formats JSON command
   │
   ▼
4. SOCKET CONNECTION (localhost:9876)
   │
   │  Sends: {"action": "add_cube", "params": {"location": [2, 3, 5]}}
   │
   ▼
5. BLENDER ADDON (Inside Blender)
   │
   │  Receives JSON → Parses command
   │  Executes: bpy.ops.mesh.primitive_cube_add(location=(2, 3, 5))
   │  Creates material with red color
   │
   ▼
6. BLENDER VIEWPORT
   │
   │  Red cube appears at (2, 3, 5)
   │
   ▼
7. RESULT RETURN
   │
   │  Addon → Socket → MCP Server → AI → User
   │  "Success: Cube created at position (2, 3, 5)"
```

## Component Responsibilities

### External MCP Server
- ✅ MCP protocol implementation
- ✅ AI assistant communication
- ✅ Tool registration and documentation
- ✅ Command translation
- ✅ Error handling and responses

### Blender Addon
- ✅ Socket server inside Blender
- ✅ bpy API access
- ✅ Command execution
- ✅ UI panel for control
- ✅ Background thread handling

### Communication Protocol
- ✅ JSON over TCP socket
- ✅ Port 9876 (configurable)
- ✅ Request-response pattern
- ✅ Error propagation

## Security Model

```
┌─────────────────────────────────────────────────────────────┐
│  Network Boundary                                           │
│                                                             │
│  ┌───────────────────┐         ┌───────────────────┐      │
│  │  External MCP     │◄───────►│  Blender Addon    │      │
│  │  Server           │  Local  │  (bpy access)     │      │
│  │  (localhost only) │  Socket │  (localhost only) │      │
│  └───────────────────┘         └───────────────────┘      │
│                                                             │
│  ⚠️  Both bind to localhost only                           │
│  ⚠️  No external network exposure                          │
│  ⚠️  Windows Firewall protection                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Startup Sequence

```
Step 1: Install Prerequisites
   ├── Python 3.8+ with pip
   ├── Blender 3.0+
   └── Python dependencies (pip install -r requirements.txt)

Step 2: Install Blender Addon
   ├── Open Blender
   ├── Edit → Preferences → Add-ons → Install
   ├── Select blender_addon/__init__.py
   └── Enable "Blender MCP Bridge"

Step 3: Start Blender Addon Server
   ├── Press N in 3D Viewport
   ├── Click "MCP" tab
   └── Click "Start MCP Server"
   
Step 4: Start External MCP Server
   ├── Open Command Prompt
   ├── cd C:\path\to\blender-mcp-comprehensive
   └── Run: start-windows.bat

Step 5: Configure AI Client
   ├── Add MCP server to client config
   └── Restart AI client

Step 6: Ready to Use!
   └── Send AI commands to control Blender
```

## Shutdown Sequence

```
1. Stop External MCP Server
   └── Close Command Prompt or Ctrl+C

2. Stop Blender Addon Server
   └── Click "Stop MCP Server" in Blender

3. Close Blender (Optional)
   └── File → Quit
```

## Error Handling Flow

```
Error at any level → Propagates up:

bpy.ops error
   ↓
Blender Addon catches → Formats error JSON
   ↓
Socket sends error response
   ↓
MCP Server receives → Formats for AI
   ↓
AI Assistant receives → Shows user-friendly message
   ↓
User sees: "Error: Object 'Cube' not found"
```

## Platform Compatibility

### Windows 11 (Primary)
- ✅ Fully supported
- ✅ Native .bat and .ps1 scripts
- ✅ Windows paths handled automatically
- ✅ Windows Firewall integration

### Linux/Mac (Compatible)
- ✅ Use .sh scripts instead of .bat
- ✅ Same Python code works
- ✅ Same Blender addon works
- ✅ Path separators handled by Python

## Performance Characteristics

- **Latency**: ~50-200ms per command (network + execution)
- **Throughput**: 10-50 commands/second
- **Memory**: ~50MB for MCP server, Blender uses standard memory
- **CPU**: Minimal (mostly I/O bound)

## Future Enhancements

Potential improvements:
- WebSocket support for real-time updates
- Authentication and encryption
- Multi-user support
- Remote Blender control
- Batch command execution
- Command queuing and prioritization
