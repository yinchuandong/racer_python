import pygame
from pygame import gfxdraw


def polygon(screen, x1, y1, x2, y2, x3, y3, x4, y4, color):
    points = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    # points = [[x1 - 10, y1 - 10], [x2 - 10, y2 - 10], [x3 -10, y3 -10], [x4-10, y4-10]]
    # pygame.draw.polygon(screen, color, points, 0)
    # gfxdraw.aapolygon(screen, points, color)
    gfxdraw.filled_polygon(screen, points, color)
    return


def segment(screen, width, lanes, x1, y1, w1, x2, y2, w2, fog, color):
    r1 = rumble_width(w1, lanes)
    r2 = rumble_width(w2, lanes)
    l1 = lane_marker_width(w1, lanes)
    l2 = lane_marker_width(w2, lanes)

    pygame.draw.rect(screen, color.grass, (0, y2, width, y1 - y2))

    polygon(screen, x1 - w1 - r1, y1, x1 - w1, y1, x2 - w2, y2, x2 - w2 - r2, y2, color.rumble)
    polygon(screen, x1 + w1 + r1, y1, x1 + w1, y1, x2 + w2, y2, x2 + w2 + r2, y2, color.rumble)
    polygon(screen, x1 - w1, y1, x1 + w1, y1, x2 + w2, y2, x2 - w2, y2, color.road)

    if 'lane' in color:
        lanew1 = w1 * 2 / lanes
        lanew2 = w2 * 2 / lanes
        lanex1 = x1 - w1 + lanew1
        lanex2 = x2 - w2 + lanew2
        for lane in range(1, lanes):
            polygon(screen, lanex1 - l1 / 2, y1, lanex1 + l1 / 2, y1,
                    lanex2 + l2 / 2, y2, lanex2 - l2 / 2, y2, color.lane)
            lanex1 += lanew1
            lanex2 += lanew2

    return


def rumble_width(projected_road_width, lanes):
    return projected_road_width / max(6, 2 * lanes)


def lane_marker_width(projected_road_width, lanes):
    return projected_road_width / max(32, 8 * lanes)


if __name__ == '__main__':
    print range(1, 10)
