import performance_analysing

perf = performance_analysing.time_analysing()


def timer_start():
    perf.set_time_point("Start")


def timer_stop():
    perf.set_time_point("Stop")


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

    def __init__(self, char):
        self.positions = Ziffer.models[char][:]  # kopiere die Instanz sodass keine Referenz mehr entsteht
        self.probieren_index = 0
        self.bekommt_von = []
        self.char = char

    def aktionen_zum_ziel(self, ziel_char):
        self.char = ziel_char
        model = Ziffer.models[ziel_char]
        wegnehmen = 0
        hinzulegen = 0

        for i in range(7):
            if not model[i] == self.positions[i]:
                if model[i]:
                    hinzulegen += 1
                else:
                    wegnehmen += 1
        return wegnehmen, hinzulegen

    def min_umformung_mit_n_stäbchen(self, n_requested):  # hinzu - wegnehmen = anzahl an zu wenigen stäbchen im system
        # wir wollen eine Ziffer finden die - n_requested bzw
        global aktionen_übrig
        rekord = float("inf")
        erfolg = False
        for char in self.models:
            wegnehmen, hinzulegen = self.aktionen_zum_ziel(char)
            if wegnehmen - hinzulegen == n_requested:
                if max((wegnehmen, hinzulegen)) <= aktionen_übrig:
                    erfolg = True
                    rekord = max((wegnehmen, hinzulegen)) if rekord > max((wegnehmen, hinzulegen)) else rekord
        return erfolg, rekord


def get_input():
    pfad = "hexmax1.txt"
    text = open(pfad, "r").read()
    zeilen = text.split("\n")
    zeilen.pop(-1)

    ziffern = []  # sammelt alle Ziffern
    print(zeilen[0])
    for char in zeilen[0]:
        ziffern.append(Ziffer(char))
    aktionen = int(zeilen[1])
    print("Aktionen", aktionen)
    return ziffern, aktionen


def print_ziffern(list_ziffern):
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


def rek(aktuelle_ziffer_index=0):
    global versuchsliste, aktionen_übrig, offers, requests, ziffern
    print("\r", '_' * (aktuelle_ziffer_index + 1), aktionen_übrig, end="")
    if aktuelle_ziffer_index >= len(ziffern) or aktionen_übrig == 0:
        if 0 == len(offers) == len(requests):
            return True
    else:
        aktuelle_ziffer = ziffern[aktuelle_ziffer_index]
        for char in versuchsliste:
            wegnehmen, hinzufügen = aktuelle_ziffer.aktionen_zum_ziel(char)
            if max((
                    wegnehmen,
                    hinzufügen)) > aktionen_übrig:  # wenn nicht genug aktionen_übrig übrig sind um diese ziffer zu ändern
                continue
            log = []  # log = [(list, objekt)]

            if wegnehmen > hinzufügen:
                for _ in range(wegnehmen - hinzufügen):
                    if len(requests) > 0:
                        annehmende_ziffer = ziffern[requests[0]]
                        annehmende_ziffer.bekommt_von.append(aktuelle_ziffer_index)
                        log.append((annehmende_ziffer.bekommt_von, aktuelle_ziffer_index))
                    else:
                        offers.append(aktuelle_ziffer_index)
                        log.append((offers, aktuelle_ziffer_index))
            elif hinzufügen > wegnehmen:
                for _ in range(hinzufügen - wegnehmen):
                    if len(offers) > 0:  # wenn es angebote gibt
                        anbietende_ziffer_id = offers[0]
                        aktuelle_ziffer.bekommt_von.append(anbietende_ziffer_id)
                        log.append((aktuelle_ziffer.bekommt_von, anbietende_ziffer_id))
                    else:
                        offers.append(aktuelle_ziffer_index)
                        log.append((offers, aktuelle_ziffer_index))
            aktionen_übrig -= max((wegnehmen, hinzufügen))

            if rek(aktuelle_ziffer_index + 1): return True
            aktionen_übrig += max((wegnehmen, hinzufügen))
            for a, b in log:
                a.remove(b)
            log.clear()
    return False


