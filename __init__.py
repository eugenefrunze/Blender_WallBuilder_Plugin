bl_info = {
    "name": "BIG BLENDER PLUGIN",
    "description": "Architectural plugin",
    "author": "Eugene Frunze",
    "version": (0, 9),
    "blender": (3, 0, 0),
    "category": "UI",
    "location": "View3D > Sidebar > WALL BUILDER / TOOLS & PROPS",
    "url": "https://blue7.it"
}

from . import data_types
from . import utils
from . import operators
from . import properties
from . import panels
# from . import tile_generator

#---------------------------------------------------------------------------------------------------
# TEST-EDU PART HERE -------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
# from .gpu_edu import gpu_test_main
from . import test
#---------------------------------------------------------------------------------------------------
#END TEST-EDU --------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

import bpy


def register():
    panels.register()
    operators.register()
    properties.register()
    # tile_generator.register()

#---------------------------------------------------------------------------------------------------
# TEST-EDU PART HERE -------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
    # gpu_test_main.register()
    test.register()
#---------------------------------------------------------------------------------------------------
#END TEST-EDU --------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


def unregister():
    panels.unregister()
    operators.unregister()
    properties.unregister()
    # tile_generator.unregister()

#---------------------------------------------------------------------------------------------------
# TEST-EDU PART HERE -------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
    # gpu_test_main.register()
    test.unregister()
#---------------------------------------------------------------------------------------------------
#END TEST-EDU --------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    register()