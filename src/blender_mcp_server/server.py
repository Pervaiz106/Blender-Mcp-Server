"""
Comprehensive Blender MCP Server

A production-ready MCP server providing 47+ tools for Blender integration
covering scene management, object operations, materials, mesh operations,
animation, rendering, file I/O, camera and lighting systems.
"""

import asyncio
import json
import logging
import os
import socket
import tempfile
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, AsyncIterator, Union

import bpy
from fastmcp import FastMCP, Context, Image
from pydantic import BaseModel, Field
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("BlenderMCPServer")

# Configuration constants
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9876
BLENDER_SOCKET_TIMEOUT = 30.0

# Pydantic models for type safety
class SceneInfo(BaseModel):
    """Model for scene information"""
    name: str
    frame_start: int
    frame_end: int
    frame_current: int
    object_count: int
    collection_count: int
    material_count: int
    scene_units: Dict[str, Any]
    render_settings: Dict[str, Any]

class ObjectInfo(BaseModel):
    """Model for object information"""
    name: str
    type: str
    location: List[float]
    rotation: List[float]
    scale: List[float]
    visible: bool
    material_slots: List[str]
    parent: Optional[str] = None
    children: List[str] = []
    mesh_info: Optional[Dict[str, Any]] = None
    animation_data: Optional[Dict[str, Any]] = None

class MaterialInfo(BaseModel):
    """Model for material information"""
    name: str
    type: str
    nodes: List[Dict[str, Any]]
    textures: List[str]
    viewport_color: List[float]
    material_output: str

class CameraInfo(BaseModel):
    """Model for camera information"""
    name: str
    location: List[float]
    rotation: List[float]
    fov: float
    lens: float
    clip_start: float
    clip_end: float
    active: bool

class LightInfo(BaseModel):
    """Model for light information"""
    name: str
    type: str
    location: List[float]
    rotation: List[float]
    energy: float
    color: List[float]
    cast_shadows: bool

