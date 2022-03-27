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

objects_types = (
    ('WALL', 'wall', ''),
    ('FLOOR', 'floor', ''),
    ('OPENING', 'opening', '')
)

openings_types = (
    ('WINDOW1', 'window 1', ''),
    ('DOOR1', 'door 1', ''),
)