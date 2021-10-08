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

from bpy.types import NodesModifier

#append folder
sys.path.append('C:\\code\\big_blender_plugin\\wall_builder')
import data_types

import panel
import wb_operators
importlib.reload(panel)
importlib.reload(wb_operators)



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

    bpy.types.Object.opening_type = bpy.props.EnumProperty(
        name='opening type',
        items=data_types.openings_types
    )

    bpy.types.Object.opening_top_offset = bpy.props.FloatProperty(
        name='opening top offset',
        default=0
    )

    bpy.types.Object.level = bpy.props.IntProperty(
        name='object level',
        default=0
    )

    
    classes = [
        panel.MainMenu,
        wb_operators.WallBuilder
    ]
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    bpy.utils.unregister_class(panel.MainMenu)

if __name__ == "__main__":
    register()