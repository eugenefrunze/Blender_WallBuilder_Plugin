import bpy
import bmesh


class OT_Test_Operator(bpy.types.Operator):
    bl_idname = 'object.test_bmesh'
    bl_label = 'test bmesh'

    def execute(self, context):

        verts = []
        edges = []
        polys = []

        verts.append([1, 1, 0])
        verts.append([-1, 1, 0])
        verts.append([-1, -1, 0])
        verts.append([1, -1, 0])

        print(verts)




        return {'FINISHED'}

def register():
    from bpy.utils import register_class

    register_class(OT_Test_Operator)
def unregister():
    from bpy.utils import unregister_class

    unregister_class(OT_Test_Operator)