@dataclass
class BlenderConnection:
    """Handles connection to Blender addon via socket"""
    host: str
    port: int
    sock: Optional[socket.socket] = None
    
    def connect(self) -> bool:
        """Establish connection to Blender addon"""
        if self.sock:
            return True
            
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(BLENDER_SOCKET_TIMEOUT)
            self.sock.connect((self.host, self.port))
            logger.info(f"Connected to Blender at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Blender: {str(e)}")
            self.sock = None
            return False
    
    def disconnect(self):
        """Close connection to Blender addon"""
        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                logger.error(f"Error disconnecting from Blender: {str(e)}")
            finally:
                self.sock = None

    def send_command(self, command_type: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send command to Blender and get response"""
        if not self.sock and not self.connect():
            raise ConnectionError("Not connected to Blender")
        
        command = {
            "type": command_type,
            "params": params or {},
            "id": str(uuid.uuid4()),
            "timestamp": time.time()
        }
        
        try:
            # Send command
            message = json.dumps(command)
            self.sock.sendall(message.encode('utf-8'))
            
            # Receive response
            response_data = self._receive_response()
            response = json.loads(response_data.decode('utf-8'))
            
            if response.get("status") == "error":
                raise Exception(response.get("message", "Unknown error from Blender"))
            
            return response.get("result", {})
        
        except socket.timeout:
            logger.error("Socket timeout waiting for Blender response")
            self.sock = None
            raise Exception("Timeout waiting for Blender response")
        except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
            logger.error(f"Socket connection error: {str(e)}")
            self.sock = None
            raise Exception(f"Connection to Blender lost: {str(e)}")
        except Exception as e:
            logger.error(f"Error communicating with Blender: {str(e)}")
            self.sock = None
            raise Exception(f"Communication error with Blender: {str(e)}")

    def _receive_response(self, buffer_size: int = 8192) -> bytes:
        """Receive complete response from Blender"""
        chunks = []
        self.sock.settimeout(BLENDER_SOCKET_TIMEOUT)
        
        while True:
            try:
                chunk = self.sock.recv(buffer_size)
                if not chunk:
                    if not chunks:
                        raise Exception("Connection closed before receiving data")
                    break
                
                chunks.append(chunk)
                
                # Check if complete JSON received
                try:
                    data = b''.join(chunks)
                    json.loads(data.decode('utf-8'))
                    return data
                except json.JSONDecodeError:
                    continue
                    
            except socket.timeout:
                if chunks:
                    break
                raise
            
        if chunks:
            return b''.join(chunks)
        raise Exception("No data received")

# Global connection manager
_blender_connection = None

def get_blender_connection() -> BlenderConnection:
    """Get or create persistent Blender connection"""
    global _blender_connection
    
    if _blender_connection is not None:
        try:
            # Test connection
            _blender_connection.send_command("ping")
            return _blender_connection
        except Exception as e:
            logger.warning(f"Existing connection invalid: {str(e)}")
            try:
                _blender_connection.disconnect()
            except:
                pass
            _blender_connection = None
    
    # Create new connection
    if _blender_connection is None:
        host = os.getenv("BLENDER_HOST", DEFAULT_HOST)
        port = int(os.getenv("BLENDER_PORT", DEFAULT_PORT))
        _blender_connection = BlenderConnection(host=host, port=port)
        
        if not _blender_connection.connect():
            raise Exception("Could not connect to Blender. Make sure the Blender addon is running.")
        
        logger.info("Created new persistent connection to Blender")
    
    return _blender_connection

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage server startup and shutdown lifecycle"""
    try:
        logger.info("BlenderMCP Comprehensive server starting up")
        
        # Validate Blender connection on startup
        try:
            blender = get_blender_connection()
            blender.send_command("get_server_info")
            logger.info("Successfully validated Blender connection")
        except Exception as e:
            logger.warning(f"Blender connection validation failed: {str(e)}")
            logger.warning("Ensure Blender addon is running before using tools")
        
        yield {}
        
    finally:
        global _blender_connection
        if _blender_connection:
            logger.info("Disconnecting from Blender on shutdown")
            _blender_connection.disconnect()
            _blender_connection = None
        logger.info("BlenderMCP Comprehensive server shut down")

# Create MCP server
mcp = FastMCP(
    "BlenderMCP Comprehensive",
    lifespan=server_lifespan
)

# =============================================================================
# SCENE MANAGEMENT TOOLS (8 tools)
# =============================================================================

@mcp.tool
def create_scene(ctx: Context, name: str = "New Scene") -> str:
    """Create a new Blender scene with the specified name.
    
    Args:
        name: Name for the new scene
        
    Returns:
        Success message with scene details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("create_scene", {"name": name})
        
        if result.get("success"):
            return f"Scene '{name}' created successfully with {result.get('object_count', 0)} objects"
        else:
            return f"Failed to create scene: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error creating scene: {str(e)}")
        return f"Failed to create scene: {str(e)}"

@mcp.tool
def set_scene_properties(ctx: Context, frame_start: int = 1, frame_end: int = 250, 
                        frame_current: int = 1, units: str = "metric") -> str:
    """Set Blender scene properties including frame range and units.
    
    Args:
        frame_start: Starting frame number (default: 1)
        frame_end: Ending frame number (default: 250)
        frame_current: Current frame number (default: 1)
        units: Units system - 'metric', 'imperial', or 'none' (default: 'metric')
        
    Returns:
        Success message with updated properties
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("set_scene_properties", {
            "frame_start": frame_start,
            "frame_end": frame_end,
            "frame_current": frame_current,
            "units": units
        })
        
        return f"Scene properties updated: {result.get('message', 'Success')}"
    except Exception as e:
        logger.error(f"Error setting scene properties: {str(e)}")
        return f"Failed to set scene properties: {str(e)}"

@mcp.tool
def get_scene_info(ctx: Context) -> str:
    """Get comprehensive information about the current Blender scene.
    
    Returns:
        JSON-formatted scene information including objects, collections, materials, etc.
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_scene_info")
        
        # Convert to formatted JSON
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting scene info: {str(e)}")
        return f"Failed to get scene info: {str(e)}"

@mcp.tool
def duplicate_scene(ctx: Context, source_name: str, new_name: str) -> str:
    """Duplicate an existing scene with a new name.
    
    Args:
        source_name: Name of the scene to duplicate
        new_name: Name for the new duplicated scene
        
    Returns:
        Success message with duplication details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("duplicate_scene", {
            "source_name": source_name,
            "new_name": new_name
        })
        
        if result.get("success"):
            return f"Scene '{source_name}' duplicated as '{new_name}' with {result.get('object_count', 0)} objects"
        else:
            return f"Failed to duplicate scene: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error duplicating scene: {str(e)}")
        return f"Failed to duplicate scene: {str(e)}"

@mcp.tool
def delete_scene(ctx: Context, scene_name: str, confirm: bool = False) -> str:
    """Delete a scene by name.
    
    Args:
        scene_name: Name of the scene to delete
        confirm: Confirmation flag to prevent accidental deletion (must be True)
        
    Returns:
        Success or error message
    """
    try:
        if not confirm:
            return "Scene deletion requires confirmation=True parameter"
        
        blender = get_blender_connection()
        result = blender.send_command("delete_scene", {
            "scene_name": scene_name
        })
        
        if result.get("success"):
            return f"Scene '{scene_name}' deleted successfully"
        else:
            return f"Failed to delete scene: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error deleting scene: {str(e)}")
        return f"Failed to delete scene: {str(e)}"

@mcp.tool
def set_world_properties(ctx: Context, color: List[float] = [0.05, 0.05, 0.05], 
                        background_type: str = "WORLD") -> str:
    """Set world (environment) properties for the scene.
    
    Args:
        color: RGB color values (0.0 to 1.0) for world background
        background_type: Type of background - 'WORLD', 'SKY', 'HEMI', etc.
        
    Returns:
        Success message with updated world properties
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("set_world_properties", {
            "color": color,
            "background_type": background_type
        })
        
        return f"World properties updated: {result.get('message', 'Success')}"
    except Exception as e:
        logger.error(f"Error setting world properties: {str(e)}")
        return f"Failed to set world properties: {str(e)}"

@mcp.tool
def get_world_properties(ctx: Context) -> str:
    """Get current world (environment) properties.
    
    Returns:
        JSON-formatted world properties information
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_world_properties")
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting world properties: {str(e)}")
        return f"Failed to get world properties: {str(e)}"

