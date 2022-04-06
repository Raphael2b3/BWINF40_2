import sys  # um die Rekursionstiefe zu modifizieren


class ZifferSystem:

    def __init__(self, char):
        self.positions = ziffern_models[char][:]  # kopiere die Instanz sodass keine Referenz mehr entsteht
        self.notyet_empty_indeces = []
        self.notyet_filled_indeces = []
        self.char = char
        self.ursprungschar = char

    def set_ziel_char(self, ziel_char):
        self.char = ziel_char  # setzt den char wert zum ziel
        model = ziffern_models[ziel_char]
        wegnehmen = 0
        hinzulegen = 0
        self.notyet_empty_indeces.clear()
        self.notyet_filled_indeces.clear()
        for i in range(7):
            if not model[i] == self.positions[i]:
                if model[i]:
                    hinzulegen += 1
                    self.notyet_filled_indeces.append(i)
                else:
                    wegnehmen += 1
                    self.notyet_empty_indeces.append(i)  # sticks müssen von Pos weggenommen werden
        return wegnehmen, hinzulegen


class ZiffernChangeInformation:

    def __init__(self, weg, hin, _notyet_empty_indeces, _notyet_filled_indeces):
        self.min_aktion = min(weg, hin)
        self.weg = weg
        self.hin = hin
        self.stick_mangel = hin - weg
        self.notyet_empty_indeces = _notyet_empty_indeces
        self.notyet_filled_indeces = _notyet_filled_indeces


def get_input(_pfad):
    text = open(_pfad, "r").read()
    zeilen = text.split("\n")
    print(zeilen[0])
    _ziffern = [ZifferSystem(char) for char in zeilen[0]]  # Instanzierung der Ziffernsysteme
    aktionen = int(zeilen[1])
    print("Aktionen: ", aktionen)
    return _ziffern, aktionen


def print_ziffern():  # printet die momentane Anordnung der Sticks
    zeile_1 = ""
    zeile_2 = ""
    zeile_3 = ""

    for ziffer in ziffern:
        zeile_1 += f" {'_' if ziffer.positions[0] else ' '}  "
        zeile_2 += f"{'|' if ziffer.positions[3] else ' '}{'_' if ziffer.positions[1] else ' '}{'|' if ziffer.positions[4] else ' '} "
        zeile_3 += f"{'|' if ziffer.positions[5] else ' '}{'_' if ziffer.positions[2] else ' '}{'|' if ziffer.positions[6] else ' '} "

    print("____")
    print(zeile_1)
    print(zeile_2)
    print(zeile_3)
    print()


def ausgabe():
    print("Ergebnis:\nEnd-Hexadezimalzahl")
    print("\nAusgangssituation:")
    print_ziffern()
    for z in ziffern:
        z.set_ziel_char(z.char)
    # Stick-Umlegung Ausgabe:
    aktion_debug = 1
    for z_from in ziffern:  # ...
        for i in z_from.notyet_empty_indeces:  # ... alle noch nicht leeren positionen werden gesucht
            found = False  # helper
            for z_to in ziffern:
                for j in z_to.notyet_filled_indeces:  # Ziffern werden auf noch nicht gefüllte Positionen durchsucht
                    z_from.positions[i], z_to.positions[j] = False, True  # Umlegung des Sticks
                    print_ziffern()  # ausgabe der Situation nach Umlegung des Sticks
                    print("==== Das war Aktion", aktion_debug)
                    aktion_debug += 1
                    found = True
                    break
                if found:
                    z_to.notyet_filled_indeces.pop(0)  # entfernt index aus der liste der noch nicht belegten Positionen
                    break

    print("Ergebnis:\nEnd-Hexadezimalzahl")
    for ziffer in ziffern:
        print(ziffer.char, end="")
    print("\n--ENDE--")


