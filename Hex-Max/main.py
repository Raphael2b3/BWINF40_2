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

# region Finished
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
        self.bekommt_von = []
        self.useless_indeces = []
        self.char = char
        self.ursprungschar = char
        self.active = False
        self.char_i = 0
        self.log = None

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
        return f"{self.char} ci{self.char_i} act{self.active} log{self.log} id{self.id}"


class Dictionary2d:

    def __init__(self):
        self.value = {}

    def __contains__(self, item):
        return item in self.value

    def key_exists(self, key1, key2=None):
        if not key1 in self.value:
            return False
        if key2 is not None and key2 not in self.value[key1]:
            return False
        return True

    def get_value(self, key1, key2=None):
        if not key1 in self.value:
            return 0
        if key2 is None:
            return self.value[key1]
        if key2 not in self.value[key1]:
            # v = self.value[key1][key2] = self.get_value(key1+1, 0)
            return 0
        return self.value[key1][key2]

    def set_value(self, key1, key2, value):
        if key1 not in self.value:
            self.value[key1] = {key2: value}
        else:
            self.value[key1][key2] = value

    def set_value_extra(self, key1, key2, value):
        if key1 not in self.value:
            self.value[key1] = {key2: value}
        else:
            for k in self.value[key1].keys():
                if k > key2:
                    if self.value[key1][k] < value:
                        self.value[key1][k] = value
            self.value[key1][key2] = value


class Inf:

    def __init__(self, weg, hin, useless_i):
        self.min_aktion = min(weg, hin)
        self.weg = weg
        self.hin = hin
        self.stick_mangel = hin - weg
        self.useless_indeces = useless_i

    def __eq__(self, other):
        return self.weg == other.weg and self.hin == other.hin and self.useless_indeces == other.useless_indeces


def get_input(pfad):
    text = open(pfad, "r").read()
    zeilen = text.split("\n")
    zeilen.pop(-1)
    #
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


def try_change_char(start_char, zielchar, offers, requests):
    """
    Findet heraus wie viele aktionen wirklich getan werden müssen und berücksichtigt dabei schon beiseite gelegte sticks
    :param wegnehmen:
    :param hinzufügen:
    :param aktuelle_ziffer_index:
    :param aktuelle_ziffer:
    :return: aktionen, offers, requests, d_offers(zunahme), d_requests(zunahme)
    """
    global tabelle
    d_offers, d_requests = 0, 0
    # TODO Überarbeite die art und weise wie du äste skipst beim ausprobieren
    inf = tabelle[start_char][zielchar]
    aktionen = inf.min_aktion  # es müssen mindetens die unter einander zu tauschenden sticks
    if inf.stick_mangel > 0:  # es wird aus offers genommen
        offers -= inf.stick_mangel  # offers verringert sich
        d_offers = -inf.stick_mangel  # um wieviel offers zu genommen hat
        if offers < 0:  # es muss eine eigene request aufgegeben werden...
            aktionen -= offers  # ...das ist eine extra aktion
            requests -= offers
            d_requests -= offers
            d_offers -= offers  # weil offers ist momentan <0 und bildet auch den überhängsel ab,
            # dieser muss aus dem delta entfernt werden...
            offers = 0  # ...da offers auf 0 gesetzt wird
    elif inf.stick_mangel < 0:  # es wird aus requests genommen
        requests += inf.stick_mangel  # so viele es requests werden befriedigt
        d_requests = inf.stick_mangel
        if requests < 0:  # es muss ein angebot für alle sichtbar erstellt werden
            aktionen -= requests  # das kostet
            offers -= requests  # offers erhöht sich
            d_offers -= requests
            d_requests -= requests
            requests = 0

    return aktionen, offers, requests, d_offers, d_requests


def undo_action(log, aktionen_übrig, offers, requests):
    aktionen, d_offers, d_requests = log
    aktionen_übrig += aktionen
    offers -= d_offers
    requests -= d_requests
    return aktionen_übrig, offers, requests


def aktionen_planen(aktuelle_ziffer, offers, requests, tabelle):
    inf = tabelle[aktuelle_ziffer.ursprungschar][aktuelle_ziffer.char]

    for _ in range(inf.hin if inf.weg >= inf.hin else inf.weg):
        aktuelle_ziffer.bekommt_von.append(aktuelle_ziffer.id)

    for _ in range(abs(inf.stick_mangel)):
        if inf.stick_mangel > 0:  # es wird aus offers genommen
            if len(offers) > 0:
                o = offers.pop(-1)
                aktuelle_ziffer.bekommt_von.append(o)
            else:
                requests.append(aktuelle_ziffer.id)
        elif inf.stick_mangel < 0:  # es wird aus requests genommen
            if len(requests) > 0:
                o = requests.pop(-1)
                ziffern[o].bekommt_von.append(aktuelle_ziffer.id)
            else:
                offers.append(aktuelle_ziffer.id)
    aktuelle_ziffer.useless_indeces = inf.useless_indeces.copy()
    return offers, requests


