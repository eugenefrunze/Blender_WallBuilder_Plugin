import bpy
from bpy.props import CollectionProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import SelectedUvElement
# from . import wb_properties
from .. import data_types
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from .. import utils


# WALL BUILDER --------------------------------------------------------------------------------------
class WallBuilder(bpy.types.Operator):
    bl_idname = 'object.wall_builder'
    bl_label = 'GANERATOR HANDLER'
    bl_options = {'REGISTER', 'UNDO'}

    is_reset: bpy.props.BoolProperty()

    wall_profile_curve: bpy.types.Object

    handler1 = 0

    # wallbuilder custom methods from here
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
        if context.active_object.wall_builder_props.object_type == 'WALL' and \
            context.active_object.type == 'CURVE':
            height: float
            thickness: float
            if self.__class__.__name__ == 'WBProps':
                height = self.height
                thickness = self.thickness
            else:
                height = context.object.wall_builder_props.height
                thickness = context.object.wall_builder_props.thickness

            # getting references for all points of the wallshape
            points = []
            #check if taper object created (or the wall is just a curve at the moment)
            if context.active_object.wall_builder_props.wall_profile_curve != None:
                for point in context.active_object.data.bevel_object.data.splines[0].points:
                    points.append(point)

            #if points is empty, then the wall is just a curve at the moment
            if len(points) > 0:
                if context.object.wall_builder_props.position == 'INSIDE':
                    # 1st point
                    points[0].co[0] = 0
                    points[0].co[1] = height
                    # 2nd point
                    points[1].co[0] = thickness
                    points[1].co[1] = height
                    # 3rd point
                    points[2].co[0] = thickness
                    points[2].co[1] = 0
                    # 4th point
                    points[3].co[0] = 0
                    points[3].co[1] = 0

                elif context.object.wall_builder_props.position == 'CENTER':
                    # 1st point
                    points[0].co[0] = -(thickness / 2)
                    points[0].co[1] = height
                    # 2nd point
                    points[1].co[0] = thickness / 2
                    points[1].co[1] = height
                    # 3rd point
                    points[2].co[0] = thickness / 2
                    points[2].co[1] = 0
                    # 4th point
                    points[3].co[0] = -(thickness / 2)
                    points[3].co[1] = 0

                elif context.object.wall_builder_props.position == 'OUTSIDE':
                    # 1st point
                    points[0].co[0] = -thickness
                    points[0].co[1] = height
                    # 2nd point
                    points[1].co[0] = 0
                    points[1].co[1] = height
                    # 3rd point
                    points[2].co[0] = 0
                    points[2].co[1] = 0
                    # 4th point
                    points[3].co[0] = -thickness
                    points[3].co[1] = 0


    def generate_object(self, context) -> list:
        obj = context.object
        wb_props = obj.wall_builder_props
        obj_conv_collection = obj.users_collection[0]
        if obj.wall_builder_props.object_type == 'WALL':
            # setting object base parameters
            obj.data.dimensions = '2D'
            obj.name = 'wb_wall_{0}_{1}'.format('inner' if wb_props.is_inner_wall else 'outer', wb_props.level)
            # geometry nodes modifier
            geom_nodes_mod = bpy.context.object.modifiers.new("wb_geom_nodes", 'NODES')
            node_group = geom_nodes_mod.node_group
            node_group.name = '{}_geom_nodes_node_group'.format(obj.name)
            # creating nodes
            nd_input = node_group.nodes['Group Input']
            nd_output = node_group.nodes['Group Output']
            nd_set_shade_smooth = node_group.nodes.new(type="GeometryNodeSetShadeSmooth")
            nd_bool_openings = node_group.nodes.new(type="GeometryNodeMeshBoolean")
            # setting params
            nd_output.location = (500, 0)
            nd_set_shade_smooth.inputs[2].default_value = False
            nd_bool_openings.name = 'mrBoolshit'
            nd_bool_openings.location = (300, -100)
            # create links
            nd_input.outputs.clear()
            nd_output.outputs.clear()
            utils.node_group_link(node_group, nd_input.outputs['Geometry'], nd_set_shade_smooth.inputs['Geometry'])
            utils.node_group_link(node_group, nd_set_shade_smooth.outputs['Geometry'],
                                  nd_bool_openings.inputs['Mesh 1'])
            utils.node_group_link(node_group, nd_output.inputs['Geometry'], nd_bool_openings.outputs['Mesh'])
            # shape curve from here
            bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple_Type='Rectangle',
                                 Simple_width=1, Simple_length=0, use_cyclic_u=True)
            obj_profile = context.object
            obj.wall_builder_props.wall_profile_curve = obj_profile
            obj.data.use_fill_caps = True
            obj_profile.name = f'{obj.name}_taper'
            obj_profile_data = obj_profile.data
            obj_profile_data.fill_mode = 'NONE'
            bpy.ops.curve.spline_type_set(type='POLY')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.collection.objects_remove_active()
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = obj
            obj.data.bevel_mode = 'OBJECT'
            obj.data.bevel_object = obj_profile
            # set the sizes of newly generated wall
            self.set_wall_position(context)
            obj.wall_builder_props.is_converted = True

        elif obj.wall_builder_props.object_type == 'OPENING':
            pass

        elif obj.wall_builder_props.object_type == 'FLOOR':
            # setting object base parameters
            obj.data.bevel_mode = 'ROUND'
            obj.data.extrude = obj.wall_builder_props.height / 2
            obj.data.fill_mode = 'BOTH'
            obj.name = 'wb_floor_{0}'.format(wb_props.level)
            # geometry nodes modifier
            geom_nodes_mod = bpy.context.object.modifiers.new("wb_geom_nodes", 'NODES')
            node_group = geom_nodes_mod.node_group
            node_group.name = '{}_geom_nodes_node_group'.format(obj.name)
            # creating nodes
            nd_input = node_group.nodes['Group Input']
            nd_output = node_group.nodes['Group Output']
            nd_set_shade_smooth = node_group.nodes.new(type="GeometryNodeSetShadeSmooth")
            # setting params
            nd_output.location = (500, 0)
            nd_set_shade_smooth.inputs[2].default_value = False
            # create links
            utils.node_group_link(node_group, nd_input.outputs['Geometry'], nd_set_shade_smooth.inputs['Geometry'])
            utils.node_group_link(node_group, nd_output.inputs['Geometry'], nd_set_shade_smooth.outputs['Geometry'])
            # set object as converted in wall_builder_props
            obj.wall_builder_props.is_converted = True

    def reset_object(self, obj: bpy.types.Object):
        if obj.wall_builder_props.object_type == 'WALL':
            # remove the geom nodes modifier
            try:
                geom_nodes_mod = obj.modifiers['wb_geom_nodes']
            except KeyError:
                print('OBJECT HAD NO wb_geom_nodes MODIFIER')
            else:
                obj.modifiers.remove(geom_nodes_mod)
            # deleting the profile curve
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
            # clearing the fill mode if obj previously was a floor
            obj.data.fill_mode = 'NONE'
            # clearing the openings list
            obj.openings.clear()
            obj.opening_index = -1
            # setting the object is not converted
            obj.wall_builder_props.is_converted = False

        elif obj.wall_builder_props.object_type == 'FLOOR':
            # if object has geom nodes modifier (ex. prev was floor)
            try:
                geom_nodes_mod = obj.modifiers['wb_geom_nodes']
            except KeyError:
                print('OBJECT HAD NO wb_geom_nodes MODIFIER')
            else:
                obj.modifiers.remove(geom_nodes_mod)
            # setting the spline parameters
            obj.data.extrude = 0
            obj.data.fill_mode = 'NONE'
            obj.wall_builder_props.is_converted = False

    # wallbuilder class methods here
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'CURVE'

    def execute(self, context):
        obj = context.object
        if obj.wall_builder_props.is_converted:
            self.reset_object(obj)
            self.report({'INFO'}, 'OBJECT HAS BEEN RESET')
            return {'FINISHED'}
        else:
            self.generate_object(context)
            self.report({'INFO'}, 'OBJECT GENERATED')
            return {'FINISHED'}


