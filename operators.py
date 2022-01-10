import bpy
from .utils import get_object_bounds_coords, get_bounder_vertices, set_parent


class CurveAdder(bpy.types.Operator):
    bl_idname = 'object.curve_adder'
    bl_label = 'ADD CURVE'
    bl_options = {'REGISTER', 'UNDO'}

    curve_type: bpy.props.StringProperty(
        default='Line'
    )

    def execute(self, context):
        if self.curve_type == 'Line':
            #adding line
            bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple_Type='Line', shape='3D', use_cyclic_u=False)
            bpy.ops.transform.resize(value=(1, 1, 0))
            bpy.ops.curve.spline_type_set(type='POLY')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        elif self.curve_type == 'Rectangle':
            pass

        return {'FINISHED'}


class OpeningsBoundsCreator(bpy.types.Operator):
    bl_idname = 'object.openings_bounds_creator'
    bl_label = 'CREATE BOUNDS'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None

    #CLASS METHODS ---------------------------------------------------------------------------------
    def execute(self, context):
        obj = context.object
        #get object's bounds
        obj_bounds_cords = get_object_bounds_coords(obj, 'WORLD')
        print(obj_bounds_cords)

        #create bounds object
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bounds_obj = context.object
        bounds_obj.display_type = 'WIRE'
        bnds_obj_sides = get_bounder_vertices(bounds_obj)
        for idx, v_grp in enumerate(bnds_obj_sides):
            print(v_grp)
            for v_ind in v_grp:
                if idx < 3:
                    bounds_obj.data.vertices[v_ind].co[idx] = obj_bounds_cords[idx]
                    # print(f'object: {bounds_obj.name}, vertex: {bounds_obj.data.vertices[v_ind]}, co:{bounds_obj.data.vertices[v_ind].co[idx]}')
                else:
                    bounds_obj.data.vertices[v_ind].co[idx-3] = obj_bounds_cords[idx]
                    # print(f'object: {bounds_obj.name}, vertex: {bounds_obj.data.vertices[v_ind]}, co:{bounds_obj.data.vertices[v_ind].co[idx-3]}')
        
        #setting origin to the center of bounding
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

        #setting bounding object as parent for opening
        set_parent([obj], bounds_obj, True, context)

        return {'FINISHED'}

#END OF OpeningsBoundsCreator ----------------------------------------------------------------------

classes = [
    CurveAdder,
    OpeningsBoundsCreator
]


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)


if __name__ == '__main__':
    register()
