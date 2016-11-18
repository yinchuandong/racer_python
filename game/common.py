from map import Map


# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

COLORS = Map({
    'SKY': (114, 215, 238),
    'TREE': (0, 81, 8),
    'FOG': (0, 81, 8),
    'LIGHT': Map({'road': (107, 107, 107), 'grass': (16, 170, 16), 'rumble': (85, 85, 85), 'lane': (204, 204, 204)}),
    'DARK': Map({'road': (105, 105, 105), 'grass': (0, 154, 0), 'rumble': (187, 187, 187)}),
    'START': Map({'road': WHITE, 'grass': WHITE, 'rumble': WHITE}),
    'FINISH': Map({'road': BLACK, 'grass': BLACK, 'rumble': BLACK})
})
