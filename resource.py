import pygame
from pygame.image import load
from map import Map


def preload():
    SPRITES = Map({
        'PALM_TREE': load('images/sprites/palm_tree.png').convert_alpha(),
        'BILLBOARD08': load('images/sprites/billboard08.png').convert_alpha(),
        'TREE1': load('images/sprites/tree1.png').convert_alpha(),
        'DEAD_TREE1': load('images/sprites/dead_tree1.png').convert_alpha(),
        'BILLBOARD09': load('images/sprites/billboard09.png').convert_alpha(),
        'BOULDER3': load('images/sprites/boulder3.png').convert_alpha(),
        'COLUMN': load('images/sprites/column.png').convert_alpha(),
        'BILLBOARD01': load('images/sprites/billboard01.png').convert_alpha(),
        'BILLBOARD06': load('images/sprites/billboard06.png').convert_alpha(),
        'BILLBOARD05': load('images/sprites/billboard05.png').convert_alpha(),
        'BILLBOARD07': load('images/sprites/billboard07.png').convert_alpha(),
        'BOULDER2': load('images/sprites/boulder2.png').convert_alpha(),
        'TREE2': load('images/sprites/tree2.png').convert_alpha(),
        'BILLBOARD04': load('images/sprites/billboard04.png').convert_alpha(),
        'DEAD_TREE2': load('images/sprites/dead_tree2.png').convert_alpha(),
        'BOULDER1': load('images/sprites/boulder1.png').convert_alpha(),
        'BUSH1': load('images/sprites/bush1.png').convert_alpha(),
        'CACTUS': load('images/sprites/cactus.png').convert_alpha(),
        'BUSH2': load('images/sprites/bush2.png').convert_alpha(),
        'BILLBOARD03': load('images/sprites/billboard03.png').convert_alpha(),
        'BILLBOARD02': load('images/sprites/billboard02.png').convert_alpha(),
        'STUMP': load('images/sprites/stump.png').convert_alpha(),
        'SEMI': load('images/sprites/semi.png').convert_alpha(),
        'TRUCK': load('images/sprites/truck.png').convert_alpha(),
        'CAR03': load('images/sprites/car03.png').convert_alpha(),
        'CAR02': load('images/sprites/car02.png').convert_alpha(),
        'CAR04': load('images/sprites/car04.png').convert_alpha(),
        'CAR01': load('images/sprites/car01.png').convert_alpha(),
        'PLAYER_UPHILL_LEFT': load('images/sprites/player_uphill_left.png').convert_alpha(),
        'PLAYER_UPHILL_STRAIGHT': load('images/sprites/player_uphill_straight.png').convert_alpha(),
        'PLAYER_UPHILL_RIGHT': load('images/sprites/player_uphill_right.png').convert_alpha(),
        'PLAYER_LEFT': load('images/sprites/player_left.png').convert_alpha(),
        'PLAYER_STRAIGHT': load('images/sprites/player_straight.png').convert_alpha(),
        'PLAYER_RIGHT': load('images/sprites/player_right.png').convert_alpha(),
    })
    # the reference sprite width should be 1/3rd the (half-)roadWidth
    SPRITES.SCALE = 0.3 * (1.0 / SPRITES.PLAYER_STRAIGHT.get_width())
    SPRITES.BILLBOARDS = [SPRITES.BILLBOARD01, SPRITES.BILLBOARD02, SPRITES.BILLBOARD03, SPRITES.BILLBOARD04,
                          SPRITES.BILLBOARD05, SPRITES.BILLBOARD06, SPRITES.BILLBOARD07,
                          SPRITES.BILLBOARD08, SPRITES.BILLBOARD09]
    SPRITES.PLANTS = [SPRITES.TREE1, SPRITES.TREE2, SPRITES.DEAD_TREE1, SPRITES.DEAD_TREE2, SPRITES.PALM_TREE,
                      SPRITES.BUSH1, SPRITES.BUSH2, SPRITES.CACTUS, SPRITES.STUMP,
                      SPRITES.BOULDER1, SPRITES.BOULDER2, SPRITES.BOULDER3]
    SPRITES.CARS = [SPRITES.CAR01, SPRITES.CAR02, SPRITES.CAR03, SPRITES.CAR04, SPRITES.SEMI, SPRITES.TRUCK]
    return SPRITES


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    SPRITES = preload()
    pygame.display.set_caption('racer')
    print SPRITES.SCALE
    print SPRITES.PLAYER_STRAIGHT.get_rect()

    print '1'
