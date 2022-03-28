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
class ZifferSystem:
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
        self.positions = ZifferSystem.models[char][:]  # kopiere die Instanz sodass keine Referenz mehr entsteht
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
        model = ZifferSystem.models[ziel_char]
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
        model = ZifferSystem.models[self.char]
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


class CharInformationDict2D:

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

    def set_value_filtered(self, key1, key2, value):
        if key1 not in self.value:
            self.value[key1] = {key2: value}
        else:
            for k in self.value[key1].keys():
                if k > key2:
                    if self.value[key1][k][0] < value[0]:
                        self.value[key1][k][0] = value[0]
                    if self.value[key1][k][1] < value[1]:
                        self.value[key1][k][1] = value[1]
                else:
                    if self.value[key1][k][0] > value[0]:
                        value[0] = self.value[key1][k][0]
                    if self.value[key1][k][1] < value[1]:
                        value[0] = self.value[key1][k][0]

            self.value[key1][key2] = value


class ZiffernChangeInformation:

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
        ziffern.append(ZifferSystem(char, i))
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
    :return: aktionen, offers, requests, d_offers(zunahme), d_requests(zunahme)
    """
    global tabelle
    d_offers, d_requests = 0, 0
    bu_offers, bu_requests = offers, requests
    inf = tabelle[start_char][zielchar]
    aktionen = inf.min_aktion  # es müssen mindetens die unter einander zu tauschenden sticks
    if inf.stick_mangel > 0:  # es wird aus offers genommen
        offers -= inf.stick_mangel  # offers verringert sich
        d_offers = -inf.stick_mangel  # um wieviel offers zu genommen hat
        if offers < 0:  # es muss eine eigene request aufgegeben werden...
            aktionen -= offers  # ...das ist eine extra aktion
            requests -= offers
            # dieser muss aus dem delta entfernt werden...
            offers = 0  # ...da offers auf 0 gesetzt wird
    elif inf.stick_mangel < 0:  # es wird aus requests genommen
        requests += inf.stick_mangel  # so viele es requests werden befriedigt
        d_requests = inf.stick_mangel
        if requests < 0:  # es muss ein angebot für alle sichtbar erstellt werden
            aktionen -= requests  # das kostet
            offers -= requests  # offers erhöht sich
            requests = 0

    return aktionen, offers, requests, d_offers, d_requests, bu_offers, bu_requests


def undo_action(log, actions_left):
    aktionen, d_offers, d_requests, bu_offers, bu_requests = log
    actions_left += aktionen
    return actions_left, bu_offers, bu_requests


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
    offers_list = []
    requests_list = []
    for ziffer in ziffern:
        aktionen_planen(ziffer, offers_list, requests_list, tabelle)
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
        ziffern_.append(ZifferSystem(versuchsliste[i], i))

    for z in ziffern_:
        temp = {}
        for char in versuchsliste:
            wegnehmen, hinzulegen = z.aktionen_zum_ziel(char)
            temp[char] = ZiffernChangeInformation(wegnehmen, hinzulegen, z.useless_indeces.copy())
        t[z.ursprungschar] = temp
    return t


def maximiere_ziffern_iter(versuchsliste, actions_left, offers, requests, ziffern):
    # man geht immer vom best case aus
    _index = 0
    ausgleichs_werte = CharInformationDict2D()
    while True:
        if _index == len(ziffern):  # wenn es keine Ziffern mehr zum Verändern gibt
            if 0 == offers == requests:  # win condition
                print("Es passt halt 1 Line 316")
                break
            _index -= 1  # Miserfolg
            continue

        aktuelle_ziffer = ziffern[_index]  # betrachtete aktuelle Ziffer
        if not aktuelle_ziffer.active:  # aktuelle ziffer wird betrachtet
            if actions_left == 0:  # die ziffer kann sich nicht mehr verändern nach Schema 1
                if 0 == offers == requests:  # win condition
                    print("Es passt halt 2 Line 324")
                    break
                _index -= 1  # Misserfolg
                continue

            aktuelle_ziffer.active = True  # die ziffer hier kann überprüft werden
            char = versuchsliste[aktuelle_ziffer.char_i]  # iteriert durch alle Hex-Zahlen durch
            # Simuliert das Umwandeln dieser Ziffer und returned die Situation wie sie dann aussehen wird
            aktionen, offers, requests, d_offers, d_requests, bu_offers, bu_requests = try_change_char(
                aktuelle_ziffer.ursprungschar, char,
                offers, requests)
            # macht backup von dieser Situation
            log = (aktionen, d_offers, d_requests, bu_offers, bu_requests)
            aktuelle_ziffer.log = log
            aktuelle_ziffer.char = char
            actions_left -= aktionen  # durch diesen Versuch verändert sich auch die übrigen Aktionen
            if actions_left < 0:  # wenn mehr Aktionen gebraucht als verfügbar, diese Ziffer unmöglich
                continue  # durch ziffer.active = True: im nächsten durchgang wird Überprüfungsschema2 probiert
            if ausgleichs_werte.key_exists(_index + 1, actions_left):
                # falls schon berechnet wurde, was der maximale Ausgleichswert ist
                zielausgleich = offers + requests  # offers oder requests ist 0
                ausgleichswert = ausgleichs_werte.get_value(_index + 1, actions_left)
                if ausgleichswert[0 if offers > 0 else 1] < zielausgleich:  # wenn der Zielausgleich nicht erreicht werden kann
                    continue  # wir wissen, dass dieser Char nicht möglich ist
            _index += 1  # nächste ziffer wird betrachtet
        else:
            # backup laden
            aktionen, d_offers, d_requests, bu_offers, bu_requests = aktuelle_ziffer.log

            if actions_left >= 0:  # nur wenn die Simulation eine potenzielle Situation erschaffen
                # nun wird überprüft, ob ein Ausgleich noch möglich ist der übrigen stäbchen möglich ist
                # man darf nicht mehr aktionen verbraucht haben als zugänglich
                ausgleichbar, n_maximal_ausgeglichen = ausgleich_der_stäbchen_iter(_index + 1,
                                                                                   actions_left, ziffern, offers,
                                                                                   requests)
                if ausgleichbar: break  # win condition

                # setzt nur, wenn es noch nicht existiert und wirklich besser ist
                ausgleichs_werte.set_value_filtered(_index, actions_left + aktionen, n_maximal_ausgeglichen)

            # Simulation rückgängig machen
            actions_left, offers, requests = actions_left + aktionen, bu_offers, bu_requests
            aktuelle_ziffer.active = False
            aktuelle_ziffer.char_i += 1
            aktuelle_ziffer.char = aktuelle_ziffer.ursprungschar

            if aktuelle_ziffer.char_i == len(versuchsliste):
                aktuelle_ziffer.char_i = 0
                _index -= 1
    return True


def ausgleich_der_stäbchen_iter(index, actions_left, ziffern, offers, requests):
    global ausgleichs_werte2
    """
    Diese Funktion verteilt beiseite gelegte Sticks auf die restlichen
    Ziffernsysteme so das dabei auch noch eine maximale Hexadezimalzahl entsteht
    :param index: index der letzten festgelegten ziffer
    :return: Erfolg (bool)
    """

    start_index = index
    while start_index <= index:
        zielausgleich = offers + requests
        if index == len(ziffern):  # keine Ziffern mehr überprüfbar
            if zielausgleich == 0: return True, 0  # win condition
            ausgleichs_werte2.set_value_filtered(index, actions_left, [0, 0])
            index -= 1
            continue
        # betrachtete aktuelle Ziffer
        aktuelle_ziffer = ziffern[index]
        if not aktuelle_ziffer.active:  # first touch
            if zielausgleich == 0: return True, 0  # win condition

            char = versuchsliste[aktuelle_ziffer.char_i]  # char durch iterieren
            # simulation machen
            aktionen, offers, requests, d_offers, d_requests, bu_offers, bu_requests = try_change_char(
                aktuelle_ziffer.ursprungschar, char, offers, requests)
            actions_left -= aktionen
            aktuelle_ziffer.char = char
            aktuelle_ziffer.active = True
            # backup für situation
            aktuelle_ziffer.log = (aktionen, d_offers, d_requests, bu_offers, bu_requests)

            new_zielausgleich = offers + requests
            if actions_left < 0:
                continue  # dieser char funktioniert nicht, weil zu viele aktionen gebraucht werden

            if ausgleichs_werte2.key_exists(index + 1, actions_left):  # wenn wir den besten ausgleichswert
                # von den nächsten Ziffern kennen
                max_ausgleich = ausgleichs_werte2.get_value(index + 1, actions_left)
                if max_ausgleich[0 if offers > 0 else 1] < new_zielausgleich:
                    continue  # wir können diesen Char ausschließen
            index += 1  # die Nächste Ziffer wird betrachtet
        else:  # second touch
            # load the back up
            aktionen, d_offers, d_requests, bu_offers, bu_requests = aktuelle_ziffer.log

            # undo simulation
            actions_left, offers, requests = actions_left + aktionen, bu_offers, bu_requests
            aktuelle_ziffer.active = False
            aktuelle_ziffer.char = aktuelle_ziffer.ursprungschar
            aktuelle_ziffer.char_i += 1

            if ausgleichs_werte2.key_exists(index + 1,
                                            actions_left):  # wenn wir den Ausgleichswert von der nächsten Ziffer kennen
                upperwin = ausgleichs_werte2.get_value(index + 1, actions_left)  # was ist dieser Wert?
                actual_win = [(-d_offers) + upperwin[0], (-d_requests) + upperwin[1]]
                # wie hoch wäre dieser Win auf unsere Situation
                ausgleichs_werte2.set_value_filtered(index, actions_left,
                                                     actual_win)  # setzt es nur, wenn es auch wirklich besser ist

            if aktuelle_ziffer.char_i == len(versuchsliste):  # every char was checked
                aktuelle_ziffer.char_i = 0
                index -= 1
    return False, ausgleichs_werte2.get_value(start_index, actions_left)


# endregion

timer_start()

pfad = "hexmax0.txt"
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
    ausgleichs_werte2 = CharInformationDict2D()
    versuchsliste = "FEDCBA9876543210"  # Hex-Zahlen zum durch iterieren
    tabelle = gen_tabelle()  # tabelle[goalchar][startchar]
    ziffern, actions_left = get_input(pfad)  # input aus Text-Datei
    offers = 0  # liste von ziffer_ids dessen ziffer striche zur verfügen stellen
    requests = 0  # liste von ziffer_ids dessen ziffer striche Anfragen
    maximiere_ziffern_iter(versuchsliste, actions_left, offers, requests, ziffern)  # haupt funktion

    ausgabe()
    print("\nout of", actions_left)

timer_stop()
