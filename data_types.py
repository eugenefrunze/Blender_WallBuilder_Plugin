import bpy

#---------------------------------------------------------------------------------------------------
# global plugin types
#---------------------------------------------------------------------------------------------------

customers_json = []

# customers_json_example = [
#     {
#         "ucm_id":"2", "mc_id":"1", "client_id":"391", "wall_height":"2500", "wall_out_thickness":"290",
#         "wall_in_thickness":"125", "wall_middle_thickness":"20", "windows_top":"2400", "foundation":"350",
#         "ceiling":"250", "mc_name":"Streif Haus GmbH", "client_name":"George Flor\u00e9"
#     },
#     {
#         "ucm_id":"3", "mc_id":"4", "client_id":"0", "wall_height":"2500", "wall_out_thickness":"320","wall_in_thickness":"150", "wall_middle_thickness":"0", "windows_top":"2130", "foundation":"350",
#         "ceiling":"250", "mc_name":"BSH Vertriebs GmbH", "client_name": None
#     },
#     {
#         "ucm_id":"4", "mc_id":"14", "client_id":"0", "wall_height":"2500", "wall_out_thickness":"290","wall_in_thickness":"125", "wall_middle_thickness":"0", "windows_top":"2125", "foundation":"350",
#         "ceiling":"250", "mc_name":"Apollo HAUS GmbH i. G. ", "client_name": None
#     },
#     {
#         "ucm_id":"5", "mc_id":"5","client_id":"0", "wall_height":"2500", "wall_out_thickness":"320",
#         "wall_in_thickness":"150", "wall_middle_thickness":"0", "windows_top":"2130", "foundation":"350",
#         "ceiling":"250", "mc_name":"Bodenseehaus Bau AG (Suisse)", "client_name":None
#     }
# ]

levels = (
    ('KG', 'KG (basement)', ''),
    ('EG', 'EG (1st floor)', ''),
    ('OG', 'OG (2nd floor)', ''),
    ('THIRD', '3rd floor', ''),
    ('DG', 'DG (last floor)', '')
)

class Objects_types:

    type: str
    name: str
    desc: str
    subtype: object

    def __init__(self, type='', name='', desc='', subtype=None):
        self.type = type
        self.name = name
        self.desc = desc
        self.subtype = subtype

    def get_prop_enum(self):
        return (self.type, self.name, self.desc)


def get_objects_types():
    wall = Objects_types('WALL', 'Wall', 'Wall desc')
    floor = Objects_types('FLOOR', 'Floor', 'Floor desc')
    opening = Objects_types('OPENING', 'Opening', 'Floor desc')
    helper = Objects_types('HELPER', 'Helper', 'Helper desc')
    return (wall.get_prop_enum(), floor.get_prop_enum(), opening.get_prop_enum(), helper.get_prop_enum())


openings_types = (
    ('WINDOW1', 'window 1', ''),
    ('DOOR1', 'door 1', ''),
)

helper_types = (
    ('WINDOW', 'Window helper', ''),
    ('DOOR', 'Door hepler', '')
)

wall_types = (
    ('OUTER', 'Outer wall', ''),
    ('INNER', 'Inner wall', '')
)

#---------------------------------------------------------------------------------------------------
# tools types
#---------------------------------------------------------------------------------------------------

fast_objects_types = (
    ('RECTANGLE', 'Rectangle', ''),
    ('LINE', 'Line', '')
)



#---------------------------------------------------------------------------------------------------
# register / unregister
#---------------------------------------------------------------------------------------------------

def register():
    from bpy.utils import register_class
    register_class(Objects_types)


def unregister():
    from bpy.utils import unregister_class
    unregister_class(Objects_types)


if __name__ == '__main__':
    register()