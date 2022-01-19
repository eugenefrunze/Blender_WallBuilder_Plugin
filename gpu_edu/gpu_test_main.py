import bpy
import blf

from . draw_op import OT_draw_operator

addon_keymaps = []

def register():
    from bpy.utils import register_class
    register_class(OT_draw_operator)

    kcfg = bpy.context.window_manager.keyconfigs.addon
    print('KEYCONFIG: ', kcfg)
    if kcfg:
        km = kcfg.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('object.draw_op', 'F', 'PRESS', shift=True, ctrl=True)

        addon_keymaps.append((km, kmi))

def unregister():
    from bpy.utils import unregister_class

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    unregister_class(OT_draw_operator)

# if __name__ == '__main__':
#     register()