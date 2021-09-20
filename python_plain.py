import bpy

class MrMenu(bpy.types.Menu):
    bl_label = 'test jopa menu'
    bl_idname = 'OBJECT_MT_jopamenu'
    # bl_category = 'Jopa menu'
    # bl_space_type = 'VIEW_3D'
    # bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        layout.label(text='DOROU')
        layout.operator('wm.jopa_operator')


class SimpleJopaOperator(bpy.types.Operator):
    bl_idname='wm.jopa_operator'
    bl_label='invoke jopa operator'

    x: bpy.props.IntProperty()
    y: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        self.report({'INFO'}, f'mouse coords are: {self.x} {self.y}')
        return {'FINISHED'}

    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y =event.mouse_y
        return self.execute(context)


bpy.utils.register_class(SimpleJopaOperator)
bpy.utils.register_class(MrMenu)

# bpy.ops.wm.jopa_operator('INVOKE_DEFAULT')
# bpy.ops.wm.jopa_operator('EXEC_DEFAULT')
    