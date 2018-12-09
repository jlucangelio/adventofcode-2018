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

circle = [12, 6, 13, 3, 14, 7, 15, 0, 16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 22, 11, 1]
current_marble = 20

starting_marble = 23
current_player = (starting_marble - 1 - 1) % nplayers
next_marble = starting_marble

while next_marble <= last_marble:
    if next_marble % 23 == 1:
        # Insert 22.
        for _ in range(22):
            idx = (current_marble + 2) % len(circle)
            circle.insert(idx, next_marble)
            current_marble = idx
            next_marble += 1
            current_player = (current_player + 1) % nplayers
    else:
        if next_marble % 23 != 0:
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

        next_marble += 1
        current_player = (current_player + 1) % nplayers

    # print next_marble, circle, current_marble

print max(scores.values())
