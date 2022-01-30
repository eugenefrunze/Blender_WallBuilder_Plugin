import bpy
from . import data_types
import urllib.request, urllib.error, json
from json.decoder import JSONDecodeError

from mathutils import Vector


#---------------------------------------------------------------------------------------------------
# BASIC OPERATIONS
#---------------------------------------------------------------------------------------------------

#set object parent
def set_parent(children: list, parent: bpy.types.Object, keep_transform: bool, context: bpy.context) -> None:
    """children have to be a list or tuple"""
    ctx = context.copy()
    ctx['active_object'] = parent
    ctx['selected_objects'] = children
    ctx['selected_editable_objects'] = children
    bpy.ops.object.parent_set(ctx, keep_transform=keep_transform)


#---------------------------------------------------------------------------------------------------
# CUSTOM OPERATIONS
#---------------------------------------------------------------------------------------------------


#objects generation --------------------------------------------------------------------------------

#get object's bounds in coords
def get_object_bounds_coords(object: bpy.types.Object, space: str = 'WORLD') -> tuple:
    """calculates an object's maximum and minimum world positions
    on axes. Returns a tuple of type: (x_max, y_max, z_max, x_min, y_min, z_min).
    Space should be 'WORLD' for global coords system, and 'OBJECT' for local coords system"""

    obj_verts = object.data.vertices
    v_cords_x = []
    v_cords_y = []
    v_cords_z = []
    for v in obj_verts:
        if space == 'WORLD':
            v_cords_x.append((object.matrix_world @ v.co)[0])
            v_cords_y.append((object.matrix_world @ v.co)[1])
            v_cords_z.append((object.matrix_world @ v.co)[2])
        elif space == 'OBJECT':
            v_cords_x.append(v.co[0])
            v_cords_y.append(v.co[1])
            v_cords_z.append(v.co[2])
    x_min = min(v_cords_x)
    x_max = max(v_cords_x)
    y_min = min(v_cords_y)
    y_max = max(v_cords_y)
    z_min = min(v_cords_z)
    z_max = max(v_cords_z)
    # print(z_min)
    
    return (x_max, y_max, z_max, x_min, y_min, z_min)

#get object's bounds vertices indices
def get_bounder_vertices(object: bpy.types.Object) -> list:
    """gets parallelepiped object that will be used as bounding box,
    and returns groups of vertices of faces, depending on the position
    of the polygons normals in relation to the coordinate axes. Returns
    list of lists vertices in the order: [[x+][y+][z+],[x-],[y-],[z-]]"""

    obj_data = object.data
    v_idxs = [[], [], [], [], [], []]
    # print('V DATA HERE')
    for p in obj_data.polygons:
        for idx, v in enumerate(list(p.normal)):
            if v > 0:
                v_idxs[idx] = list(p.vertices)
            elif v < 0:
                v_idxs[idx + 3] = list(p.vertices)

    return v_idxs

#curves generators
def curve_create_line(self, context, start: tuple, end: tuple) -> bpy.types.Object:
    bpy.ops.curve.simple(
        align='WORLD', 
        location=(0, 0, 0), 
        rotation=(0, 0, 0), 
        Simple_Type='Line', 
        shape='2D', 
        outputType='POLY', 
        use_cyclic_u=False,
        edit_mode=False)
    obj = context.object
    mat_world = obj.matrix_world
    obj.data.splines[0].points[0].co = mat_world.inverted() @ Vector(start)

    point0_pos = obj.data.splines[0].points[0].co
    obj.data.splines[0].points[1].co = (point0_pos[0] + context.scene.tools_props.new_length, point0_pos[1], point0_pos[2], point0_pos[3])
    


    # bpy.ops.transform.resize(value=(1, 1, 0))
    # mat_world = obj.matrix_world
    # obj.data.splines[0].points[0].co = mat_world.inverted() @ Vector(start)
    # end_vec = Vector((start[0] + context.scene.tools_props.new_length, end[1], end[2], end[3]))
    # print(end_vec)
    # obj.data.splines[0].points[1].co = mat_world.inverted() @ end_vec
    
    context.object.data.fill_mode = 'NONE'
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

    return context.object

def curve_create_rectangle(self, context) -> bpy.types.Object:
    length = context.scene.tools_props.new_length
    width = context.scene.tools_props.new_width
    #create shape
    bpy.ops.curve.simple(
        align='WORLD', 
        location=(0, 0, 0), 
        rotation=(0, 0, 0), 
        Simple_Type='Rectangle', 
        Simple_width=width, 
        Simple_length=length, 
        shape='2D', 
        outputType='POLY', 
        use_cyclic_u=True, 
        edit_mode = False)
    #remove filling
    context.object.data.fill_mode = 'NONE'
    

    return context.object

#geometry nodes ------------------------------------------------------------------------------------

#geom nodes connector method
def node_group_link(node_group, node1_output, node2_input):
    node_group.links.new(node1_output, node2_input)


#web operations ------------------------------------------------------------------------------------

#generate customers list from API
def get_customers_info():
    interface_list_generated = []
    url = 'https://www.bauvorschau.com/api/clients_measures'
    errmessage = 'BBP->Utils->get_customers_info(): '
    try:
        responce = urllib.request.urlopen(url)
    except urllib.error.URLError as err:
        print(errmessage, err)
        return [('URL_ERR', 'CUSTOMERS DATA NOT LOADED', 'error in the utils->get_customers_info()->urlopen()')]
    else:
        try:
            customers = json.loads(responce.read())
        except JSONDecodeError as err:
            print(errmessage, err)
            return [('JSON_ERR', 'CUSTOMERS DATA NOT LOADED', 'error in the Butils->get_customers_info()->json.loads()')]
        else:
            data_types.customers_json = customers
            for customer in customers:
                interface_list_generated.append((customer['ucm_id'], customer['mc_name'], ''))

            return interface_list_generated
