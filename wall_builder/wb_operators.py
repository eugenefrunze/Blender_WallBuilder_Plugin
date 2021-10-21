import bpy
import data_types

class WallBuilder(bpy.types.Operator):
    bl_idname = 'object.wall_builder'
    bl_label = 'DO THE MAGIC'
    bl_options = {'REGISTER', 'UNDO'}

    #TEMP ELEMENTS
    FLOOR_HEIGHT = 0.15
    WALL_HEIGHT = 0

    def place_openings(self, context, openings_types):
        pass
        # mesh_openings = []
        # helpers_openings = []

        # for obj in context.scene.objects:
        #     if obj.name in (ty[0] for ty in data_types.openings_types) and obj.type == 'CURVE':
        #         helpers_openings.append(obj)
        #     elif obj.name in ['door1', 'window1']:
        #         mesh_openings.append(obj)

        # print(helpers_openings, mesh_openings)

    def select_and_activate_only_object(self, context, source_object, debug: bool = False):
        pass
        # bpy.ops.object.select_all(action='DESELECT')
        # source_object.select_set(True)
        # context.view_layer.objects.active = source_object
        # if debug:
        #     print('AAaAAAAA')
        #     print('BbBBbbBb')

    @staticmethod
    def debug_method(message: str):
        print('==============================================')
        print(message)
        print('----------------------------------------------')

    @staticmethod
    def create_node_group(obj: bpy.types.Object) -> tuple():
        if obj.wall_builder_props.object_type == 'WALL':
            modifier = obj.modifiers.new('wb_geom_nodes', 'NODES')
            node_group = modifier.node_group
            node_group.name = '{}_wb_node_group'.format(obj.name)

            
            node_curve_to_mesh = node_group.nodes.new(type='GeometryNodeCurveToMesh')



            return (modifier, node_group)
        elif obj.wall_builder_props.object_type == 'OPENING':
            WallBuilder.debug_method('create_node_group: it\'s a {}'.format(obj.wall_builder_props.object_type))
        elif obj.wall_builder_props.object_type == 'FLOOR':
            WallBuilder.debug_method('create_node_group: it\'s a {}'.format(obj.wall_builder_props.object_type))


    @staticmethod
    def get_wb_objects(coll: str):
        return bpy.data.collections[coll].objects

    def execute(self, context):
        # add geom nodes modifier to outside walls
        wb_objects = WallBuilder.get_wb_objects(bpy.context.object.users_collection[0].name)
        WallBuilder.create_node_group(bpy.context.object)
        WallBuilder.debug_method('wb_objects are: {}'.format(wb_objects))


        
        # original_curve_object: bpy.types.Object = context.object
        # mesh_object: bpy.types.Object = None
        # source_mesh_object: bpy.types.Object = None
        # # the_context: bpy.types.Context = context.copy()

        # bpy.context.object.data.resolution_u = 1 #lower the res to avoid extra verts on U-closer segment
        # bpy.ops.object.convert(target='MESH', keep_original=True)

        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.select_mode(type='EDGE')
        # bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.edge_face_add()
        # bpy.ops.object.mode_set(mode='OBJECT')

        # context.object.name = 'EG_mrSource'
        # source_mesh_object = context.object

        # #EG floor
        # bpy.ops.object.duplicate_move(
        #     OBJECT_OT_duplicate={
        #         "linked":False,
        #         "mode":'TRANSLATION'
        #         },
        #     TRANSFORM_OT_translate={
        #         "value":(0, 0, 0),
        #         "orient_type":'GLOBAL',
        #         "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)),
        #         "orient_matrix_type":'GLOBAL',
        #         "constraint_axis":(False, False, False),
        #         "mirror":False,
        #         "use_proportional_edit":False
        #         }
        #     )

        # context.object.name = 'EG_floor'
        # bpy.ops.object.mode_set(mode='EDIT')

        # bpy.ops.mesh.extrude_region_move(
        #     MESH_OT_extrude_region={
        #             "use_normal_flip":False,
        #             "use_dissolve_ortho_edges":False,
        #             "mirror":False
        #         },
        #             TRANSFORM_OT_translate={
        #             "value":(0, 0, self.FLOOR_HEIGHT),
        #             "orient_type":'NORMAL',
        #             "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        #             "orient_matrix_type":'NORMAL',
        #             "constraint_axis":(False, False, True),
        #             "mirror":False
        #         }
        #     )

        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.mode_set(mode='OBJECT')

        # #EG out walls
        # self.select_and_activate_only_object(context, source_mesh_object)

        # bpy.ops.object.duplicate_move(
        #     OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
        #     TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False}
        #     )

        # context.object.name = 'EG_wall_outer'

        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.inset(thickness=context.object.outer_wall_thickness)
        # bpy.ops.mesh.delete(type='FACE')
        # bpy.ops.mesh.select_all(action='SELECT')

        # self.WALL_HEIGHT = context.object.wall_height

        # bpy.ops.mesh.extrude_region_move(
        #     MESH_OT_extrude_region={
        #             "use_normal_flip":False,
        #             "use_dissolve_ortho_edges":False,
        #             "mirror":False
        #         },
        #             TRANSFORM_OT_translate={
        #             "value":(0, 0, context.object.wall_height),
        #             "orient_type":'NORMAL',
        #             "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        #             "orient_matrix_type":'NORMAL',
        #             "constraint_axis":(False, False, True),
        #             "mirror":False
        #         }
        #     )

        # bpy.ops.mesh.select_all(action='DESELECT')
        # bpy.ops.object.mode_set(mode='OBJECT')

        # bpy.ops.transform.translate(value=(0, 0, self.FLOOR_HEIGHT), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        # #OG floor
        # self.select_and_activate_only_object(context, context.scene.objects['EG_floor'])

        # bpy.ops.object.duplicate_move(
        #     OBJECT_OT_duplicate={
        #         "linked":False,
        #         "mode":'TRANSLATION'
        #         },
        #     TRANSFORM_OT_translate={
        #         "value":(0, 0, context.object.wall_height + self.FLOOR_HEIGHT),
        #         "orient_type":'GLOBAL',
        #         "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        #         "orient_matrix_type":'GLOBAL',
        #         "constraint_axis":(False, False, False),
        #         "mirror":False,
        #         "use_proportional_edit":False
        #         }
        #     )

        # context.object.name = 'OG_floor'

        # #EG inner walls

        # self.select_and_activate_only_object(context, context.scene.objects['plan_EG_shaper_inner_walls'])
        # print(context.object.scale[1])
        # bpy.ops.transform.resize(
        #     value=(1, self.WALL_HEIGHT, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False
        # )
        # bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # self.select_and_activate_only_object(context, context.scene.objects['plan_EG_wall_inner'])
        # context.object.data.bevel_object = bpy.data.objects["plan_EG_shaper_inner_walls"]

        # bpy.ops.transform.translate(
        #     value=(0, 0, context.object.scale[1] * self.FLOOR_HEIGHT),
        #     orient_type='GLOBAL',
        #     orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        #     orient_matrix_type='GLOBAL',
        #     constraint_axis=(False, False, True),
        #     mirror=True, use_proportional_edit=False,
        #     proportional_edit_falloff='SMOOTH',
        #     proportional_size=1, use_proportional_connected=False,
        #     use_proportional_projected=False    
        # )

        # bpy.ops.object.convert(target='MESH')
        # bpy.context.object.data.use_auto_smooth = True
        # bpy.context.object.data.auto_smooth_angle = 0.523599

        # self.place_openings(context, data_types.openings_types)

        # self.report({'INFO'}, f'WALL BUILDER: {self.bl_label}')
        # return {'FINISHED'}

        self.report({'INFO'}, 'WALL BUILDER: {}'.format(self.bl_label))
        return {'FINISHED'}

def register():
    from bpy.utils import register_class
    register_class(WallBuilder)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(WallBuilder)

if __name__ == "__main__":
    register()

    