from posixpath import pardir
from typing import ContextManager
import bpy
import time
import sys
import os
import importlib



# import bs4
sys.path.append('C:\\Users\\miloslavsky\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages')
from bs4 import BeautifulSoup

#append plugin dir
sys.path.append('C:\\code\\big_blender_plugin')
import plugin_types
obj_params = plugin_types.svg_attribs
obj_types = plugin_types.objects_types
print(obj_params)
print(obj_types)

# intro
print('==============================')
print('ENTER THE SCRIPT')
print('------------------------------')

# timer init
start_time = time.time()

# script info
bl_info = {
    "name": "SVG_Handler_tool"
}

#tool methods
def get_main_walls(floor: str):
    return bpy.data.objects['walls_base']

# panel
class SCENE_PT_MainPanel(bpy.types.Panel):
    bl_idname = "SCENE_PT_SVG_handler_panel"
    bl_label = "SVG Handler"
    bl_category = "SVG Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text='Welcome to SVG tools')
        layout.prop(context.scene, 'svg_floorplan')
        layout.operator(SVGHandlerOperator.bl_idname, icon='EXPERIMENTAL')

#operators
class SVGHandlerOperator(bpy.types.Operator):
    bl_idname = 'object.svg_handler_operator'
    bl_label = 'Work with SVG'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #soup
        if context.scene.svg_floorplan:
            svg_path = os.path.join(os.path.dirname(bpy.data.filepath), os.path.basename(context.scene.svg_floorplan))
            print(f'THE SVG PATH IS: {svg_path}')
            bpy.ops.import_curve.svg(filepath=svg_path, filter_glob='*.svg')
            f = open(svg_path)
            svg_string = f.read()
            soup = BeautifulSoup(svg_string, 'xml')
            print(soup.find_all('path')[1].get('bbp_type'))
            
        #     #set attribs to object
            for path in soup.find_all('path'):
                id = path.get('id')
                if id in bpy.data.objects.keys():
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = bpy.data.objects[id]
                    obj = bpy.context.object
                    obj.select_set(True)
                    print('----------')
                    print(obj)
                    obj.b_type = path.get(obj_params['type'])
                    obj.b_height = float(path.get(obj_params['height']))
                    obj.b_level = path.get(obj_params['level'])
                    obj.b_elevation = float(path.get(obj_params['elevation']))
                    print(obj.b_type)
                    print(obj.b_height)
                    print(obj.b_level)
                    print(obj.b_elevation)
                    print('----------')
                    #convert to mesh
                    bpy.ops.object.convert(target='MESH')

                    #extrude
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                    bpy.ops.mesh.select_mode(type='FACE')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.tris_convert_to_quads()
                    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False},TRANSFORM_OT_translate={"value":(0, 0, (obj.b_height / 1000)), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True)})
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    #elevate
                    bpy.ops.transform.translate(value=(0, 0, obj.b_elevation / 1000), orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                    #deselect
                    bpy.data.objects[id].select_set(False)

            #join all holes in walls
            holes_objects = [] #objects to join as holes
            for obj in bpy.data.objects:
                if obj.b_type in obj_types:
                    holes_objects.append(obj)
            context_holes = bpy.context.copy() #create context for join operation
            context_holes['active_object'] = holes_objects[0]
            context_holes['selected_editable_objects'] = holes_objects
            bpy.ops.object.join(context_holes)
            holes_object = context_holes['active_object']
            # print(holes_object)

            #===========================debug code here =================================#

            #get all wall_base objects
            walls_base = []
            for obj in bpy.data.objects:
                if obj.b_type == 'wall_base':
                    walls_base.append(obj)
            context_walls_base = bpy.context.copy()
            context_walls_base['active_object'] = walls_base[0]
            context_walls_base['selected_editable_objects'] = walls_base
            bpy.ops.object.join(context_walls_base)
            the_walls = context_walls_base['active_object']
            bpy.ops.object.modifier_add(context_walls_base, type='BOOLEAN')
            the_walls.modifiers["Boolean"].object = holes_object
            bpy.ops.object.modifier_apply(context_walls_base, modifier="Boolean", report=True)
            # bpy.context.view_layer.objects.active = holes_object
            bpy.ops.object.select_all(action='DESELECT')
            holes_object.select_set(True)
            bpy.ops.object.delete(use_global=False, confirm=False)

            #place win-doors
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = bpy.data.objects['dr1']
            # bpy.data.objects['dr1'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.736767, 0.794722, 0)
            # bpy.ops.object.select_all(action='DESELECT')

            bpy.context.view_layer.objects.active = bpy.data.objects['dr2']
            bpy.data.objects['dr2'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.375131, 0.0138236, 0)
            bpy.ops.object.select_all(action='DESELECT')


            bpy.context.view_layer.objects.active = bpy.data.objects['dr3']
            bpy.data.objects['dr3'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.0145002, 0.553633, 0.27)
            bpy.ops.object.select_all(action='DESELECT')



            bpy.context.view_layer.objects.active = bpy.data.objects['w1']
            bpy.data.objects['w1'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.140013, 0.0144971, 0.090002)
            bpy.ops.object.select_all(action='DESELECT')



            bpy.context.view_layer.objects.active = bpy.data.objects['w2']
            bpy.data.objects['w2'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.787016, 0.0144971, 0.090002)
            bpy.ops.object.select_all(action='DESELECT')



            bpy.context.view_layer.objects.active = bpy.data.objects['w3']
            bpy.data.objects['w3'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.918518, 0.554657, 0.415973)
            bpy.ops.object.select_all(action='DESELECT')


            bpy.context.view_layer.objects.active = bpy.data.objects['w5']
            bpy.data.objects['w5'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.918518, 0.252715, 0.415973)
            bpy.ops.object.select_all(action='DESELECT')


            bpy.context.view_layer.objects.active = bpy.data.objects['w6']
            bpy.data.objects['w6'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.0157798, 0.417205, 0.144973)
            bpy.ops.object.select_all(action='DESELECT')


            bpy.context.view_layer.objects.active = bpy.data.objects['w7']
            bpy.data.objects['w7'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.163003, 0.793348, 0.090002)
            bpy.ops.object.select_all(action='DESELECT')


            bpy.context.view_layer.objects.active = bpy.data.objects['w8']
            bpy.data.objects['w8'].select_set(True)
            bpy.context.object.hide_viewport = False
            bpy.context.object.location = (0.388008, 0.793348, 0.090002)
            bpy.ops.object.select_all(action='DESELECT')

            bpy.context.view_layer.objects.active = bpy.data.objects['roof_import']
            bpy.context.object.location = (0, 0.8065, 0.345)

            bpy.context.view_layer.objects.active = bpy.data.objects['walls_inner_import']
            bpy.context.object.location = (0.568648, 0.790926, 0.125)



            #===========================debug code end =================================#




        else:
            self.report({'WARNING'}, f'YOU HAVEN\'T SPECIFIED SVG FILE HONEY')
            return{'FINISHED'}

        


        self.report({'INFO'}, f'{self.bl_idname} HAS EXECUTED')
        return{'FINISHED'}



classes = {
    SCENE_PT_MainPanel,
    SVGHandlerOperator
}

# register
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.svg_floorplan = bpy.props.StringProperty(
        name = 'floorplan file',
        subtype='FILE_PATH'
    )

    bpy.types.Object.b_type = bpy.props.StringProperty(
        name='type of the floorplan object',
        default=''
    )

    bpy.types.Object.b_level = bpy.props.StringProperty(
        name='level of the floorplan object',
        default=''
    )

    bpy.types.Object.b_height = bpy.props.FloatProperty(
        name='height of the floorplan object',
        default=0
    )

    bpy.types.Object.b_elevation = bpy.props.FloatProperty(
        name='elevation of the floorpan object',
        default=0
    )

    # bpy.types.Object.someA = bpy.props.PointerProperty

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.b_height
    del bpy.types.Object.b_level
    del bpy.types.Object.b_type

if __name__ == "__main__":
    register()

# time print
print(f'TIME HAS TAKEN TO LOAD: %.2f' % (time.time() - start_time))