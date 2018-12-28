import math

INPUT = """#ip 2
seti 123 0 3
bani 3 456 3
eqri 3 72 3
addr 3 2 2
seti 0 0 2
seti 0 6 3
bori 3 65536 4
seti 7041048 8 3
bani 4 255 5
addr 3 5 3
bani 3 16777215 3
muli 3 65899 3
bani 3 16777215 3
gtir 256 4 5
addr 5 2 2
addi 2 1 2
seti 27 6 2
seti 0 1 5
addi 5 1 1
muli 1 256 1
gtrr 1 4 1
addr 1 2 2
addi 2 1 2
seti 25 1 2
addi 5 1 5
seti 17 8 2
setr 5 2 4
seti 7 9 2
eqrr 3 0 5
addr 5 2 2
seti 5 3 2
""".splitlines()

functions = {}

def addr(a, b, c):
    return "r%d = r%d + r%d" % (c, a, b)

def addi(a, b, c):
    return "r%d = r%d + %d" % (c, a, b)


functions["addr"] = addr
functions["addi"] = addi


def mulr(a, b, c):
    return "r%d = r%d * r%d" % (c, a, b)

def muli(a, b, c):
    return "r%d = r%d * %d" % (c, a, b)

functions["mulr"] = mulr
functions["muli"] = muli


def banr(a, b, c):
    return "r%d = r%d & r%d" % (c, a, b)

def bani(a, b, c):
    return "r%d = r%d & %x" % (c, a, b)

functions["banr"] = banr
functions["bani"] = bani


def borr(a, b, c):
    return "r%d = r%d | r%d" % (c, a, b)

def bori(a, b, c):
    return "r%d = r%d | %x" % (c, a, b)

functions["borr"] = borr
functions["bori"] = bori


def setr(a, b, c):
    return "r%d = r%d" % (c, a)

def seti(a, b, c):
    return "r%d = %d" % (c, a)

functions["setr"] = setr
functions["seti"] = seti


def gt(a, b):
    if a > b:
        return 1
    else:
        return 0

def gtir(a, b, c):
    return "r%d = %d > r%d" % (c, a, b)

def gtri(a, b, c):
    return "r%d = r%d > %d" % (c, a, b)

def gtrr(a, b, c):
    return "r%d = r%d > r%d" % (c, a, b)

functions["gtir"] = gtir
functions["gtri"] = gtri
functions["gtrr"] = gtrr


def eq(a, b):
    if a == b:
        return 1
    else:
        return 0

def eqir(a, b, c):
    return "r%d = %d == r%d" % (c, a, b)

def eqri(a, b, c):
    return "r%d = r%d == %d" % (c, a, b)

def eqrr(a, b, c):
    return "r%d = r%d == r%d" % (c, a, b)

functions["eqir"] = eqir
functions["eqri"] = eqri
functions["eqrr"] = eqrr

for i, line in enumerate(INPUT[1:]):
    f, a, b, c = line.split()
    print "[%02d] %s" % (i, functions[f](int(a), int(b), int(c)))

# n = 10550400
# n += 940
# c = 0
# for i in range(1, n+1):
#     if n % i == 0:
#         print n, i
#         c += i

# print c

# 12123620
# 29417280
