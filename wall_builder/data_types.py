properties = (
    'outer_wall_thickness',
    'inner_wall_thickness', #replace with just thickness, no outer and inner
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

levels = {
    'KG' : 'basement',
    'OG' : '2nd floor',
    'EG' : '1st floor',
    'DG' : 'last floor'
}

objects_names = (
    'floor',
    'wall_outer',
    'wall_inner',
)