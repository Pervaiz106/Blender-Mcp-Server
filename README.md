# Blender MCP Comprehensive Server

A production-ready Model Context Protocol (MCP) server providing comprehensive Blender integration with **47+ tools** covering the complete 3D creation workflow from scene management to final rendering.

## 🌟 Overview

This comprehensive MCP server enables AI systems to programmatically interact with Blender's 3D creation capabilities through a secure, well-documented interface. It provides complete access to Blender's Python API (bpy) through categorized tools for different aspects of 3D modeling, animation, and rendering.

## 🚀 Features

### Comprehensive Tool Set (47+ Tools)

#### 🎬 Scene Management (8 tools)
- `create_scene` - Create new Blender scenes
- `set_scene_properties` - Configure frame range and units
- `get_scene_info` - Get detailed scene information
- `duplicate_scene` - Clone existing scenes
- `delete_scene` - Remove scenes (with confirmation)
- `set_world_properties` - Configure world/environment settings
- `get_world_properties` - Get current world settings
- `clear_scene` - Remove all objects (with confirmation)

#### 📦 Object Operations (9 tools)
- `create_object` - Create geometric primitives and objects
- `transform_object` - Move, rotate, and scale objects
- `delete_object` - Remove objects (with confirmation)
- `duplicate_object` - Clone objects
- `join_objects` - Combine multiple objects
- `separate_objects` - Split mesh objects
- `parent_object` - Create parent-child relationships
- `unparent_object` - Remove parent relationships
- `get_object_info` - Get detailed object information

#### 🎨 Material Management (7 tools)
- `create_material` - Create PBR materials with custom properties
- `assign_material` - Apply materials to objects
- `update_material_properties` - Modify material settings
- `delete_material` - Remove materials (with confirmation)
- `duplicate_material` - Clone materials
- `get_material_info` - Get material details
- `list_materials` - List all scene materials

#### 🔧 Mesh Operations (6 tools)
- `edit_mesh` - Perform mesh editing operations (subdivide, bevel, etc.)
- `apply_modifier` - Apply modifiers to objects
- `add_modifier` - Add modifiers without applying
- `remove_modifier` - Remove modifiers (with confirmation)
- `get_mesh_info` - Get detailed mesh data (vertices, faces, etc.)
- `remesh_object` - Apply remeshing algorithms

#### 🎬 Animation System (6 tools)
- `create_animation` - Create complex animations with keyframes
- `set_keyframes` - Set individual transformation keyframes
- `play_animation` - Start animation playback
- `stop_animation` - Stop animation playback
- `clear_animation` - Remove animation data (with confirmation)
- `get_animation_info` - Get animation details

#### 🎨 Rendering Pipeline (5 tools)
- `render_scene` - Render the current scene
- `set_render_settings` - Configure render engine and quality
- `get_render_settings` - Get current render configuration
- `preview_render` - Create quick preview renders
- `get_render_preview` - Get render preview as image

#### 📁 File I/O Operations (4 tools)
- `import_file` - Import 3D models (OBJ, FBX, GLTF, STL, etc.)
- `export_file` - Export objects to various formats
- `save_scene` - Save .blend files
- `load_scene` - Load .blend files (with confirmation)

#### 📷 Camera & Lighting (4 tools)
- `create_camera` - Create cameras with custom settings
- `set_active_camera` - Set active camera for rendering
- `setup_lighting` - Apply predefined lighting setups
- `create_light` - Create individual lights (sun, spot, point, area)

#### 🔧 Utility Tools (Additional)
- `get_viewport_screenshot` - Capture viewport screenshots
- `execute_blender_code` - Execute custom Python code in Blender
- `get_server_status` - Get server and connection status

## 🏗️ Architecture

### Core Components

1. **FastMCP Server** - Built on the FastMCP 2.0 framework for production-ready MCP implementation
2. **Blender Connection** - Socket-based communication with Blender addon
3. **Tool Categories** - Organized tool sets for different 3D workflow stages
4. **Error Handling** - Robust error handling with three-tier model
5. **Security** - Input validation and confirmation mechanisms for destructive operations

