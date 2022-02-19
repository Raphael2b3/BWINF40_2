import performance_analysing

perf = performance_analysing.time_analysing()

verfügbareTage = 5  # von montag bis freitag sind 5 tage


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

    def __init__(self, start_id, _graph):
        self.start = start_id
        self.graph: Graph = _graph
        self.knoten = []
        for knoten in _graph.knoten:
            self.knoten.append(SPD_knoten(knoten, start_id))

        self.find(self.knoten[0])

    def find(self, current_knoten):
        current_weg = current_knoten.weg  # referenz is the same, its like an rename
        current_knoten.finished = True
        current_knoten.distance = current_weg.gewicht

        for kante in current_knoten.knoten.kanten:
            ziel_id = kante.anderer_knoten(current_knoten.knoten.id)
            ziel_knoten = self.knoten[ziel_id]

            if not ziel_knoten.finished and current_knoten.distance + kante.gewicht < ziel_knoten.distance:
                ziel_knoten.weg = current_weg.copy()
                ziel_knoten.weg.append(kante)
                ziel_knoten.distance = ziel_knoten.weg.gewicht

        # noinspection PyTypeChecker
        nähster_knoten: SPD_knoten = None
        tmp = False
        for knoten in self.knoten:
            if (nähster_knoten is None or knoten.distance < nähster_knoten.distance) and not knoten.finished:
                nähster_knoten = knoten
                if not knoten.finished:
                    tmp = True

        if tmp: self.find(nähster_knoten)

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
        return currentPos

    def set(self, other):  # updated diese instanz sodass keine neue erstellt werden muss
        self.weg = other.weg[:]
        self.gewicht = other.gewicht


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

    def kürzester_weg_db(self, start):
        if start not in self.kürzeste_wege:
            self.kürzeste_wege[start] = Shortest_path_database(start, self)
        return self.kürzeste_wege[start]

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
    pfad = "muellabfuhr0.txt"

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


if __name__ == '__main__':
    graph = get_input()
    gesichtete_knoten = []
    besuchte_kanten = []
    autos = [Auto(i) for i in range(verfügbareTage)]  # erstelle 5 Auto Klassen
    print(len(graph.kanten))
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
        # region finde potenzielle knoten heraus (mit minimum an Fragezeichen)
        for _ in gesichtete_knoten:
            # TODO sortiere die Knoten nach den Regeln des Auswahlverfahrens einen neuen Knoten zu finden,
            #  wie in Paint beschrieben
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

    # region OUTPUT
    for tag in range(verfügbareTage):
        print("Tag", tag, ":")
        print(autos[tag].weg)
        print()
    # endregion

    # region tmp
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
