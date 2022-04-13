from performance_analysing import *
import prozessbar


class ShortestPathDatabase:

    # Mit dem Deikstraalgorithmus wird für einen Graphen und einem Startpunkt alle Kürzesten paths berechnet

    def __init__(self, _start_id: int, blocked_streets):
        global crossings
        n_crossings = len(crossings)

        self.start = _start_id
        self.paths = [None for _ in range(n_crossings)]
        self.paths[_start_id] = Path(_start_id)
        distances = [float("inf") for _ in range(n_crossings)]
        self.finished = [False for _ in range(n_crossings)]

        # region Dijkstra Algorithm iterative
        cur_crossing_id = _start_id
        while False in self.finished:
            cur_crossing = crossings[cur_crossing_id]

            self.finished[cur_crossing_id] = True
            path: Path = self.paths[cur_crossing_id]

            distances[cur_crossing_id] = path.weight

            for street in cur_crossing.streets:
                if street in blocked_streets: continue
                goal_id = street.other_crossing(cur_crossing_id)
                if self.finished[goal_id]: continue
                if path.weight + street.weight >= distances[goal_id]: continue

                goal_path = path.copy()
                goal_path.append(street)
                distances[goal_id] = goal_path.weight
                self.paths[goal_id] = goal_path

            for i in range(n_crossings):
                if self.finished[i]: continue  # nicht wenn crossings fertig
                if self.finished[cur_crossing_id]:  # wenn betrachteter Fertig wechseln!
                    cur_crossing_id = i
                    continue
                if distances[cur_crossing_id] <= distances[i]: continue
                # bleibt bei dem i welches die kleinste distanz hat
                cur_crossing_id = i
            if distances[cur_crossing_id] == float("inf"):
                break  # abbruch weil nicht erreichbar

        # endregion

    def shortest_path(self, _id):
        return self.paths[_id] if self.finished[_id] else INF_PATH
        # wenn weg nicht existiert ist der Path unendlich lang


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
        self.used = 0

    def __eq__(self, other):
        return self.id == other

    def other_crossing(self, crossing):
        return self.start if crossing == self.stop else self.stop


class Crossing:

    def __init__(self, _id, _streets):
        self.streets = _streets
        self.n_seen_by = 0  # anzahl an Fragezeichen
        self.n_passed = 0
        self.id = _id
        self.blocked_streets = []

    def relevant(self):
        if len(self.blocked_streets) == len(self.streets):
            return False
        for i in self.streets:
            if i.used != 0 and i not in self.blocked_streets:
                self.blocked_streets.append(i)
        return len(self.blocked_streets) != len(self.streets)

    def __eq__(self, other):
        return self.id == other

    def __str__(self):
        return f"Crossing: {self.id}"


def get_input():
    path = "muellabfuhr8.txt"
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


def get_shortest_path_tree(start, blocked=None) -> ShortestPathDatabase:
    if blocked is not None and len(blocked) > 0:
        return ShortestPathDatabase(start, blocked)
    if start not in shortest_paths:
        shortest_paths[start] = ShortestPathDatabase(start, [])
    return shortest_paths[start]


def sort_noted_crossings(nc):
    # sortierung der gesichteten crossings: zuerst die, die Fragezeichen haben aber so wenige haben wie geht,
    # unter denen dann aufsteigend nach ausrufezeichen und zum schluss die, die keine Fragezeichen haben.
    swap = True
    while swap:  # BUBBLE SORT, bis nicht mehr getauscht wurde
        swap = False
        for i in range(len(nc) - 1):
            cross_a: Crossing = nc[i]  # jede Kreuzung in der Liste wird mit
            cross_b: Crossing = nc[i + 1]  # seiner nächsten verglichen

            if cross_a.n_seen_by == cross_b.n_seen_by:  # anzahl an Fragezeichen ist gleich
                if cross_a.n_passed < cross_b.n_passed:  # anzahl an Ausrufe Zeichen ist kleiner
                    continue  # nicht tauschen
                if cross_a.n_passed == cross_b.n_passed:  # anzahl ausrufezeichen ist gleich
                    if len(cross_a.streets) <= len(cross_b.streets):  # kreuzung hat weniger Straßen
                        continue  # nicht tauschen
            if 0 < cross_a.n_seen_by:  # hat Fragezeichen
                if cross_a.n_seen_by < cross_b.n_seen_by:  # hat Weniger ? als die Nächste Kreuzung
                    continue  # nicht tauschen
                if cross_b.n_seen_by == 0:  # das andere ist nicht erreichbar
                    continue  # nicht tauschen
            nc[i], nc[i + 1] = cross_b, cross_a  # tauschen
            swap = True


def mark_seen_crossings():
    for _car in cars:  # durch cars iterieren
        # markiere Fragezeichen "?"
        cur_position = crossings[_car.crossing_ids[-1]]  # aktuelle Position des cars
        for street in cur_position.streets:
            goal_id = street.other_crossing(_car.crossing_ids[-1])
            goal = crossings[goal_id]
            if not goal.relevant(): continue
            if goal not in noted_crossings:
                noted_crossings.append(goal)
            goal.n_seen_by += 1  # fragezeichen wird hinzugefügt


