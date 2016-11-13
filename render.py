import pygame


def polygon(screen, x1, y1, x2, y2, x3, y3, x4, y4, color):
    points = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    pygame.draw.polygon(screen, color, points, 0)
    return


def segment(screen, width, lanes, x1, y1, w1, x2, y2, w2, fog, color):
    r1 = rumbleWidth(w1, lanes)
    r2 = rumbleWidth(w2, lanes)
    # l1 = laneMarkerWidth(w1, lanes)
    # l2 = laneMarkerWidth(w2, lanes)

    # screen.fillStyle = color.grass
    # screen.fillRect(0, y2, width, y1 - y2)

    polygon(screen, x1 - w1 - r1, y1, x1 - w1, y1, x2 - w2, y2, x2 - w2 - r2, y2, color.rumble)
    polygon(screen, x1 + w1 + r1, y1, x1 + w1, y1, x2 + w2, y2, x2 + w2 + r2, y2, color.rumble)
    polygon(screen, x1 - w1, y1, x1 + w1, y1, x2 + w2, y2, x2 - w2, y2, color.road)

    # if color.lane:
    #     lanew1 = w1 * 2 / lanes
    #     lanew2 = w2 * 2 / lanes
    #     lanex1 = x1 - w1 + lanew1
    #     lanex2 = x2 - w2 + lanew2
        # for(lane = 1  lane < lanes  lanex1 += lanew1, lanex2 += lanew2, lane++) :
        #   polygon(screen, lanex1 - l1/2, y1, lanex1 + l1/2, y1, lanex2 + l2/2, y2, lanex2 - l2/2, y2, color.lane)

    return


def rumbleWidth(projectedRoadWidth, lanes):
    return projectedRoadWidth / max(6, 2 * lanes)


def laneMarkerWidth(projectedRoadWidth, lanes):
    return projectedRoadWidth / max(32, 8 * lanes)
