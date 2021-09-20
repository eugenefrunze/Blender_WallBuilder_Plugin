import bpy
from bpy.utils import register_class

# class VIEW3D_PT_svg_import(bpy.types.Panel):
    
class SCENE_PT_svg_import(bpy.types.Operator):
    bl_idname = 'import_scene.svg_import'
    bl_label = 'svg_import_operator'
    def execute(self, context):
        bpy.ops.import_curve.svg(bpy.context.scene.svg_import_path)


classes = [

]

def register():

    bpy.types.Scene.svg_import_path = bpy.props.StringProperty(
        name='svg path',
        default='',
        subtype='FILE_PATH'
    )

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():

    del bpy.types.Scene.svg_import_path

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()