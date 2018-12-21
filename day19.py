INPUT = """#ip 3
addi 3 16 3
seti 1 0 4
seti 1 0 1
mulr 4 1 5
eqrr 5 2 5
addr 5 3 3
addi 3 1 3
addr 4 0 0
addi 1 1 1
gtrr 1 2 5
addr 3 5 3
seti 2 9 3
addi 4 1 4
gtrr 4 2 5
addr 5 3 3
seti 1 2 3
mulr 3 3 3
addi 2 2 2
mulr 2 2 2
mulr 3 2 2
muli 2 11 2
addi 5 4 5
mulr 5 3 5
addi 5 16 5
addr 2 5 2
addr 3 0 3
seti 0 8 3
setr 3 2 5
mulr 5 3 5
addr 3 5 5
mulr 3 5 5
muli 5 14 5
mulr 5 3 5
addr 2 5 2
seti 0 0 0
seti 0 0 3
""".splitlines()

MNEMONICS = """goto 17
r4 = 1
r1 = 1
r5 = r4 * r1
if r5 == r2 goto 07
<nop>
goto 8
r0 = r4 + r0
r1 = r1 + 1
if r1 > r2 goto 12
<nop>
goto 3
r4 = r4 + 1
if r4 > r2 goto 07
<nop>
goto 2
r3 = r3 * r3
r2 = r2 + 2
r2 = r2 * r2
r2 = r3 * r2
r2 = r2 * 11
r5 = r5 + 4
r5 = r5 * r3
r5 = r5 + 16
r2 = r2 + r5
r3 = r3 + r0
goto 1
r5 = r3
r5 = r5 * r3
r5 = r3 + r5
r5 = r3 * r5
r5 = r5 * 14
r5 = r5 * r3
r2 = r2 + r5
r0 = 0
goto 1
""".splitlines()

functions = {}

def addr(a, b, c, regs):
    regs[c] = regs[a] + regs[b]

def addi(a, b, c, regs):
    regs[c] = regs[a] + b


functions["addr"] = addr
functions["addi"] = addi


def mulr(a, b, c, regs):
    regs[c] = regs[a] * regs[b]

def muli(a, b, c, regs):
    regs[c] = regs[a] * b

functions["mulr"] = mulr
functions["muli"] = muli


def banr(a, b, c, regs):
    regs[c] = regs[a] & regs[b]

def bani(a, b, c, regs):
    regs[c] = regs[a] & b

functions["banr"] = banr
functions["bani"] = bani


def borr(a, b, c, regs):
    regs[c] = regs[a] | regs[b]

def bori(a, b, c, regs):
    regs[c] = regs[a] | b

functions["borr"] = borr
functions["bori"] = bori


def setr(a, b, c, regs):
    regs[c] = regs[a]

def seti(a, b, c, regs):
    regs[c] = a

functions["setr"] = setr
functions["seti"] = seti


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

functions["gtir"] = gtir
functions["gtri"] = gtri
functions["gtrr"] = gtrr


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

functions["eqir"] = eqir
functions["eqri"] = eqri
functions["eqrr"] = eqrr

instructions = []
for line in INPUT[1:]:
    opcode, a, b, c = line.strip().split()
    instructions.append((opcode, int(a), int(b), int(c)))

regs = dict([(i, 0) for i in range(6)])
# regs[0] = 1
ip = 0
ip_binding = int(INPUT[0].split()[1])

cycle = 0
while ip < len(instructions):
    if cycle % 1000000 == 0:
        print cycle

    regs[ip_binding] = ip

    opcode, a, b, c = instructions[ip]

    # s = "%2d %s" % (ip, MNEMONICS[ip])
    # if "r3" in s and s.rfind("r3") > s.find("="):
    #     l, r = s.split("=")
    #     s = l + "=" + r.replace("r3", str(ip))
    # s += " " * (40 - len(s)) + str(regs)
    # print s
    functions[opcode](a, b, c, regs)

    ip = regs[ip_binding]
    ip +=1

    cycle += 1

print regs[0]
