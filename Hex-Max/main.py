import performance_analysing

# region performance
perf = performance_analysing.time_analysing()


def timer_start():
    perf.set_time_point("Start")
    print()


def timer_stop():
    print()
    perf.set_time_point("Stop")


# endregion

class Ziffer:
    """
        Eine Ziffer hat 7 positionen mit die mit stichen belegt werden können
          _0_
        3|_1_|4
        5|_2_|6

         _
        |_  = F =^ [1,1,0,1,0,1,0] // 1 = True; 0 = False
        |

        wir erstellen Listen die die Hexadezimalzahlen abbilden können.
        """
    models = {
        '0': [True, False, True, True, True, True, True],
        '1': [False, False, False, False, True, False, True],
        '2': [True, True, True, False, True, True, False],
        '3': [True, True, True, False, True, False, True],
        '4': [False, True, False, True, True, False, True],
        '5': [True, True, True, True, False, False, True],
        '6': [True, True, True, True, False, True, True],
        '7': [True, False, False, False, True, False, True],
        '8': [True, True, True, True, True, True, True],
        '9': [True, True, True, True, True, False, True],
        'A': [True, True, False, True, True, True, True],
        'B': [False, True, True, True, False, True, True],
        'C': [True, False, True, True, False, True, False],
        'D': [False, True, True, False, True, True, True],
        'E': [True, True, True, True, False, True, False],
        'F': [True, True, False, True, False, True, False]
    }

    def __init__(self, char, _id):
        self.id = _id
        self.positions = Ziffer.models[char][:]  # kopiere die Instanz sodass keine Referenz mehr entsteht
        self.probieren_index = 0
        self.bekommt_von = []
        self.useless_indeces = []
        self.char = char
        self.ursprungschar = char

    def aktionen_zum_ziel(self, ziel_char):
        """
        Gibt informationen wie viele Sticks falsch an ihren Platz sind und unterteilt das in
        Falsch weil stick Fehlt und Falsch weil Stick nicht da sein dürfte
        :param ziel_char:
        :return: wegnehmen, hinzufügen (für übergebenen char)
        """
        self.char = ziel_char  # setzt den char wert zum ziel
        model = Ziffer.models[ziel_char]
        wegnehmen = 0
        hinzulegen = 0
        self.useless_indeces.clear()
        for i in range(7):
            if not model[i] == self.positions[i]:
                if model[i]:
                    hinzulegen += 1
                else:
                    wegnehmen += 1
                    self.useless_indeces.append(i)  # sticks müssen von Pos weggenommen werden
        return wegnehmen, hinzulegen

    def aktionen_log_zum_ziel(self):
        model = Ziffer.models[self.char]
        wegnehmen = 0
        hinzulegen = 0
        leerepositionen = []

        for i in range(7):
            if not model[i] == self.positions[i]:
                if model[i]:
                    hinzulegen += 1
                    leerepositionen.append(i)
                else:
                    wegnehmen += 1

        t_logs = []
        sources = [self.id for _ in range(wegnehmen)] + self.bekommt_von

        for p in leerepositionen:
            gebenden_ziffer_id = sources.pop(-1)
            log = self.id, p, gebenden_ziffer_id, ziffern[gebenden_ziffer_id].useless_indeces.pop(-1)
            t_logs.append(log)
        return t_logs

    def __str__(self):
        return self.char


def get_input():
    pfad = "hexmax1.txt"
    text = open(pfad, "r").read()
    zeilen = text.split("\n")
    zeilen.pop(-1)

    ziffern = []  # sammelt alle Ziffern
    print(zeilen[0])
    i = 0
    for char in zeilen[0]:
        ziffern.append(Ziffer(char, i))
        i += 1
    aktionen = int(zeilen[1])
    print("Aktionen", aktionen)
    return ziffern, aktionen


def print_ziffern(list_ziffern):  # printet die momentane Anordnung der Sticks
    zeile_1 = ""
    zeile_2 = ""
    zeile_3 = ""

    for ziffer in list_ziffern:
        zeile_1 += f" {'_' if ziffer.positions[0] else ' '}  "
        zeile_2 += f"{'|' if ziffer.positions[3] else ' '}{'_' if ziffer.positions[1] else ' '}{'|' if ziffer.positions[4] else ' '} "
        zeile_3 += f"{'|' if ziffer.positions[5] else ' '}{'_' if ziffer.positions[2] else ' '}{'|' if ziffer.positions[6] else ' '} "

    print("____")
    print(zeile_1)
    print(zeile_2)
    print(zeile_3)
    print()


