import bpy
from .utils import get_object_bounds_coords, get_bounder_vertices, set_parent


class ExtraCurvesEnabler(bpy.types.Operator):
    bl_idname = 'custom.extracurvesenabler'
    bl_label = 'enable curve extra'
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context):
        bpy.ops.preferences.addon_enable(module="add_curve_extra_objects")

        self.report({'INFO'}, '"Add Curve: Extra Objects" modifier enabled')
        return {'FINISHED'}


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


class BoundingsHaldler(bpy.types.Operator):
    bl_idname = 'object.openings_bounds_creator'
    bl_label = 'CREATE BOUNDS'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'


    # custom methods -------------------------------------------------------------------------------

    def set_boundings_for_object(self, object, context):
        object = context.object
        #get object's bounds
        obj_bounds_cords = get_object_bounds_coords(object, 'WORLD')
        # print(obj_bounds_cords)
        #create bounds object
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bounds_obj = context.object
        bounds_obj.global_props.global_type = 'BOUNDING'
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
        set_parent([object], bounds_obj, True, context)

        #setting bounding object to an opening object parameter 'bounding_object'
        object.wall_builder_props.bounding_object = bounds_obj


    #class methods ---------------------------------------------------------------------------------
    def execute(self, context):
        obj = context.object
        #check if the object is not of bounding type
        if obj.global_props.global_type == 'BOUNDING':
            self.report({'WARNING'}, 'The object is itself a bounding!')
            return {'CANCELLED'}

        if obj.wall_builder_props.bounding_object == None:
            self.set_boundings_for_object(obj, context)
            self.report({'INFO'}, 'Bounding object created successfully')
            return {'FINISHED'}
        else:
            # cheking if object has dead (deleted) bounding object
            try:
                obj.wall_builder_props.bounding_object.select_set(True)
            except RuntimeError as err:
                print(err, 'Reason: Object had dead bounding object. Created a new one')
                self.report({'INFO'}, 'Object had dead bounding object. Created a new one')
                obj.wall_builder_props.bounding_object = None
                self.set_boundings_for_object(obj, context)
                return {'FINISHED'}
            else:
                print('Object already has a bounding object')
                obj.wall_builder_props.bounding_object.select_set(False)
                self.report({'INFO'}, 'Object already has a bounding object')
                return {'FINISHED'}

        


        

#END OF OpeningsBoundsCreator ----------------------------------------------------------------------

classes = [
    CurveAdder,
    BoundingsHaldler,
    ExtraCurvesEnabler
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