def find_next_goal():
    # finde das car mit der geringsten totalen distanz und sein weg zu dem crossings

    for _goal in noted_crossings:  # da gesichtete_knoten grade sortiert wurde, werden jetzt effizient
        # die crossings überprüft
        _best_car, _best_path = find_best_car_to(_goal)
        if _best_car is not None:  # wenn kein car gefunden wurde, wird der nächste Crossing ausprobiert
            return _best_car, _best_path
        # else: Das passiert, wenn crossings nicht erreichbar sind auf grund der geblockten streets


def find_best_car_to(_goal):
    _best_path = None
    _best_car = None
    total_path_length_of_car = float("inf")
    path_tree = get_shortest_path_tree(_goal.id, _goal.blocked_streets)
    # region findet das car welches am wenigsten car zum crossings benötigt

    for _car in cars:  # betrachtet jedes car
        path = path_tree.shortest_path(_car.crossing_ids[-1])  # schnellster Path der mindestens eine unbekannte
        # Street enthält
        tmp_ttl_pth_l = path.weight + _car.weight
        if total_path_length_of_car <= tmp_ttl_pth_l or path.weight == 0: continue
        # ein car muss gefunden werden welches noch nicht auf dem Crossing ist

        # der neue beste path wird abgespeichert
        _best_car = _car
        path = path.copy()
        path.reverse()
        _best_path = path
        total_path_length_of_car = tmp_ttl_pth_l
    return _best_car, _best_path


def goahead_on_crossings_with_2_options():
    global n_cleared_streets, n_streets
    # Crossing die nur 2 Kanten haben können weiter überfahren werden da es nur eine Möglichkeit gibt
    # fortzufahren, und zwar auf die nächste _street.
    while n_cleared_streets < n_streets:  # besseres While True
        cur_position = crossings[best_path.crossing_ids[-1]]
        if len(cur_position.streets) != 2: break
        for _street in cur_position.streets:
            if _street in best_path.streets: continue

            best_path.append(_street)
            cur_position = crossings[best_car.crossing_ids[-1]]
            cur_position.n_passed += 1
            if _street.used == 0:
                n_cleared_streets += 1
            _street.used += 1
            break


def safe_new_knowledge():
    global n_cleared_streets
    # streets und crossings werden als bekannt markiert
    for street in best_path.streets:  # erhöht die Zahl an besuchten streets
        if street.used == 0:
            n_cleared_streets += 1
        street.used += 1  # markiert street als benutzt

    for cur_crossing_id in best_path.crossing_ids[1:]:
        cur_crossing = crossings[cur_crossing_id]
        cur_crossing.n_passed += 1

        for street in cur_crossing.streets:
            goal_id = street.other_crossing(cur_crossing.id)
            goal = crossings[goal_id]
            if not goal.relevant(): continue
            if goal not in noted_crossings:
                noted_crossings.append(goal)


def remove_marks_and_find_delete_irrelevant_crossings():
    # irrelevante Crossing identifizieren
    remove_list.clear()
    for ntd_crossing in noted_crossings:  # entfernt alle Fragezeichen da neue generiert werden
        ntd_crossing.n_seen_by = 0
        if not ntd_crossing.relevant():  # crossing ist irrelevant, weil alle streets, die von ihm benutzt wurden
            remove_list.append(ntd_crossing)
    for o in remove_list: noted_crossings.remove(o)  # diese Crossing werden entfernt


def undo_bad_moves():
    # gehe bei fehlerhaften Bewegungen zurück
    for _car in cars:  # durch cars iterieren
        while len(_car.streets) > 0:  # Ein _car macht einen Teil seiner Strecke rückgängig, wenn schon überquert
            cur_crossing = crossings[_car.crossing_ids[-1]]  # aktuelle Position vom _car
            letzte_kante = _car.streets[-1]
            if letzte_kante.used == 1:
                break
            _car.remove(letzte_kante)  # verändert auch die letzte Position der Instanz
            letzte_kante.used -= 1
            cur_crossing.n_passed -= 1


def find_way_back():
    path_tree = get_shortest_path_tree(0)
    for car in cars:
        way_back = path_tree.shortest_path(car.crossing_ids[-1]).copy()
        way_back.reverse()
        car.add(way_back)


def print_solution():
    print("\n\nErgebnis:")
    for tag in range(days):
        print("Tag", tag + 1, ":")
        print(cars[tag])
        print()
    print("-Ende-")


get_time("Start")

if __name__ == '__main__':
    # Consts
    days = 5  # von montag bis freitag sind 5 tage
    start_position = 0
    n_cleared_streets = 0
    shortest_paths = {}
    noted_crossings = []
    remove_list = []
    cars = [Path(start_position) for i in range(days)]  # erstelle 5 car Klassen
    INF_PATH = Path("inf")

    crossings, streets = get_input()

    prozessbar.goal = n_streets = len(streets)

    crossings[start_position].n_passed = days
    noted_crossings.append(crossings[start_position])

    while n_cleared_streets < n_streets:  # Programm läuft bis alle streets genutzt wurden
        prozessbar.show_state(n_cleared_streets)

        mark_seen_crossings()
        sort_noted_crossings(noted_crossings)
        best_car, best_path = find_next_goal()
        goahead_on_crossings_with_2_options()
        best_car.add(best_path)  # make car move
        safe_new_knowledge()
        undo_bad_moves()

    find_way_back()

    print_solution()

get_time("Stop")
