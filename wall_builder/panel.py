import bpy
import data_types
import wb_operators

class MainMenu(bpy.types.Panel):
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
            row.prop(context.object, 'customer')

            
            for param in data_types.properties:
                row = col.row()
                row.prop(context.object, param)
                row.label(text=param)

            row = col.row()
            props = row.operator(wb_operators.WallBuilder.bl_idname)

            col = layout.column()
            
            row = col.row()
            row.label(text='object\'s props editor')

            row = col.row()
            row.prop(context.object, 'opening_type')