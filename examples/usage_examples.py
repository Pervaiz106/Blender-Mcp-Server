#!/usr/bin/env python3
"""
Comprehensive Blender MCP Server Usage Examples

This file demonstrates how to use all 47+ tools available in the Blender MCP server
across different categories: scene management, object operations, materials, mesh operations,
animation, rendering, file I/O, and camera/lighting systems.
"""

import asyncio
import json
from fastmcp import Client
from src.blender_mcp_server.server import mcp


async def example_scene_management():
    """Example usage of scene management tools"""
    print("\n🏗️  SCENE MANAGEMENT EXAMPLES")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Create a new scene
        print("Creating a new scene...")
        result = await client.call_tool("create_scene", {"name": "Example Scene"})
        print(f"Result: {result.text}")
        
        # Set scene properties
        print("\nSetting scene properties...")
        result = await client.call_tool("set_scene_properties", {
            "frame_start": 1,
            "frame_end": 300,
            "frame_current": 1,
            "units": "metric"
        })
        print(f"Result: {result.text}")
        
        # Set world properties
        print("\nSetting world environment...")
        result = await client.call_tool("set_world_properties", {
            "color": [0.1, 0.1, 0.15],
            "background_type": "WORLD"
        })
        print(f"Result: {result.text}")
        
        # Get scene information
        print("\nGetting scene information...")
        result = await client.call_tool("get_scene_info", {})
        scene_info = json.loads(result.text)
        print(f"Scene has {scene_info.get('object_count', 0)} objects")


async def example_object_operations():
    """Example usage of object operations tools"""
    print("\n📦 OBJECT OPERATIONS EXAMPLES")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Create various objects
        objects = [
            ("CUBE", "BuildingBlock", [0, 0, 0]),
            ("SPHERE", "Planet", [3, 0, 1]),
            ("CYLINDER", "Tower", [-3, 0, 0]),
            ("CONE", "Mountain", [0, 3, 0])
        ]
        
        for obj_type, name, location in objects:
            print(f"Creating {obj_type} object '{name}'...")
            result = await client.call_tool("create_object", {
                "object_type": obj_type,
                "name": name,
                "location": location
            })
            print(f"Result: {result.text}")
        
        # Transform objects
        print("\nTransforming objects...")
        result = await client.call_tool("transform_object", {
            "object_name": "BuildingBlock",
            "location": [2, 2, 0],
            "rotation": [0, 0, 1.57],
            "scale": [1.5, 1.5, 1.5]
        })
        print(f"Result: {result.text}")
        
        # Create parent-child relationships
        print("\nCreating object hierarchy...")
        result = await client.call_tool("parent_object", {
            "child_name": "Planet",
            "parent_name": "BuildingBlock",
            "keep_transform": True
        })
        print(f"Result: {result.text}")
        
        # Get object information
        print("\nGetting object information...")
        result = await client.call_tool("get_object_info", {"object_name": "BuildingBlock"})
        print(f"BuildingBlock info: {result.text[:200]}...")


async def example_material_management():
    """Example usage of material management tools"""
    print("\n🎨 MATERIAL MANAGEMENT EXAMPLES")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Create different materials
        materials = [
            {
                "name": "BrickMaterial",
                "material_type": "BSDF_PRINCIPLED",
                "base_color": [0.8, 0.3, 0.2],
                "metallic": 0.1,
                "roughness": 0.8
            },
            {
                "name": "MetalMaterial",
                "material_type": "BSDF_PRINCIPLED",
                "base_color": [0.9, 0.9, 0.9],
                "metallic": 1.0,
                "roughness": 0.2
            },
            {
                "name": "PlasticMaterial",
                "material_type": "BSDF_PRINCIPLED",
                "base_color": [0.2, 0.6, 0.8],
                "metallic": 0.0,
                "roughness": 0.3
            }
        ]
        
        for material in materials:
            print(f"Creating material '{material['name']}'...")
            result = await client.call_tool("create_material", material)
            print(f"Result: {result.text}")
        
        # Assign materials to objects
        assignments = [
            ("BuildingBlock", "BrickMaterial"),
            ("Tower", "MetalMaterial"),
            ("Mountain", "PlasticMaterial")
        ]
        
        print("\nAssigning materials to objects...")
        for obj_name, material_name in assignments:
            result = await client.call_tool("assign_material", {
                "object_name": obj_name,
                "material_name": material_name
            })
            print(f"Result: {result.text}")
        
        # List all materials
        print("\nListing all materials...")
        result = await client.call_tool("list_materials", {})
        print(f"Materials in scene: {result.text}")


