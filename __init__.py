bl_info = {
    "name": "BIG BLENDER PLUGIN",
    "description": "Architectural plugin",
    "author": "Eugene Frunze",
    "version": (0, 9),
    "blender": (3, 0, 0),
    "category": "UI",
    "location": "Unknown",
    "url": "https://blue7.it"
}

from . import data_types
from . import utils
from .wall_builder import wb_properties
from .wall_builder import wb_panel
from .wall_builder import wb_operators


import bpy


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