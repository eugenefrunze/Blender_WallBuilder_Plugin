import bpy
from mathutils import Vector

class MainPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_MainPanel'
    bl_label = 'Tile Generator panel'
    bl_category = 'TILE GENERATOR'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):

        # creation area
        layout = self.layout
        layout.label(text='Geometry')

        box = layout.box()
        box.label(text='Orientation specifiers')
        col = box.column()
        row = col.row(align=True)
        vert_props = row.operator(VertexSelector.bl_idname, icon='VERTEXSEL')
        row = col.row(align=True)
        edge_props = row.operator(EdgesSelector.bl_idname, icon='EDGESEL')
        box.label(text='Roof generator')
        col = box.column()
        row = col.row(align=True)
        props = row.operator(TileGenerator.bl_idname, icon='EXPERIMENTAL')
        row = col.row(align=True)
        if context.object:
            # if context.scene.object_tile_model:
            #     props.offset_pattern = [0.24499998 / 2, 0.416, 0]  # TileGenerator.get_pattern_offsets()
            # else:
            #     props.offset_pattern = [0, 0, 0]
            row.prop(context.object, "tiles_count_x")
            row.prop(context.object, "tiles_count_y")
            row = col.row(align=True)
            row.prop(context.scene, "object_tile_model", expand=True)
            row = col.row(align=True)
            row.prop(context.object, "bool_cutter_solver")
            props.bool_solver = context.object.bool_cutter_solver

        else:
            row.label(text='context.object is None')

        layout = self.layout
        box = layout.box()
        box.label(text='Properties')
        col = box.column()
        row = col.row()
        if bpy.context.object:
            row.label(text=f'OBJECT: {bpy.context.object.name}')
            row = col.row()
            row.prop(context.object, "prop_bias_vertical")

        layout = self.layout
        box = layout.box()
        box.label(text='test / debug')
        col = box.column()
        row = col.row()
        row.operator(RoofDimensionsCalculator.bl_idname, icon='EXPERIMENTAL')

# METHODS ======================================================================================================

def select_activate_object(object_to_select: bpy.types.Object, active: bool = False, deselect: bool = False, from_edit: bool = False, to_edit: bool = False, select_type='') -> None:
    if from_edit:
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.select_all(action='DESELECT')
    if deselect:
        return
    object_to_select.select_set(True)
    if active:
        bpy.context.view_layer.objects.active = object_to_select
    if to_edit:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if select_type:
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type=select_type)

def rotate_tile_to_roof_normal(roof: bpy.types.Object, polygons_indices) -> None:
    roof_normal = roof.data.polygons[polygons_indices[0]].normal
    vec = Vector(roof.matrix_world @ roof_normal)
    bpy.context.scene.object_tile_model.rotation_mode = 'QUATERNION'
    bpy.context.scene.object_tile_model.rotation_quaternion = vec.to_track_quat('Z', 'X')
    # setting the tile object selected and rotate it around Z
    select_activate_object(bpy.context.scene.object_tile_model, active=True, deselect=False, from_edit=True, to_edit=False)
    bpy.ops.transform.rotate(value=3.14159,
        orient_axis='Z', orient_type='LOCAL',
        constraint_axis=(False, False, True))

def get_selected_polys_indices(obj) -> list:
    """method returns a list with indices of selected faces"""
    selected_polys_indices = []
    for poly in obj.data.polygons:
        if poly.select:
            selected_polys_indices.append(poly.index)
    return selected_polys_indices

def get_tile_on_roof_location(obj: bpy.types.Object) -> Vector:
    """returns the location vector for tile object. At the moment (03.08.21)
    you have to specify reference vertex manually. Select the most __left__ vertex on the face/faces
    
    Args:
        obj (bpy.types.Object): object with verts
        
    Returns:
        Vector: returns selected vert global coords
    """
    for vert in obj.data.vertices:
        if vert.select:
            return obj.matrix_world @ vert.co
    return None

def get_selected_edges(obj: bpy.types.Object) -> list:
    """returns list of selected edges

    Args:
        obj (bpy.types.Object): object with edges

    Returns:
        list: selected edges
    """
    edges_sel = []
    for edge in obj.data.edges:
        if edge.select:
            edges_sel.append(edge.index)
    return edges_sel

# tile pattern generaator part
# method should be used to determine tiles count on width and height [x, y]. 04.08.21 - it uses fixed count: [50, 50]
def get_tiles_count(roof: bpy.types.Object) -> list:
    return [100, 100]

