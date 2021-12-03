position = (
    'outside', 
    'center',
    'outside'
)

properties = (
    'thickness',
    'position',
    'wall_height',
    'opening_elevation',
    'opening_top_offset',
    'level'
)

customers = [
    ('strafe', 'strafe desc', ''),
    ('bodenseehaus', 'boden desc', '')
]

customers_params = {
    'strafe' : {0.29, 0.12, 2.3},
    'bodenseehaus' : {0.25, 0.2, 2.9}
}

levels = (
    ('KG', 'basement (KG)', ''),
    ('OG', '2nd floor (OG)', ''),
    ('EG', '1st floor (EG)', ''),
    ('DG', 'last floor (DG)', '')
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


def get_openings_types():
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