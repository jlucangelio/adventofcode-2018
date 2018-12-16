import copy
import re

functions = {}

def addr(a, b, c, regs):
    regs[c] = regs[a] + regs[b]

def addi(a, b, c, regs):
    regs[c] = regs[a] + b


functions[0] = addr
functions[1] = addi


def mulr(a, b, c, regs):
    regs[c] = regs[a] * regs[b]

def muli(a, b, c, regs):
    regs[c] = regs[a] * b

functions[2] = mulr
functions[3] = muli


def banr(a, b, c, regs):
    regs[c] = regs[a] & regs[b]

def bani(a, b, c, regs):
    regs[c] = regs[a] & b

functions[4] = banr
functions[5] = bani


def borr(a, b, c, regs):
    regs[c] = regs[a] | regs[b]

def bori(a, b, c, regs):
    regs[c] = regs[a] | b

functions[6] = borr
functions[7] = bori


def setr(a, b, c, regs):
    regs[c] = regs[a]

def seti(a, b, c, regs):
    regs[c] = a

functions[8] = setr
functions[9] = seti


def gt(a, b):
    if a > b:
        return 1
    else:
        return 0

def gtir(a, b, c, regs):
    regs[c] = gt(a, regs[b])

def gtri(a, b, c, regs):
    regs[c] = gt(regs[a], b)

def gtrr(a, b, c, regs):
    regs[c] = gt(regs[a], regs[b])

functions[10] = gtir
functions[11] = gtri
functions[12] = gtrr


def eq(a, b):
    if a == b:
        return 1
    else:
        return 0

def eqir(a, b, c, regs):
    regs[c] = eq(a, regs[b])

def eqri(a, b, c, regs):
    regs[c] = eq(regs[a], b)

def eqrr(a, b, c, regs):
    regs[c] = eq(regs[a], regs[b])

functions[13] = eqir
functions[14] = eqri
functions[15] = eqrr


count = 0
possible_functions = dict([(i, set(range(16))) for i in range(16)])
with open("day16.input") as f:
# with open("day16.small.input") as f:
    lines = f.readlines()

    for i in range(0, len(lines), 4):
        # Before: [0, 2, 0, 2]
        # 6 0 1 1
        # After:  [0, 1, 0, 2]
        before = lines[i].strip()
        m = re.match("Before: \[([0-9]), ([0-9]), ([0-9]), ([0-9])\]", before)
        regs_before = {}
        for j in range(4):
            regs_before[j] = int(m.groups()[j])

        operation = [int(t) for t in lines[i + 1].strip().split()]

        after = lines[i + 2].strip()
        m = re.match("After:  \[([0-9]), ([0-9]), ([0-9]), ([0-9])\]", after)
        regs_after = {}
        for j in range(4):
            regs_after[j] = int(m.groups()[j])

        cur_possible_functions = set([])
        for fnum, function in functions.iteritems():
            cur_regs = copy.copy(regs_before)
            function(operation[1], operation[2], operation[3], cur_regs)
            if cur_regs == regs_after:
                cur_possible_functions.add(fnum)

        if len(cur_possible_functions) >= 3:
            count += 1

        possible_functions[operation[0]].intersection_update(cur_possible_functions)

print count
while sum([len(s) for s in possible_functions.values()]) > 16:
    for op1, s in possible_functions.iteritems():
        if len(s) == 1:
            for op2, t in possible_functions.iteritems():
                if op1 != op2:
                    e = s.pop()
                    t.discard(e)
                    s.add(e)

opcodes = {}
for op, s in possible_functions.iteritems():
    opcodes[op] = functions[s.pop()]

print opcodes

regs = dict([(i, 0) for i in range(4)])
with open("day16.2.input") as f:
    for line in f:
        operation = [int(t) for t in line.strip().split()]
        opcodes[operation[0]](operation[1], operation[2], operation[3], regs)

print regs[0]