def generate_tiles_pattern(self, roof: bpy.types.Object, tile: bpy.types.Object, tile_dimensions: Vector):

    tiles_count = get_tiles_count(roof) #tiles needed to cover the roof

    mod_arr_pattern = tile.modifiers.new('tiles pattern', 'ARRAY')
    mod_arr_pattern.use_relative_offset = False
    mod_arr_pattern.use_constant_offset = True
    mod_arr_pattern.count = 2
    mod_arr_pattern.constant_offset_displace = [(-tile_dimensions[0] * tile.prop_bias_vertical), tile_dimensions[1] / 2, 0]

    # adding width rows
    mod_arr_y = tile.modifiers.new('tiles width', 'ARRAY')
    mod_arr_y.use_relative_offset = False
    mod_arr_y.use_constant_offset = True
    mod_arr_y.constant_offset_displace = [0, -tile_dimensions[1], 0]
    mod_arr_y.count = tiles_count[0]

    # adding height rows
    mod_arr_x = tile.modifiers.new('tiles height', 'ARRAY')
    mod_arr_x.use_relative_offset = False
    mod_arr_x.use_constant_offset = True
    mod_arr_x.count = tiles_count[1]
    mod_arr_x.constant_offset_displace = [-tile_dimensions[0] * 2 * tile.prop_bias_vertical, 0, 0]

def get_roof_dimensions():
    pass

def get_lowest_edge():
    pass

# OPERATORS ======================================================================================================

class RoofDimensionsCalculator(bpy.types.Operator):
    bl_idname = 'object.dimensions_calculator'
    bl_label = 'Calculate roof dimensions'

    def execute(self, context):

        roof_object = bpy.context.object
        roof_data = roof_object.data

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'


        selected_polys = [] #saves only indices
        selected_polys_vertices = [] # only their indices
        for poly in roof_data.polygons:
            if poly.select:
                selected_polys.append(poly.index)

        print('SLAVA KPSS!!!')

        self.report({'INFO'}, f'SELECTED POLYS INDICES: {selected_polys}')
        return {'FINISHED'}

class ParametersSetter(bpy.types.Operator):
    bl_idname = 'object.selection_info'
    bl_label = 'Set parameters'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pass

        self.report({'INFO'}, 'TI LOH')
        return {'FINISHED'} 

class EdgesSelector(bpy.types.Operator):
    bl_idname = 'object.edges_selector'
    bl_label = 'Select Edges'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        roof_object = bpy.context.object
        # set mode to 'OBJECT' to refresh selection
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.types.Object.edges_border = 'get_edges_border_indices'(roof_object)
        if len(bpy.context.object.edges_border) == 0:
            self.report({'ERROR'}, f'YOU HAVEN\'T SELECTED ANY EDGES')
            return {'CANCELLED'}
        self.report({'INFO'}, f'EDGES BORDER INDICES: {bpy.context.object.edges_border}')
        return {'FINISHED'}

class VertexSelector(bpy.types.Operator):
    bl_idname = 'object.vertex_selector'
    bl_label = 'Select Vertex'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        roof_object = bpy.context.object
        debug = False
        # set mode to 'OBJECT' to refresh selection
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        # determine tile location on the roof
        tile_location = get_tile_on_roof_location(roof_object)
        if tile_location is None:
            self.report({'ERROR'}, f'YOU HAVEN\'T SELECTED ANY VERTICES')
            return {'CANCELLED'}
        bpy.types.Object.tile_initial_position = tile_location
        # debug creates plain axes in the position of selected vertex <<<<<<<<<<<<<<< DEBUG
        if debug:
            bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=tile_location, scale=(1, 1, 1))
        # ======================================================== <<<<<<<<<<<<<<< END DEBUG
        self.report({'INFO'}, f'TILE INITIAL LOCATION IS: {bpy.types.Object.tile_initial_position}')
        return {'FINISHED'}

