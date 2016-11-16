import pyglet


class Resource(object):
    def __init__(self):
        pyglet.resource.path = ['./']
        pyglet.resource.reindex()
        self.PALM_TREE = pyglet.resource.image('images/sprites/palm_tree.png')
        self.BILLBOARD08 = pyglet.resource.image('images/sprites/billboard08.png')
        self.TREE1 = pyglet.resource.image('images/sprites/tree1.png')
        self.DEAD_TREE1 = pyglet.resource.image('images/sprites/dead_tree1.png')
        self.BILLBOARD09 = pyglet.resource.image('images/sprites/billboard09.png')
        self.BOULDER3 = pyglet.resource.image('images/sprites/boulder3.png')
        self.COLUMN = pyglet.resource.image('images/sprites/column.png')
        self.BILLBOARD01 = pyglet.resource.image('images/sprites/billboard01.png')
        self.BILLBOARD06 = pyglet.resource.image('images/sprites/billboard06.png')
        self.BILLBOARD05 = pyglet.resource.image('images/sprites/billboard05.png')
        self.BILLBOARD07 = pyglet.resource.image('images/sprites/billboard07.png')
        self.BOULDER2 = pyglet.resource.image('images/sprites/boulder2.png')
        self.TREE2 = pyglet.resource.image('images/sprites/tree2.png')
        self.BILLBOARD04 = pyglet.resource.image('images/sprites/billboard04.png')
        self.DEAD_TREE2 = pyglet.resource.image('images/sprites/dead_tree2.png')
        self.BOULDER1 = pyglet.resource.image('images/sprites/boulder1.png')
        self.BUSH1 = pyglet.resource.image('images/sprites/bush1.png')
        self.CACTUS = pyglet.resource.image('images/sprites/cactus.png')
        self.BUSH2 = pyglet.resource.image('images/sprites/bush2.png')
        self.BILLBOARD03 = pyglet.resource.image('images/sprites/billboard03.png')
        self.BILLBOARD02 = pyglet.resource.image('images/sprites/billboard02.png')
        self.STUMP = pyglet.resource.image('images/sprites/stump.png')
        self.SEMI = pyglet.resource.image('images/sprites/semi.png')
        self.TRUCK = pyglet.resource.image('images/sprites/truck.png')
        self.CAR03 = pyglet.resource.image('images/sprites/car03.png')
        self.CAR02 = pyglet.resource.image('images/sprites/car02.png')
        self.CAR04 = pyglet.resource.image('images/sprites/car04.png')
        self.CAR01 = pyglet.resource.image('images/sprites/car01.png')
        self.PLAYER_UPHILL_LEFT = pyglet.resource.image('images/sprites/player_uphill_left.png')
        self.PLAYER_UPHILL_STRAIGHT = pyglet.resource.image('images/sprites/player_uphill_straight.png')
        self.PLAYER_UPHILL_RIGHT = pyglet.resource.image('images/sprites/player_uphill_right.png')
        self.PLAYER_LEFT = pyglet.resource.image('images/sprites/player_left.png')
        self.PLAYER_STRAIGHT = pyglet.resource.image('images/sprites/player_straight.png')
        self.PLAYER_RIGHT = pyglet.resource.image('images/sprites/player_right.png')

        # the reference sprite width should be 1/3rd the (half-)roadWidth
        self.SCALE = 0.3 * (1.0 / self.PLAYER_STRAIGHT.width)

        self.BILLBOARDS = [self.BILLBOARD01, self.BILLBOARD02, self.BILLBOARD03, self.BILLBOARD04,
                           self.BILLBOARD05, self.BILLBOARD06, self.BILLBOARD07,
                           self.BILLBOARD08, self.BILLBOARD09]
        self.PLANTS = [self.TREE1, self.TREE2, self.DEAD_TREE1, self.DEAD_TREE2, self.PALM_TREE,
                       self.BUSH1, self.BUSH2, self.CACTUS, self.STUMP,
                       self.BOULDER1, self.BOULDER2, self.BOULDER3]
        self.CARS = [self.CAR01, self.CAR02, self.CAR03, self.CAR04, self.SEMI, self.TRUCK]

        return


SPRITES = Resource()


if __name__ == '__main__':
    print SPRITES.SCALE
    print SPRITES.PALM_TREE.width, SPRITES.PALM_TREE.height
    print '1'
