import time
import math
import random


def timestamp():
    return int(round(time.time() * 1000))


def limit(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def interpolate(a, b, percent):
    return a + (b - a) * percent


def ease_in(a, b, percent):
    return a + (b - a) * math.pow(percent, 2)


def ease_out(a, b, percent):
    return a + (b - a) * (1 - math.pow(1 - percent, 2))


def ease_in_out(a, b, percent):
    return a + (b - a) * ((-math.cos(percent * math.pi) / 2) + 0.5)


def exponential_fog(distance, density):
    return 1 / (math.pow(math.e, (distance * distance * density)))


def random_int(min_value, max_value):
    return random.randint(min_value, max_value)


def random_choice(options):
    return random.choice(options)


def percent_remaining(n, total):
    return (n % total) / total


def accelerate(v, accel, dt):
    return v + (accel * dt)


def increase(start, increment, max):
    result = start + increment
    while result >= max:
        result -= max
    while result < 0:
        result += max
    return result


def project(p, camera_x, camera_y, camera_z, camera_depth, width, height, road_width):
    p.camera.x = (p.world.x if 'x' in p.world else 0) - camera_x
    p.camera.y = (p.world.y if 'y' in p.world else 0) - camera_y
    p.camera.z = (p.world.z if 'z' in p.world else 0) - camera_z
    p.screen.scale = camera_depth / p.camera.z
    p.screen.x = round((width / 2) + (p.screen.scale * p.camera.x * width / 2))
    p.screen.y = round((height / 2) - (p.screen.scale * p.camera.y * height / 2))
    p.screen.w = round((p.screen.scale * road_width * width / 2))
    return


def overlap(x1, w1, x2, w2, percent=1.0):
    half = percent / 2
    min1 = x1 - (w1 * half)
    max1 = x1 + (w1 * half)
    min2 = x2 - (w2 * half)
    max2 = x2 + (w2 * half)
    return not ((max1 < min2) or (min1 > max2))


if __name__ == '__main__':
    print 'util.py'
    from map import Map
    # print timestamp()
    # print limit(2, 0, 3)
    # print random_int(0, 9)
    # print random_choice(['a', 'b', 'c'])
