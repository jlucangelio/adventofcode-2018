import copy

def react(polymer):
    res = copy.copy(polymer)
    i = 0
    while i < len(res) - 1:
        if (res[i].lower() == res[i+1].lower() and
            res[i] != res[i+1]):
            del res[i]
            del res[i]
            i -= 1
        else:
            i += 1

    return res


def remove(polymer, unit):
    res = copy.copy(polymer)

    i = 0
    while i < len(res):
        if res[i].lower() == unit:
            del res[i]
        else:
            i += 1

    return res


with open("day05.input") as f:
    polymer = list(f.read())

# print polymer

print len(react(polymer))

min_length = None
for o in range(ord("a"), ord("a") + 26):
    c = chr(o)
    l = len(react(remove(polymer, c)))
    if min_length is not None:
        if l < min_length:
            min_length = l
    else:
        min_length = l

print min_length
