import re

from collections import namedtuple

Bot = namedtuple("Bot", "x y z r")

Point3 = namedtuple("Point3", "x y z")
# Prism = namedtuple("Prism", "top bottom")

ORIGIN = Point3(0, 0, 0)

def min_origin(points):
    return min(points, key=lambda p: distance(p, ORIGIN))


def max_origin(points):
    return max(points, key=lambda p: distance(p, ORIGIN))


class Prism(object):
    @classmethod
    def from_bot(cls, bot):
        min_x = bot.x - bot.r
        min_y = bot.y - bot.r
        min_z = bot.z - bot.r
        max_x = bot.x + bot.r
        max_y = bot.y + bot.r
        max_z = bot.z + bot.r

        b = Point3(min_x, min_y, min_z)
        t = Point3(max_x, max_y, max_z)
        return cls(t, b)


    def __init__(self, top, bottom):
        min_x = bottom.x
        min_y = bottom.y
        min_z = bottom.z
        max_x = top.x
        max_y = top.y
        max_z = top.z

        self.left_back_bottom = Point3(min_x, min_y, min_z)     # 000
        self.left_back_top = Point3(min_x, min_y, max_z)        # 001
        self.left_front_bottom = Point3(min_x, max_y, min_z)    # 010
        self.left_front_top  = Point3(min_x, max_y, max_z)      # 011

        self.right_back_bottom  = Point3(max_x, min_y, min_z)   # 100
        self.right_back_top  = Point3(max_x, min_y, max_z)      # 101
        self.right_front_bottom  = Point3(max_x, max_y, min_z)  # 110
        self.right_front_top  = Point3(max_x, max_y, max_z)     # 111

        self.bottom = self.left_back_bottom
        self.top = self.right_front_top

        self.corners = []
        for x in [min_x, max_x]:
            for y in [min_y, max_y]:
                for z in [min_z, max_z]:
                    self.corners.append(Point3(x, y, z))


    def volume(self):
        return abs(self.top.x - self.bottom.x) * abs(self.top.y - self.bottom.y) * abs(self.top.z - self.bottom.z)


    def contains(self, point):
        return (point.x >= self.bottom.x and point.x <= self.top.x and
                point.y >= self.bottom.y and point.y <= self.top.y and
                point.z >= self.bottom.z and point.z <= self.top.z)


    def __str__(self):
        return "[b=%s, t=%s]" % (self.bottom, self.top)


    def intersection(self, other):
        v = self.volume()
        vo = other.volume()

        if v > vo:
            bigger = self
            smaller = other
        else:
            bigger = other
            smaller = self

        # print smaller, bigger

        contained = [c for c in smaller.corners if bigger.contains(c)]
        ncorners = len(contained)
        if ncorners == 1:
            # Only one corner of the smaller prism is contained in the larger prism.
            c = contained.pop()
            # print c
            k = [bc for bc in bigger.corners if smaller.contains(bc)].pop()

            bottom = min([c, k], key=lambda p: distance(p, ORIGIN))
            top = max([c, k], key=lambda p: distance(p, ORIGIN))
            return Prism(top, bottom)

        elif ncorners == 2:
            # print "line"
            # Which dimension is shared between the two corners?
            c1, c2 = contained

            if c1.x == c2.x:
                pass
            elif c1.y == c2.y:
                pass
            elif c1.z == c2.z:
                pass
            else:
                print "error ncorners 2"
                return None

        elif ncorners == 4:
            # print "face"
            for dim in range(3):
                if all([corner[dim] == contained[0][dim] for corner in contained]):
                    # The face on |dim| is contained in |bigger|.

                    contained_dim = contained[0][dim]
                    if contained_dim == smaller.top[dim]:
                        # print "case 1"
                        # Intersection goes from bigger.bottom to smaller.top.
                        top = max_origin(contained)
                        m = list(min_origin(contained))
                        m[dim] = bigger.bottom[dim]
                        bottom = Point3(*m)

                    elif contained_dim == smaller.bottom[dim]:
                        # print "case 2"
                        # Intersection goes from smaller.bottom to bigger.top.
                        bottom = min_origin(contained)
                        m = list(max_origin(contained))
                        m[dim] = bigger.top[dim]
                        top = Point3(*m)
                    return Prism(top, bottom)

            print "error ncorners 4"
            return None

        elif ncorners == 8:
            # |smaller| is fully contained in |bigger|.
            return Prism(smaller.top, smaller.bottom)

        else:
            # Prisms don't intersect.
            return None


def distance(bot, other):
    return abs(bot.x - other.x) + abs(bot.y - other.y) + abs(bot.z - other.z)


bots = []
strongest = None

min_x = None
min_y = None
min_z = None
max_x = None
max_y = None
max_z = None

with open("day23.small.input") as f:
    # pos=<86508574,12573428,20533848>, r=83193725
    for line in f:
        m = re.match("pos=\<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)\>, r=([0-9]+)", line.strip())
        x, y, z, r = [int(t) for t in m.groups()]

        b = Bot(x, y, z, r)

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
print "part 1:", sum([1 for b in bots if distance(strongest, b) <= strongest.r])

# p = Prism.from_bot(Bot(5, 5, 5, 10))
# q = Prism(Point3(15, 15, 15), Point3(-5, -5, -5))

# print p.contains(Point3(6,6,6))
# print p.contains(Point3(16,16,16))
# print q.contains(Point3(6,6,6))
# print q.contains(Point3(16,16,16))

# print q.intersection(Prism(bottom=Point3(14, 14, 14), top=Point3(24, 24, 24)))
# print

# line_int = Prism(bottom=Point3(14, 14, 14), top=Point3(14, 16, 16))
# print q.intersection(line_int)
# print

# face_int = Prism(bottom=Point3(10, 10, 14), top=Point3(11, 11, 16))
# print q.intersection(face_int)
# print

prisms = [Prism.from_bot(b) for b in bots]
print "nbots", len(prisms)
cur_intersections = {}
for i, p in enumerate(prisms):
    for j, q in enumerate(prisms):
        if i < j:
            intersection = p.intersection(q)
            if intersection:
                cur_intersections[frozenset([i, j])] = intersection

print len(cur_intersections), cur_intersections

prev_intersections = None
while len(cur_intersections) > 1:
    prev_intersections = cur_intersections
    cur_intersections = {}

    for idxs, prism in prev_intersections.iteritems():
        if not prism:
            continue
        for new_idx, q in enumerate(prisms):
            new_idxs = idxs.union([new_idx])
            if new_idxs in prev_intersections:
                continue

            intersection = prism.intersection(q)

            if intersection:
                cur_intersections[new_idxs] = intersection

    print cur_intersections

if len(cur_intersections) == 1:
    prism = cur_intersections[cur_intersections.keys().pop()]
    print prism
    print min_origin(prism.corners)
else:
    # print prev_intersections
    # print max(prev_intersections, key=lambda t: len(t[1]))
    print min_origin(max(prev_intersections, key=lambda t: len(t[1]))[0].corners)
