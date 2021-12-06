# import stand alone modules
import blf
import bpy

font_info = {
    "font_id": 0,
    "handler": None,
}


def init():
    """init function - runs once"""
    import os
    # Create a new font object, use external ttf file.
    font_path = bpy.path.abspath('//Zeyada.ttf')
    # Store the font indice - to use later.
    if os.path.exists(font_path):
        font_info["font_id"] = blf.load(font_path)
    else:
        # Default font.
        font_info["font_id"] = 0

    # set the font drawing routine to run every frame
    font_info["handler"] = bpy.types.SpaceView3D.draw_handler_add(
        draw_callback_px, (None, None), 'WINDOW', 'POST_PIXEL')


def draw_callback_px(self, context):
    """Draw on the viewports"""
    # BLF drawing routine
    font_id = font_info["font_id"]
    blf.position(font_id, 200, 80, 0)
    blf.size(font_id, 40, 72)
    blf.draw(font_id, "Hello World")

class Jopa(bpy.types.Operator):
    bl_idname = 'object.jopa'
    bl_label = 'jopa handler'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        init()

        return {'FINISHED'}

def register():
    from bpy.utils import register_class
    register_class(Jopa)


def unregister():
    from bpy.utils import unregister_class
    unregister_class(Jopa)

if __name__ == "__main__":
    register()