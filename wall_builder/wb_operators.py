import bpy
from bpy.ops import node
from bpy.props import CollectionProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import NodeGroup
import data_types
import blf
import gpu
from gpu_extras.batch import batch_for_shader
import utils

#BLF TEXT DRAWING ----------------------------------------------------------------------------------

class DrawLine():
    def __init__(self):
        self.handler = None

    def draw(self, coords):
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.shader.bind()
        self.shader.uniform_float("color", (1, 1, 0, 1))
        self.batch = batch_for_shader(self.shader, 'LINES', {"pos": coords})
        self.batch.draw(self.shader)

    def start_handler(self, context):
        self.handler = bpy.types.SpaceView3D.draw_handler_add(self.draw, ([(0, 0, 0), context.object.location],), 'WINDOW', 'POST_VIEW')

    def remove_handler(self):
        bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')

class DrawTextClass():

    def __init__(self, context):
        self.handler = None

    def draw_callback_px(self, context):
        font_id = 0
        blf.position(font_id, 1, 1, 0)
        # blf.rotation(font_id, 90)
        ui_scale = bpy.context.preferences.system.ui_scale
        # blf.size(font_id, int(0 * bpy.context.preferences.view.ui_scale), int((72 * bpy.context.preferences.system.dpi)))
        blf.size(font_id, 1, int((72 * bpy.context.preferences.system.dpi)))
        blf.draw(font_id, context.object.name)

    def draw(self, context):
        self.handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, (context,), 'WINDOW', 'POST_PIXEL')

    def remove_handler(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')

#getting the DrawtTextClass from the namespace
drawtextclass = DrawTextClass(bpy.context)
dns = bpy.app.driver_namespace
dns['drawtextclass'] = drawtextclass

dns['drawlineobj'] = DrawLine()


#WALL BUILDER --------------------------------------------------------------------------------------
class WallBuilder(bpy.types.Operator):
    bl_idname = 'object.wall_builder'
    bl_label = 'GANERATOR HANDLER'
    bl_options = {'REGISTER', 'UNDO'}

    is_reset: bpy.props.BoolProperty()

    wall_profile_curve: bpy.types.Object

    handler1 = 0

    def set_customer_preset(self, context):
        obj_converted = context.object
        if obj_converted.wall_builder_props.object_type == 'WALL':
            for customer in data_types.customers_json:
                if customer['ucm_id'] == obj_converted.wall_builder_props.customer:
                    obj_converted.wall_builder_props.height = float(customer['wall_height']) / 1000
                    if self.is_inner_wall:
                        obj_converted.wall_builder_props.thickness = float(customer['wall_in_thickness']) / 1000
                    else:
                        obj_converted.wall_builder_props.thickness = float(customer['wall_out_thickness']) / 1000
        elif obj_converted.wall_builder_props.object_type == 'FLOOR':
            for customer in data_types.customers_json:
                if customer['ucm_id'] == obj_converted.wall_builder_props.customer:
                    obj_converted.wall_builder_props.height = float(customer['ceiling']) / 1000

    def set_wall_position(self, context):
        if context.active_object.wall_builder_props.object_type == 'WALL':
            height: float
            thickness: float
            if self.__class__.__name__ == 'WBProps':
                height = self.height
                thickness = self.thickness
            else:
                height = context.object.wall_builder_props.height
                thickness = context.object.wall_builder_props.thickness            

            #getting references for all points of the wallshape
            points = []
            for point in context.active_object.data.bevel_object.data.splines[0].points:
                points.append(point)

            if context.object.wall_builder_props.position == 'INSIDE':
                #1st point
                points[0].co[0] = 0
                points[0].co[1] = height
                #2nd point
                points[1].co[0] = thickness
                points[1].co[1] = height
                #3rd point
                points[2].co[0] = thickness
                points[2].co[1] = 0
                #4th point
                points[3].co[0] = 0
                points[3].co[1] = 0

            elif context.object.wall_builder_props.position == 'CENTER':
                #1st point
                points[0].co[0] = -(thickness/2)
                points[0].co[1] = height
                #2nd point
                points[1].co[0] = thickness/2
                points[1].co[1] = height
                #3rd point
                points[2].co[0] = thickness/2
                points[2].co[1] = 0
                #4th point
                points[3].co[0] = -(thickness/2)
                points[3].co[1] = 0

            elif context.object.wall_builder_props.position == 'OUTSIDE':
                #1st point
                points[0].co[0] = -thickness
                points[0].co[1] = height
                #2nd point
                points[1].co[0] = 0
                points[1].co[1] = height
                #3rd point
                points[2].co[0] = 0
                points[2].co[1] = 0
                #4th point
                points[3].co[0] = -thickness
                points[3].co[1] = 0


    def generate_object(self, context) -> list:
        obj_converted = context.object
        obj_conv_collection = obj_converted.users_collection[0]
        if obj_converted.wall_builder_props.object_type == 'WALL':
            #setting object base parameters
            obj_converted.name = 'wb_wall'
            obj_converted.data.dimensions = '2D'
            #geometry nodes modifier
            geom_nodes_mod = bpy.context.object.modifiers.new("wb_geom_nodes", 'NODES')
            node_group = geom_nodes_mod.node_group
            node_group.name = '{}_geom_nodes_node_group'.format(obj_converted.name)
            #creating nodes
            nd_input = node_group.nodes['Group Input']
            nd_output = node_group.nodes['Group Output']
            nd_set_shade_smooth = node_group.nodes.new(type="GeometryNodeSetShadeSmooth")
            nd_bool_openings = node_group.nodes.new(type="GeometryNodeMeshBoolean")
            #setting params
            nd_output.location = (500, 0)
            nd_set_shade_smooth.inputs[2].default_value = False
            nd_bool_openings.name = 'mrBoolshit'
            nd_bool_openings.location = (300, -100)
            #create links
            nd_input.outputs.clear()
            nd_output.outputs.clear()
            utils.node_group_link(node_group, nd_input.outputs['Geometry'], nd_set_shade_smooth.inputs['Geometry'])
            utils.node_group_link(node_group, nd_set_shade_smooth.outputs['Geometry'], nd_bool_openings.inputs['Mesh 1'])
            utils.node_group_link(node_group, nd_output.inputs['Geometry'], nd_bool_openings.outputs['Mesh'])
            #shape curve from here
            bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple_Type='Rectangle', Simple_width=1, Simple_length=0, use_cyclic_u=True)
            obj_profile = context.object
            obj_converted.wall_builder_props.wall_profile_curve = obj_profile
            obj_profile.name = f'{obj_converted.name}_taper'
            obj_profile_data = obj_profile.data
            obj_profile_data.fill_mode = 'NONE'
            bpy.ops.curve.spline_type_set(type='POLY')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.collection.objects_remove_active()
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = obj_converted
            obj_converted.data.bevel_mode = 'OBJECT'
            obj_converted.data.bevel_object = obj_profile
            #set the sizes of newly generated wall
            self.set_wall_position(context)
            obj_converted.wall_builder_props.is_converted = True

        elif obj_converted.wall_builder_props.object_type == 'OPENING':
            pass

        elif obj_converted.wall_builder_props.object_type == 'FLOOR':
            #setting object base parameters
            obj_converted.data.bevel_mode = 'ROUND'
            obj_converted.data.extrude = obj_converted.wall_builder_props.height
            obj_converted.data.fill_mode = 'BOTH'
            #geometry nodes modifier
            geom_nodes_mod = bpy.context.object.modifiers.new("wb_geom_nodes", 'NODES')
            node_group = geom_nodes_mod.node_group
            node_group.name = '{}_geom_nodes_node_group'.format(obj_converted.name)
            #creating nodes
            nd_input = node_group.nodes['Group Input']
            nd_output = node_group.nodes['Group Output']
            nd_set_shade_smooth = node_group.nodes.new(type="GeometryNodeSetShadeSmooth")
            #setting params
            nd_output.location = (500, 0)
            nd_set_shade_smooth.inputs[2].default_value = False
            #create links
            utils.node_group_link(node_group, nd_input.outputs['Geometry'], nd_set_shade_smooth.inputs['Geometry'])
            utils.node_group_link(node_group, nd_output.inputs['Geometry'], nd_set_shade_smooth.outputs['Geometry'])
            #set object as converted in wall_builder_props
            obj_converted.wall_builder_props.is_converted = True


    def reset_object(self, obj: bpy.types.Object):
        if obj.wall_builder_props.object_type == 'WALL':
            #remove the geom nodes modifier
            try:
                geom_nodes_mod = obj.modifiers['wb_geom_nodes']
            except KeyError:
                print('OBJECT HAD NO wb_geom_nodes MODIFIER')
            else:
                obj.modifiers.remove(geom_nodes_mod)
            #deleting the profile curve
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.data.bevel_object = None
            bpy.ops.object.select_all(action='DESELECT')
            try:
                if obj.wall_builder_props.wall_profile_curve:
                    obj.wall_builder_props.wall_profile_curve.select_set(True)
            except RuntimeError:
                pass
            else:
                bpy.ops.object.delete()
            obj.select_set(True)
            obj.wall_builder_props.wall_profile_curve = None
            #clearing the fill mode if obj previously was a floor
            obj.data.fill_mode = 'NONE'
            #clearing the openings list
            obj.openings.clear()
            obj.opening_index = -1
            #setting the object is not converted
            obj.wall_builder_props.is_converted = False

        elif obj.wall_builder_props.object_type == 'FLOOR':
            #if object has geom nodes modifier (ex. prev was floor)
            try:
                geom_nodes_mod = obj.modifiers['wb_geom_nodes']
            except KeyError:
                print('OBJECT HAD NO wb_geom_nodes MODIFIER')
            else:
                obj.modifiers.remove(geom_nodes_mod)
            #setting the spline parameters
            obj.data.extrude = 0
            obj.data.fill_mode = 'NONE'
            obj.wall_builder_props.is_converted = False

 

    #CLASS METHODS HERE
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'CURVE'

    def execute(self, context):
        obj = context.object
        # dns = bpy.app.driver_namespace
        # drawtextclass = dns.get('drawtextclass')
        if obj.wall_builder_props.is_converted:

            # if dns.get('drawlineobj').handler is not None:
            #     dns.get('drawlineobj').remove_handler()
            #     dns.get('drawlineobj').handler = None

            # if drawtextclass.handler is not None:
            #     drawtextclass.remove_handler(context)
            #     drawtextclass.handler = None
            self.reset_object(obj)
            self.report({'INFO'}, 'OBJECT HAS BEEN RESET')
            return {'FINISHED'}
        else:
            # if dns.get('drawlineobj').handler == None:
            #     dns.get('drawlineobj').start_handler(context)

            # if drawtextclass.handler == None:
            #     drawtextclass.draw(context)
            self.generate_object(context)
            self.report({'INFO'}, 'OBJECT GENERATED')
            return {'FINISHED'}