# END OF WALLBUILDER OPERATOR


# BUILDING ASSEMBLER --------------------------------------------------------------------------------
class BuildingAssembler(bpy.types.Operator):
    bl_idname = 'object.building_assembler'
    bl_label = 'ASSEMBLE THE BUILDING'
    bl_options = {'REGISTER', 'UNDO'}

    def generate_floor(self, objs: dict, level: str, init_loc, elevation):
        '''elevation - maximum z point of the prev level or previous placed object in the current
                level. It updates every time when the next object or level positioned above the previous'''
        # max height of outside walls
        max_wall_height = 0
        floor_added: bool = False
        # setting objs locations and calculating elevation
        for group in objs[level]:
            for obj in objs[level][group]:
                wb_props = obj.wall_builder_props
                if wb_props.object_type == 'FLOOR':
                    obj.location = (init_loc[0], init_loc[1], elevation + (wb_props.height / 2))
                    elevation += wb_props.height
                    floor_added = True
                elif wb_props.object_type == 'WALL':
                    if floor_added:
                        obj.location = (init_loc[0], init_loc[1], elevation)
                    else:
                        floor_height = objs[level]['floors'][0].wall_builder_props.height
                        obj.location = (init_loc[0], init_loc[1], elevation + floor_height)
                    if wb_props.height > max_wall_height:
                        max_wall_height = wb_props.height
        elevation += max_wall_height
        # getting the key of the next level
        objs_temp = list(objs)
        try:
            next_level = objs_temp[objs_temp.index(level) + 1]
        except (ValueError, IndexError):
            next_level = None

        return {'next_level': next_level, 'elevation': elevation}

    def assemble_building(self, context):
        # filling the all objs holder. Floors must be the first in the dictionary as they increase
        # the global elevation to use it later for the walls of the same level

        # generate objects dictionary
        objs = {}
        for level in data_types.levels:
            objs[level[0]] = {'floors': [], 'outer_walls': [], 'inner_walls': []}
        # filling the objects dictionary
        wb_objects = context.scene.wall_builder_scene_props.plans_collection.objects
        for obj in wb_objects:
            wb_props = obj.wall_builder_props
            for level in data_types.levels:
                if wb_props.level == level[0] and wb_props.object_type == 'WALL' and not wb_props.is_inner_wall:
                    objs[level[0]]['outer_walls'].append(obj)
                if wb_props.level == level[0] and wb_props.object_type == 'WALL' and wb_props.is_inner_wall:
                    objs[level[0]]['inner_walls'].append(obj)
                if wb_props.level == level[0] and wb_props.object_type == 'FLOOR':
                    objs[level[0]]['floors'].append(obj)

        # ASSEMBLING THE OBJECTS (WORKS ONLY FOR MAXIMUM 4-LEVEL ON-GROUND BUILDING (WITHOUT CELLAR))
        # getting EG (1st floor) wall position as
        init_loc = context.scene.wall_builder_scene_props.alignment_object.location
        EG_level_max_height = max(
            [a.wall_builder_props.height for a in objs['EG']['outer_walls']])  # the highest wall on EG (1st fl)
        # assembling EG (1st floor)
        for group in objs['EG']:
            for obj in objs['EG'][group]:
                obj.location = init_loc
        # assembling OG (2nd floor)
        OG_data = self.generate_floor(objs, 'OG', init_loc, EG_level_max_height)
        # assembling THIRD (3rd floor)
        THIRD_data = self.generate_floor(objs, OG_data['next_level'], init_loc, OG_data['elevation'])
        # assembling THIRD (3rd floor)
        DG_data = self.generate_floor(objs, THIRD_data['next_level'], init_loc, THIRD_data['elevation'])

    def execute(self, context):
        # print(self.generate_first_floor(context))
        self.assemble_building(context)
        info = 'BUILDING HAS ASSEMBLED'
        self.report({'INFO'}, info)
        return {'FINISHED'}


