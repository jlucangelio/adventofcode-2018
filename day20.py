from collections import namedtuple, deque

INPUT = "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"
INPUT = "ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))"
# INPUT = "ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN"
# INPUT = "ENWWW(NEEE|SSE(EE|N))"

class Pos(namedtuple("Pos", "x y")):
    __slots__ = ()

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)


N = Pos(0, -1)
S = Pos(0, 1)
W = Pos(-1, 0)
E = Pos(1, 0)

DIRS = {}
DIRS["N"] = N
DIRS["S"] = S
DIRS["E"] = E
DIRS["W"] = W

def parse(regex, begin, end):
    # print "parse", regex[begin:end]
    if begin == end:
        return 0

    if regex.find("(", begin, end) == -1 and regex.find(")", begin, end):
        branches = regex[begin:end].split("|")
        return max([len(b) for b in branches])

    first_branch_begin = regex.find("(", begin, end)
    first_branch_end = -1
    stack = []
    cur_branch_begin = -1
    branches = []
    for i in range(first_branch_begin, end):
        c = regex[i]
        # print c

        if c == "(":
            # print i, "open paren"
            stack.append(i)
            if len(stack) == 1:
                cur_branch_begin = i + 1
        elif c == ")":
            # print i, "close paren"
            stack.pop()
            if len(stack) == 0:
                first_branch_end = i
                # print "begin", cur_branch_begin, "end", i
                branches.append(parse(regex, cur_branch_begin, i))
                break
        elif c == "|":
            if len(stack) > 1:
                continue
            else:
                # print "begin", cur_branch_begin, "end", i
                branches.append(parse(regex, cur_branch_begin, i))
                cur_branch_begin = i + 1

    return len(regex[begin:first_branch_begin]) + max(branches) + parse(regex, first_branch_end + 1, end)


def walk(regex, begin, end):
    if begin == end:
        return []

    if regex.find("(", begin, end) == -1 and regex.find(")", begin, end):
        branches = regex[begin:end].split("|")
        # print "branches", branches
        return branches

    first_branch_begin = regex.find("(", begin, end)
    first_branch_end = -1
    stack = []
    cur_branch_begin = -1
    branches = []
    for i in range(first_branch_begin, end):
        c = regex[i]
        # print c

        if c == "(":
            # print i, "open paren"
            stack.append(i)
            if len(stack) == 1:
                cur_branch_begin = i + 1
        elif c == ")":
            # print i, "close paren"
            stack.pop()
            if len(stack) == 0:
                first_branch_end = i
                # print "begin", cur_branch_begin, "end", i
                branches.extend(walk(regex, cur_branch_begin, i))
                break
        elif c == "|":
            if len(stack) > 1:
                continue
            else:
                # print "begin", cur_branch_begin, "end", i
                branches.extend(walk(regex, cur_branch_begin, i))
                cur_branch_begin = i + 1

    res = []
    prefix = regex[begin:first_branch_begin]
    suffixes = walk(regex, first_branch_end + 1, end)
    # print "prefix", prefix
    for b in branches:
        # print "b", b
        if len(suffixes) > 0:
            for c in suffixes:
                # print "c", c
                res.append(prefix + b + c)
        else:
            res.append(prefix + b)

    return res


# print parse(INPUT, 0, len(INPUT))
# for w in walk(INPUT, 0, len(INPUT)):
#     print w

# directions = walk(INPUT, 0, len(INPUT))
with open("day20.input") as f:
    regex = f.read()
    directions = walk(regex, 1, len(regex) - 1)

maze = {}
neighbors = {}
for route in directions:
    cur = Pos(0, 0)
    for direction in route:
        if cur not in neighbors:
            neighbors[cur] = set()
        n = cur + DIRS[direction]
        neighbors[cur].add(n)
        cur = n

# print neighbors

# BFS out from 0,0
visiting = deque()
visiting.append((Pos(0, 0), 0))
visited = set()
distances = {}
while len(visiting) > 0:
    pos, dist = visiting.popleft()

    if pos in visited:
        continue

    if pos in neighbors:
        for n in neighbors[pos]:
            visiting.append((n, dist + 1))

    visited.add(pos)
    distances[pos] = dist

# print distances
# print distances[Pos(0,0)]
print max(distances.values())
print sum([1 for d in distances.values() if d >= 1000])