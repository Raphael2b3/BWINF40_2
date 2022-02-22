import performance_analysing

perf = performance_analysing.time_analysing()


def timer_start():
    perf.set_time_point("Start")


def timer_stop():
    perf.set_time_point("Stop")


class Shortest_path_database:
    wege = []

    def __init__(self, _start_id, graph, geblockte_kanten):
        n_knoten = len(graph.knoten)
        if _start_id == 53 and geblockte_kanten == [112,119,161]:
            print("I found you")
        self.start = _start_id

        wege = [Weg(_start_id) for _ in range(n_knoten)]
        distanzen = [float("inf") for _ in range(n_knoten)]
        fertige = [False for _ in range(n_knoten)]
        knoten = graph.knoten

        # region Daijkstra Algorithm iterative
        betrachteter_knoten_id = _start_id
        kaka = 0
        while False in fertige:
            kaka+=1
            betrachteter_knoten = knoten[betrachteter_knoten_id]

            fertige[betrachteter_knoten_id] = True
            weg = wege[betrachteter_knoten_id]

            distanzen[betrachteter_knoten_id] = weg.gewicht

            for _kante in betrachteter_knoten.kanten:
                if _kante in geblockte_kanten: continue
                ziel_id = _kante.anderer_knoten(betrachteter_knoten_id)

                if fertige[ziel_id]: continue
                if weg.gewicht + _kante.gewicht >= distanzen[ziel_id]: continue
                ziel_weg = weg.copy()
                if not ziel_weg.append(_kante):
                    print("Error accourt")
                distanzen[ziel_id] = ziel_weg.gewicht
                wege[ziel_id] = ziel_weg

            beste_id = 0
            for i in range(n_knoten):
                if fertige[i]: continue
                if fertige[betrachteter_knoten_id]:
                    betrachteter_knoten_id = i
                    continue
                if distanzen[betrachteter_knoten_id] <= distanzen[i]: continue
                betrachteter_knoten_id = i
        # endregion
        self.wege = wege

    def kürzester_weg_zu(self, _id):
        return self.wege[_id]


class Weg:
    # Quasi wie eine Liste lauter kanten
    # start: int ID von Knoten
    def __init__(self, start):
        self.start: int = start
        self.kanten = []
        self.gewicht = 0
        self.knoten = [start]

    def append(self, o):
        self.kanten.append(o)
        self.gewicht += o.gewicht
        if o.anderer_knoten(self.knoten[-1]) is None:
            return False
        self.knoten.append(o.anderer_knoten(self.knoten[-1]))
        return True

    def remove(self, _objekt):
        self.kanten.pop(-1)
        self.gewicht -= _objekt.gewicht
        self.knoten.pop(-1)

    def copy(self):
        t = Weg(self.start)
        t.kanten = self.kanten[:]
        t.gewicht = self.gewicht
        t.knoten = self.knoten[:]
        return t

    def add(self, other):
        for i in other.kanten:
            self.append(i)

    def reverse(self):
        self.start = self.knoten[-1]
        self.kanten.reverse()
        self.knoten.reverse()

    def __str__(self):
        t = f"__Weg__\nInsgesammte Strecke: {self.gewicht}\nRoute:K{self.start}"
        currentpos = self.start
        for w in self.kanten:
            ziel = w.anderer_knoten(currentpos)
            t += f"->({w.gewicht})K{ziel}"
            currentpos = ziel
        return t


class Kante:
    def __init__(self, start, stop, gewicht, _id):
        self.id = _id
        self.start = start
        self.stop = stop
        self.gewicht = gewicht
        self.used = 0

    def __str__(self):
        return f"Kante: K{self.start} -> K{self.stop}({self.gewicht})"

    def __eq__(self, other):
        return self.id == other

    def anderer_knoten(self, knoten):
        if knoten == self.stop:
            return self.start
        if knoten == self.start:
            return self.stop
        return None
        raise  # Knoten Existiert nicht in Kante
        # TODO dieser fehler tritt auf wenn bei "muellabfuhr6.txt" ein Shortest path baum erstellt wird


