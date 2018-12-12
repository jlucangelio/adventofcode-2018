INITIAL_STATE = "#..#####.#.#.##....####..##.#.#.##.##.#####..####.#.##.....#..#.#.#...###..#..###.##.#..##.#.#.....#"

rules = {}

with open("day12.input") as f:
    for line in f:
        condition, _, result = line.strip().split()
        rules[condition] = result == "#"

pots = dict([(i, c == "#") for i, c in enumerate(INITIAL_STATE)])

leftmost_plant = 0
rightmost_plant = INITIAL_STATE.rfind("#")
for gen in range(1000):
    new_pots = {}
    for center_pot in range(leftmost_plant - 2, rightmost_plant + 3):
        state = []
        for pot_offset in range(-2, 3):
            alive = pots.get(center_pot + pot_offset, False)
            if alive:
                state.append("#")
            else:
                state.append(".")

        state = "".join(state)
        alive = rules[state]
        new_pots[center_pot] = rules[state]
        if alive and center_pot < leftmost_plant:
            leftmost_plant = center_pot
        if alive and center_pot > rightmost_plant:
            rightmost_plant = center_pot

    pots = new_pots

total = 0
for pot, alive in pots.iteritems():
    if alive:
        total += pot

print total