@mcp.tool
def clear_scene(ctx: Context, confirm: bool = False) -> str:
    """Clear all objects from the current scene.
    
    Args:
        confirm: Confirmation flag to prevent accidental deletion (must be True)
        
    Returns:
        Success or error message
    """
    try:
        if not confirm:
            return "Scene clearing requires confirmation=True parameter"
        
        blender = get_blender_connection()
        result = blender.send_command("clear_scene")
        
        if result.get("success"):
            return f"Scene cleared successfully. {result.get('deleted_count', 0)} objects removed"
        else:
            return f"Failed to clear scene: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error clearing scene: {str(e)}")
        return f"Failed to clear scene: {str(e)}"

# =============================================================================
# OBJECT OPERATIONS TOOLS (9 tools)
# =============================================================================

@mcp.tool
def create_object(ctx: Context, object_type: str, name: str, location: List[float] = [0, 0, 0]) -> str:
    """Create a new object in the Blender scene.
    
    Args:
        object_type: Type of object - 'CUBE', 'SPHERE', 'CYLINDER', 'CONE', 'PLANE', etc.
        name: Name for the new object
        location: XYZ coordinates for object location (default: [0, 0, 0])
        
    Returns:
        Success message with object details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("create_object", {
            "object_type": object_type.upper(),
            "name": name,
            "location": location
        })
        
        if result.get("success"):
            return f"Object '{name}' created successfully at location {location}"
        else:
            return f"Failed to create object: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error creating object: {str(e)}")
        return f"Failed to create object: {str(e)}"

@mcp.tool
def transform_object(ctx: Context, object_name: str, location: List[float] = None,
                    rotation: List[float] = None, scale: List[float] = None) -> str:
    """Transform (move, rotate, scale) an existing object.
    
    Args:
        object_name: Name of the object to transform
        location: New XYZ coordinates (optional)
        rotation: New XYZ rotation in radians (optional)
        scale: New XYZ scale factors (optional)
        
    Returns:
        Success message with transformation details
    """
    try:
        blender = get_blender_connection()
        transform_data = {"object_name": object_name}
        
        if location is not None:
            transform_data["location"] = location
        if rotation is not None:
            transform_data["rotation"] = rotation
        if scale is not None:
            transform_data["scale"] = scale
        
        result = blender.send_command("transform_object", transform_data)
        
        return f"Object '{object_name}' transformed: {result.get('message', 'Success')}"
    except Exception as e:
        logger.error(f"Error transforming object: {str(e)}")
        return f"Failed to transform object: {str(e)}"

@mcp.tool
def delete_object(ctx: Context, object_name: str, confirm: bool = False) -> str:
    """Delete an object from the scene.
    
    Args:
        object_name: Name of the object to delete
        confirm: Confirmation flag to prevent accidental deletion (must be True)
        
    Returns:
        Success or error message
    """
    try:
        if not confirm:
            return "Object deletion requires confirmation=True parameter"
        
        blender = get_blender_connection()
        result = blender.send_command("delete_object", {
            "object_name": object_name
        })
        
        if result.get("success"):
            return f"Object '{object_name}' deleted successfully"
        else:
            return f"Failed to delete object: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error deleting object: {str(e)}")
        return f"Failed to delete object: {str(e)}"

@mcp.tool
def duplicate_object(ctx: Context, source_name: str, new_name: str = None) -> str:
    """Duplicate an existing object.
    
    Args:
        source_name: Name of the object to duplicate
        new_name: Name for the new duplicated object (optional)
        
    Returns:
        Success message with duplication details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("duplicate_object", {
            "source_name": source_name,
            "new_name": new_name
        })
        
        actual_name = new_name or f"{source_name}.001"
        if result.get("success"):
            return f"Object '{source_name}' duplicated as '{actual_name}'"
        else:
            return f"Failed to duplicate object: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error duplicating object: {str(e)}")
        return f"Failed to duplicate object: {str(e)}"

@mcp.tool
def join_objects(ctx: Context, object_names: List[str], joined_name: str) -> str:
    """Join multiple objects into a single object.
    
    Args:
        object_names: List of object names to join
        joined_name: Name for the resulting joined object
        
    Returns:
        Success message with join details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("join_objects", {
            "object_names": object_names,
            "joined_name": joined_name
        })
        
        if result.get("success"):
            return f"Objects {', '.join(object_names)} joined into '{joined_name}'"
        else:
            return f"Failed to join objects: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error joining objects: {str(e)}")
        return f"Failed to join objects: {str(e)}"

@mcp.tool
def separate_objects(ctx: Context, object_name: str, mode: str = "SELECTED") -> str:
    """Separate a mesh object into individual objects.
    
    Args:
        object_name: Name of the object to separate
        mode: Separation mode - 'SELECTED', 'MATERIAL', 'LOOSE' (default: 'SELECTED')
        
    Returns:
        Success message with separation details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("separate_objects", {
            "object_name": object_name,
            "mode": mode
        })
        
        if result.get("success"):
            separated_count = result.get("separated_count", 0)
            return f"Object '{object_name}' separated into {separated_count} objects"
        else:
            return f"Failed to separate objects: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error separating objects: {str(e)}")
        return f"Failed to separate objects: {str(e)}"

