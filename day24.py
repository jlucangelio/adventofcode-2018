import copy
import re

IMMUNE = 0
INFECTION = 1

SIDE = {
    "immune": IMMUNE,
    "infection": INFECTION
}

SIDE_NAME = {
    IMMUNE: "immune",
    INFECTION: "infection"
}

FIRE = 0
BLUDGEONING = 1
COLD = 2
RADIATION = 3
SLASHING = 4

ATTACK_TYPE = {
    "fire": FIRE,
    "bludgeoning": BLUDGEONING,
    "cold": COLD,
    "radiation": RADIATION,
    "slashing": SLASHING
}

class Group(object):
    def __init__(self, side, index, nunits, unit_hp, attack_damage, attack_type, initiative, immunities, weaknesses):
        self.side = side
        self.index = index
        self.nunits = nunits
        self.unit_hp = unit_hp
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.target = None


    def ep(self):
        return self.nunits * self.attack_damage


    def alive(self):
        return self.nunits > 0


    def select_target(self, target):
        self.target = target


    def tentative_damage(self, target):
        if self.attack_type in target.immunities:
            return 0
        elif self.attack_type in target.weaknesses:
            return self.ep() * 2
        else:
            return self.ep()


    def attack(self):
        if not self.target:
            return False

        damage = self.tentative_damage(self.target)
        if damage == 0:
            return False

        units_killed = min(damage // self.target.unit_hp, self.target.nunits)
        self.target.nunits -= units_killed

        # template = "%s group %d attacks defending group %d with damage %d killing %d units"
        # print template % (SIDE_NAME[self.side], self.index, self.target.index, damage, units_killed)
        return True


    def __str__(self):
        return "Group %d contains %d units, ep %d" % (self.index, self.nunits, self.ep())


def battle(infection, immune, boost=0):
    # infection = copy.deepcopy(orig_infection)
    # immune = copy.deepcopy(orig_immune)

    for g in immune:
        g.attack_damage += boost

    while len(immune) > 0 and len(infection) > 0:
        sides = {}
        sides[IMMUNE] = immune
        sides[INFECTION] = infection
        targets = {}
        targets[IMMUNE] = set()
        targets[INFECTION] = set()

        infection_sorted = sorted(infection, key=lambda g: (g.ep(), g.initiative), reverse=True)
        immune_sorted = sorted(immune, key=lambda g: (g.ep(), g.initiative), reverse=True)

        for team in [infection_sorted, immune_sorted]:
            for g in team:
                if not g.alive():
                    continue

                g.select_target(None)
                possible_targets = sorted(sides[1 - g.side], key=lambda t: (g.tentative_damage(t), t.ep(), t.initiative), reverse=True)
                chosen_target = None
                for pt in possible_targets:
                    if g.tentative_damage(pt) > 0 and pt.alive and pt not in targets[g.side]:
                        # print "%s group %d would deal defending group %d %d damage" % (SIDE_NAME[g.side], g.index, pt.index, g.tentative_damage(pt))
                        chosen_target = pt
                        break

                if chosen_target:
                    g.select_target(chosen_target)
                    targets[g.side].add(chosen_target)

        attack_happened = False
        groups = immune + infection
        attack_order = sorted(groups, key=lambda g: g.initiative, reverse=True)
        for g in attack_order:
            if g.alive():
                did_attack = g.attack()
                attack_happened = attack_happened or did_attack

        if not attack_happened:
            break

        # print sum([g.nunits for g in immune if g.alive()])
        # print sum([g.nunits for g in infection if g.alive()])
        # print "infection"
        # for ing in sorted(infection, key=lambda g: (g.ep(), g.initiative), reverse=True):
        #     if ing.alive():
        #         print ing
        # print "immune"
        # for img in sorted(immune, key=lambda g: (g.ep(), g.initiative), reverse=True):
        #     if img.alive():
        #         print img

        immune = [g for g in immune if g.alive()]
        infection = [g for g in infection if g.alive()]

    return infection, immune

groups = {}
groups["immune"] = []
groups["infection"] = []

for filename in ["day24.immune.input", "day24.infection.input"]:
# for filename in ["day24.immune.small.input", "day24.infection.small.input"]:
    with open(filename) as file:
        side = filename.split(".")[1]

        for i, line in enumerate(file):
            # 3020 units each with 3290 hit points with an attack that does 10 radiation damage at initiative 16
            # 1906 units each with 37289 hit points (immune to radiation; weak to fire) with an attack that does 28 radiation damage at initiative 3
            m = re.match("(?P<nunits>[0-9]+) units each with (?P<unit_hp>[0-9]+) hit points(?: \((?P<modifier>[a-z ,;]+)\))? with an attack that does (?P<attack_damage>[0-9]+) (?P<attack_type>[a-z]+) damage at initiative (?P<initiative>[0-9]+)", line.strip())

            modifiers = {}
            modifiers["immune"] = []
            modifiers["weak"] = []
            if m.group("modifier"):
                for section in m.group("modifier").split("; "):
                    modifier_type = section.split()[0]
                    types = [ATTACK_TYPE[t] for t in section.split(" ", 2)[2].split(", ")]
                    modifiers[modifier_type] = set(types)

            nunits = int(m.group("nunits"))
            unit_hp = int(m.group("unit_hp"))
            attack_damage = int(m.group("attack_damage"))
            attack_type = ATTACK_TYPE[m.group("attack_type")]
            initiative = int(m.group("initiative"))
            groups[side].append(Group(SIDE[side], i + 1, nunits, unit_hp, attack_damage, attack_type, initiative, modifiers["immune"], modifiers["weak"]))

immune = copy.deepcopy(groups["immune"])
infection = copy.deepcopy(groups["infection"])
infection, immune = battle(infection, immune)

print sum([g.nunits for g in immune if g.alive()])
print sum([g.nunits for g in infection if g.alive()])
print

for boost in xrange(1, 1000000):
    # print boost
    infection, immune = battle(copy.deepcopy(groups["infection"]), copy.deepcopy(groups["immune"]), boost)

    remaining_infection = sum([g.nunits for g in infection if g.alive()])
    remaining_immune = sum([g.nunits for g in immune if g.alive()])

    print remaining_infection, remaining_immune

    if remaining_immune > 0 and remaining_infection == 0:
        # print boost
        break
