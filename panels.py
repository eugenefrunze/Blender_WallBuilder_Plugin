from ast import operator
import bpy
from . import operators


#---------------------------------------------------------------------------------------------------
# wall builder panel
#---------------------------------------------------------------------------------------------------

class WBPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_MainMenu'
    bl_label = 'wall builder panel'
    bl_category = 'WALL BUILDER'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def get_object_buttons(self, layout): # ------------$%&5756&7 what is this? --------------------
        row = layout.row()
        props = row.operator(operators.WallBuilder.bl_idname)


    # template for header
    # def draw_header(self, context):
    #         layout = self.layout
    #         layout.label(text="MY TEST HEADER")
    #         layout.prop(context.object.wb_props, 'height')


    def draw(self, context):
        layout = self.layout
        if context.object:
            col = layout.column()
            
            # tex = bpy.data.textures['jopa']
            # col.template_preview(tex, show_buttons=False)

            # row = col.row()
            # row.operator(operators.CustomersBaseHandler.bl_idname, text='GET CUSTOMERS INFO')

            row = col.row()
            row.label(text='OBJECT: {} ({})'.format(context.object.name, context.object.type))
            
            box = layout.box()
            col = box.column()
            row = col.row()
            row.label(text='OBJECT PROPS:')

            row = col.row()
            row.prop(context.object.wb_props, 'customer')

            row = col.row()
            row.prop(context.object.wb_props, 'object_type')

            #IF WALL
            if context.object.wb_props.object_type == 'WALL':

                row = col.row()
                row.prop(context.object.wb_props, 'level')

                #geom nodes props
                row = col.row()
                modif_geom_nodes = context.object.modifiers.get('wb_geom_nodes')
                
                row = col.row()
                row.prop(context.object.wb_props, 'height')
                
                row = col.row()
                row.prop(context.object.wb_props, 'thickness')

                row = col.row()
                row.prop(context.object.wb_props, 'position', text='wall position (ex. photoshop stroke')

                row = col.row()

                try:
                    spline = context.object.data.splines[0]
                except AttributeError:
                    pass
                else:
                    row.prop(spline, 'use_cyclic_u', text='close wall shape')
                    
                row = col.row()
                row.prop(context.object.wb_props, 'is_inner_wall')

                #CONVERT OR RESET THE OBJECT -------------------------------------------------------
                if context.object.wb_props.is_converted:
                    row = col.row()
                    row.operator(operators.WallBuilder.bl_idname, text='RESET WALL', icon='CANCEL')
                else:
                    row = col.row()
                    props = row.operator(operators.WallBuilder.bl_idname, text='CONVERT WALL', icon='SHADERFX')

                #IF OBJECT HAS OPENINGS ------------------------------------------------------------
                if context.object.wb_props.is_converted:
                    box = layout.box()
                    col = box.column()
                    row = col.row()
                    row.label(text='OPENINGS:')
                    row = col.row()
                    row.template_list('OPENINGS_UL_Item', '', bpy.context.object, 'openings', bpy.context.object, 'opening_index', rows=1)

                    row = col.row(align=True)
                    
                    row.operator('object.opnenings_adder', text='ADD OPENINGS').action = 'ADD'
                    row.operator('object.opnenings_adder', text='REMOVE OPENING').action = 'REMOVE'
                    row.operator('object.opnenings_adder', icon='TRIA_UP', text='').action = 'UP'
                    row.operator('object.opnenings_adder', icon='TRIA_DOWN', text='').action = 'DOWN'
                    
                    col = box.column()
                    
                    col.row().operator(operators.BoundingsHaldler.bl_idname, text='CREATE OPENING BOUNDS', icon='FILE_3D')
                    col.row().operator(operators.OpeningsAttacher.bl_idname, text='ATTACH / DETACH OPENINGS')                    
                    col.row().operator(operators.OpeningsAligner.bl_idname, text='ALIGN OPENINGS')
                    
                    
            #IF OPENING
            elif context.object.wb_props.object_type == 'OPENING':
                row = col.row()
                row.prop(context.object.wb_props, 'opening_type')

            #IF HELPER
            elif context.object.wb_props.object_type == 'HELPER':
                row = col.row()
                row.prop(context.object. wb_props, 'helper_type')

            #IF FLOOR
            elif context.object.wb_props.object_type == 'FLOOR':
                row = col.row()
                row.prop(context.object.wb_props, 'level')
                row = col.row()
                row.prop(context.object.wb_props, 'height', text='Floor height')

                if context.object.wb_props.is_converted:
                    row = col.row()
                    row.operator(operators.WallBuilder.bl_idname, text='RESET FLOOR', icon='CANCEL')
                else:
                    row = col.row()
                    props = row.operator(operators.WallBuilder.bl_idname, text='CONVERT FLOOR', icon='SHADERFX')

            box = layout.box()
            col = box.column()
            row=col.row()
            row.label(text='WALL BUILDER TOOLS')

            #SNAPPING CAST
            # row = col.row()
            # if context.object.wb_props.snapping_cast and context.object.wb_props.object_type == 'WALL':
            #     row.label(text=f'CAST OBJECT: {context.object.wb_props.snapping_cast.name}')
            #     row = col.row()
            #     row.operator(operators.SnappingCopyHandler.bl_idname, text='REMOVE SNAPPING CAST').action = 'REMOVE'
            # elif context.object.wb_props.object_type == 'WALL':
            #     row.operator(operators.SnappingCopyHandler.bl_idname, text='CREATE CAST FOR SNAPPING').action = 'ADD'

            #MAIN CAST
            row = col.row()
            if context.object.wb_props.object_type == 'WALL':
                row.operator(operators.MainCastHandler.bl_idname, text='CREATE CAST', icon='SHADERFX').action = 'ADD'
            elif context.object.wb_props.object_type == 'HELPER' and context.object.wb_props.cast_source:
                row.label(text=f'SOURCE OBJECT: {context.object.wb_props.cast_source}')
                row = col.row()
                row.operator(operators.MainCastHandler.bl_idname, text='REMOVE CAST', icon='CANCEL').action = 'REMOVE'

            box = layout.box()
            col = box.column()
            row=col.row()
            row.label(text='AUTO ASSEMBLER PROPS:')
            

            row=col.row()
            plans_collection = row.prop(data=context.scene.wb_props,property='plans_collection', slider=True)

            row = col.row()
            row.prop(data=context.scene.wb_props,property='alignment_object', slider=True)

            row = col.row()
            row.operator(operators.BuildingAssembler.bl_idname, text='ASSEMBLE THE BUILDING')


