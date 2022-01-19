import bpy
from . import data_types

from bpy.props import PointerProperty, EnumProperty, \
    FloatProperty, BoolProperty, IntProperty, \
        CollectionProperty, StringProperty

class ObjectsProps(bpy.types.PropertyGroup):
    
    type: StringProperty(
        name = 'global type of plugin object'
    )

class SceneProps(bpy.types.PropertyGroup):

    library_fbx_import_path: StringProperty(
        subtype='DIR_PATH'
    )


def register():
    from bpy.utils import register_class
    register_class(ObjectsProps)
    register_class(SceneProps)

    bpy.types.Object.props = bpy.props.PointerProperty(type=ObjectsProps)
    bpy.types.Scene.props = bpy.props.PointerProperty(type=SceneProps)


def unregister():
    from bpy.utils import unregister_class
    unregister_class(ObjectsProps)
    unregister_class(SceneProps)


    del bpy.types.Object.props
    del bpy.types.Scene.props


# if __name__ == '__main__':
#     register()