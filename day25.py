def dist(point, other):
    return sum([abs(point[i] - other[i]) for i in range(4)])


POINTS = []
# with open("day25.small.input") as file:
with open("day25.input") as file:
    for line in file:
        point = tuple([int(c) for c in line.strip().split(",")])
        POINTS.append(point)

constellations = []

for point in POINTS:
    # if len(constellations) == 0:
    #     constellations.add([point])
    #     continue

    near = []
    for i, c in enumerate(constellations):
        for other in c:
            if dist(point, other) <= 3:
                near.append(i)
                break

    new_c = set()
    for idx in reversed(near):
        c = constellations.pop(idx)
        new_c.update(c)
    new_c.add(point)
    constellations.append(new_c)

print len(constellations)
