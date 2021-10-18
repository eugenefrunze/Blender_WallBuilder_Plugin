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

import wb_properties
import panel
import wb_operators
importlib.reload(panel)
importlib.reload(wb_operators)
importlib.reload(wb_properties)



def register():
    
    classes = [
        panel.MainMenu,
        wb_operators.WallBuilder,
    ]
    for cls in classes:
        bpy.utils.register_class(cls)

    wb_properties.register()

def unregister():
    bpy.utils.unregister_class(panel.MainMenu)

if __name__ == "__main__":
    register()