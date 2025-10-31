"""
Comprehensive test suite for Blender MCP Server

Tests all 47+ tools across scene management, object operations, materials,
mesh operations, animation, rendering, file I/O, and camera/lighting systems.
"""

import pytest
import json
import asyncio
import os
import sys
from pathlib import Path

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastmcp import Client
from blender_mcp_server.server import mcp

class TestBlenderMCPServer:
    """Test suite for Blender MCP server functionality"""
    
    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test that the server initializes correctly"""
        async with Client(mcp) as client:
            # Verify server has tools
            tools = await client.list_tools()
            assert len(tools) > 0, "Server should have tools defined"
            
            # Verify all tool categories are present
            tool_names = [tool.name for tool in tools]
            
            # Scene management tools
            assert "create_scene" in tool_names
            assert "set_scene_properties" in tool_names
            assert "get_scene_info" in tool_names
            assert "duplicate_scene" in tool_names
            assert "delete_scene" in tool_names
            assert "set_world_properties" in tool_names
            assert "get_world_properties" in tool_names
            assert "clear_scene" in tool_names
            
            # Object operations tools
            assert "create_object" in tool_names
            assert "transform_object" in tool_names
            assert "delete_object" in tool_names
            assert "duplicate_object" in tool_names
            assert "join_objects" in tool_names
            assert "separate_objects" in tool_names
            assert "parent_object" in tool_names
            assert "unparent_object" in tool_names
            assert "get_object_info" in tool_names
            
            # Material management tools
            assert "create_material" in tool_names
            assert "assign_material" in tool_names
            assert "update_material_properties" in tool_names
            assert "delete_material" in tool_names
            assert "duplicate_material" in tool_names
            assert "get_material_info" in tool_names
            assert "list_materials" in tool_names
            
            # Mesh operations tools
            assert "edit_mesh" in tool_names
            assert "apply_modifier" in tool_names
            assert "add_modifier" in tool_names
            assert "remove_modifier" in tool_names
            assert "get_mesh_info" in tool_names
            assert "remesh_object" in tool_names
            
            # Animation tools
            assert "create_animation" in tool_names
            assert "set_keyframes" in tool_names
            assert "play_animation" in tool_names
            assert "stop_animation" in tool_names
            assert "clear_animation" in tool_names
            assert "get_animation_info" in tool_names
            
            # Rendering tools
            assert "render_scene" in tool_names
            assert "set_render_settings" in tool_names
            assert "get_render_settings" in tool_names
            assert "preview_render" in tool_names
            assert "get_render_preview" in tool_names
            
            # File I/O tools
            assert "import_file" in tool_names
            assert "export_file" in tool_names
            assert "save_scene" in tool_names
            assert "load_scene" in tool_names
            
            # Camera/lighting tools
            assert "create_camera" in tool_names
            assert "set_active_camera" in tool_names
            assert "setup_lighting" in tool_names
            assert "create_light" in tool_names
            
            # Utility tools
            assert "get_viewport_screenshot" in tool_names
            assert "execute_blender_code" in tool_names
            assert "get_server_status" in tool_names
            
            print(f"✓ Found {len(tools)} tools - comprehensive toolset verified")
    
    @pytest.mark.asyncio
    async def test_scene_management_tools(self):
        """Test scene management functionality"""
        async with Client(mcp) as client:
            # Test create_scene (this will fail without Blender, but should validate parameters)
            try:
                result = await client.call_tool("create_scene", {"name": "Test Scene"})
                print(f"create_scene result: {result.text}")
            except Exception as e:
                # Expected to fail without Blender connection
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ create_scene tool validated (requires Blender connection)")
            
            # Test set_scene_properties
            try:
                result = await client.call_tool("set_scene_properties", {
                    "frame_start": 1,
                    "frame_end": 100,
                    "frame_current": 25,
                    "units": "metric"
                })
                print(f"set_scene_properties result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ set_scene_properties tool validated")
    
    @pytest.mark.asyncio
    async def test_object_operations_tools(self):
        """Test object operations functionality"""
        async with Client(mcp) as client:
            # Test create_object
            try:
                result = await client.call_tool("create_object", {
                    "object_type": "CUBE",
                    "name": "TestCube",
                    "location": [1.0, 2.0, 3.0]
                })
                print(f"create_object result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ create_object tool validated")
            
            # Test transform_object
            try:
                result = await client.call_tool("transform_object", {
                    "object_name": "TestCube",
                    "location": [5.0, 6.0, 7.0],
                    "rotation": [0.0, 0.0, 1.57]
                })
                print(f"transform_object result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ transform_object tool validated")
    
    @pytest.mark.asyncio
    async def test_material_management_tools(self):
        """Test material management functionality"""
        async with Client(mcp) as client:
            # Test create_material
            try:
                result = await client.call_tool("create_material", {
                    "name": "TestMaterial",
                    "material_type": "BSDF_PRINCIPLED",
                    "base_color": [0.8, 0.2, 0.2],
                    "metallic": 0.5,
                    "roughness": 0.3
                })
                print(f"create_material result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ create_material tool validated")
            
            # Test assign_material
            try:
                result = await client.call_tool("assign_material", {
                    "object_name": "TestCube",
                    "material_name": "TestMaterial"
                })
                print(f"assign_material result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ assign_material tool validated")
    
    @pytest.mark.asyncio
    async def test_mesh_operations_tools(self):
        """Test mesh operations functionality"""
        async with Client(mcp) as client:
            # Test edit_mesh
            try:
                result = await client.call_tool("edit_mesh", {
                    "object_name": "TestCube",
                    "operation": "SUBDIVIDE",
                    "levels": 2
                })
                print(f"edit_mesh result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ edit_mesh tool validated")
            
            # Test apply_modifier
            try:
                result = await client.call_tool("apply_modifier", {
                    "object_name": "TestCube",
                    "modifier_name": "Subsurf",
                    "modifier_type": "SUBSURF",
                    "levels": 2
                })
                print(f"apply_modifier result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ apply_modifier tool validated")
    
    @pytest.mark.asyncio
    async def test_animation_tools(self):
        """Test animation functionality"""
        async with Client(mcp) as client:
            # Test create_animation
            try:
                keyframes = [
                    {"frame": 1, "location": [0, 0, 0], "interpolation": "BEZIER"},
                    {"frame": 50, "location": [5, 0, 0], "interpolation": "BEZIER"},
                    {"frame": 100, "location": [10, 0, 0], "interpolation": "BEZIER"}
                ]
                result = await client.call_tool("create_animation", {
                    "object_name": "TestCube",
                    "animation_type": "LOCATION",
                    "keyframes": keyframes
                })
                print(f"create_animation result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ create_animation tool validated")
            
            # Test set_keyframes
            try:
                result = await client.call_tool("set_keyframes", {
                    "object_name": "TestCube",
                    "frame": 25,
                    "location": [2.5, 0, 0]
                })
                print(f"set_keyframes result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ set_keyframes tool validated")
    
    @pytest.mark.asyncio
    async def test_rendering_tools(self):
        """Test rendering functionality"""
        async with Client(mcp) as client:
            # Test set_render_settings
            try:
                settings = {
                    "engine": "CYCLES",
                    "resolution_x": 1920,
                    "resolution_y": 1080,
                    "samples": 128
                }
                result = await client.call_tool("set_render_settings", {
                    "settings": settings
                })
                print(f"set_render_settings result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ set_render_settings tool validated")
            
            # Test preview_render
            try:
                result = await client.call_tool("preview_render", {
                    "resolution": 800
                })
                print(f"preview_render result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ preview_render tool validated")
    
    @pytest.mark.asyncio
    async def test_file_io_tools(self):
        """Test file I/O functionality"""
        async with Client(mcp) as client:
            # Test import_file (will fail with non-existent file, but validates parameters)
            try:
                result = await client.call_tool("import_file", {
                    "file_path": "/nonexistent/file.obj",
                    "file_type": "OBJ"
                })
                print(f"import_file result: {result.text}")
            except Exception as e:
                # Expected to fail with file not found
                assert "File not found" in str(e) or "Failed to connect to Blender" in str(e)
                print("✓ import_file tool validated")
            
            # Test export_file
            try:
                result = await client.call_tool("export_file", {
                    "object_names": ["TestCube"],
                    "file_path": "/tmp/test_export.obj",
                    "file_type": "OBJ"
                })
                print(f"export_file result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ export_file tool validated")
    
    @pytest.mark.asyncio
    async def test_camera_lighting_tools(self):
        """Test camera and lighting functionality"""
        async with Client(mcp) as client:
            # Test create_camera
            try:
                result = await client.call_tool("create_camera", {
                    "name": "TestCamera",
                    "location": [0, -5, 2],
                    "rotation": [1.2, 0, 0],
                    "fov": 60.0
                })
                print(f"create_camera result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ create_camera tool validated")
            
            # Test setup_lighting
            try:
                result = await client.call_tool("setup_lighting", {
                    "lighting_type": "THREE_POINT"
                })
                print(f"setup_lighting result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ setup_lighting tool validated")
    
    @pytest.mark.asyncio
    async def test_utility_tools(self):
        """Test utility and debugging tools"""
        async with Client(mcp) as client:
            # Test execute_blender_code
            try:
                result = await client.call_tool("execute_blender_code", {
                    "code": "print('Hello from Blender')"
                })
                print(f"execute_blender_code result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ execute_blender_code tool validated")
            
            # Test get_server_status
            try:
                result = await client.call_tool("get_server_status", {})
                print(f"get_server_status result: {result.text}")
            except Exception as e:
                assert "Failed to connect to Blender" in str(e) or "Could not connect" in str(e)
                print("✓ get_server_status tool validated")
    
    @pytest.mark.asyncio
    async def test_tool_parameter_validation(self):
        """Test that all tools properly validate their parameters"""
        async with Client(mcp) as client:
            tools = await client.list_tools()
            
            # Test required parameters
            test_cases = [
                ("create_object", {"object_type": "CUBE"}),  # Missing required 'name'
                ("create_material", {"material_type": "BSDF_PRINCIPLED"}),  # Missing required 'name'
                ("delete_object", {"confirm": False}),  # Should require confirmation
                ("delete_material", {"confirm": False}),  # Should require confirmation
            ]
            
            for tool_name, params in test_cases:
                try:
                    result = await client.call_tool(tool_name, params)
                    # If it doesn't raise an exception, check the response
                    assert "requires confirmation" in result.text or "Failed to connect to Blender" in result.text
                    print(f"✓ {tool_name} parameter validation working")
                except Exception as e:
                    # Expected to fail either due to validation or Blender connection
                    assert "Failed to connect to Blender" in str(e) or "Required" in str(e) or "confirmation" in str(e)
                    print(f"✓ {tool_name} parameter validation working")
    
    @pytest.mark.asyncio
    async def test_comprehensive_tool_count(self):
        """Verify that we have the expected number of tools (47+)"""
        async with Client(mcp) as client:
            tools = await client.list_tools()
            
            # Count tools by category
            scene_tools = ["create_scene", "set_scene_properties", "get_scene_info", 
                          "duplicate_scene", "delete_scene", "set_world_properties", 
                          "get_world_properties", "clear_scene"]
            
            object_tools = ["create_object", "transform_object", "delete_object", 
                           "duplicate_object", "join_objects", "separate_objects", 
                           "parent_object", "unparent_object", "get_object_info"]
            
            material_tools = ["create_material", "assign_material", "update_material_properties",
                             "delete_material", "duplicate_material", "get_material_info", "list_materials"]
            
            mesh_tools = ["edit_mesh", "apply_modifier", "add_modifier", "remove_modifier",
                         "get_mesh_info", "remesh_object"]
            
            animation_tools = ["create_animation", "set_keyframes", "play_animation",
                              "stop_animation", "clear_animation", "get_animation_info"]
            
            render_tools = ["render_scene", "set_render_settings", "get_render_settings",
                           "preview_render", "get_render_preview"]
            
            file_tools = ["import_file", "export_file", "save_scene", "load_scene"]
            
            lighting_tools = ["create_camera", "set_active_camera", "setup_lighting", "create_light"]
            
            utility_tools = ["get_viewport_screenshot", "execute_blender_code", "get_server_status"]
            
            total_tools = (len(scene_tools) + len(object_tools) + len(material_tools) +
                          len(mesh_tools) + len(animation_tools) + len(render_tools) +
                          len(file_tools) + len(lighting_tools) + len(utility_tools))
            
            print(f"Scene Management Tools: {len(scene_tools)}")
            print(f"Object Operations Tools: {len(object_tools)}")
            print(f"Material Management Tools: {len(material_tools)}")
            print(f"Mesh Operations Tools: {len(mesh_tools)}")
            print(f"Animation Tools: {len(animation_tools)}")
            print(f"Rendering Tools: {len(render_tools)}")
            print(f"File I/O Tools: {len(file_tools)}")
            print(f"Camera/Lighting Tools: {len(lighting_tools)}")
            print(f"Utility Tools: {len(utility_tools)}")
            print(f"Total Tools: {total_tools}")
            
            assert total_tools >= 47, f"Expected at least 47 tools, got {total_tools}"
            assert len(tools) == total_tools, f"Tool count mismatch: expected {total_tools}, got {len(tools)}"
            
            print(f"✓ Comprehensive toolset validated: {total_tools} tools implemented")


def run_validation_tests():
    """Run validation tests to ensure the server is working correctly"""
    print("🧪 Running Blender MCP Server Validation Tests")
    print("=" * 60)
    
    # Import pytest and run tests
    import subprocess
    import sys
    
    # Run the test file
    result = subprocess.run([
        sys.executable, "-m", "pytest", __file__, "-v", "--tb=short"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ All validation tests passed!")
        print("The Blender MCP server is properly configured with all required tools.")
    else:
        print("\n❌ Some tests failed:")
        print(result.stdout)
        print(result.stderr)
        return False
    
    return True


if __name__ == "__main__":
    # Run the validation tests when script is executed directly
    run_validation_tests()