async def example_mesh_operations():
    """Example usage of mesh operations tools"""
    print("\n🔧 MESH OPERATIONS EXAMPLES")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Add modifiers to objects
        modifiers = [
            {
                "object_name": "BuildingBlock",
                "modifier_name": "SubsurfModifier",
                "modifier_type": "SUBSURF",
                "levels": 2
            },
            {
                "object_name": "Planet",
                "modifier_name": "SubsurfModifier",
                "modifier_type": "SUBSURF",
                "levels": 3
            }
        ]
        
        for modifier in modifiers:
            print(f"Adding {modifier['modifier_type']} modifier to {modifier['object_name']}...")
            result = await client.call_tool("add_modifier", modifier)
            print(f"Result: {result.text}")
        
        # Perform mesh editing operations
        print("\nPerforming mesh editing operations...")
        result = await client.call_tool("edit_mesh", {
            "object_name": "Mountain",
            "operation": "SUBDIVIDE",
            "levels": 1
        })
        print(f"Result: {result.text}")
        
        # Get mesh information
        print("\nGetting mesh information...")
        result = await client.call_tool("get_mesh_info", {"object_name": "BuildingBlock"})
        mesh_info = json.loads(result.text)
        print(f"BuildingBlock has {mesh_info.get('vertex_count', 'unknown')} vertices")


async def example_animation():
    """Example usage of animation tools"""
    print("\n🎬 ANIMATION EXAMPLES")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Create animation for the planet orbiting the building block
        print("Creating orbital animation for Planet...")
        keyframes = [
            {"frame": 1, "location": [3, 0, 1], "interpolation": "BEZIER"},
            {"frame": 75, "location": [0, 3, 1], "interpolation": "BEZIER"},
            {"frame": 150, "location": [-3, 0, 1], "interpolation": "BEZIER"},
            {"frame": 225, "location": [0, -3, 1], "interpolation": "BEZIER"},
            {"frame": 300, "location": [3, 0, 1], "interpolation": "BEZIER"}
        ]
        
        result = await client.call_tool("create_animation", {
            "object_name": "Planet",
            "animation_type": "LOCATION",
            "keyframes": keyframes
        })
        print(f"Result: {result.text}")
        
        # Set additional keyframes for rotation
        print("\nSetting rotation keyframes...")
        result = await client.call_tool("set_keyframes", {
            "object_name": "BuildingBlock",
            "frame": 150,
            "rotation": [0, 0, 3.14]
        })
        print(f"Result: {result.text}")
        
        # Get animation information
        print("\nGetting animation information...")
        result = await client.call_tool("get_animation_info", {"object_name": "Planet"})
        print(f"Planet animation info: {result.text[:300]}...")
        
        # Play animation
        print("\nPlaying animation...")
        result = await client.call_tool("play_animation", {
            "frame_start": 1,
            "frame_end": 300
        })
        print(f"Result: {result.text}")


async def example_rendering():
    """Example usage of rendering tools"""
    print("\n🎨 RENDERING EXAMPLES")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Set render settings
        print("Setting render configuration...")
        result = await client.call_tool("set_render_settings", {
            "settings": {
                "engine": "CYCLES",
                "resolution_x": 1920,
                "resolution_y": 1080,
                "samples": 128,
                "use_denoising": True
            }
        })
        print(f"Result: {result.text}")
        
        # Create preview render
        print("\nCreating preview render...")
        result = await client.call_tool("preview_render", {"resolution": 800})
        print(f"Result: {result.text}")
        
        # Get render settings
        print("\nGetting current render settings...")
        result = await client.call_tool("get_render_settings", {})
        print(f"Current settings: {result.text[:200]}...")


