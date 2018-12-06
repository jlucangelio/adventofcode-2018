total = 0

with open("day1.input") as f:
    for line in f:
        total += int(line.strip())

print total

with open("day1.input") as f:
    changes = [int(freq) for freq in f.readlines()]
    print changes

cur_freq = 0
seen_freqs = set()
i = 0
while True:
    cur_freq += changes[i]
    i = (i + 1) % len(changes)
    if cur_freq in seen_freqs:
        break
    else:
        seen_freqs.add(cur_freq)

print cur_freq
