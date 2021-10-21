import types
import bpy
import data_types

from bpy.props import PointerProperty, EnumProperty, FloatProperty, BoolProperty, \
    IntProperty, FloatVectorProperty, CollectionProperty, StringProperty

class WBProps(bpy.types.PropertyGroup):
    customer: EnumProperty(
            name='customer preset',
            items=data_types.customers
        )

    object_type: EnumProperty(
        name='object type',
        items=data_types.objects_types,
        default='WALL'
    )
    
    position: EnumProperty(
        name='position',
        items=(
            ('INSIDE', 'Inside', ''),
            ('CENTER', 'Center', ''),
            ('OUTSIDE', 'Outside', '')
            ),
        default='INSIDE'
        )

    thickness: FloatProperty(
            name='wall thickness',
            default=0
        )

    wall_height: FloatProperty(
            name='wall height',
            default=0
        )

    opening_elevation: FloatProperty(
            name='openings average elevation',
            default=0
            )

    opening_type: EnumProperty(
            name='opening type',
            items=data_types.openings_types
        )

    opening_top_offset: FloatProperty(
            name='opening top offset',
            default=0
        )

    level: IntProperty(
            name='object level',
            default=0
        )

    

def register():
    from bpy.utils import register_class
    register_class(WBProps)

    bpy.types.Object.wall_builder_props = bpy.props.PointerProperty(type=WBProps)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(WBProps)

if __name__ == '__main__':
    register()