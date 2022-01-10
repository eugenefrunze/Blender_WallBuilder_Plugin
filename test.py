import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

class DrawLine():
    def __init__(self):
        self.handler = None

    def draw(self, coords):
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.shader.bind()
        self.shader.uniform_float("color", (1, 1, 0, 1))
        self.batch = batch_for_shader(self.shader, 'LINES', {"pos": coords})
        self.batch.draw(self.shader)

    def start_handler(self, context):
        self.handler = bpy.types.SpaceView3D.draw_handler_add(self.draw, ([context.object.data.vertices[7].co, context.object.location],), 'WINDOW', 'POST_VIEW')

    def remove_handler(self):
        bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')


#register DrawLine in driver namespace
dns = bpy.app.driver_namespace
dns['drawline'] = DrawLine()


class SizesDrawer(bpy.types.Operator):
    bl_idname = 'object.dimensions_drawer'
    bl_label = 'dimensions operator'
    bl_options = {'REGISTER', 'UNDO'}

    is_drawing: bpy.props.BoolProperty(
        default=False
    )

    def temp_get_object_side(self, obj):
        verts = obj.data.edges[8].vertices
        verts_coords = []
        verts_coords.append(obj.matrix_world @ obj.data.vertices[7].co)
        verts_coords.append(obj.matrix_world @ obj.data.vertices[3].co)

        print(verts_coords)

        return verts_coords


    def execute(self, context):
        obj = context.object
        dns = bpy.app.driver_namespace
        #start and remove line handlers
        print(dns.get('drawline'))
        if dns.get('drawline').handler is not None:
            dns.get('drawline').remove_handler()
            dns.get('drawline').handler = None
        else:
            # coords = self.temp_get_object_side(obj)
            dns.get('drawline').start_handler(context)
    
        return {'FINISHED'}


# class SizesDrawer(bpy.types.Operator):
#     bl_idname = 'object.dimensions_drawer'
#     bl_label = 'dimensions operator'
#     bl_options = {'REGISTER', 'UNDO'}

#     _handle = None
    
#     def draw_main(context):
#         shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
#         shader.bind()
#         shader.uniform_float("color", (1, 1, 0, 1))
#         batch = batch_for_shader(shader, 'LINES', {"pos": (0, 0, 0)})
#         batch.draw(shader)

#     @staticmethod
#     def handle_add(self, context):
#         if SizesDrawer._handle is None:
#             SizesDrawer._handle = bpy.types.SpaceView3D.draw_handler_add(SizesDrawer.draw_main(context), 'WINDOW', 'POST_VIEW')

#     @staticmethod
#     def handle_remove(self):
#         bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')

#     def execute(self, context):
#         self.handle_add()
    
#         return {'FINISHED'}


classes = [
    SizesDrawer
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