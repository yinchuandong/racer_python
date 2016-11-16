import random
import sys
import math

import pyglet

from map import Map
import util
import render
from resource import SPRITES
from common import *


FPS = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


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

game_window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
# pyglet.gl.glTranslatef(0, -SCREEN_HEIGHT, 0)


class Racer(object):

    def __init__(self):
        self.reset()
        return

    def reset(self):
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
        # todo: need to be removed
        # self.background = None
        # self.sprites = None
        self.resolution = SCREEN_HEIGHT / 480.0
        self.road_width = 2000
        self.segment_length = 200
        self.rumble_length = 3
        self.track_length = None
        self.lanes = 3
        self.field_of_view = 100
        self.camera_height = 1000
        self.camera_depth = 1.0 / math.tan((self.field_of_view / 2.0) * math.pi / 180.0)
        self.draw_distance = 300
        self.player_sprite = pyglet.sprite.Sprite(img=SPRITES.PLAYER_STRAIGHT)
        self.player_x = 0
        self.player_z = self.camera_height * self.camera_depth
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

        self.key_left = False
        self.key_right = False
        self.key_faster = False
        self.key_slower = False

        self.reset_road()
        return

    def last_y(self):
        length = len(self.segments)
        return 0 if length == 0 else self.segments[length - 1].p2.world.y

    def find_segment(self, z):
        index = int(math.floor(float(z) / self.segment_length) % len(self.segments))
        return self.segments[index]

    def add_segment(self, curve, y):
        n = len(self.segments)
        segment = Map()
        segment.index = n

        segment.p1 = Map()
        segment.p1.world = Map()
        segment.p1.world.y = self.last_y()
        segment.p1.world.z = n * self.segment_length
        segment.p1.camera = Map()
        segment.p1.screen = Map()

        segment.p2 = Map()
        segment.p2.world = Map()
        segment.p2.world.y = y
        segment.p2.world.z = (n + 1) * self.segment_length
        segment.p2.camera = Map()
        segment.p2.screen = Map()

        segment.curve = curve
        segment.sprites = []
        segment.cars = []
        segment.color = COLORS.DARK if math.floor(float(n) / self.rumble_length) % 2 == 0 else COLORS.LIGHT

        # todo: add color
        self.segments.append(segment)
        # print self.segments
        return

    def add_sprite(self, n, sprite_img, offset):
        sprite = pyglet.sprite.Sprite(img=sprite_img)
        self.segments[n].sprites.append(Map({'source': sprite, 'offset': offset}))
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

    def add_straight(self, num=ROAD.LENGTH.MEDIUM):
        self.add_road(num, num, num, 0, 0)
        # todo:
        self.track_length = len(self.segments) + self.segment_length
        return

    def add_hill(self, num=ROAD.LENGTH.MEDIUM, height=ROAD.HILL.MEDIUM):
        self.add_road(num, num, num, 0, height)
        return

    def add_curve(self, num=ROAD.LENGTH.MEDIUM, curve=ROAD.CURVE.MEDIUM, height=ROAD.HILL.MEDIUM):
        self.add_road(num, num, num, curve, height)
        return

    def add_low_rolling_hills(self, num=ROAD.LENGTH.MEDIUM, height=ROAD.HILL.MEDIUM):
        self.add_road(num, num, num, 0, height / 2)
        self.add_road(num, num, num, 0, -height)
        self.add_road(num, num, num, ROAD.CURVE.EASY, height)
        self.add_road(num, num, num, 0, 0)
        self.add_road(num, num, num, -ROAD.CURVE.EASY, height / 2)
        self.add_road(num, num, num, 0, 0)
        return

    def add_s_curves(self):
        self.add_road(ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, -ROAD.CURVE.EASY, ROAD.HILL.NONE)
        self.add_road(ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, ROAD.CURVE.MEDIUM, ROAD.HILL.MEDIUM)
        self.add_road(ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, ROAD.CURVE.EASY, -ROAD.HILL.LOW)
        self.add_road(ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, -ROAD.CURVE.EASY, ROAD.HILL.MEDIUM)
        self.add_road(ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, ROAD.LENGTH.MEDIUM, -ROAD.CURVE.MEDIUM, -ROAD.HILL.MEDIUM)
        return

    def add_bumps(self):
        self.add_road(10, 10, 10, 0, 5)
        self.add_road(10, 10, 10, 0, -2)
        self.add_road(10, 10, 10, 0, -5)
        self.add_road(10, 10, 10, 0, 8)
        self.add_road(10, 10, 10, 0, 5)
        self.add_road(10, 10, 10, 0, -7)
        self.add_road(10, 10, 10, 0, 5)
        self.add_road(10, 10, 10, 0, -2)
        return

    def add_down_hill_to_end(self, num=200):
        self.add_road(num, num, num, -ROAD.CURVE.EASY, -self.last_y() / self.segment_length)
        return

    def reset_road(self):
        self.segments = []

        self.add_straight(ROAD.LENGTH.SHORT)
        self.add_low_rolling_hills()
        self.add_s_curves()
        self.add_curve(ROAD.LENGTH.MEDIUM, ROAD.CURVE.MEDIUM, ROAD.HILL.LOW)
        self.add_bumps()
        self.add_low_rolling_hills()
        self.add_curve(ROAD.LENGTH.LONG * 2, ROAD.CURVE.MEDIUM, ROAD.HILL.MEDIUM)
        self.add_straight()
        self.add_hill(ROAD.LENGTH.MEDIUM, ROAD.HILL.HIGH)
        self.add_s_curves()
        self.add_curve(ROAD.LENGTH.LONG, -ROAD.CURVE.MEDIUM, ROAD.HILL.NONE)
        self.add_hill(ROAD.LENGTH.LONG, ROAD.HILL.HIGH)
        self.add_curve(ROAD.LENGTH.LONG, ROAD.CURVE.MEDIUM, -ROAD.HILL.LOW)
        self.add_bumps()
        self.add_hill(ROAD.LENGTH.LONG, -ROAD.HILL.MEDIUM)
        self.add_straight()
        self.add_s_curves()
        self.add_down_hill_to_end()

        # todo
        self.reset_sprites()
        self.reset_cars()

        self.segments[self.find_segment(self.player_z).index + 2].color = COLORS.START
        self.segments[self.find_segment(self.player_z).index + 3].color = COLORS.START

        for n in range(self.rumble_length):
            self.segments[len(self.segments) - 1 - n].color = COLORS.FINISH
        self.track_length = len(self.segments) * self.segment_length

        return

    def reset_sprites(self):
        return
        self.add_sprite(20, SPRITES.BILLBOARD07, -1)
        self.add_sprite(40, SPRITES.BILLBOARD06, -1)
        self.add_sprite(60, SPRITES.BILLBOARD08, -1)
        self.add_sprite(80, SPRITES.BILLBOARD09, -1)
        self.add_sprite(100, SPRITES.BILLBOARD01, -1)
        self.add_sprite(120, SPRITES.BILLBOARD02, -1)
        self.add_sprite(140, SPRITES.BILLBOARD03, -1)
        self.add_sprite(160, SPRITES.BILLBOARD04, -1)
        self.add_sprite(180, SPRITES.BILLBOARD05, -1)

        self.add_sprite(240, SPRITES.BILLBOARD07, -1.2)
        self.add_sprite(240, SPRITES.BILLBOARD06, 1.2)
        self.add_sprite(len(self.segments) - 25, SPRITES.BILLBOARD07, -1.2)
        self.add_sprite(len(self.segments) - 25, SPRITES.BILLBOARD06, 1.2)

        # add palm tree
        n = 10
        while(n < 200):
            self.add_sprite(n, SPRITES.PALM_TREE, 0.5 + random.random() * 0.5)
            self.add_sprite(n, SPRITES.PALM_TREE, 1 + random.random() * 2)
            n += 4 + int(math.floor(n / 100.0))

        # add column
        for n in range(250, 1000, 5):
            self.add_sprite(n, SPRITES.COLUMN, 1.1)
            self.add_sprite(n + util.random_int(0, 5), SPRITES.TREE1, -1 - (random.random() * 2))
            self.add_sprite(n + util.random_int(0, 5), SPRITES.TREE2, -1 - (random.random() * 2))

        # add plants
        for n in range(200, len(self.segments), 3):
            self.add_sprite(n, util.random_choice(SPRITES.PLANTS),
                            util.random_choice([1, -1]) * (2 + random.random() * 5))

        # add billboards
        for n in range(1000, len(self.segments) - 50, 100):
            side = util.random_choice([1, -1])
            self.add_sprite(n + util.random_int(0, 50), util.random_choice(SPRITES.BILLBOARDS), -side)
            for i in range(20):
                sprite = util.random_choice(SPRITES.PLANTS)
                offset = side * (1.5 + random.random())
                self.add_sprite(n + util.random_int(0, 50), sprite, offset)
        return

    def reset_cars(self):
        self.cars = []
        for n in range(self.total_cars):
            offset = random.random() * util.random_choice([-0.8, 0.8])
            z = math.floor(random.random() * len(self.segments)) * self.segment_length
            sprite_img = util.random_choice(SPRITES.CARS)
            speed = self.max_speed / 4.0 + random.random() * self.max_speed / (4 if sprite_img == SPRITES.SEMI else 2)
            sprite = pyglet.sprite.Sprite(img=sprite_img)
            car = Map({'offset': offset, 'z': z, 'sprite': sprite, 'speed': speed})
            segment = self.find_segment(car.z)
            segment.cars.append(car)
            self.cars.append(car)
        return

    def update_car_offset(self, car, car_segment, player_segment, player_w):
        if car_segment.index - player_segment.index > self.draw_distance:
            return 0

        lookahead, car_w = 20, car.sprite.width * SPRITES.SCALE
        for i in range(1, lookahead):
            segment = self.segments[(car_segment.index + i) % len(self.segments)]
            if segment == player_segment and car.speed > self.speed \
                    and util.overlap(self.player_x, player_w, car.offset, car_w, 1.2):
                if (self.player_x > 0.5):
                    direction = -1
                elif (self.player_x < -0.5):
                    direction = 1
                else:
                    direction = 1 if car.offset > self.player_x else -1
                return direction * 1.0 / i * (car.speed - self.speed) / self.max_speed

            for j in range(len(segment.cars)):
                other_car = segment.cars[j]
                other_car_w = other_car.sprite.width * SPRITES.SCALE
                if car.speed > other_car.speed and util.overlap(car.offset, car_w, other_car.offset, other_car_w, 1.2):
                    if (other_car.offset > 0.5):
                        direction = -1
                    elif (other_car.offset < -0.5):
                        direction = 1
                    else:
                        direction = 1 if car.offset > other_car.offset else -1
                    return direction * 1 / i * (car.speed - other_car.speed) / self.max_speed

        # if no cars ahead, but I have somehow ended up off road, then steer back on
        if car.offset < -0.9:
            return 0.1
        elif car.offset > 0.9:
            return -0.1
        else:
            return 0

    def update_cars(self, dt, player_segment, player_w):
        old_segment = new_segment = None
        for n in range(len(self.cars)):
            car = self.cars[n]
            old_segment = self.find_segment(car.z)
            car.offset = car.offset + self.update_car_offset(car, old_segment, player_segment, player_w)
            car.z = util.increase(car.z, dt * car.speed, self.track_length)
            car.percent = util.percent_remaining(car.z, self.segment_length)
            new_segment = self.find_segment(car.z)
            if (old_segment != new_segment):
                index = old_segment.cars.index(car)
                del old_segment.cars[index]
                new_segment.cars.append(car)
        return

    def update(self, dt):
        player_segment = self.find_segment(self.position + self.player_z)
        player_w = SPRITES.PLAYER_STRAIGHT.width * SPRITES.SCALE
        speed_percent = float(self.speed) / self.max_speed
        dx = dt * 2 * speed_percent
        # start_position = self.position

        self.update_cars(dt, player_segment, player_w)
        self.position = util.increase(self.position, dt * self.speed, self.track_length)

        self.key_faster = True
        if (self.key_left):
            self.player_x = self.player_x - dx
        elif (self.key_right):
            self.player_x = self.player_x + dx

        self.player_x = self.player_x - (dx * speed_percent * player_segment.curve * self.centrifugal)

        if (self.key_faster):
            self.speed = util.accelerate(self.speed, self.accel, dt)
        elif (self.key_slower):
            self.speed = util.accelerate(self.speed, self.breaking, dt)
        else:
            self.speed = util.accelerate(self.speed, self.decel, dt)

        # print 'step:', dt, 'speed:', self.speed, 'speed_percent:', speed_percent, 'max_speed:', self.max_speed

        if self.player_x < -1 or self.player_x > 1:
            if self.speed > self.off_road_limit:
                self.speed = util.accelerate(self.speed, self.off_road_decel, dt)
                for n in range(len(player_segment.sprites)):
                    sprite = player_segment.sprites[n]
                    sprite_w = sprite.source.width * SPRITES.SCALE
                    # todo: check sprite_w/2 or 2.0
                    if (util.overlap(self.player_x, player_w, sprite.offset + sprite_w / 2.0 * (1 if sprite.offset > 0 else -1), sprite_w)):
                        self.speed = int(self.max_speed / 5.0)
                        self.position = util.increase(player_segment.p1.world.z, -self.player_z, self.track_length)
                        break

        #  check collision
        for n in range(len(player_segment.cars)):
            car = player_segment.cars[n]
            car_w = car.sprite.width * SPRITES.SCALE
            if self.speed > car.speed:
                if (util.overlap(self.player_x, player_w, car.offset, car_w, 0.8)):
                    self.speed = int(car.speed * (float(car.speed) / self.speed))
                    self.position = util.increase(car.z, -self.player_z, self.track_length)
                    # todo: add has_collision = True
                    break

        self.player_x = util.limit(self.player_x, -3, 3)  # dont ever let it go too far out of bounds
        self.speed = util.limit(self.speed, 0, self.max_speed)  # or exceed self.max_speed

        # self.sky_offset  = util.increase(self.sky_offset,  self.sky_speed  * player_segment.curve * (self.position - start_position) / self.segment_length, 1)
        # self.hill_offset = util.increase(self.hill_offset, self.hill_speed * player_segment.curve * (self.position - start_position) / self.segment_length, 1)
        # self.tree_offset = util.increase(self.tree_offset, self.tree_speed * player_segment.curve * (self.position - start_position) / self.segment_length, 1)

        # if (self.position > self.player_z):
        #     if self.current_lap_time and (start_position < self.player_z):
        #         self.last_lap_tim = self.current_lap_time
        #         self.current_lap_time = 0
        #     else:
        #         self.current_lap_time += dt
        return

    def render_sprite(self):
        base_segment = self.find_segment(self.position)
        base_percent = util.percent_remaining(self.position, self.segment_length)
        player_segment = self.find_segment(self.position + self.player_z)
        player_percent = util.percent_remaining(self.position + self.player_z, self.segment_length)
        player_y = util.interpolate(player_segment.p1.world.y, player_segment.p2.world.y, player_percent)

        maxy = SCREEN_HEIGHT

        x = 0
        dx = - (base_segment.curve * base_percent)

        # print len(self.segments)
        # import sys
        # sys.exit()
        for n in range(self.draw_distance):
            segment = self.segments[(base_segment.index + n) % len(self.segments)]
            # todo: <= should be <
            segment.looped = segment.index <= base_segment.index
            segment.fog = util.exponential_fog(float(n) / self.draw_distance, self.fog_density)
            segment.clip = maxy

            util.project(
                segment.p1,
                (self.player_x * self.road_width) - x,
                player_y + self.camera_height,
                self.position - (self.track_length if segment.looped else 0),
                self.camera_depth,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                self.road_width
            )
            util.project(
                segment.p2,
                (self.player_x * self.road_width) - x - dx,
                player_y + self.camera_height,
                self.position - (self.track_length if segment.looped else 0),
                self.camera_depth,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                self.road_width
            )

            x = x + dx
            dx = dx + segment.curve

            print 'p1:', segment.p1.screen.y, 'p2:', segment.p2.screen.y, \
                'p.c.z:', segment.p1.camera.z, 'self.c_d:', self.camera_depth, \
                'maxy:', maxy
            if ((segment.p1.camera.z <= self.camera_depth)  # behind us
                or (segment.p1.screen.y >= segment.p2.screen.y)  # back face cull
                # or (segment.p1.screen.y >= maxy)  # clip by hill
            ):
                # print 'p1:', segment.p1.screen.y, 'p2:', segment.p2.screen.y, \
                #     'p.c.z:', segment.p1.camera.z, 'self.c_d:', self.camera_depth, \
                #     'maxy:', maxy
                continue

            render.r_segment(
                SCREEN_WIDTH, 3,
                segment.p1.screen.x,
                segment.p1.screen.y,
                segment.p1.screen.w,
                segment.p2.screen.x,
                segment.p2.screen.y,
                segment.p2.screen.w,
                segment.fog,
                segment.color
            )

            maxy = segment.p2.screen.y

        # end for
        # return
        # for n in reversed(range(self.draw_distance - 1)):
        #     segment = self.segments[(base_segment.index + n) % len(self.segments)]

            # for i in range(len(segment.cars)):
            #     car = segment.cars[i]
            #     sprite_scale = util.interpolate(segment.p1.screen.scale, segment.p2.screen.scale, car.percent)
            #     sprite_x = util.interpolate(segment.p1.screen.x, segment.p2.screen.x, car.percent) + \
            #         (sprite_scale * car.offset * self.road_width * SCREEN_WIDTH / 2)
            #     sprite_y = util.interpolate(segment.p1.screen.y, segment.p2.screen.y, car.percent)
            #     render.r_sprite(SPRITES, SCREEN_WIDTH, SCREEN_HEIGHT, self.resolution,
            #                     self.road_width, car.sprite, sprite_scale, sprite_x, sprite_y,
            #                     -0.5, -1, segment.clip)

            # for i in range(len(segment.sprites)):
            #     sprite = segment.sprites[i]
            #     sprite_scale = segment.p1.screen.scale
            #     sprite_x = segment.p1.screen.x + (sprite_scale * sprite.offset * self.road_width * SCREEN_WIDTH / 2.0)
            #     sprite_y = segment.p1.screen.y
            #     render.r_sprite(SPRITES, SCREEN_WIDTH, SCREEN_HEIGHT, self.resolution,
            #                     self.road_width, sprite.source, sprite_scale, sprite_x, sprite_y,
            #                     (-1 if sprite.offset < 0 else 0), -1, segment.clip)

            # if segment == player_segment:
            #     p_height = (SCREEN_HEIGHT / 2.0) - (self.camera_depth / self.player_z * util.interpolate(
            #         player_segment.p1.camera.y, player_segment.p2.camera.y, player_percent) * SCREEN_HEIGHT / 2)
            #     p_height = SCREEN_HEIGHT - p_height + self.player_sprite.height
            #     render.r_player(
            #         SPRITES, self.player_sprite, SCREEN_WIDTH, SCREEN_HEIGHT, self.resolution, self.road_width,
            #         float(self.speed) / self.max_speed, float(self.camera_depth) / self.player_z,
            #         SCREEN_WIDTH / 2,
            #         p_height,
            #         self.speed * (-1 if self.key_left else 1 if self.key_right else 0),
            #         player_segment.p2.world.y - player_segment.p1.world.y
            #     )
        # import sys
        # sys.exit()
        return


racer = Racer()
my_car = pyglet.sprite.Sprite(img=SPRITES.PALM_TREE)
fps_display = pyglet.clock.ClockDisplay()

@game_window.event
def on_draw():
    game_window.clear()
    racer.render_sprite()
    fps_display.draw()
    # my_car.draw()
    return

def update(dt):
    my_car.x += 1
    return

def test():
    racer = Racer()
    racer.add_segment(1, 2)
    return


if __name__ == '__main__':
    pyglet.clock.schedule_interval(racer.update, 1 / 120.0)
    # pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
    # test()
    # print list(reversed(range(10)))