@mcp.tool
def parent_object(ctx: Context, child_name: str, parent_name: str, keep_transform: bool = True) -> str:
    """Set parent-child relationship between objects.
    
    Args:
        child_name: Name of the child object
        parent_name: Name of the parent object
        keep_transform: Whether to keep child's transform (default: True)
        
    Returns:
        Success message with parent-child relationship details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("parent_object", {
            "child_name": child_name,
            "parent_name": parent_name,
            "keep_transform": keep_transform
        })
        
        if result.get("success"):
            return f"Object '{child_name}' parented to '{parent_name}'"
        else:
            return f"Failed to parent object: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error parenting object: {str(e)}")
        return f"Failed to parent object: {str(e)}"

@mcp.tool
def unparent_object(ctx: Context, child_name: str, keep_transform: bool = True) -> str:
    """Remove parent-child relationship from an object.
    
    Args:
        child_name: Name of the child object
        keep_transform: Whether to keep child's transform (default: True)
        
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("unparent_object", {
            "child_name": child_name,
            "keep_transform": keep_transform
        })
        
        if result.get("success"):
            return f"Object '{child_name}' unparented successfully"
        else:
            return f"Failed to unparent object: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error unparenting object: {str(e)}")
        return f"Failed to unparent object: {str(e)}"

@mcp.tool
def get_object_info(ctx: Context, object_name: str) -> str:
    """Get detailed information about a specific object.
    
    Args:
        object_name: Name of the object to get information about
        
    Returns:
        JSON-formatted object information
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_object_info", {
            "object_name": object_name
        })
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting object info: {str(e)}")
        return f"Failed to get object info: {str(e)}"

# =============================================================================
# MATERIAL MANAGEMENT TOOLS (7 tools)
# =============================================================================

@mcp.tool
def create_material(ctx: Context, name: str, material_type: str = "BSDF_PRINCIPLED",
                   base_color: List[float] = [0.8, 0.8, 0.8], metallic: float = 0.0,
                   roughness: float = 0.5) -> str:
    """Create a new material with specified properties.
    
    Args:
        name: Name for the new material
        material_type: Type of material - 'BSDF_PRINCIPLED', 'BSDF_DIFFUSE', etc.
        base_color: RGB color values (0.0 to 1.0) for base color
        metallic: Metallic factor (0.0 to 1.0)
        roughness: Roughness factor (0.0 to 1.0)
        
    Returns:
        Success message with material details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("create_material", {
            "name": name,
            "material_type": material_type,
            "base_color": base_color,
            "metallic": metallic,
            "roughness": roughness
        })
        
        if result.get("success"):
            return f"Material '{name}' created successfully"
        else:
            return f"Failed to create material: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error creating material: {str(e)}")
        return f"Failed to create material: {str(e)}"

@mcp.tool
def assign_material(ctx: Context, object_name: str, material_name: str, material_slot: str = "") -> str:
    """Assign a material to an object.
    
    Args:
        object_name: Name of the object to assign material to
        material_name: Name of the material to assign
        material_slot: Specific material slot (optional)
        
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("assign_material", {
            "object_name": object_name,
            "material_name": material_name,
            "material_slot": material_slot
        })
        
        if result.get("success"):
            return f"Material '{material_name}' assigned to object '{object_name}'"
        else:
            return f"Failed to assign material: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error assigning material: {str(e)}")
        return f"Failed to assign material: {str(e)}"

@mcp.tool
def update_material_properties(ctx: Context, material_name: str, properties: Dict[str, Any]) -> str:
    """Update material properties.
    
    Args:
        material_name: Name of the material to update
        properties: Dictionary of properties to update
        
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("update_material_properties", {
            "material_name": material_name,
            "properties": properties
        })
        
        return f"Material '{material_name}' properties updated: {result.get('message', 'Success')}"
    except Exception as e:
        logger.error(f"Error updating material properties: {str(e)}")
        return f"Failed to update material properties: {str(e)}"

@mcp.tool
def delete_material(ctx: Context, material_name: str, confirm: bool = False) -> str:
    """Delete a material from the scene.
    
    Args:
        material_name: Name of the material to delete
        confirm: Confirmation flag to prevent accidental deletion (must be True)
        
    Returns:
        Success or error message
    """
    try:
        if not confirm:
            return "Material deletion requires confirmation=True parameter"
        
        blender = get_blender_connection()
        result = blender.send_command("delete_material", {
            "material_name": material_name
        })
        
        if result.get("success"):
            return f"Material '{material_name}' deleted successfully"
        else:
            return f"Failed to delete material: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error deleting material: {str(e)}")
        return f"Failed to delete material: {str(e)}"

@mcp.tool
def duplicate_material(ctx: Context, source_name: str, new_name: str) -> str:
    """Duplicate an existing material.
    
    Args:
        source_name: Name of the material to duplicate
        new_name: Name for the new duplicated material
        
    Returns:
        Success message with duplication details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("duplicate_material", {
            "source_name": source_name,
            "new_name": new_name
        })
        
        if result.get("success"):
            return f"Material '{source_name}' duplicated as '{new_name}'"
        else:
            return f"Failed to duplicate material: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error duplicating material: {str(e)}")
        return f"Failed to duplicate material: {str(e)}"

@mcp.tool
def get_material_info(ctx: Context, material_name: str) -> str:
    """Get detailed information about a material.
    
    Args:
        material_name: Name of the material to get information about
        
    Returns:
        JSON-formatted material information
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_material_info", {
            "material_name": material_name
        })
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting material info: {str(e)}")
        return f"Failed to get material info: {str(e)}"