#END OF WALLBUILDER OPERATOR
        

#BUILDING ASSEMBLER --------------------------------------------------------------------------------
class BuildingAssembler(bpy.types.Operator):
    bl_idname = 'object.building_assembler'
    bl_label = 'ASSEMBLE THE BUILDING'
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def get_assembly_coords():
        return (0, 0, 0)

    @staticmethod
    def generate_first_floor(context):

        #list of objects
        eg_wall_outer: bpy.types.Object
        og_floor: bpy.types.Object
        og_wall_outer: bpy.types.Object

        wb_objects = context.scene.wall_builder_scene_props.plans_collection.objects
        ass_coords = BuildingAssembler.get_assembly_coords()
        for object in wb_objects:
            for obj in wb_objects:
                if obj.wall_builder_props.level == 'EG' and obj.wall_builder_props.object_type == 'WALL':
                    eg_wall_outer = obj
                elif obj.wall_builder_props.level == 'OG' and obj.wall_builder_props.object_type == 'FLOOR':
                    og_floor = obj
                elif obj.wall_builder_props.level == 'OG' and obj.wall_builder_props.object_type == 'WALL':
                    og_wall_outer = obj


        #work with walls
        eg_wall_outer.location = ass_coords

        #work with OG floor
        print(eg_wall_outer.dimensions)
        og_floor.location = (ass_coords[0], ass_coords[1], eg_wall_outer.dimensions[2] + og_floor.wall_builder_props.height / 2)

        #work with OG wall
        og_wall_outer.location = (ass_coords[0], ass_coords[1], eg_wall_outer.dimensions[2] + og_floor.wall_builder_props.height)



    @staticmethod
    def generate_second_floor(context):
        pass

    def execute(self, context):
        BuildingAssembler.generate_first_floor(context)
        self.report({'INFO'}, 'BUILDING ASSEMBLER: {}'.format(self.bl_label))
        return {'FINISHED'}


