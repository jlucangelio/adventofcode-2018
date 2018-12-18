import re
import sys

from collections import namedtuple

INPUT = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

# INPUT = """y=4, x=499..501
# x=504, y=2..3"
# """

# INPUT = """y=4, x=499..501
# x=504, y=2..3"
# x=498, y=3..4"
# x=502, y=3..4"
# """

# INPUT = """x=490, y=5..15
# x=510, y=5..15
# y=15, x=491..509
# x=498, y=9..11
# x=502, y=9..11
# """

class Pos(namedtuple("Pos", "x y")):
    __slots__ = ()

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)


UP = Pos(0, -1)
DOWN = Pos(0, 1)
LEFT = Pos(-1, 0)
RIGHT = Pos(1, 0)

MOVES = [LEFT, RIGHT, UP, DOWN]

def water_blocked(sq, grid):
    return sq in grid and (grid[sq] == "#" or grid[sq] == "~")


def flow_down_and_fill_one_level(sq, grid):
    # return the new flow down spots.

    # print sq
    sq_below = sq + DOWN
    while sq_below.y <= max_y and sq_below not in grid:
        # |sq_below| is sand, so keep flowing
        grid[sq] = "|"
        sq = sq_below
        sq_below = sq_below + DOWN

    if sq_below.y > max_y:
        grid[sq] = "|"
        return (False, [])    # Not filled.

    # |sq_below| is clay or water
    if grid[sq_below] == "#" or grid[sq_below] == "~":
        is_flowing_left, left_edge = flow_sideways(sq, grid, left=True)
        is_flowing_right, right_edge = flow_sideways(sq, grid, left=False)

        filled = False
        flowing = []
        if not is_flowing_left and not is_flowing_right:
            # it's filled
            filled = True
            for i in range(left_edge.x + 1, right_edge.x):
                grid[i, sq.y] = "~"
            flowing.append(sq + UP)
        else:
            # print "mark as flowing"
            grid[sq] = "|"
            if is_flowing_left:
                flowing.append(left_edge)
            if is_flowing_right:
                flowing.append(right_edge)

        return (filled, flowing)

    elif grid[sq_below] == "|":
        grid[sq] = "|"
        return (False, [])

    else:
        print sq, grid[sq], grid[sq_below]
        print_grid(grid, min_y, max_y, max_x)
        print "error"



def flow_sideways(sq, grid, left=True):
    down = sq + DOWN

    if water_blocked(down, grid):
        if sq.x == 0:
            print "error"

        if left:
            direction = LEFT
        else:
            direction = RIGHT

        side = sq + direction
        if water_blocked(side, grid):
            grid[sq] = "|"
            return (False, side)
        else:
            grid[sq] = "|"
            return flow_sideways(side, grid, left)

    else:
        # water can flow down
        return (True, sq)


def sum_reached(grid, min_y):
    return sum([1 for p, v in grid.iteritems() if p.y >= min_y and (v == "|" or v == "~")])

def sum_retained(grid, min_y):
    return sum([1 for p, v in grid.iteritems() if p.y >= min_y and v == "~"])


def print_grid(grid, min_y, max_y, max_x):
    min_x = 0
    # max_x = 505

    # print "." * 15 + "+" + "." * (max_x - 485 - 16 + 2)
    print "." * 500 + "+" + "." * (max_x - 501 + 2)
    for j in range(1, max_y + 2):
        line = []
        for i in range(min_x, max_x + 2):
            p = Pos(i, j)
            if p in grid:
                line.append(grid[p])
            else:
                line.append(".")
        print "".join(line)


grid = {}
max_x = 0
min_y = None
max_y = 0

lines = INPUT.splitlines()
with open("day17.input") as f:
    lines = f.readlines()

for line in lines:
    m = re.match("(x|y)=([0-9]+), (x|y)=([0-9]+)\.\.([0-9]+)", line)
    c1, val1, c2, val2_begin, val2_end = m.groups()

    # print c1, val1, c2, val2_begin, val2_end
    if c1 == "x":
        x = int(val1)
        if x > max_x:
            max_x = x

        for y in range(int(val2_begin), int(val2_end) + 1):
            if not min_y or y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

            grid[Pos(x, y)] = "#"

    elif c1 == "y":
        y = int(val1)
        if not min_y or y < min_y:
            min_y = y
        if y > max_y:
                max_y = y

        for x in range(int(val2_begin), int(val2_end) + 1):
            if x > max_x:
                max_x = x

            grid[Pos(x, y)] = "#"

flow_from = [Pos(500, 0)]
while len(flow_from) > 0:
    pos = flow_from.pop()
    filled, flowing = flow_down_and_fill_one_level(pos, grid)
    flow_from.extend(flowing)


print sum_reached(grid, min_y)
print sum_retained(grid, min_y)
# print_grid(grid, min_y, max_y, max_x + 1)
