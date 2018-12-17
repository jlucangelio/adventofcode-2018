import copy

from collections import deque, namedtuple
from enum import Enum

class Position(namedtuple("Position", "x y")):
    __slots__ = ()

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)


UP = Position(0, -1)
DOWN = Position(0, 1)
LEFT = Position(-1, 0)
RIGHT = Position(1, 0)

MOVES = [LEFT, RIGHT, UP, DOWN]

def possible_moves(pos, cave):
    res = []
    for move in MOVES:
        dest = pos + move

        if (dest.x >= 0 and dest.x < len(cave) and
            dest.y >= 0 and dest.y < len(cave[0])):
                res.append(dest)

    return res


def valid_move(pos, cave):
    return (cave[pos.x][pos.y] == "." or
            (type(cave[pos.x][pos.y]) == Unit and
             not cave[pos.x][pos.y].alive))


reading_order = lambda e: (e[1], e[0])

UType = Enum("UnitType", "Elf Goblin")

class Unit(object):
    def __init__(self, t, x, y):
        self.t = t
        self.x = x
        self.y = y
        self.hp = 200
        self.attack = 3
        self.alive = True


    def pos(self):
        return Position(self.x, self.y)


    def enemies_in_range(self, cave):
        res = []

        for x, y in possible_moves(self.pos(), cave):
            c = cave[x][y]
            if type(c) == Unit and self.t != c.t and c.alive:
                # Enemy
                res.append(c)

        res.sort(key=lambda u: reading_order(u.pos()))
        return res


    def full(self):
        return "%s, (%d,%d), %d" % (str(self), self.x, self.y, self.hp)


    def __str__(self):
        return self.t.name[0]


    def __repr__(self):
        return repr(self.t.name[0])


def print_cave(cave):
    for j in range(len(cave[0])):
        line = []
        for i in range(len(cave)):
            line.append(str(cave[i][j]))
        print "".join(line)

    print


def battle(cave, units, elf_death=False, elf_attack=3):
    completed_rounds = 0

    combat = True
    winner = None
    elf_died = False
    # while completed_rounds < 21:
    while combat and not elf_died:
        units.sort(key=lambda u: (u.pos().y, u.pos().x))

        for unit in units:
            if not unit.alive:
                continue

            if unit.t == UType.Elf:
                unit.attack = elf_attack

            unit_pos = unit.pos()
            if len(unit.enemies_in_range(cave)) == 0:
                # no enemies in range, find targets
                targets = [pt for pt in units if pt.t != unit.t and pt.alive]

                if len(targets) == 0:
                    # combat ends
                    combat = False
                    winner = unit.t
                    break

                positions_in_range = set()
                for target in targets:
                    valid_moves = [p for p in possible_moves(target.pos(), cave) if valid_move(p, cave)]
                    positions_in_range.update(valid_moves)

                # move
                # find reachable targets
                q = deque()
                q.append((unit_pos, 0))
                visited = set()
                target_distances = {}
                while len(q) > 0:
                    current_pos, dist = q.popleft()
                    if current_pos in visited:
                        continue

                    if current_pos in positions_in_range:
                        target_list = target_distances.get(dist, [])
                        target_list.append(current_pos)
                        target_distances[dist] = target_list

                    for next_step in possible_moves(current_pos, cave):
                        if not valid_move(next_step, cave):
                            continue

                        if next_step in visited:
                            continue

                        q.append((next_step, dist + 1))

                    visited.add(current_pos)

                if len(target_distances) > 0:
                    # find nearest target
                    min_distances = target_distances[min(target_distances.keys())]
                    nearest = sorted(min_distances, key=reading_order)[0]

                    # find shortest path
                    path_lengths = {}
                    for first_step in possible_moves(unit_pos, cave):
                        if not valid_move(first_step, cave):
                            continue

                        q = deque()
                        q.append((first_step, 0))
                        visited = set()
                        while len(q) > 0:
                            current_pos, dist = q.popleft()

                            if current_pos in visited:
                                continue

                            if current_pos == nearest:
                                step_list = path_lengths.get(dist, [])
                                step_list.append(first_step)
                                path_lengths[dist] = step_list
                                break

                            for next_step in possible_moves(current_pos, cave):
                                if not valid_move(next_step, cave):
                                    continue

                                if next_step in visited:
                                    continue

                                q.append((next_step, dist + 1))

                            visited.add(current_pos)

                    min_paths = path_lengths[min(path_lengths.keys())]
                    first_step = sorted(min_paths, key=reading_order)[0]

                    # move
                    unit.x = first_step.x
                    unit.y = first_step.y
                    cave[unit_pos.x][unit_pos.y] = "."
                    cave[unit.x][unit.y] = unit

            # attack
            in_range = unit.enemies_in_range(cave)
            if len(in_range) > 0:
                attacked = sorted(in_range, key=lambda u: (u.hp, u.y, u.x))[0]
                # print unit.full(), attacked.full()
                attacked.hp -= unit.attack
                if attacked.hp <= 0:
                    attacked.alive = False
                    if elf_death and attacked.t == UType.Elf:
                        elf_died = True

        new_units = []
        for unit in units:
            # print unit.full()
            if not unit.alive:
                if type(cave[unit.x][unit.y]) == Unit and not cave[unit.x][unit.y].alive:
                    cave[unit.x][unit.y] = "."
            else:
                new_units.append(unit)

        units = new_units

        if combat:
            completed_rounds += 1
            # print "round", completed_rounds
            # print_cave(cave)

    return (winner, elf_died, completed_rounds, sum([u.hp for u in units if u.alive]))

original_cave = None
original_units = []
file = "day15.input"
# file = "day15.small.input"
with open(file) as f:
    lines = f.readlines()
    original_cave = [[None for _ in lines] for _ in lines[0].strip()]
    for j, line in enumerate(lines):
        for i, c in enumerate(line.strip()):
            if c == "#" or c == ".":
                original_cave[i][j] = c
            elif c == "E":
                # Elf
                elf = Unit(UType.Elf, i, j)
                original_cave[i][j] = elf
                original_units.append(elf)
            elif c == "G":
                # Goblin
                goblin = Unit(UType.Goblin, i, j)
                original_cave[i][j] = goblin
                original_units.append(goblin)

winner, elf_died, rounds, sum_hp = battle(original_cave, original_units)
print rounds, sum_hp, rounds * sum_hp, winner, elf_died

with open(file) as f:
    lines = f.readlines()
    for elf_power in range(4, 100):
        original_cave = [[None for _ in lines] for _ in lines[0].strip()]
        original_units = []
        for j, line in enumerate(lines):
            for i, c in enumerate(line.strip()):
                if c == "#" or c == ".":
                    original_cave[i][j] = c
                elif c == "E":
                    # Elf
                    elf = Unit(UType.Elf, i, j)
                    original_cave[i][j] = elf
                    original_units.append(elf)
                elif c == "G":
                    # Goblin
                    goblin = Unit(UType.Goblin, i, j)
                    original_cave[i][j] = goblin
                    original_units.append(goblin)

        winner, elf_died, rounds, sum_hp = battle(copy.copy(original_cave),
                                                  copy.copy(original_units),
                                                  elf_death=True, elf_attack=elf_power)
        print winner, elf_died, rounds, sum_hp
        if winner and winner == UType.Elf and not elf_died:
            print rounds * sum_hp
            break
