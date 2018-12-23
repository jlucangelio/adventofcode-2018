import sys

from collections import namedtuple

sys.setrecursionlimit(10000)

class Pos(namedtuple("Pos", "x y")):
    __slots__ = ()

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)


UP = Pos(0, -1)
DOWN = Pos(0, 1)
LEFT = Pos(-1, 0)
RIGHT = Pos(1, 0)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

ROCKY = 0
WET = 1
NARROW = 2

DEPTH = 4002
TARGET = Pos(5, 746)

# DEPTH = 510
# TARGET = Pos(10, 10)

max_x = TARGET.x + 1
max_y = TARGET.y + 1

geologic_index = {}
mouth = Pos(0, 0)

erosion_level = {}
erosion_level[mouth] = (0 + DEPTH) % 20183
erosion_level[TARGET] = (0 + DEPTH) % 20183

for i in range(max_x):
    geologic_index = (i * 16807)
    erosion_level[Pos(i, 0)] = (geologic_index + DEPTH) % 20183

for j in range(max_y):
    geologic_index = (j * 48271)
    erosion_level[Pos(0, j)] = (geologic_index + DEPTH) % 20183

for j in range(1, max_y):
    for i in range(1, max_x):
        if i == TARGET.x and j == TARGET.y:
            continue
        erosion_level[Pos(i, j)] = ((erosion_level[Pos(i - 1, j)] * erosion_level[Pos(i, j - 1)]) + DEPTH) % 20183

region_type = {}
risk = 0
for j in range(0, max_y):
    for i in range(0, max_x):
        p = Pos(i, j)
        region_type[p] = erosion_level[p] % 3
        risk += region_type[p]

print risk

erosion_level = {}
erosion_level[mouth] = (0 + DEPTH) % 20183
erosion_level[TARGET] = (0 + DEPTH) % 20183

for i in range(max_x):
    geologic_index = (i * 16807)
    erosion_level[Pos(i, 0)] = (geologic_index + DEPTH) % 20183

for j in range(max_y):
    geologic_index = (j * 48271)
    erosion_level[Pos(0, j)] = (geologic_index + DEPTH) % 20183

for j in range(1, max_y):
    for i in range(1, max_x):
        if i == TARGET.x and j == TARGET.y:
            continue

        erosion_level[Pos(i, j)] = ((erosion_level[Pos(i - 1, j)] * erosion_level[Pos(i, j - 1)]) + DEPTH) % 20183

def erosion(p, erosion_level):
    if p in erosion_level:
        return erosion_level[p]
    else:
        if p.y == 0:
            geologic_index = p.x * 16807
        elif p.x == 0:
            geologic_index = p.y * 48271
        else:
            geologic_index = erosion(Pos(p.x - 1, p.y), erosion_level) * erosion(Pos(p.x, p.y - 1), erosion_level)

        el = (geologic_index + DEPTH) % 20183
        erosion_level[p] = el
        return el

def region(p, region_type, erosion_level):
    if p in region_type:
        return region_type[p]
    else:
        t = erosion(p, erosion_level) % 3
        region_type[p] = t
        return t


TORCH = 0
CLIMBING_GEAR = 1
NEITHER = 2

TOOLS = [TORCH, CLIMBING_GEAR, NEITHER]

def neighbors(node):
    p, equipped_tool = node
    res = {}
    for d in DIRECTIONS:
        adj = p + d
        if adj.x >= 0 and adj.y >= 0:
            adj_r = region(adj, region_type, erosion_level)
            if (equipped_tool == NEITHER and adj_r == ROCKY or
                equipped_tool == TORCH and adj_r == WET or
                equipped_tool == CLIMBING_GEAR and adj_r == NARROW):
                    continue

            res[(adj, equipped_tool)] = 1

    for t in TOOLS:
        if t != equipped_tool:
            res[(p, t)] = 7

    return res


dist = {}
prev = {}
unvisited = set()

extra_xlen = 50
extra_ylen = 5

for i in range(max_x + extra_xlen):
    for j in range(max_y + extra_ylen):
        p = Pos(i, j)
        nodes = []
        for tool in [TORCH, CLIMBING_GEAR, NEITHER]:
            t = region(p, region_type, erosion_level)
            if t == ROCKY:
                nodes.append((p, TORCH))
                nodes.append((p, CLIMBING_GEAR))

            elif t == WET:
                nodes.append((p, CLIMBING_GEAR))
                nodes.append((p, NEITHER))

            elif t == NARROW:
                nodes.append((p, TORCH))
                nodes.append((p, NEITHER))

        for node in nodes:
            unvisited.add(node)
            dist[node] = (max_x + max_y) * 8 * 100

dist[(mouth, TORCH)] = 0
prev[(mouth, TORCH)] = None

objective = (TARGET, TORCH)

while len(unvisited) > 0:
    print len(unvisited)
    u = min(unvisited, key=lambda v: dist[v])

    if u == objective:
        break

    unvisited.remove(u)

    for n, l in neighbors(u).iteritems():
        if n in unvisited:
            alt = dist[u] + l
            if alt < dist[n]:
                dist[n] = alt
                prev[n] = u

print objective, dist[objective]
# p = prev[objective]
# while p:
#     print p, dist[p]
#     p = prev[p]
