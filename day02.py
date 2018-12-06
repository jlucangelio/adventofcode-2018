with open("day02.input") as f:
    ids = [line.strip() for line in f]

repeat_two = 0
repeat_three = 0

for _id in ids:
    print _id
    repeats = {}
    for letter in _id:
        repeats[letter] = repeats.get(letter, 0) + 1

    for key, value in repeats.items():
        if value == 2:
            print _id, key, value
            repeat_two += 1
            break

    for key, value in repeats.items():
        if value == 4:
            print "four", _id, key, value

        if value == 3:
            print _id, key, value
            repeat_three += 1
            break

    print "repeats", _id, repeat_two, repeat_three
    print

print repeat_two * repeat_three
print

for i in range(len(ids)):
    for j in range(len(ids)):
        if i < j:
            id_i = ids[i]
            id_j = ids[j]
            diffs = 0
            for k in range(len(id_i)):
                if id_i[k] != id_j[k]:
                    diffs += 1
                    if diffs > 1:
                        break

            if diffs == 1:
                print id_i, id_j
                common = ""

                for k in range(len(id_i)):
                    if id_i[k] == id_j[k]:
                        common += id_i[k]

                print common