def maximiere_ziffern(aktuelle_ziffer_index=0):
    global versuchsliste, aktionen_übrig, offers, requests, ziffern
    if aktuelle_ziffer_index == len(ziffern) or aktionen_übrig == 0:
        return 0 == len(offers) == len(requests)
    else:
        aktuelle_ziffer = ziffern[aktuelle_ziffer_index]  # betrachtete aktuelle Ziffer

        for char in versuchsliste:  # iteriert durch alle Hex-Zahlen durch

            aktionen, removes, appends = aktionen_bezogen_auf_situation(char, aktuelle_ziffer_index, aktuelle_ziffer)

            aktionen_übrig -= aktionen
            if aktionen_übrig >= 0:
                # wenn die jetzige ziffer funktionieren kann
                if maximiere_ziffern(aktuelle_ziffer_index + 1): return True
                # nun wird überprüft ob ein ausgleich noch möglich ist der übrigen stäbchen möglich ist
                if ausgleich_der_stäbchen(aktuelle_ziffer_index + 1): return True
                # wenn der danach nicht geklappt hat wird versucht die momentane Stellung irgendwie möglich zu machen

            # aktionen Rückgängig machen
            aktionen_übrig += aktionen
            for a, b in removes: a.remove(b)
            for a, b in appends: a.append(b)
        aktuelle_ziffer.char = aktuelle_ziffer.ursprungschar
    return False
    # FFFEA97B55


def aktionen_bezogen_auf_situation(char, aktuelle_ziffer_index, aktuelle_ziffer):

    """
    Findet heraus wie viele aktionen wirklich getan werden müssen und berücksichtigt dabei schon beiseite gelegte sticks
    :param wegnehmen:
    :param hinzufügen:
    :param aktuelle_ziffer_index:
    :param aktuelle_ziffer:
    :return: aktionen, removes, appends
    """
    wegnehmen, hinzufügen = aktuelle_ziffer.aktionen_zum_ziel(char)

    removes = []  # log = [(list, objekt)] later remove objekt from list
    appends = []  # log2 = [(list, objekt)] later append objekt to list

    aktionen = min((wegnehmen, hinzufügen))  # es müssen mindetens die unter einander zu tauschenden sticks
    # Aktioniert werden
    g = wegnehmen - hinzufügen
    for _ in range(abs(g)):
        if g < 0:  # es wird aus offers genommen
            if len(offers) > 0:
                o = offers.pop(-1)
                aktuelle_ziffer.bekommt_von.append(o)
                appends.append((offers, o))  # 0.append(1)
                removes.append((aktuelle_ziffer.bekommt_von, o))  # 0.remove(1)
            else:
                requests.append(aktuelle_ziffer_index)
                removes.append((requests, aktuelle_ziffer_index))  # 0.remove(1)
                aktionen += 1
        elif g > 0:  # es wird aus requests genommen
            if len(requests) > 0:
                o = requests.pop(-1)
                ziffern[o].bekommt_von.append(o)
                appends.append((requests, o))  # 0.append(1)
                removes.append((ziffern[o].bekommt_von, o))  # 0.remove(1)
            else:
                offers.append(aktuelle_ziffer_index)
                removes.append((offers, aktuelle_ziffer_index))  # 0.remove(1)
                aktionen += 1
    return aktionen, removes, appends


def maximiere_ziffern_iter(versuchsliste, aktionen_übrig, offers, requests, ziffern):
    aktuelle_ziffer_index = 0
    char_i = [0 for _ in range(len(ziffern))]
    logs: list[tuple[int, list, list]] = [None for _ in range(len(ziffern))]
    aktiv = [False for _ in range(len(ziffern))]

    while True:
        if aktuelle_ziffer_index == len(ziffern):
            if 0 == len(offers) == len(requests): break
            aktuelle_ziffer_index -= 1

        aktuelle_ziffer = ziffern[aktuelle_ziffer_index]  # betrachtete aktuelle Ziffer
        if not aktiv[aktuelle_ziffer_index]:
            if aktionen_übrig == 0:
                if 0 == len(offers) == len(requests): break
                aktuelle_ziffer_index -= 1
                continue

            ci = char_i[aktuelle_ziffer_index]
            # brauchste eig net
            if ci == len(versuchsliste):
                # input("Dein onkel numst")
                char_i[aktuelle_ziffer_index] = 0
                aktiv[aktuelle_ziffer_index] = False
                aktuelle_ziffer_index -= 1
                continue
            char = versuchsliste[ci]  # iteriert durch alle Hex-Zahlen durch

            aktionen, removes, appends = aktionen_bezogen_auf_situation(char, aktuelle_ziffer_index,
                                                                        aktuelle_ziffer)
            aktionen_übrig -= aktionen
            aktiv[aktuelle_ziffer_index] = True
            logs[aktuelle_ziffer_index] = (aktionen, removes, appends)
            if aktionen_übrig >= 0:
                aktuelle_ziffer_index += 1
        else:
            # nun wird überprüft, ob ein Ausgleich noch möglich ist der übrigen stäbchen möglich ist
            ausgleich_möglich = ausgleich_der_stäbchen_iter(aktuelle_ziffer_index + 1, aktionen_übrig, ziffern)
            if ausgleich_möglich: break
            # wenn der danach nicht geklappt hat wird versucht die momentane Stellung irgendwie möglich zu machen

            aktionen, removes, appends = logs[aktuelle_ziffer_index]

            # aktionen Rückgängig machen
            aktionen_übrig += aktionen
            for a, b in removes: a.remove(b)
            for a, b in appends: a.append(b)
            aktiv[aktuelle_ziffer_index] = False
            char_i[aktuelle_ziffer_index] += 1

    return True


