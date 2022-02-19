import performance_analysing
from builtins import print as _print
perf = performance_analysing.time_analysing()

verfügbareTage = 5  # von montag bis freitag sind 5 tage

#TODO PERFORMANCE VERBESSERN

def print(*args):
    return
    _print(*args)

def log(*args):
    _print(*args)

def timer_start():
    perf.set_time_point("Start")


def timer_stop():
    perf.set_time_point("Stop")
    input()


class SPD_knoten:

    def __init__(self, knoten, start):
        self.knoten = knoten
        self.weg: Weg = Weg(start)
        self.distance = float("inf")
        self.finished = False


class Shortest_path_database:

    def __init__(self, _start_id, _graph, _geblockte_kanten: list = None):
        if _geblockte_kanten is None:
            self.geblockte_kanten = []
        else:
            self.geblockte_kanten = _geblockte_kanten

        self.start = _start_id
        self.graph: Graph = _graph
        self.knoten = {}
        for _knoten in _graph.knoten:
            knot = SPD_knoten(_knoten, _start_id)
            self.knoten[knot.knoten.id] = knot

        self.find(self.knoten[_start_id])

    def find(self, current_knoten):
        current_weg = current_knoten.weg  # referenz is the same, its like an rename
        current_knoten.finished = True
        current_knoten.distance = current_weg.gewicht

        for _kante in current_knoten.knoten.kanten:
            if _kante in self.geblockte_kanten:
                continue
            ziel_id = _kante.anderer_knoten(current_knoten.knoten.id)
            ziel_knoten = self.knoten[ziel_id]

            if not ziel_knoten.finished and current_knoten.distance + _kante.gewicht < ziel_knoten.distance:
                ziel_knoten.weg = current_weg.copy()
                ziel_knoten.weg.append(_kante)
                ziel_knoten.distance = ziel_knoten.weg.gewicht

        nähster_knoten: SPD_knoten = None
        success = False
        for knoten in self.knoten.values():
            if (nähster_knoten is None or knoten.distance < nähster_knoten.distance) and not knoten.finished:
                nähster_knoten = knoten
                success = True

        if success: self.find(nähster_knoten)

    def kürzester_weg_zu(self, _id):
        weg = self.knoten[_id].weg
        return weg


class Weg:
    # Quasi wie eine Liste lauter kanten
    # start: int ID von Knoten
    def __init__(self, start):
        self.start: int = start
        self.weg = []
        self.gewicht = 0
        self.knoten = [start]

    def append(self, o):
        self.weg.append(o)
        self.gewicht += o.gewicht
        self.knoten.append(o.anderer_knoten(self.knoten[-1]))

    def remove(self, _objekt):
        self.weg.remove(_objekt)
        self.gewicht -= _objekt.gewicht
        self.knoten.pop(-1)

    def pop(self, i):
        self.gewicht -= self.weg[i].gewicht
        self.weg.pop(i)
        self.knoten.pop(-1)

    def copy(self):
        t = Weg(self.start)
        t.weg = self.weg[:]
        t.gewicht = self.gewicht
        t.knoten = self.knoten[:]
        return t

    def add(self, other):
        for i in other.weg:
            self.append(i)

    def __str__(self):
        t = f"Weg({self.start}->{self.ziel()}\n"
        currentpos = self.start
        for w in self.weg:
            ziel = w.anderer_knoten(currentpos)

            t += f"K{currentpos} -> K{ziel}({w.gewicht})\n"
            currentpos = ziel
            if currentpos is None:
                print("Errorcode: 69")

        return t + ")"

    def __eq__(self, other):
        return self.weg == other.weg

    def ziel(self):
        currentPos = self.start
        for kante in self.weg:
            currentPos = kante.anderer_knoten(currentPos)
        if currentPos != self.knoten[-1]:
            raise  # "DU HURENSOHN"
        return currentPos

    def set(self, other):  # updated diese instanz sodass keine neue erstellt werden muss
        self.weg = other.weg[:]
        self.gewicht = other.gewicht

    def reverse(self):
        self.start = self.ziel()
        self.weg = self.weg[::-1]
        self.knoten = self.knoten[::-1]


