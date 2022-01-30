import bpy

class PT_TEST_PANEL(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_TEST_PANEL'
    bl_label = 'test panel'
    bl_category = 'TEST PANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row = col.row()
        # row.prop(context.object.test_govno, 'test_float_1')

        row = col.row()
        row.operator(TEST_Operator.bl_idname)

        TEST_PropGroup.draw(self, context)


class TEST_PropGroup(bpy.types.PropertyGroup):

    def get_a(self):
        return 50

    a: bpy.props.IntProperty(
        default=0,
        get = lambda self: self.get_a()
    )

    def get_f(self):
        print(self['test_float_1'])
        return self['test_float_1']

    def set_f(self, value):
        self['test_float_1'] = 700

    test_float_1: bpy.props.FloatProperty(
        default=732.0,
        name = 'test_float',
        unit='LENGTH',
        get = lambda self: self.get_f(),
        set = lambda self, val: self.set_f(val)
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text='sraka')
        box.label(text=str(context.object.test_govno.a))


    

class TEST_Operator(bpy.types.Operator):
    bl_idname = 'object.test_operator83'
    bl_label = 'CALL VALUE'
    bl_options = {'REGISTER'}

    if_set: bpy.props.BoolProperty()

    # a: bpy.props.FloatProperty(name='joppa',
    # get = lambda self: self.test_return_method())

    def execute(self, context):
        p = context.object.test_govno.test_float_1
        context.object.test_govno.test_float_1 = 10

        # print(str(p) + 'AAAA')
        # self.a
        return {'FINISHED'}

def register():
    from bpy.utils import register_class

    register_class(PT_TEST_PANEL)
    register_class(TEST_Operator)
    register_class(TEST_PropGroup)

    bpy.types.Object.test_govno = bpy.props.PointerProperty(type=TEST_PropGroup)



def unregister():
    from bpy.utils import unregister_class

    unregister_class(PT_TEST_PANEL)
    unregister_class(TEST_Operator)
    unregister_class(TEST_PropGroup)

    del bpy.types.Object.test_govno