def ausgleich_der_stäbchen(index, aktionen_übrig, ziffern):
    """
    Diese Funktion verteilt beiseite gelegte Sticks auf die restlichen
    Ziffernsysteme so das dabei auch noch eine maximale Hexadezimalzahl entsteht
    :param index: index der letzten festgelegten ziffer
    :return: Erfolg (bool)
    """
    zielausgleich = len(offers) + len(requests)
    if zielausgleich == 0: return True  # Erfolg, wenn nichts mehr auszugleichen ist
    if index == len(ziffern): return False  # Rekursive -> goes back to the last point
    aktuelleziffer = ziffern[index]
    for char in versuchsliste:
        aktionen, re, ap = aktionen_bezogen_auf_situation(char, index, aktuelleziffer)

        aktionen_übrig -= aktionen

        if aktionen_übrig >= 0:
            if ausgleich_der_stäbchen(index + 1, aktionen_übrig, ziffern): return True
        aktionen_übrig += aktionen

        for l, o in ap: l.append(o)
        for l, o in re: l.remove(o)
        # aktuelleziffer.char = ursprungschar

    return False


def ausgleich_der_stäbchen_iter(index, aktionen_übrig, ziffern):
    """
    Diese Funktion verteilt beiseite gelegte Sticks auf die restlichen
    Ziffernsysteme so das dabei auch noch eine maximale Hexadezimalzahl entsteht
    :param index: index der letzten festgelegten ziffer
    :return: Erfolg (bool)
    """
    char_i = [0 for _ in range(len(ziffern))]
    logs: list[tuple[int, list, list]] = [None for _ in range(len(ziffern))]
    aktiv = [False for _ in range(len(ziffern))]
    start_index=index
    while start_index <= index:
        zielausgleich = len(offers) + len(requests)
        if zielausgleich == 0: return True
        if index == len(ziffern): index -= 1

        aktuelle_ziffer = ziffern[index]  # betrachtete aktuelle Ziffer
        if not aktiv[index]:

            ci = char_i[index]
            if ci == len(versuchsliste):
                char_i[index] = 0
                aktiv[index] = False
                index -= 1
                continue
            char = versuchsliste[ci]  # iteriert durch alle Hex-Zahlen durch
            aktionen, removes, appends = aktionen_bezogen_auf_situation(char, index,
                                                                        aktuelle_ziffer)
            aktionen_übrig -= aktionen
            aktiv[index] = True
            logs[index] = (aktionen, removes, appends)
            if aktionen_übrig >= 0:
                index += 1
        else:
            # wenn der danach nicht geklappt hat wird versucht die momentane Stellung irgendwie möglich zu machen
            aktionen, removes, appends = logs[index]

            # aktionen Rückgängig machen
            aktionen_übrig += aktionen
            for a, b in removes: a.remove(b)
            for a, b in appends: a.append(b)
            aktiv[index] = False
            char_i[index] += 1
    return False


def ausgabe():
    print("Ergebnis:\nEnd-Hexadezimalzahl")
    for ziff in ziffern:
        print(ziff.char, end="")
    print("\nAusgangssituation:")
    print_ziffern(ziffern)
    a = 1
    for az in ziffern:
        logs = az.aktionen_log_zum_ziel()

        for log in logs:
            """
            az_id: Id der stick-annehmenden Ziffer
            az_sp: Stickposition im Ziffernsystem der stick-annehmenden Ziffer
            gz_id: Id der stick-abgebenden Ziffer
            gz_sp: Stickposition im Ziffernsystem der stick-abgebenden Ziffer
            """
            az_id, az_sp, gz_id, gz_sp = log
            # tauscht sticks zwischen den beiden
            ziffern[az_id].positions[az_sp], ziffern[gz_id].positions[gz_sp] = ziffern[gz_id].positions[gz_sp], \
                                                                               ziffern[az_id].positions[az_sp]
            print_ziffern(ziffern)
            print("Das war Aktion", a)
            a += 1


