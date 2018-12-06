from collections import namedtuple

claims = {}
fabric = {}
overlap = set()

Coord = namedtuple("Coord", "x y")
Size = namedtuple("Size", "w h")

with open("day03.input") as f:
# with open("day03.small.input") as f:
    for line in f:
        # "#1 @ 185,501: 17x15"
        print line.strip()
        sclaim_no, _, scoords, ssize = line.strip().split()
        claim_no = int(sclaim_no[1:])
        coords = Coord(*[int(token) for token in scoords[:-1].split(",")])
        print coords
        size = Size(*[int(token) for token in ssize.split("x")])
        print size
        print

        claims[claim_no] = (coords, size)

        for i in range(size.w):
            for j in range(size.h):
                claim_x = coords.x + i
                claim_y = coords.y + j

                if (claim_x, claim_y) in fabric:
                    fabric[(claim_x, claim_y)] = "X"
                    overlap.add((claim_x, claim_y))
                else:
                    fabric[(claim_x, claim_y)] = claim_no

print len(overlap)

for claim_no, (coords, size) in claims.iteritems():
    broken = False
    for i in range(size.w):
        for j in range(size.h):
            claim_x = coords.x + i
            claim_y = coords.y + j

            if fabric[claim_x, claim_y] == "X":
                broken = True
                break

        if broken == True:
            break

    if not broken:
        print claim_no
