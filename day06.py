import copy

from collections import namedtuple

Coord = namedtuple("Coord", "x y")
Step = namedtuple("Step", "coord dist")

NAMES = {}

def move_one(c, distance, left, top, right, bottom):
    res = []
    if c.x - 1 >= left:
        res.append(Step(Coord(c.x - 1, c.y), distance + 1)) # Move left.
    if c.x + 1 <= right:
        res.append(Step(Coord(c.x + 1, c.y), distance + 1)) # Move right
    if c.y - 1 >= top:
        res.append(Step(Coord(c.x, c.y - 1), distance + 1)) # Move up.
    if c.y - 1 <= bottom:
        res.append(Step(Coord(c.x, c.y + 1), distance + 1)) # Move down.

    return res


def print_grid(grid, left, top, right, bottom):
    for i in range(0, bottom - top + 1):
        for j in range(0, right - left + 1):
            c = Coord(left + j, top + i)
            if grid[c][0] is None:
                print ".",
            else:
                print NAMES[grid[c][0]],

        print


def print_region(region, coords, left, top, right, bottom):
    for i in range(0, bottom - top + 1):
        for j in range(0, right - left + 1):
            c = Coord(left + j, top + i)
            if c in coords:
                print NAMES[c],
            else:
                if c in region:
                    print "#",
                else:
                    print ".",

        print


def manhattan_distance(c1, c2):
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)

with open("day06.input") as f:
# with open("day06.small.input") as f:
    coords = [Coord(*[int(c) for c in line.strip().split(", ")]) for line in f]

grid = {}

# Find bounding box.
top = 1000
left = 1000
bottom = 0
right = 0

name = "A"
for i, c in enumerate(coords):
    if c.x < left:
        left = c.x
    if c.y < top:
        top = c.y

    if c.x > right:
        right = c.x
    if c.y > bottom:
        bottom = c.y

    grid[c] = (c, 0)
    NAMES[c] = i + 1

left -= 1
top -= 1
right += 1
bottom += 1

print left, top
print right, bottom

for c in coords:
    print "c ", c
    # Do BFS starting at c.
    next_ = [Step(c, 0)]
    visited = set()
    while len(next_) > 0:
        current, distance = next_.pop(0)
        if current in visited:
            continue

        visited.add(current)
        steps = move_one(current, distance, left, top, right, bottom)

        if current in grid and grid[current][1] == 0:
            # Original coord. Add next steps, but don't update grid.
            for step in steps:
                if step.coord not in visited:
                    next_.append(step)
            continue

        if current in grid:
            # Already reached. Reached in fewer steps?
            if distance < grid[current][1]:
                grid[current] = [c, distance]
            elif distance == grid[current][1]:
                # Equidistant from two coords.
                grid[current] = [None, distance]
            else:
                # Reached in more steps, stop moving.
                continue
        else:
            # Not yet reached.
            grid[current] = [c, distance]

        for step in steps:
            if step.coord not in visited:
                next_.append(step)

# print_grid(grid, left, top, right, bottom)

counts = {}
max_count = 0
max_coord = None

for grid_coord, (name_coord, distance) in grid.iteritems():
    if name_coord not in counts:
        counts[name_coord] = (0, False)

    count, inf = counts[name_coord]
    count += 1

    if (grid_coord.x == left or grid_coord.x == right or grid_coord.y == top or
        grid_coord.y == bottom):
            inf = True

    counts[name_coord] = (count, inf)

for c in coords:
    if counts[c][0] > max_count and counts[c][1] == False:
        max_count = counts[c][0]
        max_coord = c

print max_count
print

# MAX_DISTANCE = 32
MAX_DISTANCE = 10000

safe_region = set()
for i in range(0, bottom - top + 1):
    for j in range(0, right - left + 1):
        k = Coord(left + j, top + i)
        total_distance = 0
        for c in coords:
            total_distance += manhattan_distance(c, k)
            if total_distance >= MAX_DISTANCE:
                break

        if total_distance < MAX_DISTANCE:
            safe_region.add(k)

print len(safe_region)
# print_region(safe_region, coords, left, top, right, bottom)