@mcp.tool
def list_materials(ctx: Context) -> str:
    """List all materials in the current scene.
    
    Returns:
        Formatted list of all materials
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("list_materials")
        
        materials = result.get("materials", [])
        if materials:
            formatted_list = "Materials in scene:\n"
            for material in materials:
                formatted_list += f"- {material}\n"
            return formatted_list
        else:
            return "No materials found in scene"
    except Exception as e:
        logger.error(f"Error listing materials: {str(e)}")
        return f"Failed to list materials: {str(e)}"

# =============================================================================
# MESH OPERATIONS TOOLS (6 tools)
# =============================================================================

@mcp.tool
def edit_mesh(ctx: Context, object_name: str, operation: str, **kwargs) -> str:
    """Perform mesh editing operations on an object.
    
    Args:
        object_name: Name of the mesh object to edit
        operation: Type of mesh operation - 'SUBDIVIDE', 'BEVEL', 'EXTRUDE', 'INSET', etc.
        **kwargs: Additional parameters specific to the operation
        
    Returns:
        Success message with operation details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("edit_mesh", {
            "object_name": object_name,
            "operation": operation.upper(),
            **kwargs
        })
        
        if result.get("success"):
            return f"Mesh operation '{operation}' applied to '{object_name}': {result.get('message', 'Success')}"
        else:
            return f"Failed to perform mesh operation: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error editing mesh: {str(e)}")
        return f"Failed to edit mesh: {str(e)}"

@mcp.tool
def apply_modifier(ctx: Context, object_name: str, modifier_name: str, modifier_type: str,
                  **kwargs) -> str:
    """Apply a modifier to a mesh object.
    
    Args:
        object_name: Name of the object to apply modifier to
        modifier_name: Name for the modifier
        modifier_type: Type of modifier - 'SUBSURF', 'BEVEL', 'ARRAY', 'MIRROR', etc.
        **kwargs: Additional parameters for the modifier
        
    Returns:
        Success message with modifier details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("apply_modifier", {
            "object_name": object_name,
            "modifier_name": modifier_name,
            "modifier_type": modifier_type.upper(),
            **kwargs
        })
        
        if result.get("success"):
            return f"Modifier '{modifier_type}' applied to '{object_name}'"
        else:
            return f"Failed to apply modifier: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error applying modifier: {str(e)}")
        return f"Failed to apply modifier: {str(e)}"

@mcp.tool
def add_modifier(ctx: Context, object_name: str, modifier_name: str, modifier_type: str,
                **kwargs) -> str:
    """Add a modifier to a mesh object without applying it.
    
    Args:
        object_name: Name of the object to add modifier to
        modifier_name: Name for the modifier
        modifier_type: Type of modifier - 'SUBSURF', 'BEVEL', 'ARRAY', 'MIRROR', etc.
        **kwargs: Additional parameters for the modifier
        
    Returns:
        Success message with modifier details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("add_modifier", {
            "object_name": object_name,
            "modifier_name": modifier_name,
            "modifier_type": modifier_type.upper(),
            **kwargs
        })
        
        if result.get("success"):
            return f"Modifier '{modifier_type}' added to '{object_name}' as '{modifier_name}'"
        else:
            return f"Failed to add modifier: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error adding modifier: {str(e)}")
        return f"Failed to add modifier: {str(e)}"

@mcp.tool
def remove_modifier(ctx: Context, object_name: str, modifier_name: str, confirm: bool = False) -> str:
    """Remove a modifier from a mesh object.
    
    Args:
        object_name: Name of the object to remove modifier from
        modifier_name: Name of the modifier to remove
        confirm: Confirmation flag to prevent accidental removal (must be True)
        
    Returns:
        Success or error message
    """
    try:
        if not confirm:
            return "Modifier removal requires confirmation=True parameter"
        
        blender = get_blender_connection()
        result = blender.send_command("remove_modifier", {
            "object_name": object_name,
            "modifier_name": modifier_name
        })
        
        if result.get("success"):
            return f"Modifier '{modifier_name}' removed from '{object_name}'"
        else:
            return f"Failed to remove modifier: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error removing modifier: {str(e)}")
        return f"Failed to remove modifier: {str(e)}"

@mcp.tool
def get_mesh_info(ctx: Context, object_name: str) -> str:
    """Get detailed information about a mesh object.
    
    Args:
        object_name: Name of the mesh object to get information about
        
    Returns:
        JSON-formatted mesh information including vertices, edges, faces, etc.
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_mesh_info", {
            "object_name": object_name
        })
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting mesh info: {str(e)}")
        return f"Failed to get mesh info: {str(e)}"

@mcp.tool
def remesh_object(ctx: Context, object_name: str, mode: str = "VOXEL", voxel_size: float = 0.1) -> str:
    """Remesh an object using Blender's remesh modifier.
    
    Args:
        object_name: Name of the object to remesh
        mode: Remesh mode - 'VOXEL', 'BLOCKS', 'SMOOTH' (default: 'VOXEL')
        voxel_size: Size of voxels for voxel remeshing (default: 0.1)
        
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("remesh_object", {
            "object_name": object_name,
            "mode": mode.upper(),
            "voxel_size": voxel_size
        })
        
        if result.get("success"):
            return f"Object '{object_name}' remeshed using {mode} mode"
        else:
            return f"Failed to remesh object: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error remeshing object: {str(e)}")
        return f"Failed to remesh object: {str(e)}"