# END OF BUILDING ASSEMBLER


# OPENINGS HANDLER OPERATOR -------------------------------------------------------------------------
class OpeningsHandler(bpy.types.Operator):
    bl_idname = "object.opnenings_adder"
    bl_label = "mrlist"

    action: bpy.props.EnumProperty(
        items=(
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('UP', 'Up', ''),
            ('DOWN', 'Down', '')))

    nd_loc = [0, -200]

    def add_opening_to_geom_nodes(self, construction, opening, location):
        '''construction - actual building element to add openings to'''
        try:
            modifier = construction.modifiers['wb_geom_nodes']
        except KeyError:
            print('CONSTRUCTION OBJECT HAS NO GEOM NODES MODIFIER')
        else:
            # getting node group if modif exists
            node_group = modifier.node_group
            # adding opening as object info node
            info_node = node_group.nodes.new(type="GeometryNodeObjectInfo")
            # setting the parameters
            info_node.inputs[0].default_value = opening
            info_node.transform_space = 'RELATIVE'
            info_node.location = location
            # create links
            utils.node_group_link(node_group, info_node.outputs['Geometry'],
                                  node_group.nodes['mrBoolshit'].inputs['Mesh 2'])
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
        """nd_loc - initial location for the new obj info node"""
        obj = context.object
        idx = obj.opening_index
        try:
            item = obj.openings[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(obj.openings) - 1:
                item_next = obj.openings[idx + 1].obj.name
                obj.openings.move(idx, idx + 1)
                obj.opening_index += 1
                info = 'Item "%s" moved to position %d' % (item.obj.name, obj.opening_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = obj.openings[idx - 1].obj.name
                obj.openings.move(idx, idx - 1)
                obj.opening_index -= 1
                info = 'Item "%s" moved to position %d' % (item.obj.name, obj.opening_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                obj.opening_index -= 1
                # deleting object from geom nodes modifier and refreshing geom nodes modifier
                self.remove_opening_from_geom_nodes(obj, obj.openings[idx].obj)
                self.nd_loc[1] += 200

                #-----------------------------------------------------------------------------------
                # remove opening from children  -------- DOESNT WORK PROPERLY AT THE MOMENT

                # THIS PART IS MORE PREFERABLE BUT DOESNT WORK FOR SOME REASON
                # ctx_temp = context.copy()
                # ctx_temp['selected_editable_objects'] = [obj.openings[idx]]
                # ctx_temp['selected_objects'] = [obj.openings[idx]]
                # print('SELECTED: {}'.format(ctx_temp['selected_objects']))
                # print('SELECTED EDITABLE: {}'.format(ctx_temp['selected_editable_objects']))
                # bpy.ops.object.parent_clear(ctx_temp, type='CLEAR_KEEP_TRANSFORM')

                # THIS PART SIMPLIER AND WORKS
                #check if object is not deleted, and opening is not refer to an empty object
                if obj.openings[idx].obj.name in context.view_layer.objects:
                    obj.openings[idx].obj.select_set(True)
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                    obj.openings[idx].obj.select_set(False)
                #-----------------------------------------------------------------------------------

                # removing opening from construction object
                obj.openings.remove(idx)

        if self.action == 'ADD':
            obj.select_set(False)
            
            sel_objects = context.selected_objects.copy()
            bpy.ops.object.select_all(action='DESELECT')
            for object in sel_objects:
                # check if opening is a duplicate
                if len(obj.openings) > 0:
                    for opening in obj.openings:
                        if object == opening.obj:
                            self.report({'WARNING'}, 'This object is already in the openings')
                            return {'CANCELLED'}
                # create new opening
                item = obj.openings.add()
                item.obj = object
                item.obj_id = len(obj.openings)
                obj.opening_index = len(obj.openings) - 1

                #-----------------------------------------------------------------------------------
                # setting the opening as child of obj -------- DOESNT WORK PROPERLY AT THE MOMENT

                ctx_temp = context.copy()
                ctx_temp['selected_editable_objects'] = [object]
                ctx_temp['selected_objects'] = [object]
                # ctx_temp['active_object'] = obj
                # print('THE CRAP: {0}{1}'.format(ctx_temp['selected_editable_objects'], ctx_temp['selected_objects']))
                bpy.ops.object.parent_set(ctx_temp, keep_transform=True)
                #-----------------------------------------------------------------------------------

                # putting the object to geom nodes modif
                self.add_opening_to_geom_nodes(obj, object, self.nd_loc)
                self.nd_loc[1] -= 200
                print(self.nd_loc[1])
                print(f'OPENING ADDED: {item.obj.name}')
        return {'FINISHED'}


# END OF OPENINGS HANDLER OPERATOR


# OPENINGS LIST PROP GROUP --------------------------------------------------------------------------
class OpeningsCollection(bpy.types.PropertyGroup):
    obj: PointerProperty(type=bpy.types.Object)
    obj_id: IntProperty()


# REGISTERING ---------------------------------------------------------------------------------------
classes = (WallBuilder,
           BuildingAssembler,
           OpeningsCollection,
           OpeningsHandler
           )


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Object.openings = CollectionProperty(type=OpeningsCollection)
    bpy.types.Object.opening_index = IntProperty()


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    del bpy.types.Object.openings
    del bpy.types.Object.opening_index


if __name__ == "__main__":
    register()
