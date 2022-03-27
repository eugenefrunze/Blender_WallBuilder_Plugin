from email.policy import default
from unicodedata import name
import bpy
from . import operators
from . import data_types
from . import utils

from bpy.props import PointerProperty, EnumProperty, \
    FloatProperty, BoolProperty, IntProperty, \
        CollectionProperty, StringProperty

#---------------------------------------------------------------------------------------------------
# main plugin props
#---------------------------------------------------------------------------------------------------

class ObjectsProps(bpy.types.PropertyGroup):
    type: StringProperty(name = 'global type of plugin object')

class SceneProps(bpy.types.PropertyGroup):
    library_fbx_import_path: StringProperty(subtype='DIR_PATH')
    
class CustomersData(bpy.types.PropertyGroup):
    ucm_id: IntProperty(name='ucm_id')
    mc_id: IntProperty(name='mc_id')
    client_id: IntProperty(name='client_id')
    wall_height: IntProperty(name='wall_height')
    wall_out_thickness: IntProperty(name='wall_out_thickness')
    wall_in_thickness: IntProperty(name='wall_in_thickness')
    wall_middle_thickness: IntProperty(name='wall_middle_thickness')
    windows_top: IntProperty(name='windows_top')
    foundation: IntProperty(name='foundation')
    ceiling: IntProperty(name='ceiling')
    mc_name: StringProperty(name='mc_name')
    client_name: StringProperty(name='client_name')
    
    
#---------------------------------------------------------------------------------------------------
# wall builder props
#---------------------------------------------------------------------------------------------------

class WBProps(bpy.types.PropertyGroup):
    is_converted: BoolProperty(name='Is converted',
        description='If object an Wall builder object')

    customer: EnumProperty(name='client preset',
        items=utils.get_customers_info(),
        update=operators.WallBuilder.set_customer_preset)

    object_type: EnumProperty(
        name='object type',
        items=data_types.get_objects_types())

    is_inner_wall: BoolProperty(
        name='is inner wall',
        update=operators.WallBuilder.set_customer_preset,
        default=False)

    level: EnumProperty(
        name='object level',
        items=data_types.levels)
    
    position: EnumProperty(
        name='position',
        items=(
            ('INSIDE', 'Inside', ''),
            ('CENTER', 'Center', ''),
            ('OUTSIDE', 'Outside', '')
            ),
        default='INSIDE',
        update=operators.WallBuilder.set_wall_position)

    thickness: FloatProperty(
            name='wall thickness',
            unit='LENGTH',
            default=0,
            update=operators.WallBuilder.set_wall_position)

    height: FloatProperty(
            name='height',
            unit='LENGTH',
            default=0,
            update=operators.WallBuilder.set_wall_position)

    wall_profile_curve: PointerProperty(
        type=bpy.types.Object,
        name='taper profile for the wall')

    opening_elevation: FloatProperty(
            name='openings average elevation',
            unit='LENGTH',
            default=0)

    elevation: FloatProperty(
            name='object global elevation',
            unit='LENGTH',
            default=0)

    opening_type: EnumProperty(
            name='opening type',
            items=data_types.openings_types)

    opening_top_offset: FloatProperty(
            name='opening top offset',
            unit='LENGTH',
            default=0)

    bounding_object: PointerProperty(
        name='bounding object',
        type=bpy.types.Object,
        description='bounding box object, used maily as bool cutter object for openings')
    
    helper_type: EnumProperty(
        name='helper object type',
        items=data_types.helper_types)
    
    snapping_cast: PointerProperty(
        name='snapping temporary copy',
        type=bpy.types.Object,
        description='the temporary snapping object useful to position objects on the walls'
    )


class WBSceneProps(bpy.types.PropertyGroup):
    plans_collection: PointerProperty(
        type=bpy.types.Collection,
        name='wb objects',
        description='The collection off levels objects to align')

    alignment_object: PointerProperty(
        type=bpy.types.Object,
        name='Alignment point',
        description='The object on the pivot point of which the rest of the objects are aligned')

class OpeningsCollection(bpy.types.PropertyGroup):
    obj: PointerProperty(type=bpy.types.Object)
    obj_id: IntProperty()

#---------------------------------------------------------------------------------------------------
# tools & props props
#---------------------------------------------------------------------------------------------------

class TObjectProps(bpy.types.PropertyGroup):
    pass

class TSceneProps(bpy.types.PropertyGroup):
    fast_object_type: EnumProperty(
        name='object type',
        description='fast object type',
        items=data_types.fast_objects_types,
        default='RECTANGLE')

    new_length: FloatProperty(
        name = 'length',
        unit='LENGTH',
        default=1)
    
    new_width: FloatProperty(
        name='width',
        unit='LENGTH',
        default=1)


#---------------------------------------------------------------------------------------------------
# register / unregister
#---------------------------------------------------------------------------------------------------

def register():
    from bpy.utils import register_class

    # main props
    register_class(ObjectsProps)
    register_class(SceneProps)
    bpy.types.Object.props = bpy.props.PointerProperty(type=ObjectsProps)
    bpy.types.Scene.props = bpy.props.PointerProperty(type=SceneProps)

    # wall builder props
    register_class(CustomersData)
    register_class(WBProps)
    register_class(WBSceneProps)
    register_class(OpeningsCollection)
    bpy.types.Scene.customers_data = bpy.props.CollectionProperty(type=CustomersData)
    bpy.types.Object.wb_props = bpy.props.PointerProperty(type=WBProps)
    bpy.types.Scene.wb_props = bpy.props.PointerProperty(type=WBSceneProps)
    bpy.types.Object.openings = CollectionProperty(type=OpeningsCollection)
    bpy.types.Object.opening_index = IntProperty()

    #tools props
    register_class(TObjectProps)
    register_class(TSceneProps)
    bpy.types.Object.tools_props = bpy.props.PointerProperty(type=TObjectProps)
    bpy.types.Scene.tools_props = bpy.props.PointerProperty(type=TSceneProps)


def unregister():
    from bpy.utils import unregister_class

    # main props
    unregister_class(ObjectsProps)
    unregister_class(SceneProps)
    del bpy.types.Object.props
    del bpy.types.Scene.props

    # wall builder props
    unregister_class(CustomersData)
    unregister_class(WBProps)
    unregister_class(WBSceneProps)
    unregister_class(OpeningsCollection)
    del bpy.types.Scene.customers_data
    del bpy.types.Object.wb_props
    del bpy.types.Scene.wb_props
    del bpy.types.Object.openings
    del bpy.types.Object.opening_index

    #tools props
    unregister_class(TObjectProps)
    unregister_class(TSceneProps)
    del bpy.types.Object.tools_props
    del bpy.types.Scene.tools_props