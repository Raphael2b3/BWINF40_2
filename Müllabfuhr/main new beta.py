from performance_analysing import *
import prozessbar


class Path:
    # Quasi wie eine Liste lauter streets
    # start: int ID von Crossing

    def __init__(self, start):
        if start == "inf":
            self.weight = float("inf")
            return
        self.start: int = start
        self.streets = []
        self.weight = 0
        self.crossing_ids: list[int] = [start]

    def append(self, street):
        self.streets.append(street)
        self.weight += street.weight
        self.crossing_ids.append(street.other_crossing(self.crossing_ids[-1]))

    def remove(self, _objekt):
        self.streets.pop(-1)
        self.weight -= _objekt.weight
        self.crossing_ids.pop(-1)

    def copy(self):
        t = Path(self.start)
        t.streets = self.streets[:]
        t.weight = self.weight
        t.crossing_ids = self.crossing_ids[:]
        return t

    def add(self, other):
        for i in other.streets:
            self.append(i)

    def reverse(self):
        self.start = self.crossing_ids[-1]
        self.streets.reverse()
        self.crossing_ids.reverse()

    def __str__(self):
        t = f"__Weg__\nInsgesammte Strecke: {self.weight}\nRoute:K{self.start}"
        cur_position = self.start
        for w in self.streets:
            goal = w.other_crossing(cur_position)
            t += f"->K{goal}"
            cur_position = goal
        return t


class Street:
    def __init__(self, start, stop, weight, _id):
        self.id = _id
        self.start = start
        self.stop = stop
        self.weight = weight
        self.used = False

    def __eq__(self, other):
        return self.id == other  # um geblockte streets zu erkennen

    def __gt__(self, other):
        return self.weight > other

    def __lt__(self, other):
        return self.weight < other

    def other_crossing(self, crossing_id):
        return self.start if crossing_id == self.stop else self.stop


class Crossing:

    def __init__(self, _id, _streets):
        self.streets = _streets
        self.streets.sort()
        self.id = _id
        self.used = False

    def __eq__(self, other):
        return self.id == other  # wenn geguckt wird, ob ein crossing schon bekannt ist


class Car:

    def __init__(self, position):
        self.position = crossings[position]
        self.path = Path(position)
        self.checkpoints = []
        self.decisions = {}
        self.compromised = []
        self.max_weight = 0

    def decide_next_path(self):
        while True:
            depth = len(self.path.streets)
            if depth not in self.decisions:
                self.decisions[depth] = 0

            if not self.is_compromising():
                if self.decisions[depth] < len(self.position.streets):
                    t = self.position.streets[self.decisions[depth]]
                    if not self.goal_useable(t):
                        self.decisions[depth] += 1
                        continue
                    self.path.append(t)
                    self.position = crossings[self.path.crossing_ids[-1]]
                    if self.max_weight < self.path.weight:
                        self.max_weight = self.path.weight
                    return
                self.compromised.append(depth)
                self.decisions[depth] = 0
            else:
                if self.decisions[depth] < len(self.position.streets):
                    if self.path.weight > self.max_weight:
                        self.decisions[depth] += 1
                        continue
                    t = self.position.streets[self.decisions[depth]]
                    self.path.append(t)
                    self.position = crossings[self.path.crossing_ids[-1]]
                    self.decisions[depth] += 1
                    return

    def goal_useable(self, strt: Street):
        future_pos = crossings[strt.other_crossing(self.position.id)]
        return not (strt.used or future_pos.used)


    def is_compromising(self):
        depth = len(self.path.streets)
        return depth in self.compromised

    def step_back(self):
        self.path.remove(self.path.streets[-1])
        depth = len(self.path.streets)


def find_way_back():
    path_tree = shortest_paths[0]
    for car in cars:
        way_back = path_tree[car.position.id].copy()
        way_back.reverse()
        car.path.add(way_back)


def print_solution():
    print("\n\nErgebnis:")
    for tag in range(days):
        print("Tag", tag + 1, ":")
        print(cars[tag].path)
        print()
    print("-Ende-")


def get_input():
    path = "muellabfuhr0.txt"
    text = open(path, "r").read()
    lines = text.split("\n")
    lines.pop(-1)
    _streets = []  # sammelt alle gegebenen Kanten
    for i in range(1, len(lines)):
        values = lines[i].split(" ")
        _streets.append(Street(int(values[0]), int(values[1]), int(values[2]), i - 1))

    _crossing = []
    values = lines[0].split(" ")
    for crossing_id in range(int(values[0])):
        tmp_streets = []
        for _street in _streets:
            if _street.start == crossing_id or _street.stop == crossing_id:
                tmp_streets.append(_street)
        _crossing.append(Crossing(crossing_id, tmp_streets))
    return _crossing, _streets


def get_next_car():  # gets smallest car
    car = cars[0]
    for i in range(1, days):
        if car.path.weight > cars[i].path.weight:
            car = cars[i]
    return car


get_time("Start")

if __name__ == '__main__':
    # Consts
    days = 1  # von montag bis freitag sind 5 tage
    start_position = 0
    n_cleared_streets = 0
    remove_list = []
    shortest_paths = {}
    crossings, streets = get_input()
    cars = [Car(start_position) for i in range(days)]  # erstelle 5 car Klassen
    INF_PATH = Path("inf")

    n_crossings = len(crossings)

    prozessbar.goal = n_streets = len(streets)
    while n_cleared_streets < n_streets:  # Programm läuft bis alle streets genutzt wurden
        prozessbar.show_state(n_cleared_streets)

        car = get_next_car()
        car.decide_next_path()
        for s in car.path.streets:
            p1, p2 = crossings[s.start], crossings[s.stop]
            if not s.used:
                n_cleared_streets += 1
            s.used = p2.used = p1.used = True

    for auto in cars:
        for i in auto.streets:
            if i in streets:
                streets.remove(i)
    if len(streets) != 0:
        input("YARAK")
    find_way_back()
    print_solution()

get_time("Stop")
