INPUT = (3,3,0,1,2,1)
# INPUT = (5,1,5,8,9)
# INPUT = (5,9,4,1,4)

scoreboard = [3, 7]
elf1 = 0
elf2 = 1
last_index = 0
while True:
    new_recipe = scoreboard[elf1] + scoreboard[elf2]
    srecipe = str(new_recipe)

    scoreboard.extend([int(c) for c in srecipe])

    done = False
    if last_index + len(INPUT) <= len(scoreboard):
        for index in range(last_index, len(scoreboard) - len(INPUT) + 1):
            if tuple(scoreboard[index:index + len(INPUT)]) == INPUT:
                print index
                done = True
                break

    last_index = len(scoreboard) - len(INPUT)
    if done:
        break

    elf1 = (elf1 + scoreboard[elf1] + 1) % len(scoreboard)
    elf2 = (elf2 + scoreboard[elf2] + 1) % len(scoreboard)

# print "".join([str(n) for n in scoreboard[-10:]])
