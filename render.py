import pygame
from pygame import gfxdraw
import pyglet

import util
import random

import sys


def r_polygon(x1, y1, x2, y2, x3, y3, x4, y4, color):
    color = color * 4  # 4 points correspondingly
    # pyglet.graphics.draw_indexed(
    #     4, pyglet.gl.GL_TRIANGLES,
    #     [0, 1, 2, 0, 2, 3],  # the index of points
    #     ('v2f', (x1, y1, x2, y2, x3, y3, x4, y4)),
    #     ('c3B', color),
    # )
    pyglet.graphics.draw_indexed(
        4, pyglet.gl.GL_POLYGON,
        [0, 1, 2, 3],  # the index of points
        ('v2f', (x1, y1, x2, y2, x3, y3, x4, y4)),
        ('c3B', color),
    )
    return


def r_rect(x, y, width, height, color):
    # r_polygon(x, y, x + width, y, x + width, y + height, x, y + height, color)
    r_polygon(x, y, x + width, y, x + width, y + height, x, y + height, color)
    return


def r_segment(width, lanes, x1, y1, w1, x2, y2, w2, fog, color):
    r1 = r_rumble_width(w1, lanes)
    r2 = r_rumble_width(w2, lanes)
    l1 = r_lane_marker_width(w1, lanes)
    l2 = r_lane_marker_width(w2, lanes)

    r_rect(0, y2, width, y1 - y2, color.grass)

    r_polygon(x1 - w1 - r1, y1, x1 - w1, y1, x2 - w2, y2, x2 - w2 - r2, y2, color.rumble)
    r_polygon(x1 + w1 + r1, y1, x1 + w1, y1, x2 + w2, y2, x2 + w2 + r2, y2, color.rumble)
    r_polygon(x1 - w1, y1, x1 + w1, y1, x2 + w2, y2, x2 - w2, y2, color.road)

    if 'lane' in color:
        lanew1 = w1 * 2 / lanes
        lanew2 = w2 * 2 / lanes
        lanex1 = x1 - w1 + lanew1
        lanex2 = x2 - w2 + lanew2
        for lane in range(1, lanes):
            r_polygon(lanex1 - l1 / 2, y1, lanex1 + l1 / 2, y1,
                      lanex2 + l2 / 2, y2, lanex2 - l2 / 2, y2, color.lane)
            lanex1 += lanew1
            lanex2 += lanew2

    return


def r_rumble_width(projected_road_width, lanes):
    return projected_road_width / max(6, 2 * lanes)


def r_lane_marker_width(projected_road_width, lanes):
    return projected_road_width / max(32, 8 * lanes)


def r_sprite(SPRITES, width, height, resolution, road_width, sprite, scale, dest_x, dest_y, offset_x=0, offset_y=0, clip_y=0):
    img_width = sprite.image.width
    img_height = sprite.image.height
    dest_w = (img_width * scale * width / 2.0) * (SPRITES.SCALE * road_width)
    dest_h = (img_height * scale * width / 2.0) * (SPRITES.SCALE * road_width)

    # dest_x += dest_w * offset_x
    dest_y += dest_h
    dest_x = dest_x + (dest_w * offset_x)
    dest_y = dest_y + (dest_h * offset_y)

    sprite.x = dest_x
    sprite.y = dest_y
    sprite.scale = float(dest_h) / img_height
    sprite.draw()
    return


def r_player(SPRITES, sprite, width, height, resolution, road_width, speed_percent, scale, dest_x, dest_y, steer, updown):
    bounce = 1.5 * random.random() * speed_percent * resolution * util.random_choice([-1, 1])
    # if steer < 0:
    #     sprite_img = SPRITES.PLAYER_UPHILL_LEFT if updown > 0 else SPRITES.PLAYER_LEFT
    # elif steer > 0:
    #     sprite_img = SPRITES.PLAYER_UPHILL_RIGHT if updown > 0 else SPRITES.PLAYER_RIGHT
    # else:
    #     sprite_img = SPRITES.PLAYER_UPHILL_STRAIGHT if updown > 0 else SPRITES.PLAYER_STRAIGHT

    # sprite = pyglet.sprite.Sprite(img=sprite_img)
    r_sprite(SPRITES, width, height, resolution, road_width,
             sprite, scale, dest_x, dest_y + bounce, -0.5, -1)
    return


def fog(x, y, width, height, fog):
    # todo:
    # if fog < 1:
    #     screen.globalAlpha = (1 - fog)
    #     screen.fillStyle = COLORS.FOG
    #     screen.fillRect(x, y, width, height)
    #     screen.globalAlpha = 1
    return


def test():

    return

if __name__ == '__main__':
    color = (16, 170, 16)
    print color * 4
    # print range(1, 10)
