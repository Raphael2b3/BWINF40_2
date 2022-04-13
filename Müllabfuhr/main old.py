

class ShortestPathDatabase:

    # Mit dem Deikstraalgorithmus wird für einen Graphen und einem Startpunkt alle Kürzesten wege berechnet

    def __init__(self, _start_id, graph, geblockte_kanten):
        n_knoten = len(graph.knoten)
        self.start = _start_id
        self.INFWEG = Weg("inf")

        wege = [None for _ in range(n_knoten)]
        wege[_start_id] = Weg(_start_id)
        distanzen = [float("inf") for _ in range(n_knoten)]
        fertige = [False for _ in range(n_knoten)]
        knoten = graph.knoten

        # region Daijkstra Algorithm iterative
        betrachteter_knoten_id = _start_id
        while False in fertige:
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
                ziel_weg.append(_kante)
                distanzen[ziel_id] = ziel_weg.gewicht
                wege[ziel_id] = ziel_weg

            for i in range(n_knoten):
                if fertige[i]: continue
                if fertige[betrachteter_knoten_id]:
                    betrachteter_knoten_id = i
                    continue
                if distanzen[betrachteter_knoten_id] <= distanzen[i]: continue
                betrachteter_knoten_id = i
            if distanzen[betrachteter_knoten_id] == float("inf"): break

        # endregion
        self.wege = wege
        self.fertige = fertige

    def shortest_path(self, _id):
        return self.wege[_id] if self.fertige[_id] else self.INFWEG
        # wenn weg nicht existiert ist der Weg unendlich lang


class Weg:
    # Quasi wie eine Liste lauter kanten
    # start: int ID von Knoten

    def __init__(self, start):
        if start == "inf":
            self.gewicht = float("inf")
            return
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
            t += f"->K{ziel}"
            currentpos = ziel
        return t


class Kante:
    def __init__(self, start, stop, gewicht, _id):
        self.id = _id
        self.start = start
        self.stop = stop
        self.gewicht = gewicht
        self.used = 0

    def __eq__(self, other):
        return self.id == other

    def anderer_knoten(self, knoten):
        return self.start if knoten == self.stop else self.stop



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

    def __str__(self):
        return f"Knoten: {self.id}"


class Graph:

    def __init__(self, _knoten, _kanten):
        self.knoten = _knoten
        self.kanten = _kanten
        self.kürzeste_wege: dict[int, ShortestPathDatabase] = {}

    def kürzester_weg_baum(self, start, blocked=None) -> ShortestPathDatabase:
        if blocked is not None and len(blocked) > 0:
            return ShortestPathDatabase(start, self, blocked)
        if start in self.kürzeste_wege:
            return self.kürzeste_wege[start]
        _wege = self.kürzeste_wege[start] = ShortestPathDatabase(start, self, [])
        return _wege


def get_input():
    pfad = "muellabfuhr8.txt"
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
    return Graph(knoten, kanten)


