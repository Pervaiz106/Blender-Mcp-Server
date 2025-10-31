# ✅ Blender MCP Server Installation Checklist

## ✅ Completed Steps
- [x] Download and extract project files
- [x] Python 3.12+ environment verified
- [x] Core dependencies installed (FastMCP, Pydantic, etc.)
- [x] Server files ready to run

## 🔧 Required for Production Use

### 1. Install Blender
- [ ] Download Blender 3.0+ from https://blender.org
- [ ] Install Blender on your system
- [ ] Verify installation: `blender --version`

### 2. Install Blender MCP Addon
- [ ] Download the Blender MCP addon (included in project)
- [ ] Open Blender → Preferences → Add-ons → Install
- [ ] Select `blender_mcp_addon.py` from the project
- [ ] Enable the addon in Blender preferences

### 3. Connect to AI Client
- [ ] Start Blender with addon enabled
- [ ] Click "Connect to Claude" in the addon panel
- [ ] Configure your AI client (Claude Desktop, etc.)

### 4. Start MCP Server
```bash
cd blender-mcp-comprehensive
sh run.sh
```

## 🎯 Testing Your Installation

### Test 1: Server Starts
```bash
python3 -m src.blender_mcp_server.server --help
```

### Test 2: Blender Connection
```bash
# Start Blender and click "Connect to Claude" in the addon
# Server should show: "Blender connected successfully"
```

### Test 3: AI Client Integration
- Add to your MCP client config:
```json
{
  "mcpServers": {
    "blender-mcp": {
      "command": "sh",
      "args": ["/path/to/blender-mcp-comprehensive/run.sh"]
    }
  }
}
```

## 🚀 Available Tools (47+)

Once connected, your AI can use these tools:

### Scene Management (8 tools)
- create_scene, set_scene_properties, get_scene_info
- duplicate_scene, delete_scene, clear_scene
- set_world_properties, get_world_properties

### Object Operations (9 tools)
- create_object, transform_object, delete_object
- duplicate_object, join_objects, separate_objects
- parent_object, unparent_object, get_object_info

### Materials (7 tools)
- create_material, assign_material, update_material_properties
- delete_material, duplicate_material, get_material_info, list_materials

### Mesh Operations (6 tools)
- edit_mesh, apply_modifier, add_modifier
- remove_modifier, get_mesh_info, remesh_object

### Animation (6 tools)
- create_animation, set_keyframes, play_animation
- stop_animation, clear_animation, get_animation_info

### Rendering (5 tools)
- render_scene, set_render_settings, get_render_settings
- preview_render, get_render_preview

### File I/O (4 tools)
- import_file, export_file, save_scene, load_scene

### Camera & Lighting (4 tools)
- create_camera, set_active_camera, setup_lighting, create_light

### Utilities (Additional)
- get_viewport_screenshot, execute_blender_code, get_server_status

## 🆘 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'bpy'"
**Solution:** Install Blender. The Blender Python API (bpy) is only available when Blender is installed.

### Error: "Blender not connected"
**Solution:** 
1. Open Blender
2. Enable the MCP addon
3. Click "Connect to Claude" in the addon panel
4. Restart the MCP server

### Error: "Permission denied" on run.sh
**Solution:** 
```bash
chmod +x run.sh
chmod +x install.sh
```

## 🎉 You're Ready!

Once you complete the checklist above, your Blender MCP Server will provide 47+ tools for AI-powered 3D creation!

For questions or issues, check the README.md or visit the GitHub repository.