import bpy
from . import data_types

from bpy.props import PointerProperty, EnumProperty, \
    FloatProperty, BoolProperty, IntProperty, \
        CollectionProperty, StringProperty

class GlobalObjectsProps(bpy.types.PropertyGroup):
    
    global_type: StringProperty(
        name = 'global type of plugin object'
    )





def register():
    from bpy.utils import register_class
    register_class(GlobalObjectsProps)

    bpy.types.Object.global_props = bpy.props.PointerProperty(type=GlobalObjectsProps)


def unregister():
    from bpy.utils import unregister_class
    unregister_class(GlobalObjectsProps)

    del bpy.types.Object.global_props


if __name__ == '__main__':
    register()