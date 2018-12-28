import re

from collections import namedtuple

Point3 = namedtuple("Point3", "x y z")
Bot = namedtuple("Bot", "pos r")

ORIGIN = Point3(0, 0, 0)

def distance(point, other):
    return abs(point.x - other.x) + abs(point.y - other.y) + abs(point.z - other.z)


def bot_distance(bot, other):
    return distance(bot.pos, other.pos)


def bot_in_range(bot, other_pos):
    return distance(bot.pos, other_pos) <= bot.r


def num_in_range(bot, others):
    return sum([1 for other in others if bot_distance(bot, other) <= bot.r])


def floor(n, m):
    return ((n // m)) * m


def ceil(n, m):
    return ((n // m) + 1) * m


def contained(bot, x, y, z, size):
    return (x <= bot.pos.x and bot.pos.x < x + size and
            y <= bot.pos.y and bot.pos.y < y + size and
            z <= bot.pos.z and bot.pos.z < z + size)


bots = []
strongest = None

min_x = None
min_y = None
min_z = None
max_x = None
max_y = None
max_z = None

with open("day23.input") as f:
# with open("day23.small.input") as f:
    # pos=<86508574,12573428,20533848>, r=83193725
    for line in f:
        m = re.match("pos=\<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)\>, r=([0-9]+)", line.strip())
        x, y, z, r = [int(t) for t in m.groups()]

        b = Bot(Point3(x, y, z), r)

        if strongest and r > strongest.r:
            strongest = b
        elif not strongest:
            strongest = b

        if min_x and x < min_x:
            min_x = x
        if not min_x:
            min_x = x
        if max_x and x > max_x:
            max_x = x
        if not max_x:
            max_x = x

        if min_y and y < min_y:
            min_y = y
        if not min_y:
            min_y = y
        if max_y and y > max_y:
            max_y = y
        if not max_y:
            max_y = y

        if min_z and z < min_z:
            min_z = z
        if not min_z:
            min_z = z
        if max_z and z > max_z:
            max_z = z
        if not max_z:
            max_z = z

        bots.append(b)

print strongest
print "part 1:", num_in_range(strongest, bots)

for grid_size in [100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1]:
    max_score = None
    print
    print "min", min_x, min_y, min_z, grid_size
    print "max", max_x, max_y, max_z, grid_size

    x_range = xrange(floor(min_x, grid_size), ceil(max_x, grid_size), grid_size)
    y_range = xrange(floor(min_y, grid_size), ceil(max_y, grid_size), grid_size)
    z_range = xrange(floor(min_z, grid_size), ceil(max_z, grid_size), grid_size)

    for x in x_range:
        for y in y_range:
            for z in z_range:
                point = Point3(x, y, z)
                score = 0

                if grid_size == 1:
                    score = sum(1 for b in bots if bot_in_range(b, Point3(x, y, z)))
                else:
                    score = sum(1 for b in bots if (distance(b.pos, point) - b.r) < grid_size)

                if grid_size == 1:
                    if not max_score or score > max_score:
                        max_score = score
                        best = set([Point3(x, y, z)])
                    elif score == max_score:
                        best.add(Point3(x, y, z))
                else:
                    if not max_score or score > max_score:
                        max_score = score
                        min_x = x - grid_size
                        min_y = y - grid_size
                        min_z = z - grid_size
                        max_x = x + grid_size
                        max_y = y + grid_size
                        max_z = z + grid_size

print
print best
print min(best, key=lambda b: distance(b, ORIGIN))
print "part 2:", distance(min(best, key=lambda b: distance(b, ORIGIN)), ORIGIN)
