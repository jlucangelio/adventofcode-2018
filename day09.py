import re

INPUT = "493 players; last marble is worth 71863 points"
nplayers, last_marble = re.match("([0-9]+) players; last marble is worth ([0-9]+) points", INPUT).groups()

nplayers = int(nplayers)
last_marble = int(last_marble)
# last_marble = 5 * int(last_marble)

current_player = 0
scores = dict([(p, 0) for p in range(nplayers)])
circle = [0]
current_marble = 0
# DEBUG
# nplayers = 10
# last_marble = 1618
for next_marble in range(1, last_marble + 1):
    # if next_marble % 1000 == 0:
    #     print ".",
    # if next_marble % 10000 == 0:
    #     print "", next_marble, last_marble

    if next_marble % 23 != 0:
        if len(circle) == 1:
            circle.append(next_marble)
            current_marble = 1
            continue

        idx = (current_marble + 2) % len(circle)
        circle.insert(idx, next_marble)
        current_marble = idx
    elif next_marble % 23 == 0:
        to_pop = current_marble - 7
        m = circle.pop(to_pop)
        scores[current_player] += next_marble + m
        current_marble = to_pop
    else:
        print "error"

    current_player = (current_player + 1) % nplayers
    # print circle, current_marble

print max(scores.values())