async def example_file_operations():
    """Example usage of file I/O tools"""
    print("\n📁 FILE OPERATIONS EXAMPLES")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Save the scene
        print("Saving the scene...")
        result = await client.call_tool("save_scene", {
            "file_path": "/tmp/example_scene.blend",
            "overwrite": True
        })
        print(f"Result: {result.text}")
        
        # Export objects to different formats
        print("\nExporting objects...")
        
        # Export as GLTF
        result = await client.call_tool("export_file", {
            "object_names": ["BuildingBlock", "Planet"],
            "file_path": "/tmp/example_scene.gltf",
            "file_type": "GLTF"
        })
        print(f"GLTF export result: {result.text}")
        
        # Export as OBJ
        result = await client.call_tool("export_file", {
            "object_names": ["Tower", "Mountain"],
            "file_path": "/tmp/terrain.obj",
            "file_type": "OBJ"
        })
        print(f"OBJ export result: {result.text}")


async def example_camera_lighting():
    """Example usage of camera and lighting tools"""
    print("\n📷 CAMERA & LIGHTING EXAMPLES")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Create cameras
        print("Creating cameras...")
        cameras = [
            {
                "name": "MainCamera",
                "location": [10, -10, 8],
                "rotation": [1.2, 0, 0.785],
                "fov": 60.0
            },
            {
                "name": "TopCamera",
                "location": [0, 0, 15],
                "rotation": [0, 0, 0],
                "fov": 45.0
            }
        ]
        
        for camera in cameras:
            result = await client.call_tool("create_camera", camera)
            print(f"Camera '{camera['name']}' created: {result.text}")
        
        # Set active camera
        print("\nSetting active camera...")
        result = await client.call_tool("set_active_camera", {
            "camera_name": "MainCamera"
        })
        print(f"Result: {result.text}")
        
        # Setup lighting
        print("\nSetting up lighting...")
        result = await client.call_tool("setup_lighting", {
            "lighting_type": "THREE_POINT"
        })
        print(f"Result: {result.text}")
        
        # Create additional lights
        print("\nCreating additional lights...")
        result = await client.call_tool("create_light", {
            "light_type": "SUN",
            "name": "KeyLight",
            "location": [10, -10, 10],
            "energy": 2000.0,
            "color": [1.0, 0.95, 0.9]
        })
        print(f"Result: {result.text}")
        
        result = await client.call_tool("create_light", {
            "light_type": "AREA",
            "name": "FillLight",
            "location": [-5, 5, 5],
            "energy": 500.0,
            "color": [0.8, 0.9, 1.0]
        })
        print(f"Result: {result.text}")


async def example_utility_functions():
    """Example usage of utility and debugging tools"""
    print("\n🔧 UTILITY FUNCTIONS")
    print("-" * 40)
    
    async with Client(mcp) as client:
        # Get server status
        print("Getting server status...")
        result = await client.call_tool("get_server_status", {})
        print(f"Server status: {result.text[:300]}...")
        
        # Execute custom Blender code
        print("\nExecuting custom Blender code...")
        code = '''
# Custom Blender code example
import bpy
print("Current frame:", bpy.context.scene.frame_current)
print("Object count:", len(bpy.data.objects))
'''
        result = await client.call_tool("execute_blender_code", {"code": code})
        print(f"Code execution result: {result.text}")


