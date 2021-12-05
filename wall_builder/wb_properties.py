import types
import bpy
import data_types
import wb_operators

from bpy.props import PointerProperty, EnumProperty, FloatProperty, BoolProperty, \
    IntProperty, FloatVectorProperty, CollectionProperty, StringProperty

class WBSceneProps(bpy.types.PropertyGroup):
    plans_collection: PointerProperty(
        type=bpy.types.Collection,
        name='wb objects',)

class WBProps(bpy.types.PropertyGroup):
    customer: EnumProperty(
            name='customer preset',
            items=data_types.customers
        )

    object_type: EnumProperty(
        name='object type',
        items=data_types.get_openings_types(),
        default='WALL'
    )

    is_converted: BoolProperty(
        name='is converted',
        description='is object already converter into a BBP object (ex. Wall, Opening etc.)',
        default=False

    )

    level: EnumProperty(
        name='object level',
        # items = data_types.levels # ------------------------------------ FIX THIS!!!!!!!!!!!!!!
        items =(
           ('KG', 'KG (basement)', ''),
           ('EG', 'EG (1st floor)', ''),
           ('OG', 'OG (2nd floor)', ''),
           ('DG', 'DG (last floor)', '')),
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
            default=0,
            update=wb_operators.WallBuilder.set_wall_position
        )

    height: FloatProperty(
            name='height',
            default=0,
            update=wb_operators.WallBuilder.set_wall_position
        )

    wall_profile_curve: PointerProperty(
        type=bpy.types.Object,
        name='taper profile for the wall'
    )

    opening_elevation: FloatProperty(
            name='openings average elevation',
            default=0
            )

    elevation: FloatProperty(
            name='object global elevation',
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

    align_marker: PointerProperty(
        type=bpy.types.Object,
        name='align marker')


def register():
    from bpy.utils import register_class
    register_class(WBProps)
    register_class(WBSceneProps)

    bpy.types.Object.wall_builder_props = bpy.props.PointerProperty(type=WBProps)


    bpy.types.Scene.wall_builder_scene_props = bpy.props.PointerProperty(type=WBSceneProps)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(WBProps)
    unregister_class(WBSceneProps)


if __name__ == '__main__':
    register()