# =============================================================================
# ANIMATION SYSTEM TOOLS (6 tools)
# =============================================================================

@mcp.tool
def create_animation(ctx: Context, object_name: str, animation_type: str = "LOCATION",
                    keyframes: List[Dict[str, Any]] = None) -> str:
    """Create animation keyframes for an object.
    
    Args:
        object_name: Name of the object to animate
        animation_type: Type of animation - 'LOCATION', 'ROTATION', 'SCALE', 'ALL'
        keyframes: List of keyframe data with frame, value, and interpolation info
        
    Returns:
        Success message with animation details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("create_animation", {
            "object_name": object_name,
            "animation_type": animation_type.upper(),
            "keyframes": keyframes or []
        })
        
        if result.get("success"):
            keyframe_count = result.get("keyframe_count", 0)
            return f"Animation created for '{object_name}' with {keyframe_count} keyframes"
        else:
            return f"Failed to create animation: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error creating animation: {str(e)}")
        return f"Failed to create animation: {str(e)}"

@mcp.tool
def set_keyframes(ctx: Context, object_name: str, frame: int, location: List[float] = None,
                 rotation: List[float] = None, scale: List[float] = None) -> str:
    """Set keyframes for object transformation at specific frames.
    
    Args:
        object_name: Name of the object
        frame: Frame number for the keyframe
        location: XYZ location values (optional)
        rotation: XYZ rotation values in radians (optional)
        scale: XYZ scale values (optional)
        
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        keyframe_data = {
            "object_name": object_name,
            "frame": frame
        }
        
        if location is not None:
            keyframe_data["location"] = location
        if rotation is not None:
            keyframe_data["rotation"] = rotation
        if scale is not None:
            keyframe_data["scale"] = scale
        
        result = blender.send_command("set_keyframes", keyframe_data)
        
        return f"Keyframes set for '{object_name}' at frame {frame}: {result.get('message', 'Success')}"
    except Exception as e:
        logger.error(f"Error setting keyframes: {str(e)}")
        return f"Failed to set keyframes: {str(e)}"

@mcp.tool
def play_animation(ctx: Context, frame_start: int = 1, frame_end: int = 250) -> str:
    """Play animation in the viewport.
    
    Args:
        frame_start: Starting frame for playback
        frame_end: Ending frame for playback
        
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("play_animation", {
            "frame_start": frame_start,
            "frame_end": frame_end
        })
        
        return f"Animation playback started: {result.get('message', 'Success')}"
    except Exception as e:
        logger.error(f"Error playing animation: {str(e)}")
        return f"Failed to play animation: {str(e)}"

@mcp.tool
def stop_animation(ctx: Context) -> str:
    """Stop animation playback in the viewport.
    
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("stop_animation")
        
        return f"Animation stopped: {result.get('message', 'Success')}"
    except Exception as e:
        logger.error(f"Error stopping animation: {str(e)}")
        return f"Failed to stop animation: {str(e)}"

@mcp.tool
def clear_animation(ctx: Context, object_name: str, confirm: bool = False) -> str:
    """Clear all animation data from an object.
    
    Args:
        object_name: Name of the object to clear animation from
        confirm: Confirmation flag to prevent accidental deletion (must be True)
        
    Returns:
        Success or error message
    """
    try:
        if not confirm:
            return "Animation clearing requires confirmation=True parameter"
        
        blender = get_blender_connection()
        result = blender.send_command("clear_animation", {
            "object_name": object_name
        })
        
        if result.get("success"):
            return f"Animation cleared from '{object_name}'"
        else:
            return f"Failed to clear animation: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error clearing animation: {str(e)}")
        return f"Failed to clear animation: {str(e)}"

@mcp.tool
def get_animation_info(ctx: Context, object_name: str) -> str:
    """Get animation information for an object.
    
    Args:
        object_name: Name of the object to get animation info for
        
    Returns:
        JSON-formatted animation information
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_animation_info", {
            "object_name": object_name
        })
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting animation info: {str(e)}")
        return f"Failed to get animation info: {str(e)}"

# =============================================================================
# RENDERING PIPELINE TOOLS (5 tools)
# =============================================================================

@mcp.tool
def render_scene(ctx: Context, output_path: str = None, frame: int = None) -> str:
    """Render the current scene.
    
    Args:
        output_path: Output file path for the render (optional)
        frame: Specific frame to render (optional, renders current frame if None)
        
    Returns:
        Success message with render details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("render_scene", {
            "output_path": output_path,
            "frame": frame
        })
        
        if result.get("success"):
            render_time = result.get("render_time", "Unknown")
            return f"Scene rendered successfully in {render_time} seconds"
        else:
            return f"Failed to render scene: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error rendering scene: {str(e)}")
        return f"Failed to render scene: {str(e)}"

