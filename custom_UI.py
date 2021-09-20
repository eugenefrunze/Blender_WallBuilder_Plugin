import bpy
import bgl
import gpu

from bpy.types import Operator

class OT_drawer(Operator):
    bl_idname = 'object.draw_op'
    bl_label = 'draw operator'
    bl_description = 'op for drawing'
    bl_options = {'REGISTER'}

    def __init__(self):
        self.draw_handle = None
        self.draw_event = None

        self.widgets = []

    def invoke(self, context, event):
        
        self.create_batch()

        args = (self, context)
        self.register_handlers(args, context)

    