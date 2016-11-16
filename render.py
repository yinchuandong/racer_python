import pygame
from pygame import gfxdraw
import util
import random


def r_polygon(screen, x1, y1, x2, y2, x3, y3, x4, y4, color):
    points = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    # points = [[x1 - 10, y1 - 10], [x2 - 10, y2 - 10], [x3 -10, y3 -10], [x4-10, y4-10]]
    # pygame.draw.polygon(screen, color, points, 0)
    # gfxdraw.aapolygon(screen, points, color)
    gfxdraw.filled_polygon(screen, points, color)
    return


def r_segment(screen, width, lanes, x1, y1, w1, x2, y2, w2, fog, color):
    r1 = r_rumble_width(w1, lanes)
    r2 = r_rumble_width(w2, lanes)
    l1 = r_lane_marker_width(w1, lanes)
    l2 = r_lane_marker_width(w2, lanes)

    pygame.draw.rect(screen, color.grass, (0, y2, width, y1 - y2))

    r_polygon(screen, x1 - w1 - r1, y1, x1 - w1, y1, x2 - w2, y2, x2 - w2 - r2, y2, color.rumble)
    r_polygon(screen, x1 + w1 + r1, y1, x1 + w1, y1, x2 + w2, y2, x2 + w2 + r2, y2, color.rumble)
    r_polygon(screen, x1 - w1, y1, x1 + w1, y1, x2 + w2, y2, x2 - w2, y2, color.road)

    if 'lane' in color:
        lanew1 = w1 * 2 / lanes
        lanew2 = w2 * 2 / lanes
        lanex1 = x1 - w1 + lanew1
        lanex2 = x2 - w2 + lanew2
        for lane in range(1, lanes):
            r_polygon(screen, lanex1 - l1 / 2, y1, lanex1 + l1 / 2, y1,
                      lanex2 + l2 / 2, y2, lanex2 - l2 / 2, y2, color.lane)
            lanex1 += lanew1
            lanex2 += lanew2

    return


def r_rumble_width(projected_road_width, lanes):
    return projected_road_width / max(6, 2 * lanes)


def r_lane_marker_width(projected_road_width, lanes):
    return projected_road_width / max(32, 8 * lanes)


def r_sprite(screen, SPRITES, width, height, resolution, road_width, sprite, scale, dest_x, dest_y, offset_x=0, offset_y=0, clip_y=0):
    rect = sprite.get_rect()  # x,y,w,h
    dest_w = (rect[2] * scale * width / 2.0) * (SPRITES.SCALE * road_width)
    dest_h = (rect[3] * scale * width / 2.0) * (SPRITES.SCALE * road_width)

    dest_x = dest_x + (dest_w * offset_x)
    dest_y = dest_y + (dest_h * offset_y)

    clip_h = max(0, dest_y + dest_h - clip_y) if clip_y != 0 else 0

    if (clip_h < dest_h):
        # screen.drawImage(sprites, sprite.x, sprite.y, sprite.w, sprite.h -
        #                  (sprite.h * clip_h / dest_h), dest_x, dest_y, dest_w, dest_h - clip_h)
        # sprite = pygame.transform.scale(sprite, (rect[2], int(rect[3] * clip_h / float(dest_h))))
        # print sprite.get_rect()
        # sprite = pygame.transform.scale(sprite, (int(dest_w), int(dest_h)))
        if dest_w > 500 or dest_h > 500:
            # print dest_w, dest_h
            return
        s_sprite = pygame.transform.scale(sprite, (int(dest_w), int(dest_h)))
        # print dest_w, dest_h, scale
        # print sprite.get_rect()
        # print dest_h, clip_h, clip_y
        # print dest_x, dest_y, dest_w, dest_h
        # print dest_w, dest_h
        # import sys
        # sys.exit()
        screen.blit(s_sprite, (dest_x, dest_y, dest_w, dest_h))
    return


def r_player(screen, SPRITES, width, height, resolution, road_width, speed_percent, scale, dest_x, dest_y, steer, updown):
    bounce = 1.5 * random.random() * speed_percent * resolution * util.random_choice([-1, 1])
    if steer < 0:
        sprite = SPRITES.PLAYER_UPHILL_LEFT if updown > 0 else SPRITES.PLAYER_LEFT
    elif steer > 0:
        sprite = SPRITES.PLAYER_UPHILL_RIGHT if updown > 0 else SPRITES.PLAYER_RIGHT
    else:
        sprite = SPRITES.PLAYER_UPHILL_STRAIGHT if updown > 0 else SPRITES.PLAYER_STRAIGHT

    r_sprite(screen, SPRITES, width, height, resolution, road_width,
             sprite, scale, dest_x, dest_y + bounce, -0.5, -1)
    return


def fog(screen, x, y, width, height, fog):
    # todo:
    # if fog < 1:
    #     screen.globalAlpha = (1 - fog)
    #     screen.fillStyle = COLORS.FOG
    #     screen.fillRect(x, y, width, height)
    #     screen.globalAlpha = 1
    return


if __name__ == '__main__':
    print range(1, 10)