# Blender MCP Addon - Receives commands from MCP Server
bl_info = {
    "name": "Blender MCP Bridge",
    "author": "MiniMax Agent",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > MCP",
    "description": "Bridge between Blender and MCP Server for AI-controlled 3D operations",
    "category": "System",
}

import bpy
import socket
import threading
import json
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import Operator, Panel, AddonPreferences


class MCPAddonPreferences(AddonPreferences):
    bl_idname = __name__

    host: StringProperty(
        name="Host",
        description="Host address for MCP server connection",
        default="localhost",
    )
    
    port: IntProperty(
        name="Port",
        description="Port number for MCP server connection",
        default=9876,
        min=1024,
        max=65535,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "host")
        layout.prop(self, "port")


class MCP_OT_StartServer(Operator):
    """Start the MCP Bridge Server inside Blender"""
    bl_idname = "mcp.start_server"
    bl_label = "Start MCP Server"
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        
        # Start server in background thread
        server_thread = threading.Thread(
            target=start_mcp_server,
            args=(prefs.host, prefs.port),
            daemon=True
        )
        server_thread.start()
        
        self.report({'INFO'}, f"MCP Server started on {prefs.host}:{prefs.port}")
        return {'FINISHED'}


class MCP_OT_StopServer(Operator):
    """Stop the MCP Bridge Server"""
    bl_idname = "mcp.stop_server"
    bl_label = "Stop MCP Server"
    bl_options = {'REGISTER'}

    def execute(self, context):
        global server_running
        server_running = False
        self.report({'INFO'}, "MCP Server stopped")
        return {'FINISHED'}


class MCP_PT_Panel(Panel):
    """MCP Bridge Control Panel"""
    bl_label = "MCP Bridge"
    bl_idname = "MCP_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MCP'

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[__name__].preferences
        
        box = layout.box()
        box.label(text="Connection Settings:", icon='LINKED')
        box.label(text=f"Host: {prefs.host}")
        box.label(text=f"Port: {prefs.port}")
        
        layout.separator()
        
        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator("mcp.start_server", icon='PLAY')
        row.operator("mcp.stop_server", icon='PAUSE')
        
        layout.separator()
        
        status_box = layout.box()
        status_box.label(text="Status:", icon='INFO')
        if server_running:
            status_box.label(text="Server Running ✓", icon='CHECKMARK')
        else:
            status_box.label(text="Server Stopped", icon='X')


# Global server state
server_running = False
server_socket = None


def start_mcp_server(host, port):
    """Start socket server to receive MCP commands"""
    global server_running, server_socket
    
    server_running = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        server_socket.settimeout(1.0)  # Allow periodic checking of server_running
        
        print(f"[MCP Bridge] Server listening on {host}:{port}")
        
        while server_running:
            try:
                client_socket, address = server_socket.accept()
                print(f"[MCP Bridge] Client connected: {address}")
                
                # Handle client in a separate thread
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_thread.start()
                
            except socket.timeout:
                continue  # Check server_running flag
            except Exception as e:
                print(f"[MCP Bridge] Accept error: {e}")
                break
                
    except Exception as e:
        print(f"[MCP Bridge] Server error: {e}")
    finally:
        if server_socket:
            server_socket.close()
        server_running = False
        print("[MCP Bridge] Server stopped")


def handle_client(client_socket):
    """Handle individual client connections"""
    try:
        while server_running:
            # Receive command
            data = client_socket.recv(4096)
            if not data:
                break
            
            try:
                command = json.loads(data.decode('utf-8'))
                print(f"[MCP Bridge] Received command: {command.get('action')}")
                
                # Execute command and get result
                result = execute_command(command)
                
                # Send response
                response = json.dumps(result)
                client_socket.sendall(response.encode('utf-8'))
                
            except json.JSONDecodeError as e:
                error_response = json.dumps({
                    "success": False,
                    "error": f"Invalid JSON: {str(e)}"
                })
                client_socket.sendall(error_response.encode('utf-8'))
                
    except Exception as e:
        print(f"[MCP Bridge] Client handler error: {e}")
    finally:
        client_socket.close()
        print("[MCP Bridge] Client disconnected")


def execute_command(command):
    """Execute bpy command from MCP server"""
    try:
        action = command.get('action')
        params = command.get('params', {})
        
        # Map actions to bpy operations
        if action == 'add_cube':
            bpy.ops.mesh.primitive_cube_add(**params)
            return {"success": True, "message": "Cube added"}
            
        elif action == 'add_sphere':
            bpy.ops.mesh.primitive_uv_sphere_add(**params)
            return {"success": True, "message": "Sphere added"}
            
        elif action == 'add_cylinder':
            bpy.ops.mesh.primitive_cylinder_add(**params)
            return {"success": True, "message": "Cylinder added"}
            
        elif action == 'delete_object':
            obj_name = params.get('name')
            if obj_name and obj_name in bpy.data.objects:
                bpy.data.objects.remove(bpy.data.objects[obj_name])
                return {"success": True, "message": f"Object '{obj_name}' deleted"}
            return {"success": False, "error": "Object not found"}
            
        elif action == 'move_object':
            obj_name = params.get('name')
            location = params.get('location', [0, 0, 0])
            if obj_name and obj_name in bpy.data.objects:
                bpy.data.objects[obj_name].location = location
                return {"success": True, "message": f"Object '{obj_name}' moved"}
            return {"success": False, "error": "Object not found"}
            
        elif action == 'render':
            bpy.ops.render.render(write_still=True)
            return {"success": True, "message": "Render complete"}
            
        elif action == 'save_file':
            filepath = params.get('filepath')
            bpy.ops.wm.save_as_mainfile(filepath=filepath)
            return {"success": True, "message": f"File saved to {filepath}"}
            
        elif action == 'eval':
            # Execute arbitrary Python code (use with caution)
            code = params.get('code')
            result = eval(code)
            return {"success": True, "result": str(result)}
            
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


# Registration
classes = (
    MCPAddonPreferences,
    MCP_OT_StartServer,
    MCP_OT_StopServer,
    MCP_PT_Panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("[MCP Bridge] Addon registered")


def unregister():
    global server_running
    server_running = False
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("[MCP Bridge] Addon unregistered")


if __name__ == "__main__":
    register()