async def example_complete_workflow():
    """Example of a complete 3D scene creation workflow"""
    print("\n🚀 COMPLETE WORKFLOW EXAMPLE")
    print("=" * 50)
    print("Creating a complete 3D scene from scratch...")
    
    async with Client(mcp) as client:
        # Step 1: Setup scene
        print("\n1. Setting up scene...")
        await client.call_tool("create_scene", {"name": "Complete Scene"})
        await client.call_tool("set_scene_properties", {
            "frame_start": 1,
            "frame_end": 500,
            "frame_current": 1,
            "units": "metric"
        })
        
        # Step 2: Create environment
        print("\n2. Creating environment...")
        await client.call_tool("set_world_properties", {
            "color": [0.05, 0.1, 0.15],
            "background_type": "WORLD"
        })
        
        # Step 3: Create objects
        print("\n3. Creating 3D objects...")
        objects = [
            ("CUBE", "Ground", [0, 0, -1]),
            ("SPHERE", "Sun", [0, 0, 10]),
            ("CYLINDER", "Tree", [5, 3, 0]),
            ("CONE", "Pyramid", [-5, -3, 0])
        ]
        
        for obj_type, name, location in objects:
            await client.call_tool("create_object", {
                "object_type": obj_type,
                "name": name,
                "location": location
            })
        
        # Step 4: Create materials
        print("\n4. Creating materials...")
        materials = [
            {
                "name": "GroundMat",
                "material_type": "BSDF_PRINCIPLED",
                "base_color": [0.3, 0.8, 0.2],
                "roughness": 0.8
            },
            {
                "name": "SunMat",
                "material_type": "BSDF_PRINCIPLED",
                "base_color": [1.0, 0.9, 0.5],
                "emission": 5.0
            },
            {
                "name": "TreeMat",
                "material_type": "BSDF_PRINCIPLED",
                "base_color": [0.4, 0.2, 0.1],
                "roughness": 0.7
            },
            {
                "name": "PyramidMat",
                "material_type": "BSDF_PRINCIPLED",
                "base_color": [0.8, 0.6, 0.3],
                "metallic": 0.3,
                "roughness": 0.5
            }
        ]
        
        for material in materials:
            await client.call_tool("create_material", material)
        
        # Step 5: Assign materials
        print("\n5. Assigning materials...")
        assignments = [
            ("Ground", "GroundMat"),
            ("Sun", "SunMat"),
            ("Tree", "TreeMat"),
            ("Pyramid", "PyramidMat")
        ]
        
        for obj_name, mat_name in assignments:
            await client.call_tool("assign_material", {
                "object_name": obj_name,
                "material_name": mat_name
            })
        
        # Step 6: Add modifiers
        print("\n6. Adding mesh modifiers...")
        await client.call_tool("add_modifier", {
            "object_name": "Tree",
            "modifier_name": "Subsurf",
            "modifier_type": "SUBSURF",
            "levels": 2
        })
        
        await client.call_tool("add_modifier", {
            "object_name": "Ground",
            "modifier_name": "Subsurf",
            "modifier_type": "SUBSURF",
            "levels": 1
        })
        
        # Step 7: Setup lighting and camera
        print("\n7. Setting up lighting and camera...")
        await client.call_tool("setup_lighting", {
            "lighting_type": "THREE_POINT"
        })
        
        await client.call_tool("create_camera", {
            "name": "SceneCamera",
            "location": [8, -8, 6],
            "rotation": [1.1, 0, 0.785],
            "fov": 60.0
        })
        
        await client.call_tool("set_active_camera", {
            "camera_name": "SceneCamera"
        })
        
        # Step 8: Create simple animation
        print("\n8. Creating animation...")
        await client.call_tool("set_keyframes", {
            "object_name": "Sun",
            "frame": 1,
            "location": [0, 0, 10]
        })
        
        await client.call_tool("set_keyframes", {
            "object_name": "Sun",
            "frame": 250,
            "location": [0, 0, 15]
        })
        
        # Step 9: Render preview
        print("\n9. Creating preview render...")
        await client.call_tool("set_render_settings", {
            "settings": {
                "engine": "CYCLES",
                "resolution_x": 1280,
                "resolution_y": 720,
                "samples": 64
            }
        })
        
        await client.call_tool("preview_render", {"resolution": 800})
        
        # Step 10: Save scene
        print("\n10. Saving complete scene...")
        await client.call_tool("save_scene", {
            "file_path": "/tmp/complete_scene.blend",
            "overwrite": True
        })
        
        print("\n✅ Complete workflow finished successfully!")
        print("A full 3D scene has been created with:")
        print("- 4 geometric objects")
        print("- 4 custom materials")
        print("- Mesh modifiers")
        print("- Lighting setup")
        print("- Camera configuration")
        print("- Simple animation")
        print("- Preview render")
        print("- Saved .blend file")


async def main():
    """Run all examples"""
    print("🎭 Blender MCP Comprehensive Server - Usage Examples")
    print("=" * 60)
    
    try:
        # Run individual category examples
        await example_scene_management()
        await example_object_operations()
        await example_material_management()
        await example_mesh_operations()
        await example_animation()
        await example_rendering()
        await example_file_operations()
        await example_camera_lighting()
        await example_utility_functions()
        
        # Run complete workflow
        await example_complete_workflow()
        
        print("\n🎉 All examples completed successfully!")
        print("The Blender MCP server provides comprehensive 3D modeling capabilities")
        print("through an intuitive, AI-friendly interface.")
        
    except Exception as e:
        print(f"\n❌ Example failed: {str(e)}")
        print("Note: This is expected if Blender is not running or not connected.")
        print("The server is ready to work once the Blender addon is active.")


if __name__ == "__main__":
    # Run all examples
    asyncio.run(main())