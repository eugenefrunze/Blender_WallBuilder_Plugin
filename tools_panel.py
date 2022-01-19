import bpy
from . import operators
from . import test




class WB_PT_CreatePanel(bpy.types.Panel):
    bl_idnname = 'VIEW3D_PT_tools_panel'
    bl_label = 'Tools and parameters panel'
    bl_category = 'TOOLS & PROPS'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        if context.object:
            row = col.row()
            row.label(text=f'OBJECT: {context.object.name}')

            row = col.row()
            row.label(text=f'GLOBAL TYPE: {context.object.props.type}')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='PARAMETERS')

        row = col.row()
        row.operator(operators.ExtraCurvesEnabler.bl_idname, text='ENABLE EXTRA CURVES', icon='MOD_CURVE')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='CREATE OBJECTS')

        row = col.row()
        row.operator(operators.CurveAdder.bl_idname, text='ADD CURVE', icon='MOD_CURVE')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='OPENINGS TOOLS')

        row = col.row()
        row.operator(operators.BoundingsHaldler.bl_idname, text='CREATE BOUNDS', icon='FILE_3D')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='MEASURES TOOLS')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='FBX IMPORTER')

        row = col.row()
        row.prop(context.scene.props, 'library_fbx_import_path')

        row = col.row()
        row.operator(operators.FBXLibraryImporter.bl_idname, text='IMPORT FBX', icon='DECORATE_DRIVER')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='Test Modal Operator')

        row = col.row()
        row.operator(operators.OT_TestModalOperator.bl_idname, text='Test Modal Operator')

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='OT_TestGPUDrawer')

        row = col.row()
        row.operator(operators.OT_TestGPUDrawer.bl_idname, text='OT_TestGPUDrawer')


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