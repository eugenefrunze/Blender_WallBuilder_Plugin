import bpy
from bpy.types import Panel

class MOVER_PT_panel(Panel):
    bl_label = 'mrPanel'
    bl_idname = 'MOVER_PT_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MOVER'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row()
        if context.object:
            row.prop(context.object, 'height')

# def create_wall_profile():
#     bpy.ops.curve.simple(align='WORLD', location=(-0.5, 0, 0), rotation=(0, 0, 0), Simple_Type='Point', use_cyclic_u=False)
#     bpy.ops.curve.simple(align='WORLD', location=(-0.5, 1, 0), Simple_Type='Point', use_cyclic_u=False)
#     bpy.ops.curve.simple(align='WORLD', location=(0.5, 1, 0), Simple_Type='Point', use_cyclic_u=False)
#     bpy.ops.curve.simple(align='WORLD', location=(0.5, 0, 0), Simple_Type='Point', use_cyclic_u=False)

def create_wall_line():
    pass

points_coords = []

def create_wall_profile(context) -> list:
    bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple_Type='Rectangle', Simple_width=1, Simple_length=1, use_cyclic_u=True)
    obj = context.object
    data = obj.data
    obj.name = 'wb_wall_profile'
    #saving the profile context
    ctx_wall_profile = context.copy()

    #get all points
    points = []
    for point in data.splines[0].points:
        points.append(point)
    
    #setting parameters
    obj.data.fill_mode = 'NONE'
    bpy.ops.curve.spline_type_set(type='POLY')
    obj.data.splines[0].use_cyclic_u = True
    bpy.ops.transform.translate(value=(0, 0.5, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
    # bpy.ops.curve.select_all(action='DESELECT')
    # bpy.ops.object.mode_set(mode='OBJECT')

    # for i in range(0, 2):
    #     points_coords.append(obj.data.splines[0].points[i].co)

    # # print(points_coords[0][0])

    return points

def set_wall_profile_center():
    pass

def set_wall_profile_left():
    pass

def set_wall_profile_right():
    pass

def translate_point_position(self, context):
    # print(self.height)
    # bpy.context.object.data.splines[0].points[0][0].co[1] = self.height
   bpy.context.object.data.splines[0].points[0].co[1] = self.height
   bpy.context.object.data.splines[0].points[1].co[1] = self.height
    # points_coords[0] = self.height
    # points_coords[1] = self.heigth


def register():
    bpy.utils.register_class(MOVER_PT_panel)

    bpy.types.Object.height = bpy.props.FloatProperty(
        default=1,
        update=translate_point_position
    )     

wall_prof_points = create_wall_profile(bpy.context)
# wall_prof_points[0].select = True
# bpy.ops.object.mode_set(mode='EDIT')


def unregister():
    bpy.utils.unregister_class(MOVER_PT_panel)

    del bpy.types.Object.height

if __name__ == '__main__':
    register()