if __name__ == '__main__':
    verfügbareTage = 5  # von montag bis freitag sind 5 tage
    start_position = 0
    graph = get_input()

    n_besuchtekanten = 0
    n_kanten = len(graph.kanten)

    gesichtete_knoten = []
    besuchte_kanten = []
    removelist = []
    neuestrecke: list[Knoten] = []

    strecken = [Weg(start_position) for i in range(verfügbareTage)]  # erstelle 5 Auto Klassen

    start_knoten = graph.knoten[start_position]
    start_knoten.überquert_von = verfügbareTage

    bar_length = 20
    barhelper = 0

    while n_besuchtekanten < n_kanten:
        # region Prozessbar
        fortschritt = round(n_besuchtekanten * 100 / n_kanten, 2)
        print("\r", f"{fortschritt}%",
              "#" * int(fortschritt * bar_length / 100) + "." * int(bar_length - (fortschritt * bar_length / 100)),
              end="")
        if fortschritt > barhelper * 5: barhelper += 1
        # endregion

        # region Situation Analysieren
        # region Fragezeichen erstmal entfernen
        removelist.clear()
        for knoten in gesichtete_knoten:  # entfernt alle Fragezeichen da neue generiert werden
            knoten.ziel_von = 0  # frage zeichen entfernen
            if not knoten.relevant():  # knoten ist irrelevant
                removelist.append(knoten)
        for o in removelist: gesichtete_knoten.remove(o)
        # endregion

        for strecke in strecken:
            # region gehe bei fehlerhaften bewegungen zurück

            knoten = graph.knoten[strecke.knoten[-1]]
            while len(strecke.kanten) > 0:  # grenze
                knoten = graph.knoten[strecke.knoten[-1]]  # NEW !!!!!!!!! <==========================================
                letzte_kante = strecke.kanten[-1]
                if letzte_kante.used == 1: #or knoten.relevant():  # NEW !!!!!!!!! <====================================
                    break
                strecke.remove(letzte_kante)
                letzte_kante.used -= 1
                knoten.überquert_von -= 1
            # endregion

            # region makiere Fragezeichen
            knoten = graph.knoten[
                strecke.knoten[-1]]  # muss neu deklariert werden da eventuell der letzte knoten sich verändert hat
            if knoten not in gesichtete_knoten and knoten.relevant(): gesichtete_knoten.append(knoten)
            for kante in knoten.kanten:
                ziel_id = kante.anderer_knoten(strecke.knoten[-1])
                ziel = graph.knoten[ziel_id]
                if not ziel.relevant(): continue
                if ziel not in gesichtete_knoten:
                    gesichtete_knoten.append(ziel)
                ziel.ziel_von += 1  # fragezeichen wird hinzu gefügt
            # endregion

        # region checke auch übergangene Knoten
        for knoten in neuestrecke:
            for kante in knoten.kanten:
                ziel_id = kante.anderer_knoten(knoten.id)
                ziel = graph.knoten[ziel_id]
                if not ziel.relevant(): continue
                if ziel not in gesichtete_knoten:
                    gesichtete_knoten.append(ziel)
                # fragezeichen wird hinzu gefügt

        # endregion

        # endregion

        # region sortierung der gesichteten knoten zuerst die die Fragezeichen haben aber so wenige haben wie geht,
        # unter denen dann aufsteigend nach ausrufezeichen und zum schluss die die keine Fragezeichen haben.
        swap = True
        while swap:
            swap = False
            for i in range(len(gesichtete_knoten) - 1):
                knotA: Knoten = gesichtete_knoten[i]
                knotB: Knoten = gesichtete_knoten[i + 1]

                if (knotA.ziel_von == knotB.ziel_von and (knotA.überquert_von < knotB.überquert_von or (
                        knotA.überquert_von == knotB.überquert_von and len(knotA.kanten) <= len(
                    knotB.kanten)))) or (
                        0 < knotA.ziel_von and (knotA.ziel_von < knotB.ziel_von or knotB.ziel_von == 0)): continue
                gesichtete_knoten[i], gesichtete_knoten[i + 1] = knotB, knotA
                swap = True
        # endregion

        # region finde das auto mit der geringsten totalen distanz und sein weg zu dem knoten

        for knoten in gesichtete_knoten:  # da gesichtete_knoten grade sortiert wurde werden jetzt effizient
            # die knoten überprüft
            geblockte_kanten = []
            for kante in knoten.kanten:
                if kante.used != 0:
                    geblockte_kanten.append(kante)

            if len(geblockte_kanten) == len(knoten.kanten): continue  # wenn von einem Knoten alle Kanten verwendet
            # wurden wird dieser ignoriert

            wege = graph.kürzester_weg_baum(knoten.id, geblockte_kanten)
            # region findet das auto welches am wenigsten strecke zum knoten benötigt
            beste_strecke = None
            strecketotal = float("inf")
            bester_weg = None

            for strecke in strecken:
                weg = wege.shortest_path(strecke.knoten[-1])
                tmp_strecketotal = weg.gewicht + strecke.gewicht
                if strecketotal < tmp_strecketotal or weg.gewicht == 0: continue
                if strecketotal == tmp_strecketotal and weg.gewicht >= bester_weg.gewicht: continue # NEU!!! ===============
                weg = weg.copy()
                beste_strecke = strecke
                weg.reverse()
                bester_weg = weg
                strecketotal = tmp_strecketotal
            # endregion

            if beste_strecke is None: continue  # wenn kein Auto gefunden wurde wird der nächste Knoten ausprobiert

            # region kanten und knoten werden als bekannt makiert
            for kante in bester_weg.kanten:

                if kante.used == 0:
                    n_besuchtekanten += 1
                kante.used += 1

            neuestrecke.clear()
            for _knoten_id in bester_weg.knoten[1:]:
                knoten = graph.knoten[_knoten_id]
                neuestrecke.append(knoten)
                knoten.überquert_von += 1

            beste_strecke.add(bester_weg)
            # endregion

            # region Knoten die nur zwei kanten haben werden identifiziert
            """
            Knoten die nur 2 Kanten haben können weiter überfahren werden da es nur eine Möglichkeit gibt 
            fort zu fahren, und zwar auf die nächste kante.
            """
            while n_besuchtekanten < n_kanten:

                if len(knoten.kanten) != 2: break
                for kante in knoten.kanten:
                    if kante not in beste_strecke.kanten:
                        beste_strecke.append(kante)
                        knoten = graph.knoten[beste_strecke.knoten[-1]]
                        neuestrecke.append(knoten)
                        knoten.überquert_von += 1
                        if kante.used == 0: n_besuchtekanten += 1
                        kante.used += 1
                        break
            # endregion

            break
        # endregion

    # region Rückwege generieren
    rückwege = graph.kürzester_weg_baum(0)
    for strecke in strecken:
        rw = rückwege.shortest_path(strecke.knoten[-1]).copy()
        rw.reverse()
        strecke.add(rw)
    # endregion

    # region Ausgabe des Ergebnissen

    print("\n\nErgebnis:")
    for tag in range(verfügbareTage):
        print("Tag", tag + 1, ":")
        print(strecken[tag])
        print()
    print("-Ende-")

    # endregion
