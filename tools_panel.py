import bpy
from . import operators
from . import test




class WB_PT_CreatePanel(bpy.types.Panel):
    bl_idnname = 'VIEW3D_PT_WBCreatePanel'
    bl_label = 'wall builder create panel'
    bl_category = 'TOOLS PANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='OBJECTS TOOLS')

        row = col.row()
        row.operator(operators.CurveAdder.bl_idname, text='ADD CURVE', icon='MOD_CURVE')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='OPENINGS TOOLS')

        row = col.row()
        row.operator(operators.OpeningsBoundsCreator.bl_idname, text='CREATE BOUNDS', icon='FILE_3D')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='MEASURES TOOLS')

        row = col.row()
        row.operator(test.SizesDrawer.bl_idname, text='ENABLE MEASURES', icon='FILE_3D')


classes = [
    WB_PT_CreatePanel
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