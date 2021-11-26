from types import LambdaType
import bpy

class MAIN_PT_panel(bpy.types.Panel):
    bl_idname = 'MAIN_PT_panel'
    bl_label = 'test panel 1'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'test_UI_setter'

    def draw(self, context):
        if context.object.modifiers['Subdivision']:
            layout = self.layout
            col = layout.column()
            row = col.row()
            row.prop(context.object, 'test_single_prop')
            # bpy.context.object.modifiers['Subdivision'].levels = context.object.test_single_prop
            row = col.row()
            row.prop(context.object, 'test_enum_single_prop')


class modifier_OT_recorder(bpy.types.Operator):
    bl_idname = 'object.proprecorder'
    bl_label = 'record the prop'

    def execute(self, context):
        pass

    def invoke(self, context, event):
        pass


classes = [MAIN_PT_panel,
            modifier_OT_recorder]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.test_single_prop = bpy.props.IntProperty(name='single int prop', min=0, max=15, default=0)
    bpy.types.Object.test_enum_single_prop = bpy.props.EnumProperty(
        items=(
            ('1', '1', ''),
            ('2', '2', ''),
            ('3', '3', ''),
        )
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()