@mcp.tool
def set_render_settings(ctx: Context, settings: Dict[str, Any]) -> str:
    """Set render engine and quality settings.
    
    Args:
        settings: Dictionary of render settings to update
        
    Returns:
        Success message with updated settings
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("set_render_settings", {
            "settings": settings
        })
        
        return f"Render settings updated: {result.get('message', 'Success')}"
    except Exception as e:
        logger.error(f"Error setting render settings: {str(e)}")
        return f"Failed to set render settings: {str(e)}"

@mcp.tool
def get_render_settings(ctx: Context) -> str:
    """Get current render engine and quality settings.
    
    Returns:
        JSON-formatted render settings
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_render_settings")
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting render settings: {str(e)}")
        return f"Failed to get render settings: {str(e)}"

@mcp.tool
def preview_render(ctx: Context, resolution: int = 800) -> str:
    """Create a quick preview render at reduced resolution.
    
    Args:
        resolution: Maximum resolution for preview render (default: 800)
        
    Returns:
        Success message with preview details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("preview_render", {
            "resolution": resolution
        })
        
        if result.get("success"):
            return f"Preview render created at {resolution}x{resolution} resolution"
        else:
            return f"Failed to create preview render: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error creating preview render: {str(e)}")
        return f"Failed to create preview render: {str(e)}"

@mcp.tool
def get_render_preview(ctx: Context, max_size: int = 800) -> Image:
    """Get a preview render as an image.
    
    Args:
        max_size: Maximum size in pixels for the preview
        
    Returns:
        Preview render as Image object
    """
    try:
        blender = get_blender_connection()
        
        # Create temporary file for preview
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"blender_preview_{uuid.uuid4()}.png")
        
        result = blender.send_command("get_render_preview", {
            "max_size": max_size,
            "output_path": temp_path
        })
        
        if "error" in result:
            raise Exception(result["error"])
        
        if not os.path.exists(temp_path):
            raise Exception("Preview file was not created")
        
        # Read and return image
        with open(temp_path, 'rb') as f:
            image_bytes = f.read()
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except:
            pass
        
        return Image(data=image_bytes, format="png")
        
    except Exception as e:
        logger.error(f"Error getting render preview: {str(e)}")
        raise Exception(f"Failed to get render preview: {str(e)}")

# =============================================================================
# FILE I/O TOOLS (4 tools)
# =============================================================================

@mcp.tool
def import_file(ctx: Context, file_path: str, file_type: str = "AUTO") -> str:
    """Import a file into the Blender scene.
    
    Args:
        file_path: Path to the file to import
        file_type: File type - 'AUTO', 'OBJ', 'FBX', 'GLTF', 'STL', etc.
        
    Returns:
        Success message with import details
    """
    try:
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        blender = get_blender_connection()
        result = blender.send_command("import_file", {
            "file_path": file_path,
            "file_type": file_type.upper()
        })
        
        if result.get("success"):
            imported_objects = result.get("imported_objects", [])
            return f"Successfully imported {len(imported_objects)} objects from {file_path}"
        else:
            return f"Failed to import file: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error importing file: {str(e)}")
        return f"Failed to import file: {str(e)}"

@mcp.tool
def export_file(ctx: Context, object_names: List[str], file_path: str, file_type: str = "GLTF") -> str:
    """Export objects from the Blender scene to a file.
    
    Args:
        object_names: List of object names to export (empty list for all objects)
        file_path: Path for the exported file
        file_type: File type - 'OBJ', 'FBX', 'GLTF', 'STL', etc.
        
    Returns:
        Success message with export details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("export_file", {
            "object_names": object_names,
            "file_path": file_path,
            "file_type": file_type.upper()
        })
        
        if result.get("success"):
            return f"Successfully exported {len(object_names)} objects to {file_path}"
        else:
            return f"Failed to export file: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error exporting file: {str(e)}")
        return f"Failed to export file: {str(e)}"

@mcp.tool
def save_scene(ctx: Context, file_path: str, overwrite: bool = False) -> str:
    """Save the current Blender scene to a .blend file.
    
    Args:
        file_path: Path for the .blend file
        overwrite: Whether to overwrite existing file (default: False)
        
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("save_scene", {
            "file_path": file_path,
            "overwrite": overwrite
        })
        
        if result.get("success"):
            return f"Scene saved successfully to {file_path}"
        else:
            return f"Failed to save scene: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error saving scene: {str(e)}")
        return f"Failed to save scene: {str(e)}"

@mcp.tool
def load_scene(ctx: Context, file_path: str, confirm: bool = False) -> str:
    """Load a .blend file, replacing the current scene.
    
    Args:
        file_path: Path to the .blend file to load
        confirm: Confirmation flag to prevent accidental overwriting (must be True)
        
    Returns:
        Success or error message
    """
    try:
        if not confirm:
            return "Scene loading requires confirmation=True parameter"
        
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        blender = get_blender_connection()
        result = blender.send_command("load_scene", {
            "file_path": file_path
        })
        
        if result.get("success"):
            return f"Scene loaded successfully from {file_path}"
        else:
            return f"Failed to load scene: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error loading scene: {str(e)}")
        return f"Failed to load scene: {str(e)}"

# =============================================================================
# CAMERA/LIGHTING TOOLS (4 tools)
# =============================================================================

@mcp.tool
def create_camera(ctx: Context, name: str = "Camera", location: List[float] = [0, -5, 2],
                 rotation: List[float] = [1.2, 0, 0], fov: float = 50.0) -> str:
    """Create a new camera in the scene.
    
    Args:
        name: Name for the new camera
        location: XYZ coordinates for camera location
        rotation: XYZ rotation in radians
        fov: Field of view in degrees (default: 50.0)
        
    Returns:
        Success message with camera details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("create_camera", {
            "name": name,
            "location": location,
            "rotation": rotation,
            "fov": fov
        })
        
        if result.get("success"):
            return f"Camera '{name}' created successfully at location {location}"
        else:
            return f"Failed to create camera: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error creating camera: {str(e)}")
        return f"Failed to create camera: {str(e)}"

