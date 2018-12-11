# INPUT = 18
INPUT = 9798

power_levels = [[0 for _ in range(300)] for _ in range(300)]

max_power = 0
max_x = 0
max_y = 0
max_size = 0
for x in range(300):
    for y in range(300):
        rack_id = x + 10
        p = rack_id * y
        p += INPUT
        p = p * rack_id
        if p < 100:
            p = 0
        else:
            p = int(str(p)[-3])
        p -= 5
        power_levels[x][y] = p

        if p > max_power:
            max_power = p
            max_x = x
            max_y = y
            max_size = 1

squares = {}
# max_power = 0
# max_x = 0
# max_y = 0
for x in range(298):
    for y in range(298):
        p = (power_levels[x    ][y] +
             power_levels[x + 1][y] +
             power_levels[x + 2][y] +
             power_levels[x    ][y + 1] +
             power_levels[x + 1][y + 1] +
             power_levels[x + 2][y + 1] +
             power_levels[x    ][y + 2] +
             power_levels[x + 1][y + 2] +
             power_levels[x + 2][y + 2])
        if p > max_power:
            max_power = p
            max_x = x
            max_y = y
            max_size = 3

        squares[(x, y, 3)] = p

# print "%d,%d" % (max_x, max_y), max_power

for x in range(299):
    for y in range(299):
        p = (power_levels[x    ][y] +
             power_levels[x + 1][y] +
             power_levels[x    ][y + 1] +
             power_levels[x + 1][y + 1])
        if p > max_power:
            max_power = p
            max_x = x
            max_y = y
            max_size = 2

        squares[(x, y, 2)] = p

for s in range(3, 300):
    size = s + 1
    print size
    for left in range(300 - s):
        for top in range(300 - s):
            p = 0
            subsquare_size = None
            for computed in range(s, 1, -1):
                if size % computed == 0:
                    subsquare_size = computed
                    break

            if subsquare_size:
                # Add up squares of computed*computed size.
                for x in range(left, left + size, computed):
                    for y in range(top, top + size, computed):
                        p += squares[x, y, computed]
            else:
                # Add up the (size-1)*(size-1) square in the top left.
                p += squares[(left, top, size - 1)]
                # Add the bottom row.
                for x in range(left, left + size):
                    p += power_levels[x][top + size - 1]
                # Add the rightmost column, but skip the last cell to avoid
                # counting it twice.
                for y in range(top, top + size - 1):
                    p += power_levels[left + size - 1][y]

            if p > max_power:
                max_power = p
                max_x = left
                max_y = top
                max_size = size

            squares[(left, top, size)] = p

print "%d,%d,%d" % (max_x, max_y, max_size)
