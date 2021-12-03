import bpy
from bpy.props import CollectionProperty, IntProperty, StringProperty
from bpy.types import DepsgraphObjectInstance, Object
import data_types

class WallBuilder(bpy.types.Operator):
    bl_idname = 'object.wall_builder'
    bl_label = 'GANERATOR HANDLER'
    bl_options = {'REGISTER', 'UNDO'}

    #TEMP ELEMENTS
    FLOOR_HEIGHT = 0.15
    WALL_HEIGHT = 0

    reset_object: bpy.props.BoolProperty()

    @staticmethod
    def debug_method(message: str):
        print('>>============================================')
        print(message)
        print('----------------------------------------------')

    @staticmethod
    def get_profile_shape(position: str):
        
        points = {
            'OUTSIDE' : (
                (0, 0, 0),
                (-1, 0, 0),
                (-1, -1, 0),
                (0, -1, 0) 
            ),
            'CENTER' : (
                (0.5, 0, 0),
                (-0.5, 0, 0),
                (-0.5, -1, 0),
                (0.5, -1, 0)
            ),
            'INSIDE' : (
                (0, 0, 0),
                (1, 0, 0),
                (1, -1, 0),
                (0, -1, 0)
            )
        }

        return points[position]

    @staticmethod
    def generate_object_old(obj: bpy.types.Object) -> tuple():
        if obj.wall_builder_props.object_type == 'WALL':

            try:
                wb_geom_mod = obj.modifiers['wb_geom_nodes']
            except KeyError:
                print('this guy dont have a mod')

                for spline in obj.data.splines:
                    if not spline.use_cyclic_u:
                        spline.use_cyclic_u = True

                modifier = obj.modifiers.new('wb_geom_nodes', 'NODES')
                node_group = modifier.node_group
                node_group.name = '{}_wb_node_group'.format(obj.name)
                
                #creating inputs
                inp_thickness = node_group.inputs.new(type='NodeSocketFloat', name='thickness')
                inp_height = node_group.inputs.new(type='NodeSocketFloat', name='heigth')
                inp_position = node_group.inputs.new(type='NodeSocketInt', name='position')
                
                #creating new nodes
                nd_input = node_group.nodes['Group Input']
                nd_output = node_group.nodes['Group Output']
                nd_curve_to_mesh = node_group.nodes.new(type='GeometryNodeCurveToMesh')


                #POINTS
                #out
                nd_quadrilateral_outside = node_group.nodes.new(type='GeometryNodeCurvePrimitiveQuadrilateral')
                #out point 1
                nd_quadrilateral_outside_point1 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_outside_point1.location = (-4000, 400)
                node_group.links.new(nd_quadrilateral_outside_point1.outputs['Vector'], nd_quadrilateral_outside.inputs['Point 1'])
                #out point 2
                nd_quadrilateral_outside_point2 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_outside_point2.location = (-4000, 250)
                nd_quadrilateral_outside_point2.vector[0] = -1
                nd_outside_point2_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_outside_point2_sep_xyz.location = (-3600, 600)
                node_group.links.new(nd_quadrilateral_outside_point2.outputs['Vector'], nd_outside_point2_sep_xyz.inputs['Vector'])
                nd_outside_point2_math = node_group.nodes.new(type='ShaderNodeMath')
                nd_outside_point2_math.operation = 'MULTIPLY'
                nd_outside_point2_math.location = (-3400, 600)
                node_group.links.new(nd_outside_point2_sep_xyz.outputs['X'], nd_outside_point2_math.inputs[0])
                nd_outside_point2_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_outside_point2_combine_xyz.location = (-3200, 600)
                node_group.links.new(nd_outside_point2_math.outputs['Value'], nd_outside_point2_combine_xyz.inputs['X'])
                node_group.links.new(nd_outside_point2_combine_xyz.outputs['Vector'], nd_quadrilateral_outside.inputs['Point 2'])
                #out point 3
                nd_quadrilateral_outside_point3 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_outside_point3.location = (-4000, 100)
                nd_quadrilateral_outside_point3.vector[0] = -1
                nd_quadrilateral_outside_point3.vector[1] = -1
                nd_outside_point3_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_outside_point3_sep_xyz.location = (-3600, 200)
                node_group.links.new(nd_quadrilateral_outside_point3.outputs['Vector'], nd_outside_point3_sep_xyz.inputs['Vector'])
                nd_outside_point3_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_outside_point3_math1.operation = 'MULTIPLY'
                nd_outside_point3_math1.location = (-3400, 200)
                node_group.links.new(nd_outside_point3_sep_xyz.outputs['X'], nd_outside_point3_math1.inputs[0])
                nd_outside_point3_math2 = node_group.nodes.new(type='ShaderNodeMath')
                nd_outside_point3_math2.operation = 'MULTIPLY'
                nd_outside_point3_math2.location = (-3400, 0)
                node_group.links.new(nd_outside_point3_sep_xyz.outputs['Y'], nd_outside_point3_math2.inputs[0])
                nd_outside_point3_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_outside_point3_combine_xyz.location = (-3200, 200)
                node_group.links.new(nd_outside_point3_math1.outputs['Value'], nd_outside_point3_combine_xyz.inputs['X'])
                node_group.links.new(nd_outside_point3_math2.outputs['Value'], nd_outside_point3_combine_xyz.inputs['Y'])
                node_group.links.new(nd_outside_point3_combine_xyz.outputs['Vector'], nd_quadrilateral_outside.inputs['Point 3'])
                #out point 4
                nd_quadrilateral_outside_point4 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_outside_point4.location = (-4000, -50)
                nd_quadrilateral_outside_point4.vector[1] = -1
                nd_outside_point4_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_outside_point4_sep_xyz.location = (-3600, -200)
                node_group.links.new(nd_quadrilateral_outside_point4.outputs['Vector'], nd_outside_point4_sep_xyz.inputs['Vector'])
                nd_outside_point4_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_outside_point4_math1.operation = 'MULTIPLY'
                nd_outside_point4_math1.location = (-3400, -200)
                node_group.links.new(nd_outside_point4_sep_xyz.outputs['Y'], nd_outside_point4_math1.inputs[0])
                nd_outside_point4_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_outside_point4_combine_xyz.location = (-3200, -200)
                node_group.links.new(nd_outside_point4_math1.outputs['Value'], nd_outside_point4_combine_xyz.inputs['Y'])
                node_group.links.new(nd_outside_point4_combine_xyz.outputs['Vector'], nd_quadrilateral_outside.inputs['Point 4'])




                #center
                nd_quadrilateral_center = node_group.nodes.new(type='GeometryNodeCurvePrimitiveQuadrilateral')
                #center point 1
                nd_quadrilateral_center_point1 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_center_point1.location = (-4000, -600)
                nd_quadrilateral_center_point1.vector[0] = 0.5

                nd_center_point1_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_center_point1_sep_xyz.location = (-3800, -600)
                node_group.links.new(nd_quadrilateral_center_point1.outputs['Vector'], nd_center_point1_sep_xyz.inputs['Vector'])

                nd_center_point1_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_center_point1_math1.operation = 'MULTIPLY'
                nd_center_point1_math1.location = (-3600, -600)
                node_group.links.new(nd_center_point1_sep_xyz.outputs['X'], nd_center_point1_math1.inputs[0])

                nd_center_point1_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_center_point1_combine_xyz.location = (-3400, -600)
                node_group.links.new(nd_center_point1_math1.outputs['Value'], nd_center_point1_combine_xyz.inputs['X'])
                node_group.links.new(nd_center_point1_combine_xyz.outputs['Vector'], nd_quadrilateral_center.inputs['Point 1'])

                #center point 2
                nd_quadrilateral_center_point2 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_center_point2.location = (-4000, -750)
                nd_quadrilateral_center_point2.vector[0] = -0.5

                nd_center_point2_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_center_point2_sep_xyz.location = (-3800, -750)
                node_group.links.new(nd_quadrilateral_center_point2.outputs['Vector'], nd_center_point2_sep_xyz.inputs['Vector'])

                nd_center_point2_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_center_point2_math1.operation = 'MULTIPLY'
                nd_center_point2_math1.location = (-3600, -800)
                node_group.links.new(nd_center_point2_sep_xyz.outputs['X'], nd_center_point2_math1.inputs[0])

                nd_center_point2_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_center_point2_combine_xyz.location = (-3400, -750)
                node_group.links.new(nd_center_point2_math1.outputs['Value'], nd_center_point2_combine_xyz.inputs['X'])
                node_group.links.new(nd_center_point2_combine_xyz.outputs['Vector'], nd_quadrilateral_center.inputs['Point 2'])

                #center point 3
                nd_quadrilateral_center_point3 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_center_point3.location = (-4000, -900)
                nd_quadrilateral_center_point3.vector[0] = -0.5
                nd_quadrilateral_center_point3.vector[1] = -1

                nd_center_point3_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_center_point3_sep_xyz.location = (-3800, -1050)
                node_group.links.new(nd_quadrilateral_center_point3.outputs['Vector'], nd_center_point3_sep_xyz.inputs['Vector'])

                nd_center_point3_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_center_point3_math1.operation = 'MULTIPLY'
                nd_center_point3_math1.location = (-3600, -1050)
                node_group.links.new(nd_center_point3_sep_xyz.outputs['X'], nd_center_point3_math1.inputs[0])

                nd_center_point3_math2 = node_group.nodes.new(type='ShaderNodeMath')
                nd_center_point3_math2.operation = 'MULTIPLY'
                nd_center_point3_math2.location = (-3600, -1250)
                node_group.links.new(nd_center_point3_sep_xyz.outputs['Y'], nd_center_point3_math2.inputs[0])

                nd_center_point3_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_center_point3_combine_xyz.location = (-3400, -1050)
                node_group.links.new(nd_center_point3_math1.outputs['Value'], nd_center_point3_combine_xyz.inputs['X'])
                node_group.links.new(nd_center_point3_math2.outputs['Value'], nd_center_point3_combine_xyz.inputs['Y'])
                node_group.links.new(nd_center_point3_combine_xyz.outputs['Vector'], nd_quadrilateral_center.inputs['Point 3'])

                #center point 4
                nd_quadrilateral_center_point4 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_center_point4.location = (-4000, -1050)
                nd_quadrilateral_center_point4.vector[0] = 0.5
                nd_quadrilateral_center_point4.vector[1] = -1

                nd_center_point4_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_center_point4_sep_xyz.location = (-3800, -1500)
                node_group.links.new(nd_quadrilateral_center_point4.outputs['Vector'], nd_center_point4_sep_xyz.inputs['Vector'])
                
                nd_center_point4_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_center_point4_math1.operation = 'MULTIPLY'
                nd_center_point4_math1.location = (-3600, -1500)
                node_group.links.new(nd_center_point4_sep_xyz.outputs['X'], nd_center_point4_math1.inputs[0])

                nd_center_point4_math2 = node_group.nodes.new(type='ShaderNodeMath')
                nd_center_point4_math2.operation = 'MULTIPLY'
                nd_center_point4_math2.location = (-3600, -1650)
                node_group.links.new(nd_center_point4_sep_xyz.outputs['Y'], nd_center_point4_math2.inputs[0])

                nd_center_point4_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_center_point4_combine_xyz.location = (-3400, -1500)
                node_group.links.new(nd_center_point4_math1.outputs['Value'], nd_center_point4_combine_xyz.inputs['X'])
                node_group.links.new(nd_center_point4_math2.outputs['Value'], nd_center_point4_combine_xyz.inputs['Y'])
                node_group.links.new(nd_center_point4_combine_xyz.outputs['Vector'], nd_quadrilateral_center.inputs['Point 4'])



                #inside
                nd_quadrilateral_inside = node_group.nodes.new(type='GeometryNodeCurvePrimitiveQuadrilateral')
                #inside point 1
                nd_quadrilateral_inside_point1 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_inside_point1.location = (-3000, -800)
                node_group.links.new(nd_quadrilateral_inside_point1.outputs['Vector'], nd_quadrilateral_inside.inputs['Point 1'])

                #inside point 2
                nd_quadrilateral_inside_point2 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_inside_point2.location = (-3000, -950)
                nd_quadrilateral_inside_point2.vector[0] = 1

                nd_inside_point2_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_inside_point2_sep_xyz.location = (-2800, -950)
                node_group.links.new(nd_quadrilateral_inside_point2.outputs['Vector'], nd_inside_point2_sep_xyz.inputs['Vector'])

                nd_inside_point2_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_inside_point2_math1.operation = 'MULTIPLY'
                nd_inside_point2_math1.location = (-2600, -950)
                node_group.links.new(nd_inside_point2_sep_xyz.outputs['X'], nd_inside_point2_math1.inputs[0])

                nd_inside_point2_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_inside_point2_combine_xyz.location = (-2400, -950)
                node_group.links.new(nd_inside_point2_math1.outputs['Value'], nd_inside_point2_combine_xyz.inputs['X'])
                node_group.links.new(nd_inside_point2_combine_xyz.outputs['Vector'], nd_quadrilateral_inside.inputs['Point 2'])

                # #inside point 3
                nd_quadrilateral_inside_point3 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_inside_point3.location = (-3000, -1100)
                nd_quadrilateral_inside_point3.vector[0] = 1
                nd_quadrilateral_inside_point3.vector[1] = -1

                nd_inside_point3_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_inside_point3_sep_xyz.location = (-2800, -1100)
                node_group.links.new(nd_quadrilateral_inside_point3.outputs['Vector'], nd_inside_point3_sep_xyz.inputs['Vector'])

                nd_inside_point3_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_inside_point3_math1.operation = 'MULTIPLY'
                nd_inside_point3_math1.location = (-2600, -1150)
                node_group.links.new(nd_inside_point3_sep_xyz.outputs['X'], nd_inside_point3_math1.inputs[0])

                nd_inside_point3_math2 = node_group.nodes.new(type='ShaderNodeMath')
                nd_inside_point3_math2.operation = 'MULTIPLY'
                nd_inside_point3_math2.location = (-2600, -1350)
                node_group.links.new(nd_inside_point3_sep_xyz.outputs['Y'], nd_inside_point3_math2.inputs[0])

                nd_inside_point3_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_inside_point3_combine_xyz.location = (-2400, -1100)
                node_group.links.new(nd_inside_point3_math1.outputs['Value'], nd_inside_point3_combine_xyz.inputs['X'])
                node_group.links.new(nd_inside_point3_math2.outputs['Value'], nd_inside_point3_combine_xyz.inputs['Y'])
                node_group.links.new(nd_inside_point3_combine_xyz.outputs['Vector'], nd_quadrilateral_inside.inputs['Point 3'])

                # #inside point 4
                nd_quadrilateral_inside_point4 = node_group.nodes.new(type='FunctionNodeInputVector')
                nd_quadrilateral_inside_point4.location = (-3000, -1250)
                nd_quadrilateral_inside_point4.vector[1] = -1

                nd_inside_point4_sep_xyz = node_group.nodes.new(type='ShaderNodeSeparateXYZ')
                nd_inside_point4_sep_xyz.location = (-2800, -1550)
                node_group.links.new(nd_quadrilateral_inside_point4.outputs['Vector'], nd_inside_point4_sep_xyz.inputs['Vector'])

                nd_inside_point4_math1 = node_group.nodes.new(type='ShaderNodeMath')
                nd_inside_point4_math1.operation = 'MULTIPLY'
                nd_inside_point4_math1.location = (-2600, -1550)
                node_group.links.new(nd_inside_point4_sep_xyz.outputs['Y'], nd_inside_point4_math1.inputs[0])

                nd_inside_point4_combine_xyz = node_group.nodes.new(type='ShaderNodeCombineXYZ')
                nd_inside_point4_combine_xyz.location = (-2400, -1550)
                node_group.links.new(nd_inside_point4_math1.outputs['Value'], nd_inside_point4_combine_xyz.inputs['Y'])
                node_group.links.new(nd_inside_point4_combine_xyz.outputs['Vector'], nd_quadrilateral_inside.inputs['Point 4'])

                #POINTS END

                nd_set_shade_smooth = node_group.nodes.new(type='GeometryNodeSetShadeSmooth')
                nd_switch = node_group.nodes.new(type='GeometryNodeSwitch')
                nd_switch2 = node_group.nodes.new(type='GeometryNodeSwitch')
                nd_switch3 = node_group.nodes.new(type='GeometryNodeSwitch')
                nd_less_than = node_group.nodes.new(type='FunctionNodeCompareFloats')
                nd_equal = node_group.nodes.new(type='FunctionNodeCompareFloats')
                nd_greater_than = node_group.nodes.new(type='FunctionNodeCompareFloats')
                #openings
                nd_object_info_window1 = node_group.nodes.new(type='GeometryNodeObjectInfo')
                nd_object_info_door1= node_group.nodes.new(type='GeometryNodeObjectInfo')
                nd_openings_bool = node_group.nodes.new(type='GeometryNodeMeshBoolean')



                # setting the parameters
                node_group.inputs['position'].default_value = 0
                node_group.inputs['position'].min_value = -1
                node_group.inputs['position'].max_value = 1

                nd_input.location = (-5500, 0)
                nd_output.location = (1500, 0)

                nd_object_info_window1.location = (500, -100)
                nd_object_info_window1.inputs[0].default_value = bpy.data.objects['window1_bool_cutter']
                nd_object_info_window1.transform_space = 'RELATIVE'
                nd_object_info_door1.location = (700, -100)
                nd_object_info_door1.inputs[0].default_value = bpy.data.objects['door1_bool_cutter']
                nd_object_info_door1.transform_space = 'RELATIVE'
                nd_openings_bool.location = (900, -50)

                nd_quadrilateral_outside.mode = 'POINTS'
                nd_quadrilateral_outside.name = 'quad_outside'
                nd_quadrilateral_outside.label = 'quad outside'
                nd_quadrilateral_outside.location = (-1100, -200)

                profile_points = WallBuilder.get_profile_shape('OUTSIDE')
                for idx, point in enumerate(profile_points):
                    nd_quadrilateral_outside.inputs['Point {}'.format(idx + 1)].default_value = point

                nd_quadrilateral_center.mode = 'POINTS'
                nd_quadrilateral_center.name = 'quad_center'
                nd_quadrilateral_center.label = 'quad center'
                nd_quadrilateral_center.location = (-900, -200)

                profile_points = WallBuilder.get_profile_shape('CENTER')
                for idx, point in enumerate(profile_points):
                    nd_quadrilateral_center.inputs['Point {}'.format(idx + 1)].default_value = point

                nd_quadrilateral_inside.mode = 'POINTS'
                nd_quadrilateral_inside.name = 'quad_inside'
                nd_quadrilateral_inside.label = 'quad inside'
                nd_quadrilateral_inside.location = (-700, -200)

                profile_points = WallBuilder.get_profile_shape('INSIDE')
                for idx, point in enumerate(profile_points):
                    nd_quadrilateral_inside.inputs['Point {}'.format(idx + 1)].default_value = point

                nd_switch.input_type = 'GEOMETRY'
                nd_switch.location = (-500, -200)

                nd_switch2.input_type = 'GEOMETRY'
                nd_switch2.location = (-250, -200)

                nd_switch3.input_type = 'GEOMETRY'
                nd_switch3.location = (-0, -200)

                # nd_set_shade_smooth.inputs[2].default_value = True
                nd_set_shade_smooth.location = (250, 0)

                nd_less_than.operation = 'LESS_THAN'
                nd_less_than.location = (-650, 200)

                nd_equal.operation = 'EQUAL'
                nd_equal.inputs['Epsilon'].default_value = 0
                nd_equal.location = (-450, 200)

                nd_greater_than.operation = 'GREATER_THAN'
                nd_greater_than.location = (-250, 200)

                # clear default outputs
                nd_input.outputs.clear()
                nd_output.outputs.clear()

                # assigning links
                node_group.links.new(nd_input.outputs['Geometry'], nd_curve_to_mesh.inputs['Curve'])
                node_group.links.new(nd_input.outputs['thickness'], nd_outside_point2_math.inputs[1])
                node_group.links.new(nd_input.outputs['thickness'], nd_outside_point3_math1.inputs[1])
                node_group.links.new(nd_input.outputs['thickness'], nd_center_point1_math1.inputs[1])
                node_group.links.new(nd_input.outputs['thickness'], nd_center_point2_math1.inputs[1])
                node_group.links.new(nd_input.outputs['thickness'], nd_center_point3_math1.inputs[1])
                node_group.links.new(nd_input.outputs['thickness'], nd_center_point4_math1.inputs[1])
                node_group.links.new(nd_input.outputs['thickness'], nd_inside_point2_math1.inputs[1])
                node_group.links.new(nd_input.outputs['thickness'], nd_inside_point3_math1.inputs[1])
                node_group.links.new(nd_input.outputs['heigth'], nd_outside_point3_math2.inputs[1])
                node_group.links.new(nd_input.outputs['heigth'], nd_outside_point4_math1.inputs[1])
                node_group.links.new(nd_input.outputs['heigth'], nd_center_point3_math2.inputs[1])
                node_group.links.new(nd_input.outputs['heigth'], nd_center_point4_math2.inputs[1])
                node_group.links.new(nd_input.outputs['heigth'], nd_inside_point3_math2.inputs[1])
                node_group.links.new(nd_input.outputs['heigth'], nd_inside_point4_math1.inputs[1])
                node_group.links.new(nd_input.outputs['position'], nd_less_than.inputs['A'])
                node_group.links.new(nd_input.outputs['position'], nd_equal.inputs['A'])
                node_group.links.new(nd_input.outputs['position'], nd_greater_than.inputs['A'])

                node_group.links.new(nd_curve_to_mesh.outputs['Mesh'], nd_set_shade_smooth.inputs['Geometry'])
                # node_group.links.new(nd_set_shade_smooth.outputs['Geometry'], nd_output.inputs['Geometry'])

                node_group.links.new(nd_quadrilateral_outside.outputs['Curve'], nd_switch3.inputs[15])
                node_group.links.new(nd_quadrilateral_center.outputs['Curve'], nd_switch.inputs[14])
                node_group.links.new(nd_quadrilateral_center.outputs['Curve'], nd_switch2.inputs[15])
                node_group.links.new(nd_quadrilateral_inside.outputs['Curve'], nd_switch.inputs[15])

                node_group.links.new(nd_less_than.outputs['Result'], nd_switch.inputs[1])
                node_group.links.new(nd_equal.outputs['Result'], nd_switch2.inputs[1])
                node_group.links.new(nd_greater_than.outputs['Result'], nd_switch3.inputs[1])
                
                node_group.links.new(nd_switch.outputs[6], nd_switch2.inputs[14])
                node_group.links.new(nd_switch2.outputs[6], nd_switch3.inputs[14])
                node_group.links.new(nd_switch3.outputs[6], nd_curve_to_mesh.inputs['Profile Curve'])

                node_group.links.new(nd_object_info_window1.outputs['Geometry'], nd_openings_bool.inputs['Geometry 2'])
                node_group.links.new(nd_object_info_door1.outputs['Geometry'], nd_openings_bool.inputs['Geometry 2'])
                node_group.links.new(nd_set_shade_smooth.outputs['Geometry'], nd_openings_bool.inputs['Geometry 1'])
                node_group.links.new(nd_openings_bool.outputs['Geometry'], nd_output.inputs['Geometry'])

                return (modifier, node_group)
            else:
                WallBuilder.reset_object(obj, wb_geom_mod)


        elif obj.wall_builder_props.object_type == 'OPENING':
            WallBuilder.debug_method('create_node_group: it\'s a {}'.format(obj.wall_builder_props.object_type))


        elif obj.wall_builder_props.object_type == 'FLOOR':
            #prepare the floor
            obj.data.fill_mode = 'BOTH'
            for spline in obj.data.splines:
                spline.use_cyclic_u = True
            obj.data.extrude = obj.wall_builder_props.height / 2

    def reset_object(obj: bpy.types.Object, modifier):
        if obj.wall_builder_props.object_type == 'WALL':
            print('this guy has a mod')
            obj.modifiers.remove(modifier)

    def generate_object(self, context) -> list:
        obj_converted = context.object
        if obj_converted.wall_builder_props.object_type == 'WALL':
            obj_converted.name = 'wb_wall'

            bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple_Type='Rectangle', Simple_width=1, Simple_length=1, use_cyclic_u=True)
            obj_profile = context.object
            bpy.ops.curve.spline_type_set(type='POLY')
            obj_profile_data = obj_profile.data
            obj_profile.name = f'{obj_converted.name}_profile'
            #saving the profile context
            ctx_wall_profile = context.copy()

            #get all points
            points_height_co = []
            for point in obj_profile_data.splines[0].points:
                points_height_co.append(point)

            return points_height_co

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'CURVE'

    def execute(self, context):
        if True:
            co_s = self.generate_object(context)
            self.debug_method(co_s)
            
        else:
            # add geom nodes modifier to outside walls 
            WallBuilder.generate_object(bpy.context.object)

        self.report({'INFO'}, 'WALL BUILDER: {}'.format(self.bl_label))
        return {'FINISHED'}

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


class OPENINGS_OT_actions(bpy.types.Operator):
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


class CUSTOM_objectCollection(bpy.types.PropertyGroup):
    obj_type: StringProperty()
    obj_id: IntProperty()


def register():
    from bpy.utils import register_class
    register_class(WallBuilder)
    register_class(BuildingAssembler)
    register_class(CUSTOM_objectCollection)
    register_class(OPENINGS_OT_actions)

    bpy.types.Scene.custom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.custom_index = IntProperty()

def unregister():
    from bpy.utils import unregister_class
    unregister_class(WallBuilder)
    unregister_class(BuildingAssembler)
    unregister_class(CUSTOM_objectCollection)
    unregister_class(OPENINGS_OT_actions)

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

if __name__ == "__main__":
    register()

    