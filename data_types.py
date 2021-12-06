import bpy

customers = [
    {
        'client_id': 0, 'client_name': 'common', 'wall_height': 2500, 'wall_out_thickness': 300,
        'wall_in_thickness': 150, 'windows_top': 2140, 'foundation': 400, 'ceiling': 250
    },
    {
        'client_id': 1, 'client_name': 'customer1', 'wall_height': 2500, 'wall_out_thickness': 300,
        'wall_in_thickness': 150, 'windows_top': 2140, 'foundation': 400, 'ceiling': 250
    },
    {
        'client_id': 2, 'client_name': 'customer2', 'wall_height': 2500, 'wall_out_thickness': 290,
        'wall_in_thickness': 125, 'windows_top': 2400, 'foundation': 350, 'ceiling': 250
    },
    {
        'client_id': 3, 'client_name': 'customer3', 'wall_height': 2500, 'wall_out_thickness': 320,
        'wall_in_thickness': 150, 'windows_top': 2130, 'foundation': 350, 'ceiling': 250
    },
    {
        'client_id': 4, 'client_name': 'customer4', 'wall_height': 2500, 'wall_out_thickness': 290,
        'wall_in_thickness': 125, 'windows_top': 2140, 'foundation': 350, 'ceiling': 250
    },
    {
        'client_id': 5, 'client_name': 'customer5', 'wall_height': 2500, 'wall_out_thickness': 320,
        'wall_in_thickness': 150, 'windows_top': 2130, 'foundation': 350, 'ceiling': 250
    }
]

customers_json = [
    {
        "ucm_id":"1", "mc_id":"0", "client_id":"0", "wall_height":"2500", "wall_out_thickness":"300",
        "wall_in_thickness":"150", "windows_top":"2140", "foundation":"400", "ceiling":"250"
    },
    {
        "ucm_id":"2", "mc_id":"1", "client_id":"0", "wall_height":"2500", "wall_out_thickness":"290",
        "wall_in_thickness":"125", "windows_top":"2400", "foundation":"350", "ceiling":"250"
    },
    {
        "ucm_id":"3","mc_id":"4","client_id":"0","wall_height":"2500","wall_out_thickness":"320",
        "wall_in_thickness":"150","windows_top":"2130","foundation":"350","ceiling":"250"
    },
    {
        "ucm_id":"4", "mc_id":"11", "client_id":"0", "wall_height":"2500", "wall_out_thickness":"290",
        "wall_in_thickness":"125", "windows_top":"2140", "foundation":"350", "ceiling":"250"
    },
    {
        "ucm_id":"5", "mc_id":"5", "client_id":"0", "wall_height":"2500", "wall_out_thickness":"320",
        "wall_in_thickness":"150", "windows_top":"2130", "foundation":"350", "ceiling":"250"
    }
]

levels = (
    ('KG', 'KG (basement)', ''),
    ('EG', 'EG (1st floor)', ''),
    ('OG', 'OG (2nd floor)', ''),
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

    return (wall.get_prop_enum(), floor.get_prop_enum(), opening.get_prop_enum())

openings_types = (
    ('WINDOW1', 'window 1', ''),
    ('DOOR1', 'door 1', ''),
)

def register():
    from bpy.utils import register_class
    register_class(Objects_types)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(Objects_types)

if __name__ == '__main__':
    register()