class Kante:
    def __init__(self, start, stop, gewicht):
        self.start = start
        self.stop = stop
        self.gewicht = gewicht

    def __str__(self):
        return f"Kante: K{self.start} -> K{self.stop}({self.gewicht})"

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop and self.gewicht == other.gewicht

    def anderer_knoten(self, knoten):
        if knoten == self.stop:
            return self.start
        if knoten == self.start:
            return self.stop


class Knoten:

    def __init__(self, _id, kanten):
        self.kanten = kanten
        self.ziel_von = []
        self.überquert_von = []
        self.id = _id
        self.relevant = True

    def __str__(self):
        kantenSTR = ""
        for kante in self.kanten:
            kantenSTR += str(kante) + "\n"
        return f"### Knoten {self.id}:\n" + \
               kantenSTR

    def __eq__(self, other):
        return self.id == other


class Graph:

    def __init__(self, knoten, kanten):
        self.knoten = knoten
        self.kanten = kanten
        self.kürzeste_wege = {}

    def kürzester_weg_db(self, start, blocked=None):
        if blocked is None or len(blocked) == 0:
            if start not in self.kürzeste_wege:
                self.kürzeste_wege[start] = Shortest_path_database(start, self)
            return self.kürzeste_wege[start]
        return Shortest_path_database(start, self, geblockte_kanten)

    def main(self):

        return 1

    def knoten_by_id(self, id) -> Knoten:
        for o in self.knoten:
            if o.id == id:
                return o

    def __str__(self):
        knotenSTR = ""
        for knoten in self.knoten:
            knotenSTR += str(knoten) + "\n"
        return f"Graph:\n{knotenSTR}"


def get_input():
    pfad = "muellabfuhr5.txt"

    text = open(pfad, "r").read()
    zeilen = text.split("\n")
    zeilen.pop(-1)
    kanten = []  # sammelt alle gegebenen Kanten
    for i in range(1, len(zeilen)):  # ab Zeile i:1 werden die Würfel definiert
        wertederzeile = zeilen[i].split(" ")
        start = int(wertederzeile[0])
        stop = int(wertederzeile[1])
        gewicht = int(wertederzeile[2])
        kanten.append(Kante(start, stop, gewicht))

    knoten = []
    zeile1_werte = zeilen[0].split(" ")
    for knotenID in range(int(zeile1_werte[0])):
        temp_kanten = []
        for kante in kanten:
            if kante.start == knotenID or kante.stop == knotenID:
                temp_kanten.append(kante)
        knoten.append(Knoten(knotenID, temp_kanten))
    t = Weg(0)
    t.weg = kanten
    return Graph(knoten, kanten)  # Rückgabe der Würfelliste


class Auto:

    def __init__(self, _id):
        self.id = _id
        self.position = 0
        self.weg = Weg(0)

    def __str__(self):
        return f"A{self.id}P{self.position}W{self.weg}"


