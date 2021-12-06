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

wall = Objects_types('WALL', 'Wall', 'Wall desc')
floor = Objects_types('FLOOR', 'Floor', 'Floor desc')
opening = Objects_types('OPENING', 'Floor', 'Floor desc')

objects_types = (
    wall.get_prop_enum(),
    floor.get_prop_enum(),
    opening.get_prop_enum()
)

a = 5
b = str(a)
print(type(b))