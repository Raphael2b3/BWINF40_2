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

    def min_umformung_mit_n_stäbchen(self, n_requested):  #
        """
        Ziel ist eine Ziffer zu finden die n_requested Sticks zu viel im System hat
        :param n_requested: Anzahl an anfragen die zu befriedigen sind.
        :return:
        """
        global aktionen_übrig, versuchsliste
        rekord = float("inf")
        erfolg = False
        char_ = self.char
        for char in versuchsliste:
            wegnehmen, hinzulegen = self.aktionen_zum_ziel(char)
            if wegnehmen - hinzulegen != n_requested: continue
            if min((wegnehmen, hinzulegen)) > aktionen_übrig: continue
            if not rekord > min((wegnehmen, hinzulegen)): continue
            erfolg = True
            rekord = min((wegnehmen, hinzulegen))
            #  min weil die übrigen aktionen von außen übernommen werden
            char_ = char

        self.char = char_
        return erfolg, rekord


    def __str__(self):
        return self.char

def get_input():
    pfad = "hexmax0.txt"
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

# TODO Finde die bugs die du eigentlich schon kennst aber du huso hast deine Festplatte formatiert Spasst!
def rek(aktuelle_ziffer_index=0):
    global versuchsliste, aktionen_übrig, offers, requests, ziffern
    print("\r", '_' * (aktuelle_ziffer_index + 1), aktionen_übrig, end="")
    if aktuelle_ziffer_index >= len(ziffern):
        if 0 == len(offers) == len(requests):
            return True
    else:
        aktuelle_ziffer = ziffern[aktuelle_ziffer_index]
        for char in versuchsliste:
            wegnehmen, hinzufügen = aktuelle_ziffer.aktionen_zum_ziel(char)
            if max((wegnehmen,
                    hinzufügen)) > aktionen_übrig:  # wenn nicht genug aktionen_übrig übrig sind um diese ziffer zu ändern
                continue
            log = []  # log = [(list, objekt)] later remove objekt from list
            log2 = []  # log2 = [(list, objekt)] later append objekt to list
            if wegnehmen > hinzufügen:
                for _ in range(wegnehmen - hinzufügen):
                    if len(requests) > 0:
                        annehmende_ziffer = ziffern[requests[0]]
                        annehmende_ziffer.bekommt_von.append(aktuelle_ziffer_index)
                        o = requests.pop(0)
                        log2.append((requests, o))
                        log.append((annehmende_ziffer.bekommt_von, aktuelle_ziffer_index))
                    else:
                        offers.append(aktuelle_ziffer_index)
                        log.append((offers, aktuelle_ziffer_index))
            elif hinzufügen > wegnehmen:
                for _ in range(hinzufügen - wegnehmen):
                    if len(offers) > 0:  # wenn es angebote gibt
                        anbietende_ziffer_id = offers[0]
                        aktuelle_ziffer.bekommt_von.append(anbietende_ziffer_id)
                        o = offers.pop(0)
                        log2.append((offers, o))
                        log.append((aktuelle_ziffer.bekommt_von, anbietende_ziffer_id))
                    else:
                        requests.append(aktuelle_ziffer_index)
                        log.append((requests, aktuelle_ziffer_index))
            aktionen_übrig -= max((wegnehmen, hinzufügen))
            if rek(aktuelle_ziffer_index + 1): return True
            yarak = letzte_verteilung(aktuelle_ziffer_index)
            # wenn der danach nicht geklappt hat wird versucht die momentane Stellung irgendwie möglich zu machen
            if yarak: return True
            aktionen_übrig += max((wegnehmen, hinzufügen))
            for a, b in log:
                a.remove(b)
            for a, b in log2:
                a.append(b)

    return False


def permute(l, n, out, top):
    if n == 0:
        out.append(l[:])
    else:
        for i in range(min(n, top), 0, -1):
            l.append(i)
            permute(l, n - i, out, i)
            l.remove(i)
    return out


def letzte_verteilung(index):
    """
    Diese Funktion löst dieses Problem:\n
    Mit einer Anzahl N an übrigen Aktionen und einer menge von {index+1,...,len(ziffern)} Ziffern muss der Mangel/Überschuss\n
    an Stäbchen ausgeglichen werden:\n
    Bsp Situationen:\n
    4 stäbchen müssen noch auf 3 ziffern verteilt werden\n
    4 stäbchen müssen noch von 3 ziffern weggenommen werden\n


    :param index: index der letzten festgelegten ziffer
    :return:
    """
    """permutations = permute([], a, [], a) # TODO do not use permutations and find the correct awnser first try, you can doit
       blocklist = []
       perm_success = False
       sum_aktionen = 0
       permutations.reverse()
       for perm in permutations:
           blocklist.clear()
           sum_aktionen = 0
           for n in perm:
               best_akt = float("inf")
               best_i = 0
               erfolg = False
               for i in range(index+1, len(ziffern)):
                   if i in blocklist: continue
                   erfolg, aktionen = ziffern[i].min_umformung_mit_n_stäbchen(n*m)
                   if not erfolg or best_akt <= aktionen: continue
                   sum_aktionen += aktionen
                   if aktionen_übrig - sum_aktionen < 0:
                       erfolg = False
                       break
                   best_i = i
                   best_akt = aktionen

               if not erfolg:
                   perm_success = False
                   break
               else:
                   perm_success = True
               blocklist.append(best_i)
           if perm_success: break
       if perm_success:
           aktionen_übrig -= sum_aktionen
       return perm_success
   """


    global ziffern, aktionen_übrig
    a = max(len(offers), len(requests))
    m = 1 if len(offers) == 0 else -1  # Multiplikator, 1 wenn noch stäbchen in ziffern systemen fehlen,
    return rek2(a, m, index, [])


def rek2(zielausgleich, m, index, blocked):
    global aktionen_übrig, ziffern
    if zielausgleich == 0: return True
    for a in range(zielausgleich, 0, -1):
        best_i = 0
        rekord_aktion = float("inf")
        for i in range(index+1, len(ziffern)):
            if i in blocked: continue
            erfolg, min_aktion = ziffern[i].min_umformung_mit_n_stäbchen(a*m)
            if not erfolg: continue
            if min_aktion > aktionen_übrig or rekord_aktion <= min_aktion: continue
            best_i = i
            rekord_aktion = min_aktion
        if rekord_aktion == float("inf"): continue
        blocked.append(best_i)
        aktionen_übrig -= rekord_aktion
        if rek2(zielausgleich-a, m, index, blocked): return True
        blocked.remove(best_i)
        aktionen_übrig += rekord_aktion
    return False

timer_start()
if __name__ == '__main__':

    ziffern, aktionen_übrig = get_input()
    offers = []  # liste von ziffer_ids dessen ziffer striche zur verfügen stellen
    requests = []  # liste von ziffer_ids dessen ziffer striche Anfragen
    versuchsliste = "FEDCBA987654321"
    rek()

    # print_ziffern(ziffern)
    print("Result")
    for ziff in ziffern:
        print(ziff.char, end="")
    print()

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