if __name__ == '__main__':
    graph = get_input()
    gesichtete_knoten = []
    besuchte_kanten = []
    autos = [Auto(i) for i in range(verfügbareTage)]  # erstelle 5 Auto Klassen
    start_knoten = graph.knoten_by_id(0)
    start_knoten.überquert_von += [i for i in range(verfügbareTage)]
    print("Makiere Start mit allen '!'")
    while len(besuchte_kanten) < len(graph.kanten):
        log(len(besuchte_kanten), len(graph.kanten))
        """        for knoten_id in gesichtete_knoten:  # entfernt alle Fragezeichen da neue generiert werden
            knoten = graph.knoten_by_id(knoten_id)
            knoten.ziel_von.clear()  # frage zeichen gelöscht
            for auto in autos:
                if auto.position == knoten_id:
                    if auto.id not in knoten.überquert_von:
                        knoten.überquert_von.append(auto.id)
        removelist = []  # hier werden die elemente verlinkt die aus gesichtete knoten entfernt werden sollen
        for auto in autos:  # jedes auto makiert seine möglichen Zielknoten mit Fragezeichen...
            position = auto.position
            knoten = graph.knoten_by_id(position)
            for kante in knoten.kanten:
                ziel_id = kante.anderer_knoten(position)
                ziel_knoten = graph.knoten_by_id(ziel_id)
                if not ziel_knoten.relevant:
                    removelist.append(ziel_id)
                    continue
                if ziel_id not in gesichtete_knoten:
                    gesichtete_knoten.append(ziel_id)  # wenn der Knoten nun neu erreicht wurde wird dieser
                    # in die liste der bekannten knoten hinzugefügt
                ziel_knoten.ziel_von.append(auto.id)  # Makiert den Knoten
        for i in removelist:
            if i in gesichtete_knoten:
                gesichtete_knoten.remove(i)"""
        # region Markiere Knoten mit Fragezeichen + identifizieren neu gesichtete knoten + makiere ausrufezeichen
        removelist = []
        for knoten_id in gesichtete_knoten:  # entfernt alle Fragezeichen da neue generiert werden
            knoten = graph.knoten_by_id(knoten_id)
            knoten.ziel_von.clear()
            i = 0
            for kante in knoten.kanten:
                if kante in besuchte_kanten:
                    i += 1
            if i == len(knoten.kanten):
                knoten.relevant = False
                removelist.append(knoten_id)
        for o in removelist:
            gesichtete_knoten.remove(o)
        # region gehe bei fehlerhaften bewegungen zurück
        for i in range(len(autos)):

            while len(autos[i].weg.weg) > 0:
                letzte_kante = autos[i].weg.weg[-1]
                zielknoten = graph.knoten_by_id(autos[i].position)
                if zielknoten.relevant: break
                überschneidung = False
                for auto in autos[i+1:]:
                    if letzte_kante in auto.weg.weg:
                        überschneidung = True
                        break
                if not überschneidung: break
                autos[i].weg.remove(letzte_kante)
                autos[i].position = autos[i].weg.ziel()
                zielknoten.überquert_von.remove(autos[i].id)
        # endregion
        print("Alle Fragezeichen löschen")
        for auto in autos:
            if auto.position not in gesichtete_knoten:
                gesichtete_knoten.append(auto.position)
            knoten = graph.knoten_by_id(auto.position)
            for kante in knoten.kanten:
                ziel_id = kante.anderer_knoten(auto.position)

                ziel = graph.knoten_by_id(ziel_id)
                if not ziel.relevant: continue
                if ziel_id not in gesichtete_knoten:
                    gesichtete_knoten.append(ziel_id)
                ziel.ziel_von.append(auto.id)  # fragezeichen wird hinzu gefügt
        # endregion

        # region sortierung der gesichteten knoten zuerst die die Fragezeichen haben aber so wenige haben wie geht,
        # unter denen dann aufsteigend nach ausrufezeichen und zum schluss die die keine Fragezeichen haben.
        gk = gesichtete_knoten
        print("Sortiere gesichtete Knoten:", gesichtete_knoten)
        for _ in gesichtete_knoten:
            if len(gk) == 0: input("OH!????")

            for i in range(len(gk) - 1):
                knoten_id = gk[i]
                knotA = graph.knoten_by_id(knoten_id)
                knoten_id2 = gk[i + 1]
                knotB = graph.knoten_by_id(knoten_id2)
                a_hat_fragezeichen = len(knotA.ziel_von) > 0
                b_keine_fragezeichen = len(knotB.ziel_von) == 0
                a_weniger_fragezeichen = len(knotA.ziel_von) < len(knotB.ziel_von)

                a_gleichviele_fragezeichen = len(knotA.ziel_von) == len(knotB.ziel_von)

                a_nicht_mehr_ausrufezeichen = not len(knotA.überquert_von) > len(knotB.überquert_von)
                if a_hat_fragezeichen:
                    if b_keine_fragezeichen or a_weniger_fragezeichen or (
                            a_gleichviele_fragezeichen and a_nicht_mehr_ausrufezeichen):
                        continue  # nicht tauschen
                gk[i], gk[i + 1] = knoten_id2, knoten_id
        print("Ergebnis:", gesichtete_knoten)
        # endregion

        # region finde das nähste auto und sein weg zu dem knoten
        for knoten_id in gesichtete_knoten:
            print("Probiere Knoten:", knoten_id)
            knoten = graph.knoten_by_id(knoten_id)
            geblockte_kanten = []
            for kante in knoten.kanten:
                if kante in besuchte_kanten:
                    geblockte_kanten.append(kante)
            if len(geblockte_kanten) == len(knoten.kanten):
                knoten.relevant = False
                print("nächster versuch")
                continue
            wege = graph.kürzester_weg_db(knoten_id, geblockte_kanten)
            print("Wähle auto")
            bestes_auto = None
            strecketotal = float("inf")
            bester_weg = None
            for auto in autos:
                weg = wege.kürzester_weg_zu(auto.position).copy()
                tmp_strecketotal = weg.gewicht + auto.weg.gewicht
                if strecketotal > tmp_strecketotal and weg.gewicht != 0:
                    bestes_auto = auto
                    weg.reverse()
                    bester_weg = weg
                    strecketotal = tmp_strecketotal
            if bestes_auto is None: continue
            print("Gefunden:", bestes_auto)
            print("Zusätzlicher weg", bester_weg)
            for kante in bester_weg.weg:
                if kante not in besuchte_kanten:
                    besuchte_kanten.append(kante)
            for knoten_id in bester_weg.knoten[1:]:
                knoten = graph.knoten_by_id(knoten_id)
                knoten.überquert_von.append(bestes_auto.id)
                print("markiere", knoten_id, f"mit !{bestes_auto.id}")

            bestes_auto.weg.add(bester_weg)
            bestes_auto.position = knoten_id
            print("Bestes auto:", bestes_auto.id, "Weg", bestes_auto.weg)
            # region zusatz checks

            while len(besuchte_kanten) < len(
                    graph.kanten):  # knoten die nur 2 Kanten haben können weiter überfahren werden da es nur eine möglichkeit
                # fort zu fahren, Wenden ist depriorisisert
                if len(knoten.kanten) != 2: break
                for kante in knoten.kanten:
                    if kante not in bestes_auto.weg.weg:
                        print("Führe weg fort mit", kante)
                        bestes_auto.weg.append(kante)
                        bestes_auto.position = bestes_auto.weg.ziel()
                        knoten = graph.knoten_by_id(bestes_auto.position)
                        knoten.überquert_von.append(bestes_auto.id)
                        besuchte_kanten.append(kante)
                        print("markiere", knoten_id, f"mit !{bestes_auto.id}")
                        break


            # endregion

            break

    rückwege = graph.kürzester_weg_db(0)
    for auto in autos:
        rw = rückwege.kürzester_weg_zu(auto.position).copy()
        rw.reverse()
        auto.weg.add(rw)

    # region OUTPUT
    for tag in range(verfügbareTage):
        print("Tag", tag, ":")
        print(autos[tag].weg)
        print()
    # endregion

    # region tmp
    """print(len(graph.kanten))
    while len(besuchte_kanten) < len(graph.kanten):
        for tag in range(verfügbareTage):
            print("Tag", tag, ":")
            print(autos[tag].weg)
            print()

        print(len(besuchte_kanten))
        # region Markiere Knoten mit Fragezeichen + identifizieren neu gesichtete knoten
        for knoten_id in gesichtete_knoten:  # entfernt alle Fragezeichen da neue generiert werden
            knoten = graph.knoten_by_id(knoten_id)
            knoten.ziel_von.clear()

        for auto in autos:  # jedes auto makiert seine möglichen Zielknoten mit Fragezeichen...
            position = auto.position
            knoten = graph.knoten_by_id(position)
            for kante in knoten.kanten:
                ziel_id = kante.anderer_knoten(position)
                ziel_knoten = graph.knoten_by_id(ziel_id)
                if ziel_id not in gesichtete_knoten:
                    gesichtete_knoten.append(ziel_id)  # wenn der Knoten nun neu erreicht wurde wird dieser
                    # in die liste der bekannten knoten hinzugefügt
                ziel_knoten.ziel_von.append(auto.id)  # Makiert den Knoten
        print("Makierung abgeschlossen")
        for i in gesichtete_knoten:
            k = graph.knoten_by_id(i)
            print(f"Knoten{i} Fragezeichen", k.ziel_von)
        # endregion

        anzahl_record_zeichen = float("inf")
        anzahl_record_fragezeichen = float("inf")
        potenzielle_knoten = []
        # region sortiere gesichtete Knoten aufsteigend nach 1.insgesammte Zeichen 2. Fragezeichen
        for _ in gesichtete_knoten:
            for knoten_id in gesichtete_knoten:
                knoten = graph.knoten_by_id(knoten_id)
                anzahl_fragezeichen = len(knoten.ziel_von)
                anzahl_zeichen = len(knoten.überquert_von) + anzahl_fragezeichen

                if anzahl_zeichen < anzahl_record_zeichen:
                    anzahl_record_fragezeichen = float("inf")
                elif anzahl_zeichen > anzahl_record_zeichen:
                    continue

                if anzahl_record_fragezeichen < anzahl_fragezeichen or anzahl_fragezeichen == 0: continue  # ein knoten muss
                # min. ein Fragezeichen haben
                if anzahl_fragezeichen < anzahl_record_fragezeichen: potenzielle_knoten.clear()  # wenn neuer record dann werden
                # alle alten knoten entfernt
                potenzielle_knoten.append(knoten)
                anzahl_record_fragezeichen = anzahl_fragezeichen
                anzahl_record_zeichen = anzahl_zeichen

        # endregion
        print("Ausgewählter Knoten")

        nächster_knoten = None
        outer_record_distanz = 0
        outer_auto = None
        neuer_weg = None

        # region Knoten gesucht: es muss eine neue Kante überquert werden. diese Kante muss die größte streck haben.
        # Es Wird das Auto gewählt welches am wenigsten strecke haben wird
        for knoten in potenzielle_knoten:

            tmp_neuekanten = []

            # region finde die neuen kanten für diesen knoten
            for kante in knoten.kanten:
                if kante not in besuchte_kanten:
                    tmp_neuekanten.append(kante)
            # endregion

            if len(tmp_neuekanten) == 0: continue  # wenn dieser Knoten keine neue kanten besitzt, schließe Knoten aus

            neuekanten_überqu_autos = []  # [(auto, kante)]

            # region finde autos die neuekanten überquären
            for auto_id in knoten.ziel_von:
                auto = autos[auto_id]
                position = auto.position
                a_knoten = graph.knoten_by_id(position)
                for a_kante in a_knoten.kanten:  # die möglichkeiten die ein auto hat zu fahren
                    if a_kante.start == position and a_kante.stop == knoten.id or \
                            a_kante.stop == position and a_kante.start == knoten.id:
                        if a_kante in tmp_neuekanten:
                            neuekanten_überqu_autos.append((auto, a_kante))
            # endregion

            if len(neuekanten_überqu_autos) == 0: continue  # mach weiter wenn es autos gibt die neuekante überquert

            out_auto = None
            record_distanz = float("inf")
            out_kante = None
            # region finde auto welches am wenigsten strecke sammelt wenn es den aktuellen knoten erreicht
            for auto_kante in neuekanten_überqu_autos:
                auto, kante = auto_kante
                distanz = auto.weg.gewicht + kante.gewicht
                if distanz < record_distanz:
                    out_auto = auto
                    record_distanz = distanz
                    out_kante = kante
            # endregion

            if record_distanz > outer_record_distanz:  # wenn das auto mit dem geringsten weg mehr strecke braucht
                # als das bei den aktuellen
                outer_record_distanz = record_distanz
                nächster_knoten = knoten
                outer_auto = out_auto
                neuer_weg = out_kante
        # endregion

        if nächster_knoten is None:
            # region erstes Error handling
            betrachteter_knoten2 = None
            distanz2 = float("inf")
            auto2 = None
            weg2 = None
            for knoten_id in gesichtete_knoten:

                tmp_neuekanten = []
                knoten = graph.knoten_by_id(knoten_id)
                # region finde die neuen kanten für diesen knoten
                for kante in knoten.kanten:
                    if kante not in besuchte_kanten:
                        tmp_neuekanten.append(kante)
                # endregion

                if len(
                        tmp_neuekanten) == 0: continue  # wenn dieser Knoten keine neue kanten besitzt, schließe Knoten aus

                kürzesterweg_db: Shortest_path_database = graph.kürzester_weg_db(knoten.id)
                geeignetstes_auto = None
                g_distanz = float("inf")
                g_weg = None
                # region finde autos am wenigsten strecke hintersich gehabt haben werden wenn sie diesen Knoten erreichen.
                for auto in autos:
                    position = auto.position
                    weg = kürzesterweg_db.kürzester_weg_zu(position)
                    tmp_distanz = weg.gewicht + auto.weg.gewicht
                    if tmp_distanz < g_distanz:
                        geeignetstes_auto = auto
                        g_distanz = tmp_distanz
                        g_weg = weg
                # endregion

                if g_distanz < distanz2:
                    distanz2 = g_distanz
                    betrachteter_knoten2 = knoten
                    weg2 = g_weg
                    auto2 = geeignetstes_auto
            auto2.weg.add(weg2)
            # endregion
        else:
            # region wähle das fragezeichen aus
            besuchte_kanten.append(neuer_weg)
            outer_auto.weg.append(neuer_weg)
            outer_auto.position = nächster_knoten.id
            # endregion
"""
    """
        # region Knoten gesucht: es muss eine neue Kante überquert werden. diese Kante muss die größte streck haben.
        # Es Wird das Auto gewählt welches am wenigsten strecke haben wird
        for knoten in potenzielle_knoten:

            tmp_neuekanten = []

            # region finde die neuen kanten für diesen knoten
            for kante in knoten.kanten:
                if kante not in besuchte_kanten:
                    tmp_neuekanten.append(kante)
            # endregion

            if len(tmp_neuekanten) == 0: continue  # wenn dieser Knoten keine neue kanten besitzt, schließe Knoten aus

            neuekanten_überqu_autos = []  # [(auto, kante)]

            # region finde autos die neuekanten überquären
            for auto_id in knoten.ziel_von:
                auto = autos[auto_id]
                position = auto.position
                a_knoten = graph.knoten_by_id(position)
                for a_kante in a_knoten.kanten:  # die möglichkeiten die ein auto hat zu fahren
                    if a_kante.start == position and a_kante.stop == knoten.id or \
                            a_kante.stop == position and a_kante.start == knoten.id:
                        if a_kante in tmp_neuekanten:
                            neuekanten_überqu_autos.append((auto, a_kante))
            # endregion

            if len(neuekanten_überqu_autos) == 0: continue  # mach weiter wenn es autos gibt die neuekante überquert

            out_auto = None
            record_distanz = float("inf")
            out_kante = None
            # region finde auto welches am wenigsten strecke sammelt wenn es den aktuellen knoten erreicht
            for auto_kante in neuekanten_überqu_autos:
                auto, kante = auto_kante
                distanz = auto.weg.gewicht + kante.gewicht
                if distanz < record_distanz:
                    out_auto = auto
                    record_distanz = distanz
                    out_kante = kante
            # endregion

            if record_distanz > outer_record_distanz:
                outer_record_distanz = record_distanz
                nächster_knoten = knoten
                outer_auto = out_auto
                neuer_weg = out_kante
        # endregion
"""
    # endregion