# openings item format
class OPENINGS_UL_Item(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split()
        split.label(text=f'opening idx: {index}')
        # split.prop(item, 'name', text='', emboss='false', translate='false', icon='EXPERIMENTAL')
        split.label(text=item.obj.name, icon='EXPERIMENTAL')

    def invoke(self, context, ivent):
        pass


#---------------------------------------------------------------------------------------------------
# tools panel
#---------------------------------------------------------------------------------------------------

class TPanel(bpy.types.Panel):
    bl_idnname = 'VIEW3D_PT_tools_panel'
    bl_label = 'Tools and parameters panel'
    bl_category = 'TOOLS & PROPS'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        box = layout.box()
        col = box.column()
        row = col.row()
        row.label(text='FAST OBJECTS')

        row = col.row()
        row.prop(context.scene.tools_props, 'fast_object_type')

        if context.scene.tools_props.fast_object_type == 'RECTANGLE':
            row = col.row(align=False)
            row.prop(context.scene.tools_props, 'new_length')
            row.prop(context.scene.tools_props, 'new_width')
        elif context.scene.tools_props.fast_object_type == 'LINE':
            row = col.row()
            row.prop(context.scene.tools_props, 'new_length')

        row = col.row()
        row.operator(operators.CurveAdder.bl_idname, text='ADD OBJECT', icon='MOD_CURVE').curve_type = \
        context.scene.tools_props.fast_object_type
        
        try:
            spline = context.object.data.splines[0]
        except AttributeError:
            pass
        else:
            row = col.row()
            row.prop(spline, 'use_cyclic_u', text='close wall shape')

        #openings tools group
        box = layout.box()
        col = box.column()
        col.row().label(text='OPENINGS PROPERTIES')

        box = layout.box()
        col = box.column()
        col.row().label(text='TEST PROPERTIES')
        
        col.row().operator(operators.ExtraCurvesEnabler.bl_idname, text='ENABLE EXTRA CURVES', icon='MOD_CURVE')
        
        col.row().prop(bpy.data.scenes["Scene"].unit_settings, 'length_unit', text='global units')
        
        col.row().prop(context.scene.props, 'library_fbx_import_path', text='fbx path')
        
        col.row().operator(operators.FBXLibraryImporter.bl_idname, text='IMPORT FBX', icon='DECORATE_DRIVER')
        
                
        box = layout.box()
        col = box.column()
        col.row().label(text='OPENGL FEATURES')
        
        col.row().operator(operators.OT_TestGPUDrawer.bl_idname, text='MESH SIZE DRAWER')
        col.row().operator(operators.OT_SizesDrawer.bl_idname, text='DISTANCE BETWEEN CURVE POINTS')
        col.row().operator(operators.OT_DistBetweenObjects.bl_idname, text='DISTANCE BETWEEN OBJECTS')
        col.row().prop(context.scene.props, 'opengl_font_size')


#---------------------------------------------------------------------------------------------------
# register / unregister
#---------------------------------------------------------------------------------------------------

def register():
    from bpy.utils import register_class

    # wall builder panel
    register_class(WBPanel)
    register_class(OPENINGS_UL_Item)

    #tools panel
    register_class(TPanel)
 

def unregister():
    from bpy.utils import unregister_class

    #wall builder panel
    unregister_class(WBPanel)
    unregister_class(OPENINGS_UL_Item)

    #tools panel
    unregister_class(TPanel)
