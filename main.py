bigINT = 0


class Weg:

    def __init__(self):
        self.weg = []

    def append(self, o):
        self.weg.append(o)

    def gewicht(self):
        if len(self.weg) == 0:
            return bigINT
        i = 0
        for w in self.weg:
            i += w.gewicht
        return i


class Kante:
    def __init__(self, start, stop, gewicht):
        self.start = start
        self.stop = stop
        self.gewicht = gewicht

    def __str__(self):
        return f"Kante(start: {self.start},stop: {self.stop},gewicht: {self.gewicht})"

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop and self.gewicht == other.gewicht

    def anderer_knoten(self, knoten):
        if knoten == self.stop:
            return self.start
        if knoten == self.start:
            return self.stop


class Knoten:

    def __init__(self, id, kanten):
        self.kanten = kanten
        self.id = id

    def __str__(self):
        kantenSTR = ""
        for kante in self.kanten:
            kantenSTR += str(kante) + "\n"
        return f"### Knoten {self.id}:\n" + \
               kantenSTR

    def __eq__(self, other):
        return self.id == other.id


class Graph:

    def __init__(self, knoten, kanten):
        self.knoten = knoten
        self.kanten = kanten

    def strecke_pro_tag(self):
        streckeprotag = self.entfernung_von_weitester_knoten(self.knoten[0])
        return streckeprotag

    def entfernung_von_weitester_knoten(self, knoten):
        entfernung = 0
        for knot in self.knoten:
            if knot != knoten:
                kürzesterweg = self.kürzester_weg(knoten, knot, Weg(), [], Weg())
                if entfernung < kürzesterweg.gewicht():
                    entfernung = kürzesterweg.gewicht()
        return entfernung

    def kürzester_weg(self, start_knoten, end_knoten, weg, geblockte_knoten, kürzesterweg):
        if start_knoten == end_knoten and weg.gewicht() < kürzesterweg.gewicht():
            kürzesterweg = weg[:]
        else:
            geblockte_knoten.append(start_knoten)
            for kante in start_knoten.kanten:
                if kante.anderer_knoten(start_knoten) not in geblockte_knoten \
                        and weg.gewicht() + kante.gewicht < kürzesterweg.gewicht():
                    weg.append(kante)
                    kürzesterweg = self.kürzester_weg(kante.stop, end_knoten, weg, geblockte_knoten, kürzesterweg)
                    weg.pop(-1)
            geblockte_knoten.pop(-1)
        return kürzesterweg

    def __str__(self):
        knotenSTR = ""
        for knoten in self.knoten:
            knotenSTR += str(knoten) + "\n"
        return f"Graph:\n{knotenSTR}"


def get_input():
    global bigINT
    pfad = "muellabfuhr0.txt"

    text = open(pfad, "r").read()
    zeilen = text.split("\n")

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
    t = Weg()
    t.weg = kanten
    bigINT = t.gewicht()

    return Graph(knoten, kanten)  # Rückgabe der Würfelliste


if __name__ == '__main__':
    fahrplan = get_input()
