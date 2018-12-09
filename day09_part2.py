import re

from collections import namedtuple

class Node(object):
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        return "<value=%d>" % self.value


class CircularList(object):
    def __init__(self):
        self.current = None
        self.len = 0

    def insert(self, value):
        new = Node(value)

        if self.current:
            # current <-> new <-> old_next
            old_current = self.current
            old_next = self.current.next

            new.prev = old_current
            new.next = old_next
            old_current.next = new
            old_next.prev = new
            self.current = new
        else:
            self.current = new
            self.current.prev = self.current
            self.current.next = self.current

        self.len += 1

    def clockwise(self, steps):
        for _ in range(steps):
            self.current = self.current.next

    def counterclockwise(self, steps):
        for _ in range(abs(steps)):
            self.current = self.current.prev

    def remove(self):
        # old_prev <-> old_next
        ret = self.current.value
        old_prev = self.current.prev
        old_next = self.current.next
        old_prev.next = old_next
        old_next.prev = old_prev
        self.current = old_next
        self.len -= 1
        return ret

    def print_list(self):
        cur = self.current
        for _ in range(self.len):
            print cur.value,
            cur = cur.next

        print


INPUT = "493 players; last marble is worth 71863 points"
nplayers, last_marble = re.match("([0-9]+) players; last marble is worth ([0-9]+) points", INPUT).groups()

nplayers = int(nplayers)
# last_marble = int(last_marble)
last_marble = 100 * int(last_marble)

current_player = 0
scores = dict([(p, 0) for p in range(nplayers)])
circle = CircularList()
circle.insert(0)

# DEBUG
# nplayers = 9
# last_marble = 25

for next_marble in range(1, last_marble + 1):
    # circle.print_list()
    if next_marble % 23 != 0:
        circle.clockwise(1)
        circle.insert(next_marble)
    elif next_marble % 23 == 0:
        circle.counterclockwise(7)
        m = circle.remove()
        # print m
        scores[current_player] += next_marble + m
    else:
        print "error"

    current_player = (current_player + 1) % nplayers

print max(scores.values())