@mcp.tool
def set_active_camera(ctx: Context, camera_name: str) -> str:
    """Set the active camera for rendering and viewport.
    
    Args:
        camera_name: Name of the camera to set as active
        
    Returns:
        Success or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("set_active_camera", {
            "camera_name": camera_name
        })
        
        if result.get("success"):
            return f"Camera '{camera_name}' set as active camera"
        else:
            return f"Failed to set active camera: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error setting active camera: {str(e)}")
        return f"Failed to set active camera: {str(e)}"

@mcp.tool
def setup_lighting(ctx: Context, lighting_type: str = "THREE_POINT", 
                  location: List[float] = None, **kwargs) -> str:
    """Set up a predefined lighting setup.
    
    Args:
        lighting_type: Type of lighting - 'THREE_POINT', 'NATURAL', 'STUDIO', 'SUNSET'
        location: Optional location override for lights
        **kwargs: Additional lighting parameters
        
    Returns:
        Success message with lighting setup details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("setup_lighting", {
            "lighting_type": lighting_type.upper(),
            "location": location,
            **kwargs
        })
        
        if result.get("success"):
            light_count = result.get("light_count", 0)
            return f"'{lighting_type}' lighting setup created with {light_count} lights"
        else:
            return f"Failed to setup lighting: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error setting up lighting: {str(e)}")
        return f"Failed to setup lighting: {str(e)}"

@mcp.tool
def create_light(ctx: Context, light_type: str, name: str, location: List[float] = [0, 0, 5],
                energy: float = 1000.0, color: List[float] = [1.0, 1.0, 1.0]) -> str:
    """Create a new light in the scene.
    
    Args:
        light_type: Type of light - 'SUN', 'SPOT', 'POINT', 'AREA'
        name: Name for the new light
        location: XYZ coordinates for light location
        energy: Light energy/power
        color: RGB color values (0.0 to 1.0)
        
    Returns:
        Success message with light details
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("create_light", {
            "light_type": light_type.upper(),
            "name": name,
            "location": location,
            "energy": energy,
            "color": color
        })
        
        if result.get("success"):
            return f"Light '{name}' ({light_type}) created successfully at location {location}"
        else:
            return f"Failed to create light: {result.get('message', 'Unknown error')}"
    except Exception as e:
        logger.error(f"Error creating light: {str(e)}")
        return f"Failed to create light: {str(e)}"

# =============================================================================
# UTILITY AND DEBUGGING TOOLS (Additional tools for completeness)
# =============================================================================

@mcp.tool
def get_viewport_screenshot(ctx: Context, max_size: int = 800) -> Image:
    """Capture a screenshot of the current Blender 3D viewport.
    
    Args:
        max_size: Maximum size in pixels for the screenshot
        
    Returns:
        Screenshot as Image object
    """
    try:
        blender = get_blender_connection()
        
        # Create temporary file for screenshot
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"blender_screenshot_{uuid.uuid4()}.png")
        
        result = blender.send_command("get_viewport_screenshot", {
            "max_size": max_size,
            "filepath": temp_path,
            "format": "png"
        })
        
        if "error" in result:
            raise Exception(result["error"])
        
        if not os.path.exists(temp_path):
            raise Exception("Screenshot file was not created")
        
        # Read and return image
        with open(temp_path, 'rb') as f:
            image_bytes = f.read()
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except:
            pass
        
        return Image(data=image_bytes, format="png")
        
    except Exception as e:
        logger.error(f"Error capturing screenshot: {str(e)}")
        raise Exception(f"Failed to capture screenshot: {str(e)}")

@mcp.tool
def execute_blender_code(ctx: Context, code: str) -> str:
    """Execute arbitrary Python code in Blender.
    
    Args:
        code: Python code to execute in Blender
        
    Returns:
        Execution result or error message
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("execute_code", {"code": code})
        return f"Code executed successfully: {result.get('result', '')}"
    except Exception as e:
        logger.error(f"Error executing code: {str(e)}")
        return f"Code execution failed: {str(e)}"

@mcp.tool
def get_server_status(ctx: Context) -> str:
    """Get server connection status and Blender information.
    
    Returns:
        Server status and Blender information
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_server_status")
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting server status: {str(e)}")
        return f"Failed to get server status: {str(e)}"

if __name__ == "__main__":
    mcp.run()