def simulate_change(start_char, ziel_char):
    global offers, requests
    bu_offers, bu_requests = offers, requests  # backup

    change_inf = change_inf_tabelle[start_char][ziel_char]
    aktionen = change_inf.min_aktion  # es müssen mindestens die unter einander zu tauschenden sticks
    if change_inf.stick_mangel > 0:  # es wird aus offers genommen
        offers -= change_inf.stick_mangel  # offers verringert sich
        if offers < 0:  # es muss eine eigene request aufgegeben werden...
            aktionen -= offers  # ...das ist eine extra aktion
            requests -= offers
            # dieser muss aus dem delta entfernt werden...
            offers = 0  # ...da offers auf 0 gesetzt wird
    elif change_inf.stick_mangel < 0:  # es wird aus requests genommen
        requests += change_inf.stick_mangel  # so viele es requests werden befriedigt
        if requests < 0:  # es muss ein angebot für alle sichtbar erstellt werden
            aktionen -= requests  # das kostet
            offers -= requests  # offers erhöht sich
            requests = 0
    return aktionen, bu_offers, bu_requests


def maximiere_ziffern():
    global actions_left, index, offers, requests
    if index == len(ziffern) or actions_left == 0:  # wenn es keine Ziffern mehr zum Verändern gibt
        return 0 == offers - requests  # win condition

    aktuelle_ziffer = ziffern[index]  # betrachtete aktuelle Ziffer
    for char in versuchsliste:
        # Simuliert das Umwandeln dieser Ziffer und returned die Situation wie sie dann aussehen wird
        aktionen, bu_offers, bu_requests = simulate_change(aktuelle_ziffer.ursprungschar, char)
        # macht backup von dieser Situation
        actions_left -= aktionen
        if actions_left >= 0:  # wenn mehr Aktionen gebraucht als verfügbar, diese Ziffer unmöglich
            zielausgleich = offers + requests  # offers oder requests ist 0
            index += 1
            ausgleichswert = best_ausgleich()
            if ausgleichswert[0 if offers > 0 else 1] >= zielausgleich:  # wenn Zielausgleich nicht erreicht werden kann
                aktuelle_ziffer.char = char

                if maximiere_ziffern() or ausgleich_der_stäbchen():
                    return True
                aktuelle_ziffer.char = aktuelle_ziffer.ursprungschar
            index -= 1

        # Simulation rückgängig machen
        actions_left += aktionen
        offers, requests = bu_offers, bu_requests
    return False


def ausgleich_der_stäbchen():
    global index, actions_left, offers, requests
    zielausgleich = offers + requests
    if index == len(ziffern):  # keine Ziffern mehr überprüfbar
        return zielausgleich == 0  # win condition
    # betrachtete aktuelle Ziffer
    aktuelle_ziffer = ziffern[index]
    for char in versuchsliste:
        aktionen, bu_offers, bu_requests = simulate_change(aktuelle_ziffer.ursprungschar, char)
        actions_left -= aktionen
        if actions_left >= 0:  # dieser char funktioniert nicht, weil zu viele aktionen gebraucht werden
            # von den nächsten Ziffern kennen
            new_zielausgleich = offers + requests
            index += 1
            max_ausgleich = best_ausgleich()
            if max_ausgleich[0 if offers > 0 else 1] >= new_zielausgleich:
                aktuelle_ziffer.char = char
                if ausgleich_der_stäbchen():
                    return True
                aktuelle_ziffer.char = aktuelle_ziffer.ursprungschar
            index -= 1
        actions_left += aktionen
        offers, requests = bu_offers, bu_requests
    return False


def gen_tabelle():
    # t[start][ziel]
    tabelle = {}
    for z in ziffern:
        if z.ursprungschar in tabelle: continue
        temp = {}
        for char in versuchsliste:
            wegnehmen, hinzulegen = z.set_ziel_char(char)
            temp[char] = ZiffernChangeInformation(wegnehmen, hinzulegen, z.notyet_empty_indeces[:],
                                                  z.notyet_filled_indeces[:])
        tabelle[z.ursprungschar] = temp
        z.char = z.ursprungschar
    return tabelle


