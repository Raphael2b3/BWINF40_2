import time
import turtle

bigINT = 0
verfügbareTage = 5  # von montag bis freitag sind 5 tage

turtle.tracer(0)


def liste_in_listevonliste(liste, listevonliste):
    tmp = True
    for i in listevonliste:
        if len(i.weg) == len(liste):
            for j in range(len(i.weg)):
                if i.weg[j] != liste[j]:
                    tmp = False
            if tmp:
                return True
    return False


def abbruchbedingung(position, differenz_abs, differnz_record):
    return True


class Ergebnis:

    def __init__(self, weg, unschärfe, neueWege, zieldistanz):
        self.weg = weg
        self.unschärfe = unschärfe
        self.neueWege = neueWege
        self.zieldistanz = zieldistanz
        self.distanz = weg.gewicht

    def __str__(self):
        t = self.weg.__str__()
        t += f"\nUnschärfe {self.unschärfe}, neue Wege{self.neueWege}, Zieldistanz {self.zieldistanz}, distanz {self.distanz}"
        return t


class Weg:
    # Quasi wie eine Liste lauter kanten
    # start: int ID von Knoten
    def __init__(self, start):
        self.start: int = start
        self.weg = []
        self.gewicht = 0

    def append(self, o):
        self.weg.append(o)
        self.gewicht += o.gewicht

    def remove(self, object):
        self.weg.remove(object)
        self.gewicht -= object.gewicht

    def copy(self):
        t = Weg(self.start)
        t.weg = self.weg[:]
        t.gewicht = self.gewicht
        return t

    def __add__(self, other):
        t = Weg(self.start)
        a = self.weg[:] + other.weg[:]
        t.weg = a
        t.gewicht = self.gewicht + other.gewicht
        return t

    def __str__(self):
        t = f"Weg(\n"
        currentpos = self.start
        for w in self.weg:
            ziel = w.anderer_knoten(currentpos)
            t += f"Start: K{currentpos} -> K{ziel}({w.gewicht})\n"
            currentpos = ziel
        ziel = self.weg[0].anderer_knoten(currentpos)
        if ziel is None:
            for i in self.weg:
                pass  # print(i)
            # input("Stop")
        return t + ")"

    def ziel(self):  # TODO das geht effizienter
        currentpos: Knoten = self.start
        for w in self.weg:
            ziel = w.anderer_knoten(currentpos)
            currentpos = ziel
        return currentpos

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
        return f"Kante: K{self.start} -> K{self.stop}({self.gewicht})"

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

    def depriorize(self, list):
        t = []
        # good ones
        for i in self.kanten:
            if i not in list:
                t.append(i)
        # bad ones
        for i in self.kanten:
            if i in list:
                t.append(i)
        return t

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
        """t = self.strecke_pro_tag().gewicht * 2
        strecken = len(self.kanten) - 1
        min_t = strecken / 5
        print("Strecke zum weitesten knoten:", t)
        print("Strecken die es zu befahren gilt", strecken)
        print("pro tag müssen", min_t, "strecken abgefahren werden")"""  # Test 1

        t = self.fahrplan()

        return 1

    def min_strecke_pro_tag(self):
        mini = 0
        for k in self.kanten:
            mini += k.gewicht
        mini /= verfügbareTage
        return mini

    def weiteste_kante(self, knoten, kanten=None):  # knoten = Ausgangspunkt -> (weitester_knoten, weg, entfernung)
        if kanten is None: kanten = self.kanten
        weg = None
        k: Kante = None
        tweg = None
        tk = None
        for kant in kanten:
            kwA = self.kürzester_weg(knoten.id, kant.start, Weg(knoten.id), [], Weg(knoten.id))
            kwB = self.kürzester_weg(knoten.id, kant.stop, Weg(knoten.id), [], Weg(knoten.id))

            if kant in kwA.weg:
                tweg = kwA
            elif kant in kwB.weg:
                tweg = kwB
            else:
                kwA.append(kant)
                kwB.append(kant)
                if kwA.gewicht <= kwB.gewicht:
                    tweg = kwA
                else:
                    tweg = kwB
            if weg is None or weg.gewicht < tweg.gewicht:
                weg = tweg
                k = kant
        return weg, k

    def weitester_knoten(self, knoten):  # knoten = Ausgangspunkt -> (weitester_knoten, weg, entfernung)
        entfernung = 0
        weg = None
        for knot in self.knoten:
            if knot != knoten:
                kürzesterweg = self.kürzester_weg(knoten.id, knot.id, Weg(knoten.id), [], Weg(knoten.id))
                gewicht = kürzesterweg.gewicht
                if entfernung < gewicht:
                    entfernung = gewicht
                    weg = kürzesterweg
        return weg

    def kürzester_weg(self, start_knoten_id, end_knoten_id, weg, geblockte_knoten, kürzesterweg,
                      verwendete=None):
        if verwendete is None: verwendete = []
        start_knoten = self.knoten_by_id(start_knoten_id)  # instanziere StartKnoten ID
        # wenn ziel knoten erreich und weg.gewicht kleiner als von dem kürzesten weg
        if start_knoten_id == end_knoten_id and (weg.gewicht < kürzesterweg.gewicht or kürzesterweg.gewicht == 0):
            kürzesterweg = weg.copy()
        else:
            geblockte_knoten.append(start_knoten_id)  # kann nicht wieder zurückgehen
            for kante in start_knoten.depriorize(verwendete):  # zuerst die nichverwendeten Kanten
                # und dann die bereits verwendeten
                ziel_knoten_id = kante.anderer_knoten(start_knoten)
                if ziel_knoten_id not in geblockte_knoten \
                        and (weg.gewicht + kante.gewicht < kürzesterweg.gewicht or kürzesterweg.gewicht == 0):
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

    """
        def blub(self, start_knoten_id, weg, kürzesterweg, verwendete=None, zieldistanz=0, differenz=None):
            if verwendete is None: verwendete = []
    
            start_knoten = self.knoten_by_id(start_knoten_id)  # instanziere StartKnoten ID
            temp_dif = weg.gewicht - zieldistanz
    
            if start_knoten_id == 0 and 0 < temp_dif < differenz:
                kürzesterweg = weg.copy()
                differenz = temp_dif
            else:
                for kante in start_knoten.depriorize(verwendete):  # zuerst die nichverwendeten Kanten
                    # und dann die bereits verwendeten
    
                    ziel_knoten_id = kante.anderer_knoten(start_knoten)
                    zukunfts_gewicht = (weg.gewicht + kante.gewicht - zieldistanz)
                    if differenz is None or zukunfts_gewicht < differenz:
                        weg.append(kante)
                        verwendete.append(kante)
    
                        kürzesterweg, differenz = self.blub(ziel_knoten_id, weg, kürzesterweg, verwendete, zieldistanz,
                                                            differenz)
                        verwendete.remove(kante)
                        weg.remove(kante)
    
            return kürzesterweg, differenz
    """  # path finding 1.0

    def blubkopf(self, start_knoten_id, weg, out, difrecord, gegangene_wege, zieldistanz, verwendete,
                 gewonnene_strecke=0):
        start_knoten = self.knoten_by_id(start_knoten_id)  # instanziere StartKnoten ID

        abweichung_zieldastanz = gewonnene_strecke - zieldistanz if (gewonnene_strecke - zieldistanz) >= 0 else abs(
            gewonnene_strecke - zieldistanz) + 0.1
        # TODO  Das Problem:  Ich habe eine durchschnittsmenge an neuen straßen die ich protag überqueren muss. Jenäher
        #  ich an diese Menge rankomme umso wahrscheinlicher ist es dass ich nach 5 tagen bei jedem
        #  dieser suchen alle straßen durchgenommen habe.
        #  Das Funktioniert aber nicht immer. Ich vernachlässige so, Wege die viel nützen und wenige wege Doppelt nehmen.

        if start_knoten_id == 0 and abweichung_zieldastanz < difrecord and (
                weg.gewicht < out.gewicht or out.gewicht == 0):
            if not liste_in_listevonliste(weg.weg, gegangene_wege):
                out = weg.copy()
                difrecord = abweichung_zieldastanz
                # zieldistanz = weg.gewicht
        else:
            """print("Aktueller Knoten:", start_knoten)
            print("Seine kanten: ")
            for k in start_knoten.depriorize(verwendete):
                print(k)
    """
            for kante in start_knoten.depriorize(verwendete):  # zuerst die nichverwendeten Kanten
                # und dann die bereits verwendeten
                add = kante.gewicht if kante not in verwendete else 0
                ziel_knoten_id = kante.anderer_knoten(start_knoten)
                zukunfts_differenz = abs(weg.gewicht + add - zieldistanz)
                if zukunfts_differenz <= difrecord and (weg.gewicht <= out.gewicht or out.gewicht == 0):

                    # print(add)
                    gewonnene_strecke += add
                    weg.append(kante)
                    tmp = False
                    if kante not in verwendete:
                        tmp = True
                        verwendete.append(kante)

                    """print("Wir probieren", kante, "Wir hätten also", positivcount, "Punkte (Record:", precord, ")")
                    print("Ziel", zieldistanz, " Zurückgelegtestrecke", weg.gewicht)
                    #input()
            """
                    out, difrecord, gewonnene_strecke, zieldistanz = self.blubkopf(ziel_knoten_id, weg, out, difrecord,
                                                                                   gegangene_wege,
                                                                                   zieldistanz, verwendete,
                                                                                   gewonnene_strecke)
                    if tmp: verwendete.remove(kante)
                    weg.remove(kante)
                    gewonnene_strecke -= add

        return out, difrecord, gewonnene_strecke, zieldistanz

    def knoten_by_id(self, id) -> Knoten:
        for o in self.knoten:
            if o.id == id:
                return o

    def __str__(self):
        return "Graph"
        knotenSTR = ""
        for knoten in self.knoten:
            knotenSTR += str(knoten) + "\n"
        return f"Graph:\n{knotenSTR}"

    def fahrplan(self):
        zieldistanz = self.min_strecke_pro_tag()
        fahrplan = []
        besuchtewege = []
        besuchtekanten = []
        verfügbarekanten = self.kanten[:]
        centrale = self.knoten_by_id(0)
        weitestershit = int(self.weiteste_kante(centrale)[0].gewicht * 2) + 1

        ######################################
        for tag in range(14):
            if tag == 7:
                print("BIG PROBLEM")
                break
            if len(verfügbarekanten) == 0:
                print("Finished")
                for i in range(len(fahrplan)):
                    print("Tag", i + 1)
                    print(fahrplan[i])
                break

            print(besuchtekanten)
            weg, dif, goodnews, tmp_zieldistanz = self.blubkopf(centrale.id, Weg(0), Weg(0), zieldistanz, besuchtewege,
                                                                zieldistanz,
                                                                besuchtekanten)
            print("Tag ", tag + 1)
            print(weg)
            input()
            e = Ergebnis(weg, dif, goodnews, tmp_zieldistanz)
            for w in weg.weg:
                if w not in besuchtekanten:
                    besuchtekanten.append(w)
                else:
                    print("ayyy")
                if w in verfügbarekanten:
                    verfügbarekanten.remove(w)
            besuchtewege.append(weg)
            fahrplan.append(e)
            """weg, weitestekante = self.weiteste_kante(centrale, verfügbarekanten)
            for w in weg.weg:
                besuchtekanten.append(w)
                if w in verfügbarekanten:
                    verfügbarekanten.remove(w)
            position = weg.ziel()
            heimweg = self.kürzester_weg(position, centrale, Weg(position), [], Weg(position), besuchtekanten)
            for w in heimweg.weg:
                besuchtekanten.append(w)
                if w in verfügbarekanten:
                    verfügbarekanten.remove(w)
            fahrplan.append(weg + heimweg)
            print(weg + heimweg)"""  # nice try
        for i in range(len(fahrplan)):
            print("Tag", i + 1)
            print(fahrplan[i])
        print(zieldistanz)

        return fahrplan

    def draw_situation(self):
        return
        zeilen_länge = 4
        abstände = 100
        sx, sy = -100, -100  # start position
        positions = []
        pos = sx, sy
        positions.append(pos)
        self.knoten_by_id(0).draw_at(pos)

        for l in self.kanten:
            turtle.penup()
            x, y = positions[l.start]
            turtle.goto(x, y)
            turtle.pendown()
            x, y = positions[l.stop]
            turtle.goto(x, y)

        turtle.update()


def get_input():
    global bigINT
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
    bigINT = t.generate_gewicht()
    return Graph(knoten, kanten)  # Rückgabe der Würfelliste


if __name__ == '__main__':
    start = time.time()
    fahrplan = get_input()
    fahrplan.main()
    stop = time.time()

    delta = stop - start
    print("Time Required", delta)

    # t.mainloop()
