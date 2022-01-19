import bpy
import bgl
from bpy import context
import gpu

from gpu_extras.batch import batch_for_shader

class OT_draw_operator(bpy.types.Operator):
    bl_idname = 'object.draw_op'
    bl_label = 'Draw operator'
    bl_description = 'Operator for drawing'
    bl_options = {'REGISTER'}
    
    def __init__(self):
        self.draw_handle = None
        self.draw_event = None

        self.widgets = []

    def invoke(self, context, event):
        self.create_batch()

        args = (self, context)
        self.register_handlers(args, context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def register_handlers(self, args, context):
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, args, 'WINDOW', 'POST_VIEW')

        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

    def unregister_handlers(self, context):
        context.window_manager.event_timer_remove(self.draw_event)

        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')

        self.draw_handle = None
        self.draw_event = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if event.type in {'ESC'}:
            self.unregister_handlers(context)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def finish(self):
        self.unregister_handlers(context)
        return {'FINISHED'}

    def create_batch(self):

        vertices = [(0, 3, 3), (0, 4, 4), (0, 6, 2), (0, 3, 3)]

        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', {'pos': vertices})

    def draw_callback_px(self, op, context):

        self.shader.bind()
        self.shader.uniform_float('color', (1, 1, 1, 1))
        self.batch.draw(self.shader)