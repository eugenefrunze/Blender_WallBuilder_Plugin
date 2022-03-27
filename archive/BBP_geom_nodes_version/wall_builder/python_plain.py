import bpy

class OpeningsListItem(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.3)
        split.label(text='Index: %d' % (index))
        split.label(text=item.name, icon='EXPERIMENTAL')

    def invoke(self, context, event):
        pass   

class OpeningsListPanel(bpy.types.Panel):
    bl_idname = 'TEXT_PT_my_panel'
    bl_category = 'C7 WALL BUILDER'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Custom Object List Demo"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        row = layout.row()
        row.template_list("OpeningsListItem", "", scn, "custom", scn, "custom_index", rows=2)

class TestShitCollection(bpy.types.PropertyGroup):
    some1: bpy.props.StringProperty()
    some2: bpy.props.IntProperty()



classes = (
    OpeningsListItem,
    OpeningsListPanel,
    TestShitCollection
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Custom scene properties
    bpy.types.Scene.custom_index = bpy.props.IntProperty()
    bpy.types.Scene.custom = bpy.props.CollectionProperty(type=TestShitCollection)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()