import bpy

class WallBuilder(bpy.types.Operator):
    bl_idname = 'object.wall_builder'
    bl_label = 'DO THE MAGIC'
    bl_options = {'REGISTER', 'UNDO'}

    #TEMP ELEMENTS
    FLOOR_HEIGHT = 0.15
    WALL_HEIGHT = 0


    def select_and_activate_only_object(self, context, source_object):
        bpy.ops.object.select_all(action='DESELECT')
        source_object.select_set(True)
        context.view_layer.objects.active = source_object

    def execute(self, context):
        original_curve_object: bpy.types.Object = context.object
        mesh_object: bpy.types.Object = None
        source_mesh_object: bpy.types.Object = None
        # the_context: bpy.types.Context = context.copy()

        bpy.context.object.data.resolution_u = 1 #lower the res to avoid extra verts on U-closer segment
        bpy.ops.object.convert(target='MESH', keep_original=True)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.mode_set(mode='OBJECT')

        context.object.name = 'mrSource'
        source_mesh_object = context.object

        #EG floor
        bpy.ops.object.duplicate_move(
            OBJECT_OT_duplicate={
                "linked":False,
                "mode":'TRANSLATION'
                },
            TRANSFORM_OT_translate={
                "value":(0, 0, 0),
                "orient_type":'GLOBAL',
                "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)),
                "orient_matrix_type":'GLOBAL',
                "constraint_axis":(False, False, False),
                "mirror":False,
                "use_proportional_edit":False
                }
            )

        context.object.name = 'EG_floor'
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={
                    "use_normal_flip":False,
                    "use_dissolve_ortho_edges":False,
                    "mirror":False
                },
                    TRANSFORM_OT_translate={
                    "value":(0, 0, self.FLOOR_HEIGHT),
                    "orient_type":'NORMAL',
                    "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                    "orient_matrix_type":'NORMAL',
                    "constraint_axis":(False, False, True),
                    "mirror":False
                }
            )

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        #EG out walls
        self.select_and_activate_only_object(context, source_mesh_object)

        bpy.ops.object.duplicate_move(
            OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
            TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False}
            )

        context.object.name = 'mrWall'

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.inset(thickness=context.object.outer_wall_thickness)
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')

        self.WALL_HEIGHT = context.object.wall_height

        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={
                    "use_normal_flip":False,
                    "use_dissolve_ortho_edges":False,
                    "mirror":False
                },
                    TRANSFORM_OT_translate={
                    "value":(0, 0, context.object.wall_height),
                    "orient_type":'NORMAL',
                    "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                    "orient_matrix_type":'NORMAL',
                    "constraint_axis":(False, False, True),
                    "mirror":False
                }
            )

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.transform.translate(value=(0, 0, self.FLOOR_HEIGHT), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        #OG floor
        self.select_and_activate_only_object(context, context.scene.objects['EG_floor'])

        bpy.ops.object.duplicate_move(
            OBJECT_OT_duplicate={
                "linked":False,
                "mode":'TRANSLATION'
                },
            TRANSFORM_OT_translate={
                "value":(0, 0, context.object.wall_height + self.FLOOR_HEIGHT),
                "orient_type":'GLOBAL',
                "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                "orient_matrix_type":'GLOBAL',
                "constraint_axis":(False, False, False),
                "mirror":False,
                "use_proportional_edit":False
                }
            )

        context.object.name = 'OG_floor'

        #EG inner walls

        self.select_and_activate_only_object(context, context.scene.objects['EG_shaper_inner_walls'])
        print(context.object.scale[1])
        bpy.ops.transform.resize(
            value=(1, self.WALL_HEIGHT, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False
        )
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        self.select_and_activate_only_object(context, context.scene.objects['EG_wall_inner'])
        context.object.data.bevel_object = bpy.data.objects["EG_shaper_inner_walls"]

        bpy.ops.transform.translate(
            value=(0, 0, context.object.scale[1] * self.FLOOR_HEIGHT),
            orient_type='GLOBAL',
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            orient_matrix_type='GLOBAL',
            constraint_axis=(False, False, True),
            mirror=True, use_proportional_edit=False,
            proportional_edit_falloff='SMOOTH',
            proportional_size=1, use_proportional_connected=False,
            use_proportional_projected=False
        )

        bpy.ops.object.convert(target='MESH')
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 0.523599

        #DG outer walls

        context.object.name = 'OG_wall'

        
        self.report({'INFO'}, f'WALL BUILDER: {self.bl_label}')
        return {'FINISHED'}

    