import copy
from datetime import datetime

logs = []

with open("day04.input") as f:
    # [1518-10-03 00:47] falls asleep
    # [1518-07-26 23:50] Guard #487 begins shift
    # [1518-06-22 00:48] wakes up
    for line in f:
        sdt, note = line.strip().split("]")
        ymd, hm = sdt[1:].split()
        y, month, d = ymd.split("-")
        h, minute = hm.split(":")

        dt = datetime(int(y), int(month), int(d), int(h), int(minute))
        # print dt

        logs.append((dt, note.strip()))

sorted_logs = sorted(logs, key=lambda t: t[0])

# print sorted_logs

template = [0 for _ in range(60)]
guard_schedules = {}
total_slept = {}

guard = None
asleep = False
for log in sorted_logs:
    tokens = log[1].split()
    if tokens[0] == "Guard":
        guard = int(tokens[1][1:])
        if guard not in guard_schedules:
            guard_schedules[guard] = copy.copy(template)
            total_slept[guard] = 0

        asleep = False

    elif tokens[0] == "falls":
        if guard is None:
            print "error"
            break
        else:
            asleep = True
            started_sleeping = log[0].minute

    elif tokens[0] == "wakes":
        if guard is None or asleep == False:
            print "error"
            break
        else:
            woke_up = log[0].minute
            for m in range(started_sleeping, woke_up):
                guard_schedules[guard][m] = guard_schedules[guard][m] + 1
            total_slept[guard] += woke_up - started_sleeping
            asleep = False

max_guard = None
max_sleep = 0
for g, total_sleep in total_slept.iteritems():
    if total_sleep > max_sleep:
        max_guard = g
        max_sleep = total_sleep

max_minute = 0
max_minute_value = 0
for m, v in enumerate(guard_schedules[max_guard]):
    if v > max_minute_value:
        max_minute = m
        max_minute_value = v

print max_guard, max_minute, max_guard * max_minute

max_guard = 0
max_minute = 0
max_minute_value = 0
for g, schedule in guard_schedules.iteritems():
    for m, v in enumerate(schedule):
        if v > max_minute_value:
            max_guard = g
            max_minute = m
            max_minute_value = v

print max_guard, max_minute, max_guard * max_minute
