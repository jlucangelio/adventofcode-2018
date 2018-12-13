import copy

from collections import namedtuple

Coord = namedtuple("Coord", "x y")

class Coord(namedtuple("Coord", "x y")):
    __slots__ = ()

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)


UP = Coord(0, -1)
DOWN = Coord(0, 1)
LEFT = Coord(-1, 0)
RIGHT = Coord(1, 0)

turns = ["l", "s", "r"]

def find_next_turn(t):
    return turns[(turns.index(t) + 1) % len(turns)]


def dir_to_enum(d):
    if d == "^": return UP
    if d == "v": return DOWN
    if d == "<": return LEFT
    if d == ">": return RIGHT


def move(tracks, cur_turn, c, d):
    track = tracks[c]
    res_c = c + d
    res_d = d

    next_track = tracks[res_c]
    if next_track == "/":
        if d == UP:
            # /-
            res_d = RIGHT
        elif d == DOWN:
            # -/
            res_d = LEFT
        elif d == LEFT:
            # /
            # |
            res_d = DOWN
        elif d == RIGHT:
            # |
            # /
            res_d = UP

    elif next_track == "\\":
        if d == UP:
            # -\
            res_d = LEFT
        elif d == DOWN:
            # \-
            res_d = RIGHT
        elif d == LEFT:
            # |
            # \
            res_d = UP
        elif d == RIGHT:
            # \
            # |
            res_d = DOWN

    elif next_track == "+":
        if cur_turn == "l":
            if d == UP:
                res_d = LEFT
            elif d == DOWN:
                res_d = RIGHT
            elif d == LEFT:
                res_d = DOWN
            elif d == RIGHT:
                res_d = UP
        elif cur_turn == "r":
            if d == UP:
                res_d = RIGHT
            elif d == DOWN:
                res_d = LEFT
            elif d == LEFT:
                res_d = UP
            elif d == RIGHT:
                res_d = DOWN
        cur_turn = find_next_turn(cur_turn)

    return (res_c, res_d, cur_turn)


# coord to type of track
tracks = {}
# cart position to direction
cart_direction = {}
new_cart_direction = {}
# cart position to turn decision
cart_next_turn = {}
new_cart_next_turn = {}

with open("day13.input") as f:
    for y, line in enumerate(f):
        for x, c in enumerate(line.strip("\n")):
            if c == "^" or c == "v" or c == "<" or c == ">":
                coord = Coord(x, y)
                cart_direction[coord] = dir_to_enum(c)
                cart_next_turn[coord] = "l"
                if c == "^" or c == "v":
                    tracks[coord] = "|"
                elif c == "<" or c == ">":
                    tracks[coord] = "-"
            elif c != " ":
                tracks[Coord(x,y)] = c

while len(cart_direction) > 1:
    carts = sorted(cart_direction.keys(), key=lambda c: Coord(c.y, c.x))

    for i, c in enumerate(carts):
        if c not in cart_direction:
            # Another cart crashed into |c|.
            continue

        d = cart_direction[c]
        new_c, new_d, next_turn = move(tracks, cart_next_turn[c], c, d)

        if new_c in cart_direction:
            # Crash into a cart that hasn't moved yet.
            print "crash"
            print new_c.x, new_c.y
            del cart_direction[new_c]
            del cart_next_turn[new_c]
        elif new_c in new_cart_direction:
            # Crash into a cart that has already moved.
            print "crash"
            print new_c.x, new_c.y
            # Remove cart crashed into.
            del new_cart_direction[new_c]
            del new_cart_next_turn[new_c]
            # Don't add the current cart to the new state, which is the same
            # as removing it.
        else:
            # Move successfully.
            del cart_direction[c]
            del cart_next_turn[c]
            new_cart_direction[new_c] = new_d
            new_cart_next_turn[new_c] = next_turn

    cart_direction = copy.copy(new_cart_direction)
    cart_next_turn = copy.copy(new_cart_next_turn)

    new_cart_direction.clear()
    new_cart_next_turn.clear()

print
print "last"
print cart_direction.keys()[0]