def ausgabe():
    for ziffer in ziffern:
        aktionen_planen(ziffer, offers, requests, tabelle)
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
    print("Ergebnis:\nEnd-Hexadezimalzahl")
    for ziff in ziffern:
        print(ziff.char, end="")


def gen_tabelle():
    t = {}
    ziffern_ = []
    for i in range(len(versuchsliste)):
        ziffern_.append(Ziffer(versuchsliste[i], i))

    for z in ziffern_:
        temp = {}
        for char in versuchsliste:
            wegnehmen, hinzulegen = z.aktionen_zum_ziel(char)
            temp[char] = Inf(wegnehmen, hinzulegen, z.useless_indeces.copy())
        t[z.ursprungschar] = temp
    return t


def maximiere_ziffern_iter(versuchsliste, aktionen_übrig, offers, requests, ziffern):
    _index = 0
    mögliche_ausgleiche = Dictionary2d()
    while True:
        if _index == len(ziffern):
            if 0 == offers == requests:
                print("Es passt halt 1 Line 316")
                input()
                break
            _index -= 1
            continue

        aktuelle_ziffer = ziffern[_index]  # betrachtete aktuelle Ziffer
        if not aktuelle_ziffer.active:
            if aktionen_übrig == 0:
                if 0 == offers == requests:
                    print("Es passt halt 2 Line 324")
                    break
                _index -= 1
                continue
            if aktuelle_ziffer.char_i == len(versuchsliste):
                aktuelle_ziffer.char_i = 0
                aktuelle_ziffer.active = False
                _index -= 1
                continue

            char = versuchsliste[aktuelle_ziffer.char_i]  # iteriert durch alle Hex-Zahlen durch
            aktionen, offers, requests, d_offers, d_requests = try_change_char(aktuelle_ziffer.ursprungschar, char,
                                                                               offers, requests)
            log = (aktionen, d_offers, d_requests)
            aktionen_übrig -= aktionen

            if aktionen_übrig < 0:
                aktionen_übrig, offers, requests = undo_action(log, aktionen_übrig, offers, requests)
                aktuelle_ziffer.char_i += 1
                continue

            if mögliche_ausgleiche.key_exists(_index + 1, aktionen_übrig):
                zielausgleich = offers + requests
                ausgleichswert = mögliche_ausgleiche.get_value(_index + 1, aktionen_übrig)
                if ausgleichswert[0 if offers > 0 else 1] < zielausgleich:
                    aktionen_übrig, offers, requests = undo_action(log, aktionen_übrig, offers, requests)
                    aktuelle_ziffer.char_i += 1
                    continue
            aktuelle_ziffer.log = log
            aktuelle_ziffer.active = True
            aktuelle_ziffer.char = char
            _index += 1
        else:
            # nun wird überprüft, ob ein Ausgleich noch möglich ist der übrigen stäbchen möglich ist
            ausgleich_möglich, n_maximal_ausgeglichen = ausgleich_der_stäbchen_iter(_index + 1,
                                                                                    aktionen_übrig, ziffern, offers,
                                                                                    requests)
            a,b = n_maximal_ausgeglichen
            if a != 0 and b != 0:
                input("big problem")
            # print("ausgleich",offers+requests-n_maximal_ausgeglichen,"aktions left",aktionen_übrig, "ziffer", aktuelle_ziffer)
            if ausgleich_möglich:
                print("Nach nem AusgleichLine 365")
                break
            if not mögliche_ausgleiche.key_exists(_index + 1, aktionen_übrig):
                mögliche_ausgleiche.set_value(_index + 1, aktionen_übrig, n_maximal_ausgeglichen)
            # wenn der danach nicht geklappt hat wird versucht die momentane Stellung irgendwie möglich zu machen

            # aktionen Rückgängig machen
            aktionen_übrig, offers, requests = undo_action(aktuelle_ziffer.log, aktionen_übrig, offers, requests)
            aktuelle_ziffer.active = False
            aktuelle_ziffer.char_i += 1
            aktuelle_ziffer.char = aktuelle_ziffer.ursprungschar

    return True