class Knoten:

    def __init__(self, _id, kanten):
        self.kanten = kanten
        self.ziel_von = 0
        self.überquert_von = 0
        self.id = _id

    def relevant(self):
        for i in self.kanten:
            if i.used == 0: return True
        return False

    def __eq__(self, other):
        return self.id == other


class Graph:

    def __init__(self, _knoten, _kanten):
        self.knoten = _knoten
        self.kanten = _kanten
        self.kürzeste_wege: dict[int, Shortest_path_database] = {}

    def kürzester_weg_baum(self, start, blocked=None) -> Shortest_path_database:
        if blocked is not None and len(blocked) > 0:
            return Shortest_path_database(start, self, blocked)
        if start in self.kürzeste_wege:
            return self.kürzeste_wege[start]
        _wege = self.kürzeste_wege[start] = Shortest_path_database(start, self, [])
        return _wege


def get_input():
    pfad = "muellabfuhr6.txt"
    text = open(pfad, "r").read()
    zeilen = text.split("\n")
    zeilen.pop(-1)
    kanten = []  # sammelt alle gegebenen Kanten
    for i in range(1, len(zeilen)):  # ab Zeile i:1 werden die Würfel definiert
        wertederzeile = zeilen[i].split(" ")
        start = int(wertederzeile[0])
        stop = int(wertederzeile[1])
        gewicht = int(wertederzeile[2])
        kanten.append(Kante(start, stop, gewicht, i - 1))

    knoten = []
    zeile1_werte = zeilen[0].split(" ")
    for knotenID in range(int(zeile1_werte[0])):
        temp_kanten = []
        for kante in kanten:
            if kante.start == knotenID or kante.stop == knotenID:
                temp_kanten.append(kante)
        knoten.append(Knoten(knotenID, temp_kanten))
    return Graph(knoten, kanten)  # Rückgabe der Würfelliste


