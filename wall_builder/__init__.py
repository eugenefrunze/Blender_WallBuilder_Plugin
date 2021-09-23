bl_info = {
    "name": "Big Blender Plugin (addon)",
    "description": "the main template for the future plugin",
    "author": "miloslavsky",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "category": "UI",
    "location": "Unknown",
    "url": "https://blue7.it"
}

import bpy
import sys
import importlib

#append folder
sys.path.append('C:\\code\\big_blender_plugin\\wall_builder')
import data_types

import panel
import builder_operator
importlib.reload(panel)
importlib.reload(builder_operator)



def register():

    bpy.types.Object.customer = bpy.props.EnumProperty(
        name='customer preset',
        items=data_types.customers
    )

    bpy.types.Object.outer_wall_thickness = bpy.props.FloatProperty(
        name='outer wall thickness',
        default=0
    )

    bpy.types.Object.inner_wall_thickness = bpy.props.FloatProperty(
        name='inner wall thickness',
        default=0
    )

    bpy.types.Object.wall_height = bpy.props.FloatProperty(
        name='wall height',
        default=0
    )

    bpy.types.Object.opening_elevation = bpy.props.FloatProperty(
        name='openings aver elevation',
        default=0
        )

    
    classes = [
        panel.MainMenu,
        builder_operator.WallBuilder
    ]
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    bpy.utils.unregister_class(panel.MainMenu)

if __name__ == "__main__":
    register()