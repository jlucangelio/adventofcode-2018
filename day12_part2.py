INITIAL_STATE = "#..#####.#.#.##....####..##.#.#.##.##.#####..####.#.##.....#..#.#.#...###..#..###.##.#..##.#.#.....#"
GENS = 50000000000

rules = {}
with open("day12.input") as f:
    for line in f:
        condition, _, result = line.strip().split()
        rules[condition] = result == "#"

pots = {}
pots[0] = set([i for i, c in enumerate(INITIAL_STATE) if c == "#"])
pots[1] = set()

leftmost_plant = 0
rightmost_plant = INITIAL_STATE.rfind("#")
last_offsets = None
for gen in xrange(GENS):
    cur_pots = pots[gen % 2]
    next_pots = pots[(gen + 1) % 2]
    next_pots.clear()

    if gen % (GENS/1000000) == 0:
        cur_offsets = [p - gen for p in sorted(cur_pots)]
        if last_offsets:
            if cur_offsets == last_offsets:
                print sum([GENS + offset for offset in cur_offsets])
                break

        last_offsets = cur_offsets

    for center_pot in range(leftmost_plant - 2, rightmost_plant + 3):
        state = []
        for pot_offset in range(-2, 3):
            if center_pot + pot_offset in cur_pots:
                state.append("#")
            else:
                state.append(".")

        state = "".join(state)
        alive = rules[state]
        if alive:
            next_pots.add(center_pot)

    leftmost_plant = min(next_pots)
    rightmost_plant = max(next_pots)
