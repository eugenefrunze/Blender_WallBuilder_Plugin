import bpy
from bpy.props import EnumProperty

class SomeJopaClass(bpy.types.Operator):
    bl_idname = 'object.some_maker'
    bl_label = 'jopa maker script'
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'my_enum'

    my_enum: EnumProperty(
        name="My Search",
        items=(
            ('FOO', "Foo", ""),
            ('BAR', "Bar", ""),
            ('BAZ', "Baz", ""),
        ),
    )

    def execute(self, context):
        print(str(self))
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, 'my_enum')

        col = layout.column()
        col.label(text='some text here')

bpy.utils.register_class(SomeJopaClass)

bpy.ops.object.some_maker('INVOKE_DEFAULT')