timer_start()

if __name__ == '__main__':
    """
    Definitionen: 
    - Ziffer: Eine Instanz der Klasse Ziffer, enthält Informationen über ob die "Sticks" an einer Position sind
    - Ziffersystem: Meint die möglichen Postionen in einer Ziffer
    
    FFFC438B55
    FFFC997B95
     _   _   _   _   _   _   _       _   _  
    |_  |_  |_  |   |_| |_|   | |_  |_| |_  
    |   |   |   |_   _|  _|   | |_|  _|  _| 
    """
    ziffern, aktionen_übrig = get_input()  # input aus Text-Datei
    offers = []  # liste von ziffer_ids dessen ziffer striche zur verfügen stellen
    requests = []  # liste von ziffer_ids dessen ziffer striche Anfragen
    versuchsliste = "FEDCBA987654321"  # Hex-Zahlen zum durch iterieren
    # maximiere_ziffern()
    maximiere_ziffern_iter(versuchsliste, aktionen_übrig, offers, requests,
                           ziffern)  # haupt funktion
    # FFFEA97B55
    # FFFEA97B55
    # FFFFFFFE88
    # 0000000177
    ausgabe()

timer_stop()

"""
Idee 1.0

überprüfe wie viele Streichhölzer du zur verfügung hast:

Schau wie du eine Ziffer erhöhen kannst wenn du Hölzer weg nimmst
Mach dies für jede Ziffer - die anzahl an weggenommenen Streichhölzern heißt profit_streichhölzer

Wenn die Anzahl an profit_streichhölzern kleiner ist als die Anzahl an verfügbaren aktionen_übrig, müssen wir davon ausgehen 
dass diese streichhölzer nicht ausreichen werden. Es muss also Ziffern geben die an wert verlieren. 

Wenn das der Fall ist brauchen wir eine Andere Strategie:
    wir berechnen die Anzahl an streichhölzern die wir allgemein durchs weg nehmen erhalten können.

Die erste Ziffer wird versucht so hoch,
Deshalb wird ab dem Punkt wo alle verfügbaren Streichhölzer versuchen wir  

----- 
Der ansatz ist die ersten Ziffern so weit zu optimieren wie es geht
im ideal Fall ist es also FFFFFFFFFF...F1213B34

Umsetzung

"""  # Idee 1.0

"""
Idee 2.0

Jede gegeben Ziffer  des Hexadezimalsystems wird versucht zur höchst möglichen Ziffer umgewandelt zu werden.
n = 0
1. Stelle n versuchen zu erst zu (ziffer z) F dann E,D,C,B... bis zum Wert des eigenen Ziffer value,  umgewandelt zu werden
-> daraus kann das Problem folgen das Stäbchen übrig sind oder gebrauch werden.
-> Jetzt Schreiben wir einen Algorithmus der um jeden Preis versucht diesen Mangel/Überschuss zu kompensieren.
    # Hierzu können auch schon die im Request oder Pott verfügbaren Stäbchen verwendet werden. 
-> Gelingt dies innerhalb der verfügbaren aktionen_übrig. 
    wird die Ziffer n fest der Ziffer z zu geschrieben. Gehe zu schritt 2.
-> Gelingt dies nicht wird die nächste ziffer z versucht. => 1

2. Nun wird optimiert:
-> Es wird ausgerechnet wie viele Aktionen sicher getätigt werden müssen und der überschuss wird in eine Pott-Liste und der Mangel in einer Request-Liste abgespeichert
n++;=> gehe zu schritt 1.
    # wenn n das maximum erreicht hat gehe zu => 3.

3.
weise so effizient wie es geht die stäbchen den Ziffern zu und schreibe für jede Aktion einen Log
"""  # idee 2.0

"""
__Idee 3.0

Eine Mischung aus 1.0 und 2.0

Die Möglchkeiten werden gebruteforced nur das vom Bestcasesceniario (FFFFFF...F) ausgegangen wird (1.0).  
Sobald eine Ziffer die verfügbaren Aktionen ausgeschöpft hat, wird nachgeprüft ob diese Ziffer allgemein als 
letztmögliche verfügbar ist. (2.0)

"""  # idee 3.0 aktuellste