### Technology Stack

- **FastMCP 2.0** - High-performance MCP framework
- **Python 3.10+** - Modern Python with type hints
- **Pydantic** - Data validation and serialization
- **Socket Communication** - Real-time Blender integration
- **Blender Python API (bpy)** - Direct access to Blender functionality

## 📦 Installation

### Prerequisites

1. **Blender 3.0+** with the MCP addon installed
2. **Python 3.10+**
3. **uv package manager**

### Quick Start

1. **Clone or download the project:**
```bash
# The server is ready to run from the project directory
cd blender-mcp-comprehensive
```

2. **Install dependencies:**
```bash
# Dependencies will be installed automatically on first run
# or manually with:
uv sync
```

3. **Start Blender with the MCP addon:**
   - Open Blender
   - Install and enable the Blender MCP addon
   - Click "Connect to Claude" in the addon panel

4. **Run the MCP server:**
```bash
# Using the startup script
sh run.sh

# Or directly with uv
uv run python -m src.blender_mcp_server.server
```

## 🔧 Configuration

### Environment Variables

The server can be configured using environment variables:

```bash
# Blender connection settings
export BLENDER_HOST="localhost"      # Default: localhost
export BLENDER_PORT="9876"           # Default: 9876
```

### MCP Client Configuration

For Claude Desktop integration, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "blender-comprehensive": {
      "command": "sh",
      "args": ["/path/to/blender-mcp-comprehensive/run.sh"]
    }
  }
}
```

## 🚀 Usage

### Basic Usage Examples

#### Create a Simple Scene

```python
# Create a new scene
await client.call_tool("create_scene", {"name": "My Scene"})

# Add some objects
await client.call_tool("create_object", {
    "object_type": "CUBE",
    "name": "Building",
    "location": [0, 0, 0]
})

await client.call_tool("create_object", {
    "object_type": "SPHERE",
    "name": "Planet",
    "location": [5, 0, 2]
})

# Create and assign materials
await client.call_tool("create_material", {
    "name": "Brick",
    "base_color": [0.8, 0.3, 0.2],
    "roughness": 0.8
})

await client.call_tool("assign_material", {
    "object_name": "Building",
    "material_name": "Brick"
})
```

#### Create an Animation

```python
# Create orbital animation
keyframes = [
    {"frame": 1, "location": [5, 0, 2], "interpolation": "BEZIER"},
    {"frame": 100, "location": [0, 5, 2], "interpolation": "BEZIER"},
    {"frame": 200, "location": [-5, 0, 2], "interpolation": "BEZIER"},
    {"frame": 300, "location": [0, -5, 2], "interpolation": "BEZIER"},
    {"frame": 400, "location": [5, 0, 2], "interpolation": "BEZIER"}
]

await client.call_tool("create_animation", {
    "object_name": "Planet",
    "animation_type": "LOCATION",
    "keyframes": keyframes
})
```

#### Render a Scene

```python
# Configure render settings
await client.call_tool("set_render_settings", {
    "settings": {
        "engine": "CYCLES",
        "resolution_x": 1920,
        "resolution_y": 1080,
        "samples": 128
    }
})

