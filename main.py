import turtle

bigINT = 0
turtle.tracer(0)


class Weg:

    def __init__(self):
        self.weg = []
        self.gewicht = 0

    def append(self, o):
        self.weg.append(o)
        self.gewicht += o.gewicht

    def remove(self, object):
        self.weg.remove(object)
        self.gewicht = object.gewicht

    def copy(self):
        t = Weg()
        t.weg = self.weg[:]
        t.gewicht = self.gewicht
        return t

    def __str__(self):
        t = "Weg(\n"
        for i in self.weg:
            print(i)
            t += " -" + str(i) + "\n"
        return t

    def generate_gewicht(self):
        t = 0
        for i in self.weg:
            t += i.gewicht
        self.gewicht = t
        return t


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
        return self.id == other

    def draw_at(self, position):
        turtle.penup()
        turtle.goto(position[0], position[1])
        turtle.pendown()
        turtle.circle(20)
        turtle.write(self.id)


class Graph:

    def __init__(self, knoten, kanten):
        self.knoten = knoten
        self.kanten = kanten

    def main(self):
        t = self.strecke_pro_tag()
        print("strecke Pro Tag", t)
        self.draw_situation()
        return 1

    def strecke_pro_tag(self):
        streckeprotag = self.weitester_knoten(self.knoten[0])
        return streckeprotag

    def weitester_knoten(self, knoten):  # knoten = Ausgangspunkt -> (weitester_knoten, weg, entfernung)
        entfernung = 0
        weg = None
        weitester_knoten = None
        for knot in self.knoten:
            if knot != knoten:
                kürzesterweg = self.kürzester_weg(knoten.id, knot.id, Weg(), [], Weg())
                gewicht = kürzesterweg.gewicht
                if entfernung < gewicht:
                    entfernung = gewicht
                    weg = kürzesterweg
                    weitester_knoten = knoten
        return weitester_knoten, weg, entfernung

    def kürzester_weg(self, start_knoten_id, end_knoten_id, weg, geblockte_knoten, kürzesterweg):
        start_knoten = self.knoten_by_id(start_knoten_id)
        if start_knoten_id == end_knoten_id and weg.gewicht < (
                kürzesterweg.gewicht if kürzesterweg.gewicht > 0 else weg.gewicht + 1):
            kürzesterweg = weg.copy()
        else:
            geblockte_knoten.append(start_knoten_id)
            for kante in start_knoten.kanten:
                ziel_knoten_id = kante.anderer_knoten(start_knoten)
                if ziel_knoten_id not in geblockte_knoten \
                        and weg.gewicht + kante.gewicht < (
                        kürzesterweg.gewicht if kürzesterweg.gewicht > 0 else weg.gewicht + kante.gewicht + 1):
                    weg.append(kante)
                    for i in start_knoten.kanten:
                        if i.anderer_knoten(start_knoten) != ziel_knoten_id:
                            geblockte_knoten.append(i.anderer_knoten(start_knoten))
                    kürzesterweg = self.kürzester_weg(kante.anderer_knoten(start_knoten), end_knoten_id, weg,
                                                      geblockte_knoten, kürzesterweg)
                    for i in start_knoten.kanten:
                        if i.anderer_knoten(start_knoten) != ziel_knoten_id:
                            geblockte_knoten.remove(i.anderer_knoten(start_knoten))
                    weg.remove(kante)
            geblockte_knoten.remove(start_knoten_id)
        return kürzesterweg

    def knoten_by_id(self, id):
        for o in self.knoten:
            if o.id == id:
                return o

    def __str__(self):
        return "Graph"
        knotenSTR = ""
        for knoten in self.knoten:
            knotenSTR += str(knoten) + "\n"
        return f"Graph:\n{knotenSTR}"

    def draw_situation(self):
        zeilen_länge = 4
        abstände = 100
        sx, sy = (-100, -100)  # start position
        positions = []
        for i in range(len(self.knoten)):
            j = int(i / zeilen_länge)
            y = j
            x = i - zeilen_länge * j
            pos = (x * abstände + sx, y * abstände + sy)
            positions.append(pos)
            self.knoten[i].draw_at(pos)
        for l in self.kanten:
            turtle.penup()
            x, y = positions[l.start]
            turtle.goto(x,y)
            turtle.pendown()
            x, y = positions[l.stop]
            turtle.goto(x, y)

        turtle.update()


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
    bigINT = t.generate_gewicht()
    return Graph(knoten, kanten)  # Rückgabe der Würfelliste


if __name__ == '__main__':
    fahrplan = get_input()
    fahrplan.main()

    turtle.mainloop()