class TileGenerator(bpy.types.Operator):
    bl_idname = 'object.geometry_operator'
    bl_label = 'Generate tiles'
    bl_options = {'REGISTER', 'UNDO'}

    bool_solver: bpy.props.StringProperty(
        name='Solver method',
        description='Fast or exact method of bool cutting',
        default='FAST'
    )

    def execute(self, context):

        polygons_selected_indices = []
        verts_poly = []  # a list with vertices indices of the selected face
        verts_global_z = []  # a list with Z coordinates of face vertices
        verts_indices_on_edge = []  # a list with indices of the lower edge vertices
        redunant_edge_index: int # temporary edge for creation bool object

        roof_object = bpy.context.object
        roof_object_edit = bpy.context.edit_object
        roof_object_data = roof_object_edit.data
        
        # check if user has set tile model and orientation vector in the plugin panel
        if context.scene.object_tile_model and context.object.tile_initial_position:
            tile_object = context.scene.object_tile_model
            tile_dimensions = tile_object.dimensions
        else:
            self.report({'ERROR'}, 'YOU MUST SPECIFY TILE MODEL AND VERTEX BEFORE RUN GENERATOR')
            return {'CANCELLED'}

        if not tile_object.prop_bias_vertical:
            self.report({'ERROR'}, 'TILE OBJECT HAS BIAS PROPERTY 0. YOU HAVE TO SPECIFY IT FIRST')
            return {'CANCELLED'}

        # refresh selection information
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        

        for i, v in enumerate(roof_object_data.polygons[roof_object_data.polygons.active].vertices):
            verts_poly.append(v)
            verts_global_z.append((roof_object.matrix_world @ roof_object.data.vertices[v].co)[2])

        # geting one of the the lowest vertex Z position
        min_z = min(verts_global_z)

        # getting indices of vertex on the lower edge
        verts_indices_on_edge.append([val for i, val in enumerate(verts_poly) if verts_global_z[i] == min_z])
        verts_indices_on_edge = tuple(verts_indices_on_edge[0])

        # get selected polygons indices
        polygons_selected_indices = get_selected_polys_indices(roof_object)
        # rotate tile object to the roof polygons normal
        rotate_tile_to_roof_normal(roof_object, polygons_selected_indices)

        # searching for the index of the lower edge, using straight and reversed vertex indices, associated
        # with the edge, because they could been get in any order
        if verts_indices_on_edge in roof_object_data.edge_keys:
            lower_edge_index = roof_object_data.edge_keys.index(verts_indices_on_edge)
        elif verts_indices_on_edge[::-1] in roof_object_data.edge_keys:
            lower_edge_index = roof_object_data.edge_keys.index(verts_indices_on_edge[::-1])

        # selecting the lower edges. At the moment (04.08.21) you have to specify them manually
        for index in bpy.context.object.edges_border:
            roof_object.data.edges[index].select = True
        # roof_object.data.edges[lower_edge_index].select = True

        # selecting the roof object and enter the edit mode
        select_activate_object(roof_object, active=True, deselect=False, from_edit=False, to_edit=True, select_type='EDGE')

        # get extrude direction, based on roof normal. It uses 0-polygon in the list of selected polygons
        extrude_direction = Vector(roof_object.matrix_world @ roof_object_data.polygons[polygons_selected_indices[0]].normal)

        # extrude lower edge to save tile side
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False},
            TRANSFORM_OT_translate={"value":(extrude_direction[0] * 2, extrude_direction[1] * 2, 0), "orient_type":'LOCAL',
            "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'LOCAL', "constraint_axis":(True, False, False)})

        # find and redundant edge index
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        for i, edge in enumerate(context.object.data.edges):
            if edge.select:
                redunant_edge_index = i
                print(f'REDUNANT EDGE INDEX: {redunant_edge_index}')
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        # selecting faces from which the extrusion object will be created
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='FACE')
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        # select selected (omg) polygons
        for poly_index in polygons_selected_indices:
            roof_object.data.polygons[poly_index].select = True

        # setting tile position equal to selected vertex.
        # 04.08.21 bpy.context.object.tile_initial_position sat by the class VertexSelector operator
        bpy.context.scene.object_tile_model.location = bpy.context.object.tile_initial_position

        # roof tile pattern generation
        generate_tiles_pattern(self, roof_object, tile_object, tile_dimensions)

        # entering the edit mode again
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        # toggle off autowelder before use face dublication
        bpy.context.scene.tool_settings.use_mesh_automerge = False
        
        # call the extruder-cutter from here
        bpy.ops.mesh.duplicate_move(
            MESH_OT_duplicate={"mode": 1},
            TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_type": 'GLOBAL',
            "orient_matrix": ((0, 0, 0), (0, 0, 0), (0, 0, 0)),
            "orient_matrix_type": 'GLOBAL',
            "constraint_axis": (False, False, False)})

        # create and select, make active th esolver object
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        # deselect and deactivate roof object and set selection and active status to the future bool object
        # maybe have to rework it with the select_activate_object function
        bpy.context.active_object.select_set(False)
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        
        bpy.context.scene.object_bool_cutter = bpy.context.object
        
        # extrude bool object
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={"use_normal_flip": False, "use_dissolve_ortho_edges": False, "mirror": False},
            TRANSFORM_OT_translate={"value": (0, 0, 5), "orient_type": 'GLOBAL',
                                    "orient_matrix_type": 'GLOBAL',
                                    "constraint_axis": (False, False, True), "mirror": False,
                                    "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH',
                                    "proportional_size": 1, "use_proportional_connected": False,
                                    "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST',
                                    "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0),
                                    "gpencil_strokes": False, "cursor_transform": False, "texture_space": False,
                                    "remove_on_cancel": False, "release_confirm": False, "use_accurate": False,
                                    "use_automerge_and_split": False})

        # deleting face for some reason. Why? Maybe not?
        bpy.ops.mesh.delete(type='FACE')

        # moving bool object down little
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.transform.translate(value=(0, 0, -0.05), orient_type='GLOBAL',
                                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                    constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
                                    proportional_edit_falloff='SMOOTH', proportional_size=1,
                                    use_proportional_connected=False, use_proportional_projected=False,
                                    release_confirm=True)

        # applying modifiers to the roof tile object
        bpy.context.view_layer.objects.active = context.scene.object_tile_model
        bpy.ops.object.modifier_apply(modifier='tiles pattern', report=True)
        bpy.ops.object.modifier_apply(modifier='tiles width', report=True)
        bpy.ops.object.modifier_apply(modifier='tiles height', report=True)
        # applying bool modifier to cut via the shape
        bpy.context.object.modifiers.new(name='bool_to_cut', type='BOOLEAN')
        bpy.context.object.modifiers['bool_to_cut'].operation = 'INTERSECT'
        bpy.context.object.modifiers['bool_to_cut'].object = bpy.context.scene.object_bool_cutter
        bpy.context.object.modifiers["bool_to_cut"].solver = self.bool_solver
        print(f'SOLVER IS: {bpy.context.object.modifiers["bool_to_cut"].solver}')
        # apply modifier to cutted tiles
        bpy.ops.object.modifier_apply(modifier='bool_to_cut', report=False)

        # deleting the object_bool_cutter
        bool_cutter = bpy.context.scene.object_bool_cutter
        for collection in list(bool_cutter.users_collection):
            collection.objects.unlink(bool_cutter)
        if bool_cutter.users == 0:
            bpy.data.objects.remove(bool_cutter)

        # delete redunant polygons
        select_activate_object(roof_object, active=True)
        for edge_index in bpy.context.object.edges_border:
            roof_object.data.edges[edge_index].select = True
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='FACE')
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        for idx in polygons_selected_indices:
            roof_object.data.polygons[idx].select = False
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')

        self.report({'INFO'}, f'SELECTED ROOF OBJECT: {roof_object}')
        return {'FINISHED'}


