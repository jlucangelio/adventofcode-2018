import copy
import re

out_nodes = {}
in_nodes = {}
edges = set()

with open("day07.input") as f:
# with open("day07.small.input") as f:
    # "Step E must be finished before step H can begin."
    for line in f:
        regex = "Step ([A-Z]) must be finished before step ([A-Z]) can begin."
        m = re.search(regex, line.strip())
        if m is not None:
            s, t = m.groups()
            if s not in out_nodes:
                out_nodes[s] = []
                in_nodes[s] = []
            if t not in out_nodes:
                out_nodes[t] = []
                in_nodes[t] = []
            out_nodes[s].append(t)
            in_nodes[t].append(s)
            edges.add((s, t))
        else:
            print "error"

# print nodes, edges

sources = set(copy.copy(out_nodes.keys()))

for s, t in edges:
    if t in sources:
        sources.remove(t)

steps = []
visited = set()
while len(sources) > 0:
    print sources
    next_ = min(sources)
    steps.append(next_)
    visited.add(next_)
    for d in out_nodes[next_]:
        if d not in visited:
            ready = True
            for in_node in in_nodes[d]:
                if in_node not in visited:
                    ready = False
                    break

            if ready:
                sources.add(d)

    sources.remove(next_)

print "".join(steps)
print

# Part two.

def duration(task):
    return ord(task) - ord("A") + 1 + 60
    # return ord(task) - ord("A") + 1

sources = set(copy.copy(out_nodes.keys()))

for s, t in edges:
    if t in sources:
        sources.remove(t)

visited = set()
seconds = 0
num_idle = 5
# num_idle = 2
ongoing = set()
remaining_time = {}

while len(sources) > 0 or len(ongoing) > 0:
    # Assign work.
    while num_idle > 0:
        if len(sources) == 0:
            break
        next_task = min(sources)
        ongoing.add(next_task)
        sources.remove(next_task)
        remaining_time[next_task] = duration(next_task)
        num_idle -= 1

    # Do one second of work.
    for task in ongoing:
        remaining_time[task] -= 1

    # Mark completed, release workers.
    finished = set()
    for task in ongoing:
        if remaining_time[task] == 0:
            del remaining_time[task]
            finished.add(task)

    for task in finished:
        ongoing.remove(task)
        visited.add(task)
        num_idle += 1

        for d in out_nodes[task]:
            if d not in visited:
                ready = True
                for in_node in in_nodes[d]:
                    if in_node not in visited:
                        ready = False
                        break

                if ready:
                    sources.add(d)

    seconds += 1

    print sources
    print ongoing
    print visited
    print num_idle
    print

print seconds