def allgemeines_ausgleichs_potenzial():
    global actions_left
    aap_tabelle = {}
    for ziffer in ziffern:
        if ziffer.ursprungschar in aap_tabelle: continue
        start_char = ziffer.ursprungschar
        aap_tabelle[start_char] = {}
        # iteriere durch alle möglichen Ziel chars
        for zielchar in versuchsliste:

            change_inf = change_inf_tabelle[start_char][zielchar]  # change Information
            if actions_left < change_inf.min_aktion:  # wenn für diese Umwandlung nicht genügend Aktionen übrig sind
                continue

            new_value = [change_inf.hin - change_inf.min_aktion,
                         change_inf.weg - change_inf.min_aktion]  # der Mindestwert

            # [ausgleich von offers, ausgleich von requests]

            for k in aap_tabelle[start_char]:  # schaut sich die Ausgleiche von aktionen an mit
                if k <= change_inf.min_aktion:  # wenn schonmal mit max gleich vielen aktionen besser ausgeglichen wurde
                    if aap_tabelle[start_char][k][0] > new_value[0]:
                        new_value[0] = aap_tabelle[start_char][k][0]  # der neue Value übernimmt den besseren
                    if aap_tabelle[start_char][k][1] > new_value[1]:
                        new_value[1] = aap_tabelle[start_char][k][1]  # der neue Value übernimmt den besseren
            useless = []
            for k in aap_tabelle[start_char]:  # schaut sich die ausgleiche von anden
                if k > change_inf.min_aktion:  # die situationen beidem mehr aktionen verfügbar waren
                    if aap_tabelle[start_char][k][0] < new_value[0]:
                        aap_tabelle[start_char][k][0] = new_value[0]
                    if aap_tabelle[start_char][k][1] < new_value[1]:
                        aap_tabelle[start_char][k][1] = new_value[1]
                    if aap_tabelle[start_char][k] == new_value:  # wenn durch mehr aktionen nichts gewonnen wurde
                        useless.append(k)  # können wir uns diesen Vermerk sparen
            for r in useless: aap_tabelle[start_char].pop(r)
            aap_tabelle[ziffer.ursprungschar][change_inf.min_aktion] = new_value
    return aap_tabelle


def gen_ausgleichstabelle():
    tabelle = {}
    base_ausgleichs_tabelle = allgemeines_ausgleichs_potenzial()

    for i in range(len(ziffern) - 1, -1, -1):  # gehe alle ziffern Rückwerts durch
        ziffer = ziffern[i]  # spalte für ziffer i
        tabelle[i] = base_ausgleichs_tabelle[ziffer.ursprungschar].copy()

        # Ein bezug der Ergebnisse der oberen Ergebnisse
        if i + 1 not in tabelle: continue  # wenn es obere Ergebnisse gibt

        temp_keys = list(tabelle[i])[:]
        for obere_akt in tabelle[i + 1]:
            for geg_akt in temp_keys:
                new_akt = geg_akt + obere_akt
                if new_akt > actions_left: continue
                tabelle[i][new_akt] = [tabelle[i][geg_akt][0] + tabelle[i + 1][obere_akt][0],
                                       tabelle[i][geg_akt][1] + tabelle[i + 1][obere_akt][1]]
    return tabelle


def best_ausgleich():
    global index, actions_left
    max_ausgleich = (0, 0)
    if index < len(ziffern):
        for i in range(actions_left, -1, -1):
            if i not in ausgleichswert_tabelle[index]: continue
            max_ausgleich = ausgleichswert_tabelle[index][i]
            break
    return max_ausgleich


if __name__ == '__main__':
    ziffern_models = {
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
    versuchsliste = "FEDCBA9876543210"  # Hex-Zahlen zum durch iterieren
    offers = requests = index = 0

    pfad = f"hexmax5.txt"  # input("Geben sie den Pfad zur Input-Datei an:\n->")
    ziffern, actions_left = get_input(pfad)  # input aus Text-Datei

    change_inf_tabelle = gen_tabelle()  # change_inf_tabelle[start][ziel]
    ausgleichswert_tabelle = gen_ausgleichstabelle()

    sys.setrecursionlimit(len(ziffern) * len(versuchsliste) + 1)  # maximum of recursions depth
    maximiere_ziffern()  # haupt funktion
    ausgabe()
