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

#append folders
sys.path.append('C:\\code\\big_blender_plugin')
sys.path.append('C:\\code\\big_blender_plugin\\wall_builder')

import data_types
import wb_properties
import wb_panel
import wb_operators
import utils
importlib.reload(data_types)
importlib.reload(wb_panel)
importlib.reload(wb_operators)
importlib.reload(wb_properties)
importlib.reload(utils)


def register():
    wb_properties.register()
    wb_panel.register()
    wb_operators.register()

def unregister():
    wb_properties.unregister()
    wb_panel.unregister()
    wb_operators.unregister()

if __name__ == "__main__":
    register()