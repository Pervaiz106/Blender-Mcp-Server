# 📚 API Reference

This document provides a comprehensive reference for all tools available in the Blender MCP Server.

## 🔧 Tool Categories

The server provides 23 production tools organized into 6 categories:

1. [Scene Management](#-scene-management)
2. [Object Operations](#-object-operations)
3. [Material System](#-material-system)
4. [Rendering Pipeline](#-rendering-pipeline)
5. [Camera & Lighting](#-camera--lighting)
6. [Utility Tools](#-utility-tools)

---

## 🎬 Scene Management

### `create_scene`

Create a new Blender scene.

**Parameters:**
```json
{
  "name": "string",        // Scene name (required)
  "frame_start": "number", // Start frame (default: 1)
  "frame_end": "number"    // End frame (default: 250)
}
```

**Example:**
```json
{
  "name": "animation_scene",
  "frame_start": 1,
  "frame_end": 300
}
```

**Returns:**
```json
{
  "success": true,
  "message": "Scene 'animation_scene' created successfully",
  "scene_info": {
    "name": "animation_scene",
    "frame_start": 1,
    "frame_end": 300
  }
}
```

### `set_scene_properties`

Configure scene properties.

**Parameters:**
```json
{
  "name": "string",           // Scene name (required)
  "frame_start": "number",    // Start frame
  "frame_end": "number",      // End frame
  "frame_current": "number",  // Current frame
  "units": "object"           // Units object with scale, length_unit, etc.
}
```

**Example:**
```json
{
  "name": "test_scene",
  "frame_start": 1,
  "frame_end": 1000,
  "frame_current": 24,
  "units": {
    "scale_length": 1.0,
    "length_unit": "METERS"
  }
}
```

### `get_scene_info`

Get detailed information about a scene.

**Parameters:**
```json
{
  "name": "string"  // Scene name (optional, uses active scene if not provided)
}
```

**Returns:**
```json
{
  "scene_info": {
    "name": "Scene",
    "frame_start": 1,
    "frame_end": 250,
    "frame_current": 1,
    "unit_settings": {
      "scale_length": 1.0,
      "length_unit": "METERS"
    }
  }
}
```

### `duplicate_scene`

Clone an existing scene.

**Parameters:**
```json
{
  "source_name": "string",  // Source scene name (required)
  "new_name": "string"      // New scene name (required)
}
```

**Example:**
```json
{
  "source_name": "base_scene",
  "new_name": "backup_scene"
}
```

### `delete_scene`

Remove a scene (requires confirmation).

**Parameters:**
```json
{
  "scene_name": "string",  // Scene name (required)
  "confirm": "boolean"     // Confirmation required (default: false)
}
```

**Example:**
```json
{
  "scene_name": "temp_scene",
  "confirm": true
}
```

### `set_world_properties`

Configure world/environment settings.

**Parameters:**
```json
{
  "name": "string",          // World name (required)
  "color": "array",          // [r, g, b, a] background color
  "background_type": "string" // "SKY", "GRADIENT", "NODE", etc.
}
```

### `get_world_properties`

Get current world settings.

**Parameters:**
```json
{
  "name": "string"  // World name (optional)
}
```

### `clear_scene`

Remove all objects from scene (requires confirmation).

**Parameters:**
```json
{
  "confirm": "boolean"  // Confirmation required (default: false)
}
```

---

## 📦 Object Operations

### `create_object`

Create geometric primitives and objects.

**Parameters:**
```json
{
  "object_type": "string",     // "CUBE", "SPHERE", "CYLINDER", etc. (required)
  "name": "string",            // Object name (required)
  "location": "array",         // [x, y, z] position (default: [0, 0, 0])
  "rotation": "array",         // [x, y, z] rotation in radians (default: [0, 0, 0])
  "scale": "array",            // [x, y, z] scale factors (default: [1, 1, 1])
  "size": "number"             // Overall size (alternative to scale)
}
```

**Example:**
```json
{
  "object_type": "CUBE",
  "name": "building",
  "location": [0, 0, 0],
  "scale": [2, 2, 3]
}
```

**Available Object Types:**
- `CUBE`, `SPHERE`, `CYLINDER`, `CONE`, `PLANE`, `TORUS`
- `CAPSULE`, `CIRCLE`, `GRID`, `ICO_SPHERE`, `MONKEY`, `PRIMITIVE_TORUS`

### `transform_object`

Move, rotate, and scale objects.

**Parameters:**
```json
{
  "object_name": "string",  // Object name (required)
  "location": "array",      // [x, y, z] new position
  "rotation": "array",      // [x, y, z] new rotation in radians
  "scale": "array"          // [x, y, z] new scale factors
}
```

### `delete_object`

Remove objects (requires confirmation).

**Parameters:**
```json
{
  "object_name": "string",  // Object name (required)
  "confirm": "boolean"      // Confirmation required (default: false)
}
```

### `duplicate_object`

Clone objects.

**Parameters:**
```json
{
  "source_name": "string",  // Source object name (required)
  "new_name": "string",     // New object name (required)
  "location": "array",      // [x, y, z] position offset (default: [0, 0, 0])
  "link": "boolean"         // Link to scene or library (default: true)
}
```

### `join_objects`

Combine multiple objects into one.

**Parameters:**
```json
{
  "object_names": "array",  // List of object names (required)
  "joined_name": "string"   // Name for the joined object (required)
}
```

### `separate_objects`

Split mesh objects.

**Parameters:**
```json
{
  "object_name": "string",  // Object name (required)
  "mode": "string"          // "BY_MESH", "BY_MATERIAL", "BY_LOOSE_PARTS" (default: "BY_MESH")
}
```

### `parent_object`

Create parent-child relationships.

**Parameters:**
```json
{
  "child_name": "string",       // Child object name (required)
  "parent_name": "string",      // Parent object name (required)
  "keep_transform": "boolean"   // Keep world transform (default: true)
}
```

### `unparent_object`

Remove parent relationships.

**Parameters:**
```json
{
  "child_name": "string",       // Child object name (required)
  "keep_transform": "boolean"   // Keep world transform (default: true)
}
```

### `get_object_info`

Get detailed object information.

**Parameters:**
```json
{
  "object_name": "string"  // Object name (required)
}
```

**Returns:**
```json
{
  "object_info": {
    "name": "Cube",
    "type": "MESH",
    "location": [0.0, 0.0, 0.0],
    "rotation": [0.0, 0.0, 0.0],
    "scale": [1.0, 1.0, 1.0],
    "dimensions": [2.0, 2.0, 2.0],
    "vertex_count": 8,
    "face_count": 6,
    "material_count": 0
  }
}
```

---

## 🎨 Material System

### `create_material`

Create PBR materials with custom properties.

**Parameters:**
```json
{
  "name": "string",         // Material name (required)
  "base_color": "array",    // [r, g, b, a] base color (default: [0.8, 0.8, 0.8, 1.0])
  "metallic": "number",     // Metallic factor 0-1 (default: 0.0)
  "roughness": "number",    // Roughness factor 0-1 (default: 0.5)
  "emission": "array",      // [r, g, b, a] emission color
  "emission_strength": "number" // Emission strength (default: 0.0)
}
```

**Example:**
```json
{
  "name": "brick_material",
  "base_color": [0.8, 0.3, 0.2, 1.0],
  "metallic": 0.0,
  "roughness": 0.8
}
```

### `assign_material`

Apply materials to objects.

**Parameters:**
```json
{
  "object_name": "string",    // Object name (required)
  "material_name": "string",  // Material name (required)
  "material_slot": "number"   // Material slot index (default: 0)
}
```

---

## 🎨 Rendering Pipeline

### `render_scene`

Render the current scene.

**Parameters:**
```json
{
  "output_path": "string",     // Output file path (required)
  "resolution_x": "number",    // Width in pixels (default: 1920)
  "resolution_y": "number",    // Height in pixels (default: 1080)
  "engine": "string",          // Render engine "CYCLES" or "EEVEE" (default: "CYCLES")
  "samples": "number",         // Sample count (default: 128)
  "denoising": "boolean"       // Enable denoising (default: true)
}
```

**Example:**
```json
{
  "output_path": "/path/to/render.png",
  "resolution_x": 1920,
  "resolution_y": 1080,
  "engine": "CYCLES",
  "samples": 256
}
```

---

## 📷 Camera & Lighting

### `create_camera`

Create cameras with custom settings.

**Parameters:**
```json
{
  "name": "string",        // Camera name (required)
  "location": "array",     // [x, y, z] position (default: [0, 0, 0])
  "rotation": "array",     // [x, y, z] rotation in radians
  "lens": "number",        // Focal length in mm (default: 50.0)
  "fov": "number",         // Field of view in radians
  "sensor_fit": "string"   // "HORIZONTAL", "VERTICAL" (default: "HORIZONTAL")
}
```

### `setup_lighting`

Apply predefined lighting setups.

**Parameters:**
```json
{
  "lighting_type": "string",  // Lighting setup type (required)
  "intensity": "number",      // Light intensity (default: 1.0)
  "color": "array",           // [r, g, b] light color (default: [1, 1, 1])
  "location": "array"         // [x, y, z] lighting position
}
```

**Available Lighting Types:**
- `THREE_POINT` - Three-point lighting setup
- `KEY_FILL_RIM` - Key, fill, and rim lights
- `AMBIENT` - Ambient lighting
- `DIRECTIONAL` - Single directional light
- `POINT_LIGHTS` - Multiple point lights

---

## 🔧 Utility Tools

### `get_server_status`

Get server and connection status.

**Parameters:** None

**Returns:**
```json
{
  "status": "connected",
  "version": "1.0.0",
  "blender_version": "3.6.0",
  "connection_time": "2025-10-31T15:00:00Z",
  "tools_available": 23,
  "scenes_count": 1,
  "objects_count": 5
}
```

---

## 🔄 Error Handling

All tools return standardized error responses:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Detailed error message",
    "details": {
      "parameter": "problematic_parameter",
      "suggestion": "How to fix this issue"
    }
  }
}
```

### Common Error Codes:

- `OBJECT_NOT_FOUND` - Requested object doesn't exist
- `SCENE_NOT_FOUND` - Requested scene doesn't exist
- `MATERIAL_NOT_FOUND` - Requested material doesn't exist
- `INVALID_PARAMETER` - Parameter validation failed
- `CONFIRMATION_REQUIRED` - Destructive operation needs confirmation
- `BLENDER_CONNECTION_ERROR` - Failed to connect to Blender
- `PERMISSION_DENIED` - Insufficient permissions
- `INVALID_FILE_PATH` - File path is invalid or inaccessible

---

## 📝 Usage Examples

### Complete Workflow Example

```python
# 1. Create scene
await client.call_tool("create_scene", {
    "name": "showcase_scene",
    "frame_end": 500
})

# 2. Create objects
await client.call_tool("create_object", {
    "object_type": "CUBE",
    "name": "building",
    "location": [0, 0, 0],
    "scale": [3, 3, 10]
})

await client.call_tool("create_object", {
    "object_type": "SPHERE",
    "name": "planet",
    "location": [10, 0, 5],
    "scale": [2, 2, 2]
})

# 3. Create and assign materials
await client.call_tool("create_material", {
    "name": "glass_material",
    "base_color": [0.2, 0.2, 0.8, 0.1],
    "metallic": 0.0,
    "roughness": 0.0,
    "transmission": 0.9
})

await client.call_tool("assign_material", {
    "object_name": "building",
    "material_name": "glass_material"
})

# 4. Setup camera and lighting
await client.call_tool("create_camera", {
    "name": "main_camera",
    "location": [15, -15, 10],
    "rotation": [1.1, 0, 0.8]
})

await client.call_tool("setup_lighting", {
    "lighting_type": "THREE_POINT",
    "intensity": 2.0
})

# 5. Render final scene
await client.call_tool("render_scene", {
    "output_path": "/tmp/final_render.png",
    "resolution_x": 1920,
    "resolution_y": 1080,
    "samples": 512
})
```

---

## 🔗 Related Documentation

- [Quick Start Guide](../README.md#quick-start)
- [Configuration Guide](../README.md#configuration)
- [Troubleshooting](../README.md#troubleshooting)
- [Examples](../examples/usage_examples.py)

---

**Generated by MiniMax Agent** | **Last Updated: 2025-10-31**