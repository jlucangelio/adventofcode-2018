n = 940

c = 0
for i in range(1, n+1):
    if n % i == 0:
        # print n, i
        c += i

print c

n += 10550400

c = 0
for i in range(1, n+1):
    if n % i == 0:
        # print n, i
        c += i

print c
