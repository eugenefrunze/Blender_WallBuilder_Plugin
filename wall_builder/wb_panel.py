import bpy
import data_types
import wb_operators

class WBPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_MainMenu'
    bl_label = 'wall builder configurator'
    bl_category = 'C7 WALL BUILDER'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        if context.object:
            col = layout.column()

            row = col.row()
            row.label(text='active object: {} ({})'.format(context.object.name, context.object.type))

            col = layout.column()

            row = col.row()
            row.prop(context.object.wall_builder_props, 'customer')

            
            for param in data_types.properties:
                row = col.row()
                row.prop(context.object.wall_builder_props, param)
                row.label(text=param)

            row = col.row()
            props = row.operator(wb_operators.WallBuilder.bl_idname)

            col = layout.column()
            
            row = col.row()
            row.label(text='PROPS EDITOR')

            row = col.row()
            row.prop(context.object.wall_builder_props, 'object_type')

            row = col.row()
            row.prop(context.object.wall_builder_props, 'opening_type')
            
            row = col.row()
            row.prop(context.object.wall_builder_props, 'position')



def register():
    from bpy.utils import register_class
    register_class(WBPanel)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(WBPanel)

if __name__ == "__main__":
    register()