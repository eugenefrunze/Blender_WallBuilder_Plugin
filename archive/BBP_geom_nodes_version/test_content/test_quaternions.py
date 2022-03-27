import math
import bpy
import bmesh
import mathutils

C = bpy.context
D = bpy.data

# ob = C.object
# od = ob.data

roof_or = bpy.data.objects['Plane.002']
tile_or = bpy.data.objects['tile_or']

polygons = bpy.context.object.data.polygons[:]
print(polygons)
print(polygons[0].normal)
print(bpy.context.object.data.polygons[0].normal)

normal_global = roof_or.matrix_world @ polygons[0].normal
print(normal_global)
print(bpy.context.object.matrix_world @ bpy.context.object.data.polygons[0].normal)

tile_or.rotation_euler = (bpy.context.object.matrix_world @ bpy.context.object.data.polygons[0].normal).to_track_quat('-Y', 'Y').to_euler()


# roof_normal = roof_or.data.polygons[0].normal
# roof_normal_global = roof_or.matrix_world @ roof_normal
#
# roof_direction = mathutils.Vector(roof_normal_global)
# tile_or.rotation_euler = roof_direction.to_track_quat('Z', 'X').to_euler()

# bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='LOCAL',
# constraint_axis=(False, False, True),
# mirror=True, use_proportional_edit=False,
# proportional_edit_falloff='SMOOTH',
# proportional_size=1, use_proportional_connected=False,
# use_proportional_projected=False)



#tile_or.rotation_mode = 'QUATERNION'
#tile_or.rotation_quaternion = roof_direction.to_track_quat('Z')









# get selected polys and get slope methods =============================================

# def get_selected_polys(obj, debug: bool) -> [bpy.types.MeshPolygon]:
#     selected_polys = []
#     for poly in obj.data.polygons:
#         if poly.select:
#             selected_polys.append(poly)
#     if debug:
#         print(f'seleced polygons are: {selected_polys}')
#     return selected_polys


# def get_roof_rotation_coplanar(polygons, debug: bool, coplanar=True) -> float:
#     normal = polygons[0].normal
#     horiz_angle_normal_deg = math.degrees(math.atan(normal[2] / math.sqrt((normal[0] ** 2) + (normal[1] ** 2))))
#     horiz_angle_deg = 90 - horiz_angle_normal_deg
#     if debug:
#         print(f'horiz coplanar roof angle: {angle_deg} deg')
#     return horiz_angle_deg

# selected_polygons = get_selected_polys(ob, True)
# get_roof_slope_angle_coplanar(selected_polygons, coplanar=True, debug=True)


# create mesh from data ==================================================

# verts = [
#     (1.0, 1.0, 0.0),
#     (-1.0, 1.0, 0.0),
#     (-1.0, -1.0, 0.0),
#     (1.0, -1.0, 0.0)
# ]
#
# edges = [
#     (0, 1),
#     (1, 2),
#     (2, 3),
#     (3, 4)
# ]
#
# polygons = [
#     [3, 2, 1, 0]
# ]
#
#
# mesh_name = 'the_mesh'
# object_name = 'the_object'
# mesh = bpy.data.meshes.new(mesh_name)
# obj = bpy.data.objects.new(object_name, mesh)
# bpy.data.collections['Collection'].objects.link(obj)
# bpy.context.view_layer.objects.active = obj
# mesh.from_pydata(verts, [], polygons)