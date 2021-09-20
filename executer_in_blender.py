import os
import bpy

plugin_scripts_list = (
'__init__.py',
'tile_generator.py',
'floorplans_tools.py',
'custom_UI',
'python_plain.py'
)

exec(open(os.path.join(os.path.dirname(bpy.data.filepath), plugin_scripts_list[4])).read())