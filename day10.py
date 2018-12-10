import copy
import re
import time

from collections import namedtuple

Vel = namedtuple("Vel", "x y")

def print_points(point_list, top, left, bottom, right):
    points = set()
    for x, y, v in point_list:
        points.add((x, y))

    for y in range(top, bottom +1):
        line = []
        for x in range(left, right +1):
            if (x, y) in points:
                line.append("X")
            else:
                line.append(".")
        print "".join(line)
    print


points = {}
point_list = []

with open("day10.input") as f:
    for line in f:
        # position=<-10351, -10360> velocity=< 1,  1>
        regex = "position=<(( |-)[0-9]+), (( |-)[0-9]+)> velocity=<(( |-)[0-9]+), (( |-)[0-9]+)>"
        x, _, y, _, vx, _, vy, _ = re.match(regex, line).groups()
        v = Vel(int(vx), int(vy))
        points[(int(x), int(y))] = v
        point_list.append([int(x), int(y), v])

SECONDS = 15000
min_area = None
min_configuration = None
final_min_x = 0
final_min_y = 0
final_max_x = 0
final_max_x = 0
for i in range(SECONDS):
    if i % 100 == 0:
        print i

    should_print = False
    new_xs = []
    new_ys = []
    for idx in range(len(point_list)):
        px, py, v = point_list[idx]
        new_x = px + v.x
        new_y = py + v.y

        new_xs.append(new_x)
        new_ys.append(new_y)

        point_list[idx][0] = new_x
        point_list[idx][1] = new_y

    min_x = min(new_xs)
    min_y = min(new_ys)
    max_x = max(new_xs)
    max_y = max(new_ys)

    new_area = (max_x - min_x) * (max_y - min_y)
    if min_area:
        if new_area < min_area:
            min_area = new_area
            print i + 1, "seconds,", min_area, "area,", min_x, min_y, max_x, max_y
            min_configuration = copy.deepcopy(point_list)
            final_min_x = min_x
            final_min_y = min_y
            final_max_x = max_x
            final_max_y = max_y
        else:
            # Area increasing.
            break

    else:
        min_area = new_area

print_points(min_configuration, final_min_y, final_min_x, final_max_y, final_max_x)