# endregion


def ausgleich_der_stäbchen_iter(index, aktionen_übrig, ziffern, offers, requests):
    global ausgleichsvalues2
    """
    Diese Funktion verteilt beiseite gelegte Sticks auf die restlichen
    Ziffernsysteme so das dabei auch noch eine maximale Hexadezimalzahl entsteht
    :param index: index der letzten festgelegten ziffer
    :return: Erfolg (bool)
    """

    start_index = index
    while start_index <= index:
        zielausgleich = offers + requests
        if index == len(ziffern):
            if zielausgleich == 0: return True, 0
            ausgleichsvalues2.set_value(index, aktionen_übrig, (0, 0))
            index -= 1
            continue
        # betrachtete aktuelle Ziffer
        aktuelle_ziffer = ziffern[index]
        if not aktuelle_ziffer.active:  # first touch
            if zielausgleich == 0: return True, 0
            if aktuelle_ziffer.char_i == len(versuchsliste):  # every char was checked
                aktuelle_ziffer.char_i = 0
                aktuelle_ziffer.active = False
                index -= 1
                continue
            char = versuchsliste[aktuelle_ziffer.char_i]

            aktionen, offers, requests, d_offers, d_requests = try_change_char(aktuelle_ziffer.ursprungschar, char,
                                                                               offers, requests)
            log = (aktionen, d_offers, d_requests)
            aktionen_übrig -= aktionen
            new_zielausgleich = offers + requests

            if aktionen_übrig < 0:
                aktionen_übrig, offers, requests = undo_action(log, aktionen_übrig, offers, requests)
                aktuelle_ziffer.char_i += 1
                continue
            if ausgleichsvalues2.key_exists(index + 1, aktionen_übrig) and ausgleichsvalues2.key_exists(index,
                                                                                                        aktionen_übrig + aktionen):
                max_ausgleich = ausgleichsvalues2.get_value(index + 1, aktionen_übrig)
                if max_ausgleich[0 if offers>0 else 1] < new_zielausgleich:
                    aktionen_übrig, offers, requests = undo_action(log, aktionen_übrig, offers, requests)
                    aktuelle_ziffer.char_i += 1
                    continue
            aktuelle_ziffer.active = True
            aktuelle_ziffer.log = log
            aktuelle_ziffer.char = char
            index += 1
        else:  # second touch
            aktionen, d_offers, d_requests = aktuelle_ziffer.log
            upperwin = ausgleichsvalues2.get_value(index + 1, aktionen_übrig)
            # aktionen_übrig += aktionen; offers -= d_offers; requests -= d_requests
            aktionen_übrig, offers, requests = undo_action(aktuelle_ziffer.log, aktionen_übrig, offers, requests)
            aktuelle_ziffer.active = False
            aktuelle_ziffer.char = aktuelle_ziffer.ursprungschar
            aktuelle_ziffer.char_i += 1

            # ist das der char der den höchsten ausgleich macht?
            gewonnener_ausgleich = -d_offers - d_requests  # weil d_offers die zunahme beschreibt...
            actual_win = -d_offers + upperwin[0], - d_requests + upperwin[1]

            # ...wir gewinnen aber wenn d_offers <0
            if not ausgleichsvalues2.key_exists(index, aktionen_übrig):
                ausgleichsvalues2.set_value(index, aktionen_übrig, actual_win)
                # u can set it 0 by default because
                # there is always the chance to keep the char at its state
            elif ausgleichsvalues2.get_value(index, aktionen_übrig) <= sum(actual_win):
                # set this new max value only if
                ausgleichsvalues2.set_value(index, aktionen_übrig, actual_win)

    return False, ausgleichsvalues2.get_value(start_index, aktionen_übrig)


timer_start()
pfad = "hexmax5.txt"
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
    ausgleichsvalues2 = Dictionary2d()
    versuchsliste = "FEDCBA9876543210"  # Hex-Zahlen zum durch iterieren
    tabelle = gen_tabelle()  # tabelle[goalchar][startchar]
    ziffern, aktionen_übrig = get_input(pfad)  # input aus Text-Datei
    offers = 0  # liste von ziffer_ids dessen ziffer striche zur verfügen stellen
    requests = 0  # liste von ziffer_ids dessen ziffer striche Anfragen
    maximiere_ziffern_iter(versuchsliste, aktionen_übrig, offers, requests, ziffern)  # haupt funktion
    offers = []
    requests = []

    ausgabe()
    print("\nout of", aktionen_übrig)

timer_stop()
