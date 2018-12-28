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

MNEMONICS = """r3 = 123
r3 = r3 & 456
if r3 == 72 goto 05
<nop>
goto 1
r3 = 0
r4 = r3 | 0x10000
r3 = 7041048
r5 = r4 & 255
r3 = r3 + r5
r3 = r3 & 0xffffff
r3 = r3 * 65899
r3 = r3 & 0xffffff
if r4 < 256 goto 16
<nop>
goto 17
goto 28
r5 = 0
r1 = r5 + 1
r1 = r1 * 256
if r1 > r4 goto 23
<nop>
goto 24
goto 26
r5 = r5 + 1
goto 18
r4 = r5
goto 8
if r3 == r0 halt (goto 31)
r2 = r5 + r2
goto 6
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


DEBUG = False
PART1 = False

instructions = []
for line in INPUT[1:]:
    opcode, a, b, c = line.strip().split()
    instructions.append((opcode, int(a), int(b), int(c)))

ip_binding = int(INPUT[0].split()[1])

regs = dict([(i, 0) for i in range(6)])

r3s = set([])
r3_last = None

ip = 0
cycle = 0
while ip < len(instructions):
    if cycle % 100000000 == 0:
        print "cycle", cycle

    regs[ip_binding] = ip

    opcode, a, b, c = instructions[ip]

    if DEBUG:
        s = "%2d %s" % (ip, MNEMONICS[ip])
        if "r2" in s and s.rfind("r2") > s.find("="):
            l, r = s.split("=")
            s = l + "=" + r.replace("r2", str(ip))
        s += " " * (40 - len(s)) + str(regs)
        print s

    if ip == 28:
        r3_value = regs[3]
        if PART1:
            print r3_value
            break
        else:
            print len(r3s)
            if r3_value in r3s:
                print r3_last
                break
            else:
                r3s.add(r3_value)
                r3_last = r3_value

    functions[opcode](a, b, c, regs)

    ip = regs[ip_binding]
    ip +=1

    cycle += 1
