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
from . import tools_panel
from . import operators
from . import properties
from .wall_builder import wb_properties
from .wall_builder import wb_panel
from .wall_builder import wb_operators

#---------------------------------------------------------------------------------------------------
# TEST-EDU PART HERE -------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
# from .gpu_edu import gpu_test_main
#---------------------------------------------------------------------------------------------------
#END TEST-EDU --------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

import bpy


def register():
    wb_properties.register()
    wb_panel.register()
    wb_operators.register()
    tools_panel.register()
    operators.register()
    properties.register()

#---------------------------------------------------------------------------------------------------
# TEST-EDU PART HERE -------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
    # gpu_test_main.register()
#---------------------------------------------------------------------------------------------------
#END TEST-EDU --------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


def unregister():
    wb_properties.unregister()
    wb_panel.unregister()
    wb_operators.unregister()
    tools_panel.unregister()
    operators.unregister()
    properties.unregister()


if __name__ == "__main__":
    register()