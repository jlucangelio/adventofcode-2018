import copy

from collections import namedtuple

class Pos(namedtuple("Pos", "x y")):
    __slots__ = ()

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)


    def adjacents(self, side_len):
        adj = []
        if self.x > 0:
            adj.append(self + LEFT)
            if self.y > 0:
                adj.append(self + UP_LEFT)

        if self.y > 0:
            adj.append(self + UP)
            if self.x < side_len - 1:
                adj.append(self + UP_RIGHT)

        if self.x < side_len - 1:
            adj.append(self + RIGHT)
            if self.y < side_len - 1:
                adj.append(self + DOWN_RIGHT)

        if self.y < side_len - 1:
            adj.append(self + DOWN)
            if self.x > 0:
                adj.append(self + DOWN_LEFT)

        return adj


UP = Pos(0, -1)
DOWN = Pos(0, 1)
LEFT = Pos(-1, 0)
RIGHT = Pos(1, 0)

UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT
DOWN_LEFT = DOWN + LEFT
DOWN_RIGHT = DOWN + RIGHT

OPEN = ord(".")
TREES = ord("|")
LY = ord("#")

def print_area(area):
    side = len(area)

    for j in range(side):
        line = []
        for i in range(side):
            line.append(chr(area[i][j]))
        print "".join(line)

    print


def tree_sum(area):
    return sum([sum([1 for c in line if c == TREES]) for line in area])

def ly_sum(area):
    return sum([sum([1 for c in line if c == LY]) for line in area])


AREA_SIDE = 50

areas = {}
areas[0] = [[None for _ in range(AREA_SIDE)] for _ in range(AREA_SIDE)]
areas[1] = [[None for _ in range(AREA_SIDE)] for _ in range(AREA_SIDE)]

prev_areas = {}

lines = []
with open("day18.input") as f:
# with open("day18.small.input") as f:
    lines = f.readlines()

for j, line in enumerate(lines):
    for i, c in enumerate(line.strip()):
        areas[0][i][j] = ord(c)

# calculate adjacents
adjacents = [[None for _ in range(AREA_SIDE)] for _ in range(AREA_SIDE)]
for i in range(AREA_SIDE):
    for j in range(AREA_SIDE):
        adjacents[i][j] = Pos(i, j).adjacents(AREA_SIDE)

cycle = False
cycle_index = None
for m in xrange(1000):
    if m % 1000 == 0:
        print m

    area = areas[(m % 2)]
    new_area = areas[((m + 1) % 2)]

    for j in range(AREA_SIDE):
        for i in range(AREA_SIDE):
            adj = adjacents[i][j]
            if area[i][j] == OPEN:
                if sum([1 for p in adj if area[p.x][p.y] == TREES]) >= 3:
                    n = TREES
                else:
                    n = OPEN
            elif area[i][j] == TREES:
                if sum([1 for p in adj if area[p.x][p.y] == LY]) >= 3:
                    n = LY
                else:
                    n = TREES
            elif area[i][j] == LY:
                lys = sum([1 for p in adj if area[p.x][p.y] == LY])
                trees = sum([1 for p in adj if area[p.x][p.y] == TREES])

                if lys >= 1 and trees >= 1:
                    n = LY
                else:
                    n = OPEN

            new_area[i][j] = n

    if new_area == area:
        print "steady state", m
        print_area(area)
        break
    else:
        for idx, a in prev_areas.iteritems():
            if new_area == a and (m + 1) != idx:
                cycle = True
                cicle_index = (idx, m + 1)
                print "cycle", m + 1, idx
                start = idx
                period = m + 1 - idx
                final_offset = (1000000000 - start) % period
                final_area = prev_areas[start + final_offset]
                print tree_sum(final_area), ly_sum(final_area)
                print tree_sum(final_area) * ly_sum(final_area)
                break
        if cycle:
            break
        else:
            prev_areas[m + 1] = copy.deepcopy(new_area)

    # print m
    # print_area(area)

print tree_sum(areas[(m + 1) % 2]) * ly_sum(areas[(m + 1) % 2])