def ist_char_möglich(i, char):
    global ziffern, aktionen_übrig
    ziffer = ziffern[i]
    wegnehmen, hinzufügen = ziffer.aktionen_zum_ziel(char)
    if max((wegnehmen, hinzufügen)) > aktionen_übrig: return False  # ???... >= aktionen_übrig???

    n_gebrauchte_stäbchen = hinzufügen - wegnehmen  # anzahl an zu wenigen stäbchen im system

    for j in range(i + 1, len(ziffern)):  # probiere andere ziffern aus
        for i in range(n_gebrauchte_stäbchen):

            erfolg, aktionen = ziffer.min_umformung_mit_n_stäbchen(n_gebrauchte_stäbchen)
            if erfolg:
                aktionen_übrig -= max((wegnehmen, hinzufügen)) + aktionen
                return True
    return False


"""
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
"""

timer_start()
if __name__ == '__main__':
    ziffern, aktionen_übrig = get_input()
    offers = []  # liste von ziffer_ids dessen ziffer striche zur verfügen stellen
    requests = []  # liste von ziffer_ids dessen ziffer striche Anfragen
    versuchsliste = "FEDCBA987654321"
    res = ""
    for ziffer_index in range(len(ziffern)):
        for char in versuchsliste:
            if ist_char_möglich(ziffer_index, char):
                res += char
                continue

    print(res)
    # rek()

    """
    aktuelle_ziffer = ziffern[0]
    aktuelle_ziffer_index = 0
    logs = [ [] for _ in range(len(ziffern))]
    while True:
        
        #- Überprüfung ob noch versuchbare chars übrig sind
        #    - Fail: Vorherige Ziffer versucht was anderes
        #- Set: Char; Aktionen(Aufnahme, abgabe)
        #- Überprüfung ob für die Aktionen genügend n_aktionen übrig sind
        #    - Fail: Eine anderer char wird überpfrüft
        

        if not aktuelle_ziffer.probieren_index < len(versuchsliste):
            aktuelle_ziffer_index -= 1
            aktuelle_ziffer = ziffern[aktuelle_ziffer_index]
            continue

        char = versuchsliste[aktuelle_ziffer.probieren_index]

        wegnehmen, hinzufügen = aktuelle_ziffer.aktionen_zum_ziel(char)

        if max((wegnehmen, hinzufügen)) > aktionen_übrig:  # wenn nicht genug aktionen_übrig übrig sind um diese ziffer zu ändern
            aktuelle_ziffer.probieren_index += 1
            continue
        aktionen_übrig = [0, 8, 9, 12]
        if wegnehmen > hinzufügen:
            for _ in range(wegnehmen - hinzufügen):
                if len(requests) > 0:
                    annehmende_ziffer = ziffern[requests[0]]
                    annehmende_ziffer.bekommt_von.append(aktuelle_ziffer_index)
                else:
                    pot.append(aktuelle_ziffer_index)

        elif hinzufügen > wegnehmen:
            for _ in range(hinzufügen - wegnehmen):
                if len(pot) > 0:  # wenn es angebote gibt
                    anbietende_ziffer_id = pot[0]
                    aktuelle_ziffer.bekommt_von.append(anbietende_ziffer_id)
                else:
                    pot.append(aktuelle_ziffer_index)

        aktionen_übrig -= max((wegnehmen, hinzufügen))
        if aktuelle_ziffer_index >= len(ziffern) or aktionen_übrig == 0:
            if 0 == len(pot) == len(requests):
                print()
                break
            aktuelle_ziffer.probieren_index += 1
            # TODO mach den fehler rückgängig

            continue
        else:
            aktuelle_ziffer_index += 1
            ziffern[aktuelle_ziffer_index].probieren_index = 0
    """

    # print_ziffern(ziffern)
    print("Result")
    for ziff in ziffern:
        print(ziff.char, end="")
    print()
timer_stop()

n = int(input())
# TODO Löse das algorithmische problem wie unten beschrieben
"""
Die Frage ist, wie kann man der anzahl n stäbe an personen verteilen:

bei 6
kann man
6,0,0,0,0,0
5,1,0,0,0,0
4,2,0,0,0,0
3,3,0,0,0,0
1,1,4,0,0,0
1,2,3,0,0,0
1,1,1,3,0,0
1,1,2,2,0,0
1,1,1,1,2,0
1,1,1,1,1,1
das muss man algorithmisch machen 


"""