#OPENINGS LIST HANDLER OPERATOR --------------------------------------------------------------------
class OpeningsHandler(bpy.types.Operator):
    bl_idname = "custom.add_openings"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.custom) - 1:
                item_next = scn.custom[idx+1].name
                scn.custom.move(idx, idx+1)
                scn.custom_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.custom[idx-1].name
                scn.custom.move(idx, idx-1)
                scn.custom_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.custom[idx].name)
                scn.custom_index -= 1
                scn.custom.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            if context.object:
                item = scn.custom.add()
                item.name = context.object.name
                item.obj_type = context.object.type
                item.obj_id = len(scn.custom)
                scn.custom_index = len(scn.custom)-1
                info = '"%s" added to list' % (item.name)
                self.report({'INFO'}, info)
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}

class OpeningsAdder(bpy.types.Operator):
    bl_idname = "object.opnenings_adder"
    bl_label = "mrlist"

    action: bpy.props.EnumProperty(
        items=(
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def add_opening_to_geom_nodes(self, construction, opening, location):
        '''construction - actual building element to add openings to'''
        try:
            modifier = construction.modifiers['wb_geom_nodes']
        except KeyError:
            print('CONSTRUCTION OBJECT HAS NO GEOM NODES MODIFIER')
        else:
            #getting node group if modif exists
            node_group = modifier.node_group
            #adding opening as object info node
            info_node = node_group.nodes.new(type="GeometryNodeObjectInfo")
            #setting the parameters
            info_node.inputs[0].default_value = opening
            info_node.transform_space = 'RELATIVE'
            info_node.location = location
            #create links
            utils.node_group_link(node_group, info_node.outputs['Geometry'], node_group.nodes['mrBoolshit'].inputs['Mesh 2'])
            return info_node


    def remove_opening_from_geom_nodes(self, construction, info_obj: bpy.types.Object):
        '''construction - actual building element to remove opening from, info_obj - actual opening 
        object from the scene'''
        try:
            modifier = construction.modifiers['wb_geom_nodes']
        except KeyError:
            print('CONSTRUCTION OBJECT HAS NO GEOM NODES MODIFIER')
        else:
            node_group = modifier.node_group 
            nodes = node_group.nodes
            # nodes.remove(construction.openings.obj_id)
            for node in nodes:
                if node.type == 'OBJECT_INFO' and node.inputs[0].default_value == info_obj:
                    nodes.remove(node)
                    nd_bool_openings = node_group.nodes['mrBoolshit']
                    nd_output = node_group.nodes['Group Output']
                    utils.node_group_link(node_group, nd_output.inputs['Geometry'], nd_bool_openings.outputs['Mesh'])



        

    def invoke(self, context, event):
        '''nd_loc - initial location for the new obj info node'''
        obj = context.object
        idx = obj.opening_index
        if self.action == 'ADD':
            obj.select_set(False)
            nd_loc = [0, -200]
            for object in context.selected_objects:
                #check if opening is a duplicate
                if len(obj.openings) > 0:
                    for opening in obj.openings:
                        if object == opening.obj:
                            self.report({'WARNING'}, 'This object is already in the openings')
                            return {'CANCELLED'}
                #create new opening
                item = obj.openings.add()
                item.obj = object
                item.obj_id = len(obj.openings)
                obj.opening_index = len(obj.openings) - 1
                #putting the object to geom nodes modif
                self.add_opening_to_geom_nodes(obj, object, nd_loc)
                nd_loc[1] -= 200
                print(f'OPENING ADDED: {item.obj.name}')
            return {'FINISHED'}

        elif self.action == 'REMOVE':
            obj.opening_index -= 1
            #deleting object from geom nodes modifier and refreshing geom nodes modifier
            self.remove_opening_from_geom_nodes(obj, obj.openings[idx].obj)

            #removing opening from construction object
            obj.openings.remove(idx)
            return {'FINISHED'}

#OPENINGS LIST PROP GROUP (TEMP) -------------------------------------------------------------------
class CUSTOM_objectCollection(bpy.types.PropertyGroup):
    obj_type: StringProperty()
    obj_id: IntProperty()

class OpeningsCollection(bpy.types.PropertyGroup):
    obj: PointerProperty(type=bpy.types.Object)
    obj_id: IntProperty()


#REGISTERING ---------------------------------------------------------------------------------------
def register():
    from bpy.utils import register_class
    register_class(WallBuilder)
    register_class(BuildingAssembler)
    register_class(CUSTOM_objectCollection)
    register_class(OpeningsHandler)
    register_class(OpeningsCollection)
    register_class(OpeningsAdder)

    bpy.types.Scene.custom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.custom_index = IntProperty()

    bpy.types.Object.openings = CollectionProperty(type=OpeningsCollection)
    bpy.types.Object.opening_index = IntProperty()

def unregister():
    from bpy.utils import unregister_class
    unregister_class(WallBuilder)
    unregister_class(BuildingAssembler)
    unregister_class(CUSTOM_objectCollection)
    unregister_class(OpeningsHandler)
    unregister_class(OpeningsCollection)
    unregister_class(OpeningsAdder)

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

if __name__ == "__main__":
    register()

    