timer_start()
if __name__ == '__main__':
    verfügbareTage = 5  # von montag bis freitag sind 5 tage
    start_position = 0

    graph = get_input()
    n_kanten = len(graph.kanten)

    gesichtete_knoten = []
    besuchte_kanten = []
    strecken = [Weg(start_position) for i in range(verfügbareTage)]  # erstelle 5 Auto Klassen
    start_knoten = graph.knoten[start_position]
    start_knoten.überquert_von = verfügbareTage
    fortschritt = 0
    barhelper = 0
    bar = "." * 20
    removelist = []
    n_besuchtekanten = 0

    while n_besuchtekanten < n_kanten:

        # region Prozessbar
        fortschritt = round(n_besuchtekanten * 100 / n_kanten, 2)
        print("\r", fortschritt.__str__() + "%", "#" * barhelper + bar[barhelper:], end="")
        if fortschritt > barhelper * 5: barhelper += 1
        # endregion

        # region Markiere Knoten mit Fragezeichen + identifizieren neu gesichtete knoten + makiere ausrufezeichen
        removelist.clear()
        for knoten in gesichtete_knoten:  # entfernt alle Fragezeichen da neue generiert werden
            knoten.ziel_von = 0  # frage zeichen entfernen
            if not knoten.relevant():  # knoten ist irrelevant
                removelist.append(knoten)
        for o in removelist: gesichtete_knoten.remove(o)

        # TODO Verkürzung möglich
        # region gehe bei fehlerhaften bewegungen zurück
        for strecke in strecken:  # durch iteration durch die autos
            while len(strecke.kanten) > 0:  # grenze
                letzte_kante = strecke.kanten[-1]
                zielknoten = graph.knoten[strecke.knoten[-1]]
                überschneidung = False
                if letzte_kante.used == 1: break
                strecke.remove(letzte_kante)
                letzte_kante.used -= 1
                zielknoten.überquert_von -= 1
        # endregion

        for strecke in strecken:
            knoten = graph.knoten[strecke.knoten[-1]]
            if strecke.knoten[-1] not in gesichtete_knoten and knoten.relevant():
                gesichtete_knoten.append(knoten)
            for kante in knoten.kanten:
                ziel_id = kante.anderer_knoten(strecke.knoten[-1])
                ziel = graph.knoten[ziel_id]
                if not ziel.relevant(): continue
                if ziel not in gesichtete_knoten:
                    gesichtete_knoten.append(ziel)
                ziel.ziel_von += 1  # fragezeichen wird hinzu gefügt
        # endregion

        # region sortierung der gesichteten knoten zuerst die die Fragezeichen haben aber so wenige haben wie geht,
        # unter denen dann aufsteigend nach ausrufezeichen und zum schluss die die keine Fragezeichen haben.
        swap = True
        while swap:
            swap = False
            for i in range(len(gesichtete_knoten) - 1):
                knotA = gesichtete_knoten[i]
                knotB = gesichtete_knoten[i + 1]
                a_hat_fragezeichen = knotA.ziel_von > 0
                b_keine_fragezeichen = knotB.ziel_von == 0
                a_weniger_fragezeichen = knotA.ziel_von < knotB.ziel_von
                a_gleichviele_fragezeichen = knotA.ziel_von == knotB.ziel_von
                a_nicht_mehr_ausrufezeichen = not knotA.überquert_von > knotB.überquert_von

                if (b_keine_fragezeichen or a_weniger_fragezeichen or (
                        a_gleichviele_fragezeichen and a_nicht_mehr_ausrufezeichen)) and a_hat_fragezeichen:
                    continue  # nicht tauschen
                if not a_hat_fragezeichen and a_nicht_mehr_ausrufezeichen: continue

                gesichtete_knoten[i], gesichtete_knoten[i + 1] = knotB, knotA
                swap = True

        # endregion

        # region finde das nähste auto und sein weg zu dem knoten

        for knoten in gesichtete_knoten:
            geblockte_kanten = []
            for kante in knoten.kanten:
                if kante.used != 0:
                    geblockte_kanten.append(kante)

            if len(geblockte_kanten) == len(knoten.kanten): continue
            wege = graph.kürzester_weg_baum(knoten.id, geblockte_kanten)
            beste_strecke = None
            strecketotal = float("inf")
            bester_weg = None
            for strecke in strecken:
                weg = wege.kürzester_weg_zu(strecke.knoten[-1]).copy()
                tmp_strecketotal = weg.gewicht + strecke.gewicht
                if strecketotal <= tmp_strecketotal or weg.gewicht == 0: continue
                beste_strecke = strecke
                weg.reverse()
                bester_weg = weg
                strecketotal = tmp_strecketotal

            if beste_strecke is None: continue

            for kante in bester_weg.kanten:
                if kante.used == 0: n_besuchtekanten += 1
                kante.used += 1

            for _knoten_id in bester_weg.knoten[1:]:
                knoten = graph.knoten[_knoten_id]
                knoten.überquert_von += 1

            beste_strecke.add(bester_weg)
            # region zusatz checks

            while n_besuchtekanten < n_kanten:
                # knoten die nur 2 Kanten haben können weiter überfahren werden da es nur eine möglichkeit
                # fort zu fahren, Wenden ist depriorisisert
                if len(knoten.kanten) != 2: break
                for kante in knoten.kanten:
                    if kante not in beste_strecke.kanten:
                        beste_strecke.append(kante)
                        knoten = graph.knoten[beste_strecke.knoten[-1]]
                        knoten.überquert_von += 1
                        if kante.used == 0: n_besuchtekanten += 1
                        kante.used += 1
                        break
            # endregion
            break
    rückwege = graph.kürzester_weg_baum(0)
    for strecke in strecken:
        rw = rückwege.kürzester_weg_zu(strecke.knoten[-1]).copy()
        rw.reverse()
        strecke.add(rw)

    # region OUTPUT
    print("Ergebnis:")
    for tag in range(verfügbareTage):
        print("Tag", tag + 1, ":")
        print(strecken[tag])
        print()
    print("-Ende-")

    for kante in graph.kanten:
        s = False
        for auto in strecken:
            if kante in auto.kanten:
                s = True
                break
        if not s:
            print("Ergbnis FALSCH")
    # endregion
timer_stop()
