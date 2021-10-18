import bpy
import data_types

# class WBProperties(bpy.types.PropertyGroup):

def register():
    
    bpy.types.Object.customer = bpy.props.EnumProperty(
            name='customer preset',
            items=data_types.customers
        )

    bpy.types.Object.outer_wall_thickness = bpy.props.FloatProperty(
            name='outer wall thickness',
            default=0
        )

    bpy.types.Object.inner_wall_thickness = bpy.props.FloatProperty(
            name='inner wall thickness',
            default=0
        )

    bpy.types.Object.wall_height = bpy.props.FloatProperty(
            name='wall height',
            default=0
        )

    bpy.types.Object.opening_elevation = bpy.props.FloatProperty(
            name='openings aver elevation',
            default=0
            )

    bpy.types.Object.opening_type = bpy.props.EnumProperty(
            name='opening type',
            items=data_types.openings_types
        )

    bpy.types.Object.opening_top_offset = bpy.props.FloatProperty(
            name='opening top offset',
            default=0
        )

    bpy.types.Object.level = bpy.props.IntProperty(
            name='object level',
            default=0
        )

def unregister():
    pass

if __name__ == '__main__':
    register()