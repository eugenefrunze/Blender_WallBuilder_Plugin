import bpy
import gpu
from gpu_extras.batch import batch_for_shader


class DrawClass():

    def __init__(self, context):
        self.coords = [
            (-15, 0, 0), (-12.5, 5, 0), (-12.5, 5, 0), (-10, 0, 0),
            (-10, 2.5, 0), (-7.5, 5, 0), (-7.5, 5, 0), (-5, 2.5, 0),
            (-5, 2.5, 0), (-7.5, 0, 0), (-7.5, 0, 0), (-10, 2.5, 0),
            (-4, 5, 0), (1, 0, 0), (-4, 0, 0), (1, 5, 0),

        ]
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINES', {"pos": self.coords})
        self.handler = None

    def draw(self):
        self.shader.bind()
        self.shader.uniform_float("color", (1, 1, 0, 1))
        self.batch.draw(self.shader)

    def start_handler(self):
        self.handler = bpy.types.SpaceView3D.draw_handler_add(self.draw, (), 'WINDOW', 'POST_VIEW')

    def remove_handler(self):
        bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')


drawclass = DrawClass(bpy.context)
dns = bpy.app.driver_namespace
dns['drawclass'] = drawclass

class Jopa(bpy.types.Operator):
    bl_idname = 'custom.joparemover'
    bl_label = 'jopalabel'

    is_draw: bpy.props.BoolProperty()
    
    def execute(self, context):
        dns = bpy.app.driver_namespace
        drawclass = dns.get('drawclass')
        if drawclass.handler == None:
            drawclass.start_handler()
        else:
            drawclass.remove_handler()
            drawclass.handler = None

        return {'FINISHED'}

bpy.utils.register_class(Jopa)