# REGISTERING ======================================================================================================

classes = (
    MainPanel,
    TileGenerator,
    VertexSelector,
    EdgesSelector,
    ParametersSetter,
    RoofDimensionsCalculator
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.tiles_count_x = bpy.props.IntProperty(
        name='Tiles count width',
        description='Initial amount of tiles',
        default=1
      )

    bpy.types.Object.tiles_count_y = bpy.props.IntProperty(
        name='Tiles count height',
        description='Initial amount of tiles',
        default=1
    )

    # DEFINING PROPERTIES FOR THE REFERENCE TO THE TILE MODEL
    bpy.types.Scene.object_tile_model = bpy.props.PointerProperty(
        type=bpy.types.Object,
        name='Tile model',
        description='Reference to the object to use as a tile model'
    )

    bpy.types.MeshPolygon.polygon_roof_selected = bpy.props.PointerProperty(
        type=bpy.types.MeshPolygon,
        name='Roof polygon',
        description='The polygon of the roof to generate tiles on'
    )

    bpy.types.Scene.object_bool_cutter = bpy.props.PointerProperty(
        type=bpy.types.Object,
        name='Bool tile cutter',
        description='The bool shape object to cut roof tiles'
    )

    bpy.types.Object.bool_cutter_solver = bpy.props.EnumProperty(
        name='Bool solver',
        description='',
        items=[
            ('FAST', 'Fast', 'The fast'),
            ('EXACT', 'Exact', 'The exact')
        ]
    )

    bpy.types.Object.prop_bias_vertical = bpy.props.FloatProperty(
        name='Bias vertical in %',
        description='Relative vertical bias of the obect in future array. Could be used for the roof tiles to determine vertical overlap',
        default=0
    )

    bpy.types.Object.tile_initial_position = Vector()

    bpy.types.Object.edges_border = list()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.tiles_count_x
    del bpy.types.Object.tiles_count_y
    del bpy.types.Scene.object_tile_model
    # del bpy.types.Scene.tgen_proxy_path
    del bpy.types.Object.tgen_proxy_name
    del bpy.types.Scene.test_prop_caller
    del bpy.types.MeshPolygon.selected_roof_polygon