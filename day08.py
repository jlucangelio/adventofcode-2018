from collections import namedtuple

Node = namedtuple("Node", "children metadata value")

def parse_tree(numbers, index):
    nchildren = numbers[index]
    nmetadata = numbers[index + 1]

    cur_index = index + 2
    children = []
    metadata = []
    metadata_sum = 0
    value = 0
    for _ in range(nchildren):
        (tree, new_index, partial_metadata_sum) = parse_tree(numbers, cur_index)
        cur_index = new_index
        children.append(tree)
        metadata_sum += partial_metadata_sum

    for mindex in range(nmetadata):
        datum = numbers[cur_index + mindex]
        metadata.append(datum)

    metadata_sum += sum(metadata)

    if len(children) == 0:
        value = metadata_sum
    else:
        for datum in metadata:
            if datum <= len(children):
                value += children[datum - 1].value

    return (Node(children, metadata, value), cur_index + nmetadata, metadata_sum)

# with open("day08.small.input") as f:
with open("day08.input") as f:
    numbers = [int(n) for n in f.read().split()]

print parse_tree(numbers, 0)
