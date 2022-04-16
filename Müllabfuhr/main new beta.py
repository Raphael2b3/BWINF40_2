from typing import List

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
        self.crossing_ids: List[int] = [start]

    def decide_next_path(self, _wayback=False):
        position = self.get_pos_crs()
        for street in position.streets:
            if not street.important and street.usable > 0 and not _wayback:
                return street
        for street in position.streets:
            if street.important and street.usable > 0 and _wayback:
                return street

    def get_pos_crs(self):
        return crossings[self.crossing_ids[-1]]



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
        self.usable = 1
        self.important = False

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


def mark_important_streets():
    for c in crossings:
        blocked = c.streets[:]
        for s in c.streets:
            blocked.remove(s)
            path = get_shortest_paths(0, blocked)
            s.important = path[c.id].weight != float("inf")
            blocked.append(s)


def find_way_back():
    path_tree = shortest_paths[0]
    for car in cars:
        way_back = path_tree[car.get_pos_crs().id].copy()
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


def dijkstra_algorithm(_start_id, blocked_streets=None):
    if blocked_streets is None: blocked_streets = []
    paths = [INF_PATH for _ in range(n_crossings)]
    paths[_start_id] = Path(_start_id)
    finished = [False for _ in range(n_crossings)]

    cur_crossing_id = _start_id
    while False in finished:
        cur_crossing = crossings[cur_crossing_id]

        finished[cur_crossing_id] = True
        path: Path = paths[cur_crossing_id]

        for street in cur_crossing.streets:
            if street in blocked_streets: continue
            goal_id = street.other_crossing(cur_crossing_id)
            if finished[goal_id]: continue
            if path.weight + street.weight >= paths[goal_id].weight: continue

            goal_path = path.copy()
            goal_path.append(street)
            paths[goal_id] = goal_path

        for i in range(n_crossings):
            if finished[i]: continue  # nicht wenn crossings fertig
            if finished[cur_crossing_id]:  # wenn betrachteter Fertig wechseln!
                cur_crossing_id = i
                continue
            if paths[cur_crossing_id].weight <= paths[i].weight: continue
            # bleibt bei dem i welches die kleinste distanz hat
            cur_crossing_id = i
        if paths[cur_crossing_id].weight == float("inf"):
            break  # abbruch weil nicht erreichbar
    return paths


def bench_crossings():
    bad_crossings = []
    for c in crossings:
        if len(c.streets) % 2 != 0:
            bad_crossings.append(c)
    while len(bad_crossings) > 0:
        bc = bad_crossings[0]
        sp = get_shortest_paths(bc.id)
        path_to_double = sp[bad_crossings[1].id]
        for i in range(2, len(bad_crossings)):
            new_path2dbl = sp[bad_crossings[i].id]
            if path_to_double.weight > new_path2dbl.weight:
                path_to_double = new_path2dbl
        for street in path_to_double.streets:
            street.usable += 1
        bad_crossings.remove(bc)
        bad_crossings.remove(path_to_double.get_pos_crs())


def get_shortest_paths(start, blocked=None):
    if blocked is not None:
        return dijkstra_algorithm(start, blocked)
    if not start in shortest_paths:
        shortest_paths[start] = dijkstra_algorithm(start)
    return shortest_paths[start]


get_time("Start")

if __name__ == '__main__':
    # Consts
    days = 1  # von montag bis freitag sind 5 tage
    start_position = 0
    n_cleared_streets = 0
    remove_list = []
    shortest_paths = {}
    crossings, streets = get_input()
    cars = [Path(start_position) for i in range(days)]  # erstelle 5 car Klassen
    INF_PATH = Path("inf")

    n_crossings = len(crossings)
    bench_crossings()
    mark_important_streets()
    prozessbar.goal = n_streets = len(streets)
    while n_cleared_streets < n_streets:  # Programm läuft bis alle streets genutzt wurden
        prozessbar.show_state(n_cleared_streets)

        car = get_next_car()
        street = car.decide_next_path()
        street.usable -= 1
        if street.usable == 0:
            n_cleared_streets += 1

        street = car.decide_next_path()
        street.usable -= 1
        car.path.append(street)
        if street.usable == 0:
            n_cleared_streets += 1

    for auto in cars:
        for i in auto.streets:
            if i in streets:
                streets.remove(i)
    if len(streets) != 0:
        input("YARAK")
    find_way_back()
    print_solution()

get_time("Stop")
