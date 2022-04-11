import sys  # um die Rekursionstiefe zu modifizieren


class ZifferSystem:

    def __init__(self, char):
        self.positions = ziffern_models[char][:]  # kopiere die Instanz, sodas keine Referenz mehr existiert
        self.notyet_empty_indeces = []
        self.notyet_filled_indeces = []
        self.char = char
        self.ursprungschar = char

    def set_ziel_char(self, ziel_char):
        self.char = ziel_char  # setzt den char zum ziel
        model = ziffern_models[ziel_char]
        self.notyet_empty_indeces.clear()
        self.notyet_filled_indeces.clear()
        for i in range(7):
            if model[i] != self.positions[i]:
                if model[i]:
                    self.notyet_filled_indeces.append(i)
                else:
                    self.notyet_empty_indeces.append(i)  # sticks müssen von Pos weggenommen werden
        return len(self.notyet_empty_indeces), len(self.notyet_filled_indeces)


class ZiffernChangeInformation:

    def __init__(self, weg, hin, _notyet_empty_indeces, _notyet_filled_indeces):
        self.min_aktion = min(weg, hin)
        self.weg = weg
        self.hin = hin
        self.stick_mangel = hin - weg  # wie viel Sticks hinzugefügt werden müssen, wenn <0 haben wir stick Überschuss
        self.notyet_empty_indeces = _notyet_empty_indeces
        self.notyet_filled_indeces = _notyet_filled_indeces


def get_input():
    pfad = "hexmax5.txt"  # input("Geben sie den Pfad zur Input-Datei an:\n->")
    text = open(pfad, "r").read()
    zeilen = text.split("\n")
    _ziffern = [ZifferSystem(char) for char in zeilen[0]]  # Instanziierung der Ziffernsysteme
    return _ziffern, int(zeilen[1])  # Ziffern und Aktionen


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
    global angebot, nachfrage
    bu_offers, bu_requests = angebot, nachfrage  # backup

    change_inf = change_inf_tabelle[start_char][ziel_char]
    aktionen = change_inf.min_aktion  # es müssen mindestens die unter einander zu tauschenden sticks
    if change_inf.stick_mangel > 0:  # es wird aus angebot genommen
        angebot -= change_inf.stick_mangel  # angebot verringert sich
        if angebot < 0:  # es muss eine eigene request aufgegeben werden...
            aktionen -= angebot  # ...das ist eine extra aktion
            nachfrage -= angebot
            angebot = 0  # ...da angebot auf 0 gesetzt wird
    elif change_inf.stick_mangel < 0:  # es wird aus nachfrage genommen
        nachfrage += change_inf.stick_mangel  # so viele es nachfrage werden befriedigt
        if nachfrage < 0:  # es muss ein angebot für alle sichtbar erstellt werden
            aktionen -= nachfrage  # das kostet
            angebot -= nachfrage  # angebot erhöht sich
            nachfrage = 0
    return aktionen, bu_offers, bu_requests


def maximiere_ziffern():
    global actions_left, index, angebot, nachfrage
    if 0 == angebot - nachfrage:
        if index == len(ziffern):  # wenn es keine Ziffern mehr zum Verändern gibt
            return True

    aktuelle_ziffer = ziffern[index]  # betrachtete aktuelle Ziffer
    for char in versuchsliste:
        # Simuliert das Umwandeln dieser Ziffer und returned die Situation wie sie dann aussehen wird
        aktionen, bu_offers, bu_requests = simulate_change(aktuelle_ziffer.ursprungschar, char)
        # macht backup von dieser Situation
        actions_left -= aktionen
        if actions_left >= 0:  # wenn mehr Aktionen gebraucht als verfügbar, diese Ziffer unmöglich
            zielausgleich = angebot + nachfrage  # angebot oder nachfrage ist 0
            index += 1
            ausgleichswert = best_ausgleich()
            if ausgleichswert[
                0 if angebot > 0 else 1] >= zielausgleich:  # wenn Zielausgleich nicht erreicht werden kann
                aktuelle_ziffer.char = char
                if maximiere_ziffern():
                    return True
                aktuelle_ziffer.char = aktuelle_ziffer.ursprungschar
            index -= 1
        # Simulation rückgängig machen
        actions_left += aktionen
        angebot, nachfrage = bu_offers, bu_requests
    return False


def gen_tabelle_c_inf():
    # t[start][ziel]
    tabelle = {}
    for z in ziffern:
        if z.ursprungschar in tabelle: continue
        tabelle[z.ursprungschar] = {}
        for char in versuchsliste:
            wegnehmen, hinzulegen = z.set_ziel_char(char)
            tabelle[z.ursprungschar][char] = ZiffernChangeInformation(wegnehmen, hinzulegen, z.notyet_empty_indeces[:],
                                                                      z.notyet_filled_indeces[:])
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

            # [ausgleich von angebot, ausgleich von nachfrage]
            for k in aap_tabelle[start_char]:  # schaut sich die Ausgleiche von aktionen an mit
                if k <= change_inf.min_aktion:  # wenn schonmal mit max gleich vielen aktionen besser ausgeglichen wurde
                    if aap_tabelle[start_char][k][0] > new_value[0]:
                        new_value[0] = aap_tabelle[start_char][k][0]  # der neue Value übernimmt den besseren
                    if aap_tabelle[start_char][k][1] > new_value[1]:
                        new_value[1] = aap_tabelle[start_char][k][1]  # der neue Value übernimmt den besseren
            for k in aap_tabelle[start_char]:  # schaut sich die ausgleiche von anden
                if k > change_inf.min_aktion:  # die situationen beidem mehr aktionen verfügbar waren
                    if aap_tabelle[start_char][k][0] < new_value[0]:
                        aap_tabelle[start_char][k][0] = new_value[0]
                    if aap_tabelle[start_char][k][1] < new_value[1]:
                        aap_tabelle[start_char][k][1] = new_value[1]
            aap_tabelle[ziffer.ursprungschar][change_inf.min_aktion] = new_value
    aap_tabelle = entferne_unnötige_zellen(aap_tabelle)
    return aap_tabelle


def entferne_unnötige_zellen(dictionary):
    for char in dictionary:
        while True:
            to_remove = None
            keys = list(dictionary[char])[:]
            keys.sort()
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    if dictionary[char][keys[i]] != dictionary[char][keys[j]]: continue
                    to_remove = keys[j]
                    break
                if to_remove is not None: break
            if to_remove is None: break
            dictionary[char].pop(to_remove)
    return dictionary


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
    angebot = nachfrage = index = 0

    ziffern, actions_left = get_input()  # input aus Text-Datei

    change_inf_tabelle = gen_tabelle_c_inf()  # change_inf_tabelle[start][ziel]
    ausgleichswert_tabelle = gen_ausgleichstabelle()

    sys.setrecursionlimit(len(ziffern) * len(versuchsliste) + 1)  # maximum of recursions depth
    maximiere_ziffern()  # haupt funktion
    ausgabe()