# Create preview render
await client.call_tool("preview_render", {"resolution": 800})
```

### Advanced Usage

See the comprehensive examples in `/examples/usage_examples.py` which demonstrates:

- Complete workflow from scene creation to final render
- Advanced material creation and assignment
- Complex mesh operations and modifiers
- Sophisticated animation systems
- File I/O operations
- Camera and lighting setups

## 🧪 Testing

The server includes comprehensive test coverage:

### Run Validation Tests

```bash
# Run all tests
cd blender-mcp-comprehensive
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_blender_mcp_server.py::TestBlenderMCPServer::test_scene_management_tools -v
python -m pytest tests/test_blender_mcp_server.py::TestBlenderMCPServer::test_object_operations_tools -v
```

### Test Categories

- **Tool Validation** - Ensures all 47+ tools are properly exposed
- **Parameter Validation** - Tests parameter handling and error cases
- **Connection Testing** - Validates Blender connectivity
- **Integration Testing** - Tests complete workflow scenarios
- **Error Handling** - Tests failure modes and recovery

## 🔒 Security

### Safety Features

1. **Confirmation Requirements** - Destructive operations require explicit confirmation
2. **Input Validation** - All parameters are validated before processing
3. **Error Boundaries** - Comprehensive error handling prevents crashes
4. **Sandboxed Execution** - Operations run in controlled environment
5. **Connection Validation** - Verifies Blender connectivity before operations

### Safe Operations Example

```python
# Destructive operations require confirmation
await client.call_tool("delete_object", {
    "object_name": "ImportantObject",
    "confirm": True  # Required for deletion
})

await client.call_tool("clear_scene", {
    "confirm": True  # Required for clearing entire scene
})
```

## 🔧 Troubleshooting

### Common Issues

#### Connection Problems
```
Error: "Failed to connect to Blender"
```
**Solution:** Ensure Blender is running with the MCP addon enabled and "Connect to Claude" is clicked.

#### Timeout Errors
```
Error: "Timeout waiting for Blender response"
```
**Solution:** 
- Simplify requests by breaking complex operations into smaller steps
- Check Blender responsiveness
- Verify network connectivity

#### Permission Errors
```
Error: "Permission denied" during file operations
```
**Solution:** 
- Check file paths and permissions
- Ensure output directories exist
- Run with appropriate user permissions

### Debug Mode

Enable detailed logging:

```bash
export BLENDER_MCP_DEBUG=1
sh run.sh
```

## 📚 API Reference

### Tool Categories

#### Scene Management
- **create_scene(name)** - Create new scene
- **set_scene_properties(frame_start, frame_end, frame_current, units)** - Configure scene
- **get_scene_info()** - Get scene information
- **duplicate_scene(source_name, new_name)** - Clone scene
- **delete_scene(scene_name, confirm=True)** - Delete scene
- **set_world_properties(color, background_type)** - Configure environment
- **get_world_properties()** - Get world settings
- **clear_scene(confirm=True)** - Clear all objects

#### Object Operations
- **create_object(object_type, name, location)** - Create objects
- **transform_object(object_name, location, rotation, scale)** - Transform objects
- **delete_object(object_name, confirm=True)** - Delete objects
- **duplicate_object(source_name, new_name)** - Clone objects
- **join_objects(object_names, joined_name)** - Combine objects
- **separate_objects(object_name, mode)** - Split objects
- **parent_object(child_name, parent_name, keep_transform)** - Set hierarchy
- **unparent_object(child_name, keep_transform)** - Remove hierarchy
- **get_object_info(object_name)** - Get object details

*[Additional tool documentation available in source code]*

## 🤝 Contributing

### Development Setup

1. **Clone the repository**
2. **Install development dependencies:**
```bash
uv sync --dev
```

3. **Run tests:**
```bash
python -m pytest tests/ -v
```

4. **Code formatting:**
```bash
black src/ tests/
ruff check src/ tests/
```

### Adding New Tools

1. Add tool function with `@mcp.tool` decorator
2. Include comprehensive docstring with parameters
3. Add parameter validation and error handling
4. Write tests for the new tool
5. Update documentation

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all parameters and returns
- Include comprehensive docstrings
- Write unit tests for new functionality
- Maintain backward compatibility

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **FastMCP Team** - For the excellent MCP framework
- **Blender Foundation** - For the powerful 3D creation suite
- **MCP Community** - For protocol standardization
- **Python Ecosystem** - For robust development tools

## 📞 Support

- **Documentation:** Comprehensive examples and API reference included
- **Testing:** Full test suite for validation
- **Issues:** Report bugs and feature requests through GitHub issues
- **Community:** Join discussions in the MCP community channels

---

**Built with ❤️ by MiniMax Agent**

*Enabling AI-powered 3D creation through comprehensive Blender integration.*