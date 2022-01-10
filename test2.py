import bpy
import blf

class DrawTextClass():

    def __init__(self, context):
        self.handle = None

    def draw_callback_px(self, context):
        font_id = 0
        blf.position(font_id, 1, 1, 0)
        blf.size(font_id, 4, 72)
        blf.draw(font_id, 'SOME TEXT HERE')

    def draw(self, context):
        self.handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, (context,), 'WINDOW', 'POST_VIEW')

    def remove_handle(self):
        bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')


drawtextclass = DrawTextClass(bpy.context)
dns = bpy.app.driver_namespace
dns['drawtextclass'] = drawtextclass


class FontDrawerOperator(bpy.types.Operator):
    bl_idname = 'object.draw_exapmle_text'
    bl_label = 'test drawing operator'

    def execute(self, context):
        dns = bpy.app.driver_namespace
        drawtextclass = dns.get('drawtextclass')

        if drawtextclass.handle is not None:
            drawtextclass.remove_handle()
            drawtextclass.handle = None

            return {'FINISHED'}

        elif drawtextclass.handle == None:
            drawtextclass.draw(context)

            return {'FINISHED'}


def register():
    from bpy.utils import register_class
    register_class(FontDrawerOperator)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(FontDrawerOperator)

if __name__ == '__main__':
    register()