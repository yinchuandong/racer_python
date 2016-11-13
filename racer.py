import random
import sys

import pygame
from pygame.locals import *

from map import Map
import util
import render


FPS = 30
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

ROAD = Map()
ROAD.LENGTH = Map({
    'NONE': 0, 'SHORT': 25, 'MEDIUM': 50, 'LONG': 100
})
ROAD.HILL = Map({
    'NONE': 0, 'LOW': 20, 'MEDIUM': 40, 'HIGH': 100
})
ROAD.CURVE = Map({
    'NONE': 0, 'EASY': 2, 'MEDIUM': 4, 'HARD': 6
})


class Racer(object):

    def __init__(self):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('racer')

        self.step = 1.0 / FPS
        self.centrifugal = 0.3
        self.sky_speed = 0.001
        self.hill_speed = 0.002
        self.tree_speed = 0.003
        self.sky_offset = 0
        self.hill_offset = 0
        self.tree_offset = 0
        self.segments = []
        self.cars = []
        self.road_width = 2000
        self.segment_length = 200
        self.rumble_length = 3
        self.lanes = 3
        self.field_of_view = 100
        self.camera_height = 1000
        self.camera_depth = None
        self.draw_distance = 300
        self.player_x = 0
        self.player_x = None
        self.fog_density = 5
        self.position = 0  # current camera z
        self.speed = 0
        self.max_speed = self.segment_length / self.step
        self.accel = self.max_speed / 5
        self.breaking = -self.max_speed
        self.decel = - self.max_speed / 5
        self.off_road_decel = -self.max_speed / 2
        self.off_road_limit = self.max_speed / 4
        self.total_cars = 200

        self.update()
        self.img = pygame.image.load('images/sprites/billboard01.png')
        return

    def update(self):
        # self.screen.fill((255,255,255))
        # pygame.draw.rect(self.screen, (0,0,255), (200, 150, 100, 50))
        self.screen.fill(WHITE)
        # pygame.draw.polygon(self.screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)
        render.polygon(self.screen, 0, 0, 0, 100, 100, 100, 100, 0, BLACK)
        return

    def last_y(self):
        length = len(self.segments)
        return 0 if length == 0 else self.segments[length - 1].p2.word.y

    def find_segment(self, z):
        return

    def add_segment(self, curve, y):
        n = len(self.segments)
        segment = Map()
        segment.index = n

        segment.p1 = Map()
        segment.p1.word = Map()
        segment.p1.word.y = self.last_y()
        segment.p1.word.z = n * self.segment_length
        segment.p1.camera = Map()
        segment.p1.screen = Map()

        segment.p2 = Map()
        segment.p2.word = Map()
        segment.p2.word.y = y
        segment.p2.word.z = n * self.segment_length
        segment.p2.camera = Map()
        segment.p2.screen = Map()

        segment.curve = curve
        segment.sprites = []
        segment.cars = []
        # todo:
        segment.color = math.floor(float(n) / self.rumble_length)

        # todo: add color
        self.segments.append(segment)
        # print self.segments
        return

    def add_road(self, enter, hold, leave, curve, y):
        start_y = self.last_y()
        end_y = start_y + int(y) * self.segment_length
        total = enter + hold + leave
        for n in range(enter):
            self.add_segment(util.ease_in(0, curve, n / enter), util.ease_in_out(start_y, end_y, n / total))
        for n in range(hold):
            self.add_segment(curve, util.ease_in_out(start_y, end_y, (enter + n) / total))
        for n in range(leave):
            self.add_segment(util.ease_in_out(curve, 0, n / leave),
                             util.ease_in_out(start_y, end_y, (enter + hold + n) / total))
        return

    def addStraight(self, num=20):
        self.add_road(num, num, num, 0, 0)
        return

    def render_sprite(self):
        for n in range(len(self.segments)):
            segment = self.segments[n]
            render.segment(
                self.screen, SCREEN_WIDTH, 3,
                segment.p1.screen.x,
                segment.p1.screen.y,
                segment.p1.screen.w,
                segment.p2.screen.x,
                segment.p2.screen.y,
                segment.p2.screen.w,
                0,
                segment.color
            )
        return


def main():
    racer = Racer()
    racer.addStraight()
    speed = [2, 2]
    ballrect = racer.img.get_rect()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > SCREEN_WIDTH:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > SCREEN_HEIGHT:
            speed[1] = -speed[1]

        racer.update()
        racer.render_sprite()
        # racer.screen.blit(racer.img, ballrect)
        # pygame.display.flip()
        pygame.display.update()
    return


def test():
    racer = Racer()
    racer.add_segment(1, 2)
    return

if __name__ == '__main__':
    main()
    # test()
