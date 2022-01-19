from operator import le
import pathlib
import bpy

from bpy_extras.view3d_utils import location_3d_to_region_2d
from gpu import select
from .utils import get_object_bounds_coords, get_bounder_vertices, set_parent

import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader

from mathutils import Vector


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
        bounds_obj.props.type = 'BOUNDING'
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
        if obj.props.type == 'BOUNDING':
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


class FBXLibraryImporter(bpy.types.Operator):

    bl_idname = 'scene.fbx_library_importer'
    bl_label = 'IMPORT ALL FBX'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        abspath = bpy.path.abspath(context.scene.props.library_fbx_import_path)
        # print(abspath)
        import_path = pathlib.Path(abspath)
        # print(import_path)

        for import_fpath in import_path.glob('*.fbx'):
            print(str(import_fpath))
            bpy.ops.import_scene.fbx(filepath=str(import_fpath))

        return {'FINISHED'}


class OT_TestModalOperator(bpy.types.Operator):
    bl_idname = 'object.test_modal_operator'
    bl_label = 'Test Modal Operator'
    bl_options = {'REGISTER'}


    crap: bpy.props.StringProperty()
    crap2: bpy.props.StringProperty()

    # def __init__(self):
    #     self.test1 = 0
    #     self.test2 = 0

    def invoke(self, context, event: bpy.types.Event):
        self.crap = 'ZZZ'
        self.crap2 = 'ZZZ'
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

        
        # self.crap = event.type
        # self.crap2 = event.ctrl
        # return self.execute(context)
        # return {'PASS_THROUGH'}

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        # print(event.type)
        if event.type == 'MOUSEMOVE':
            print(f'MOUSEMOVE: {event.mouse_x}', f'{event.mouse_y}')
        
        elif event.type == 'LEFTMOUSE':
            print(f'LEFT {event.value} at {event.mouse_x}, {event.mouse_y}')

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            print(f'{event.type} {event.value} -- STOPPING')
            # return {'FINISHED'}
            return self.execute(context)

        return {'PASS_THROUGH'}
        

    def execute(self, context):
        self.report({'INFO'}, f'{self.bl_idname} EXECUTED {self.crap} {self.crap2}')
        return {'FINISHED'} 

class OT_TestGPUDrawer(bpy.types.Operator):
    bl_idname = 'object.gpu_drawer'
    bl_label = 'draw gpu'
    bl_options = {'REGISTER'}

    def draw_line_3d(color, start, end):
        shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": [start, end]})
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
    
    def draw_callback_3d(self, operator, context):
        vert1 = (context.object.matrix_world @ context.object.data.vertices[0].co) + Vector((0.2, 0.2, 0))
        vert2 = (context.object.matrix_world @ context.object.data.vertices[1].co) + Vector((0.2, 0.2, 0))

        pos1 = (context.object.matrix_world @ context.object.data.vertices[0].co)
        pos2 = (context.object.matrix_world @ context.object.data.vertices[0].co) + Vector((0.4, 0.4, 0))

        pos3 = (context.object.matrix_world @ context.object.data.vertices[1].co)

        pos4 = (context.object.matrix_world @ context.object.data.vertices[1].co) + Vector((0.4, 0.4, 0))

        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glEnable(bgl.GL_DEPTH_TEST)

        #draw line 1
        shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": [vert1, vert2]})
        shader.bind()
        shader.uniform_float("color", (0.0, 1.0, 0.0, 0.7))
        batch.draw(shader)

        #draw line 2
        shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": [pos1, pos2]})
        shader.bind()
        shader.uniform_float("color", (0.0, 1.0, 0.0, 0.7))
        batch.draw(shader)

        #draw line 3
        shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": [pos3, pos4]})
        shader.bind()
        shader.uniform_float("color", (0.0, 1.0, 0.0, 0.7))
        batch.draw(shader)

        # bgl.glEnd()
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_LINE_SMOOTH)
        bgl.glEnable(bgl.GL_DEPTH_TEST)
    
    def draw_callback_text_2D(self, operator, context):

        v3d = context.space_data
        rv3d = v3d.region_3d
        # region = v3d.region

        position_text = location_3d_to_region_2d(context.region, rv3d, context.object.location)

        font_id = 0
        blf.position(font_id, 2, 80, 0)
        blf.size(font_id, 20, 72)
        blf.color(font_id, 0.0, 1.0, 0.0, 1.0)

        #calculate the line size in mm
        length = ((context.object.matrix_world @ context.object.data.vertices[0].co - context.object.matrix_world @ context.object.data.vertices[1].co).length) * 1000
        

        blf.position(font_id, position_text[0], position_text[1], 0)
        blf.draw(font_id, '%.2f mm' % length)

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):

        args = (self, context)
        self._handle_3d = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_3d, args, 'WINDOW', 'POST_VIEW')
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

        #draw text 2D
        self._handle_text_2D = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_text_2D, args, 'WINDOW', 'POST_PIXEL')


        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        context.area.tag_redraw()

        if event.type in {'ESC'}:
            #remove timer handler
            context.window_manager.event_timer_remove(self.draw_event)
            #remove lines handler
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_3d, 'WINDOW')
            #remove text handler
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_text_2D, 'WINDOW')

            return {'CANCELLED'}

        return {'PASS_THROUGH'}
            

classes = [
    CurveAdder,
    BoundingsHaldler,
    ExtraCurvesEnabler,
    FBXLibraryImporter,
    OT_TestModalOperator,
    OT_TestGPUDrawer
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
