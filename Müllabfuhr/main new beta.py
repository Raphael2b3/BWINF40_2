from typing import List
from performance_analysing import *
import prozessbar


class Path:
    # Quasi wie eine Liste lauter streets
    # start: int ID von Crossing

    def __init__(self, start):
        if start == "inf":
            self.weight = float("inf")
            return
        self.start: int = start
        self.streets: List[Street] = []
        self.weight = 0
        self.crossings: List[Crossing] = [crossings[start]]
        self.position = self.crossings[-1]

    def append(self, street):
        self.streets.append(street)
        self.weight += street.weight
        self.crossings.append(street.other_crossing(self.crossings[-1].id))
        self.position = self.crossings[-1]

    def copy(self):
        t = Path(self.start)
        t.streets = self.streets[:]
        t.weight = self.weight
        t.crossings = self.crossings[:]
        t.position = self.position
        return t

    def reverse(self):
        self.start = self.crossings[-1].id
        self.streets.reverse()
        self.crossings.reverse()
        self.position = self.crossings[-1]

    def __str__(self):
        t = f"__Weg__\nInsgesammte Strecke: {self.weight}\nRoute:K{self.start}"
        for goal in self.crossings[1:]:
            t += f"->K{goal.id}"
        return t


class Street:
    def __init__(self, start, stop, weight, _id):
        self.id = _id
        self.start = start
        self.stop = stop
        self.weight = weight
        self.used = False

    def __eq__(self, other):
        return self.id == other  # um geblockte streets zu erkennen

    def __gt__(self, other):
        return self.weight > other

    def __lt__(self, other):
        return self.weight < other

    def other_crossing(self, crossing_id):
        return crossings[self.start] if crossing_id == self.stop else crossings[self.stop]


class Crossing:

    def __init__(self, _id, _streets):
        self.streets = _streets
        self.id = _id

    def __eq__(self, other):
        return self.id == other  # wenn geguckt wird, ob ein crossing schon bekannt ist


def print_solution():
    new_cars = [Car(start_position) for _ in range(days)]
    for i in range(days):
        car = cars[i]
        allstreets = []
        for s in car.streets:
            for t in inner_streets(s):
                allstreets.append(t)
        cposition = start_position
        while len(allstreets) > 0:
            choice = None
            for s in allstreets:
                if s.start == cposition or s.stop == cposition:
                    choice = s
                    break
            new_cars[i].append(choice)
            cposition = choice.other_crossing(cposition).id
            allstreets.remove(choice)

    print("\n\nErgebnis:")
    for tag in range(days):
        print("Tag", tag + 1, ":")
        print(new_cars[tag])
        print()
    print("-Ende-")


def get_input():
    path = "muellabfuhr8.txt"
    text = open(path, "r").read()
    lines = text.split("\n")
    lines.pop(-1)
    _streets = []  # sammelt alle gegebenen Kanten
    for i in range(1, len(lines)):
        values = lines[i].split(" ")
        _streets.append(Street(int(values[0]), int(values[1]), int(values[2]), i - 1))
    _crossing = []
    values = lines[0].split(" ")
    for crossing_id in range(int(values[0])):
        tmp_streets = []
        for _street in _streets:
            if _street.start == crossing_id or _street.stop == crossing_id:
                tmp_streets.append(_street)
        _crossing.append(Crossing(crossing_id, tmp_streets))
    return _crossing, _streets


def dijkstra_algorithm(_start_id, blocked_streets=None):
    if blocked_streets is None: blocked_streets = []
    paths = [INF_PATH for _ in range(n_crossings)]
    paths[_start_id] = Path(_start_id)
    finished = [False for _ in range(n_crossings)]

    cur_crossing_id = _start_id
    while False in finished:
        cur_crossing = crossings[cur_crossing_id]

        finished[cur_crossing_id] = True
        path: Path = paths[cur_crossing_id]

        for street in cur_crossing.streets:
            if street in blocked_streets: continue
            goal = street.other_crossing(cur_crossing_id)
            if finished[goal.id]: continue
            if path.weight + street.weight >= paths[goal.id].weight: continue

            goal_path = path.copy()

            goal_path.append(street)

            paths[goal.id] = goal_path

        for i in range(n_crossings):
            if finished[i]: continue  # nicht wenn crossings fertig
            if finished[cur_crossing_id]:  # wenn betrachteter Fertig wechseln!
                cur_crossing_id = i
                continue
            if paths[cur_crossing_id].weight <= paths[i].weight: continue
            # bleibt bei dem i welches die kleinste distanz hat
            cur_crossing_id = i
        if paths[cur_crossing_id].weight == float("inf"):
            break  # abbruch weil nicht erreichbar
    return paths


def find_cheapest_euler_combination(elements, combinations, best_result=(float("inf"), [])):
    if len(elements) == 0:
        weight = 0
        for kombi in combinations:
            a, b = kombi
            paths = get_shortest_paths(a.id)
            p = paths[b.id]
            weight += p.weight
        return (weight, combinations[:]) if weight < best_result[0] else best_result
    base = elements.pop(-1)
    for i in range(len(elements)):
        choose = elements.pop(i)
        combo = (base, choose)
        combinations.append(combo)
        best_result = find_cheapest_euler_combination(elements, combinations, best_result)
        combinations.pop(-1)
        elements.insert(i, choose)
    elements.append(base)
    return best_result


def eulerize_graph():
    streets_usable = {}
    for s in streets:
        streets_usable[s.id] = 1
    for pare in euler_combinations:
        a, b = pare
        paths = get_shortest_paths(a.id)
        p = paths[b.id]
        for street in p.streets:
            streets_usable[street.id] += 1
    return streets_usable


def get_shortest_paths(start, blocked=None):
    if blocked is not None:
        return dijkstra_algorithm(start, blocked)
    if not start in shortest_paths:
        shortest_paths[start] = dijkstra_algorithm(start)
    return shortest_paths[start]


get_time("Start")


class Car(Path):
    def __init__(self, start):
        super(Car, self).__init__(start)
        self.blocked = []
        self.count = {}
        self.street_usable = eulerize_graph()

    def move(self, path):
        global n_cleared_streets
        for s in path.streets:
            self.street_usable[s.id] -= 1
            if self.street_usable[s.id] == 0:
                self.blocked.append(s)
            if not s.used:
                s.used = True
                n_cleared_streets += 1
            self.append(s)

    def path_allowed(self, path):
        start = path.position.id

        future_blocked = []
        tmp_usable_inf = self.street_usable.copy()

        for s in path.streets:
            if s not in blocked_streets: continue
            tmp_usable_inf[s.id] -= 1
            if tmp_usable_inf[s.id] == 0:
                future_blocked.append(s)
        connection_paths = get_shortest_paths(start, self.blocked + future_blocked)
        for s in usable_streets:
            if not s.used and s not in self.blocked and connection_paths[s.start].weight == float("inf"):
                return False
        return True


def best_car(street: Street):  # returns the car with the less weight
    best_c = None  # best car
    best_p = None  # best path
    for car in cars:
        paths = get_shortest_paths(car.position.id)
        a = paths[street.start]
        b = paths[street.stop]
        bp = a.copy() if a.weight < b.weight else b.copy()
        # Check if enough streets are available
        bp.append(street)
        if not car.path_allowed(bp): continue
        if best_p is None or car.weight + bp.weight < best_c.weight + best_p.weight:
            best_c = car
            best_p = bp
    return best_c, best_p


def reduce_graph():
    global crossings
    for cross in crossings[1:]:
        av_st = cross.streets[:]
        if len(av_st) == 2:
            length = av_st[0].weight + av_st[1].weight
            start = av_st[0].other_crossing(cross.id)
            stop = av_st[1].other_crossing(cross.id)
            _id = n_streets + len(supportive_streets)
            new_street = Street(start.id, stop.id, length, _id)

            streets.remove(av_st[1])
            streets.remove(av_st[0])
            supportive_streets[_id] = av_st

            streets.append(new_street)

            start.streets.remove(av_st[0])
            start.streets.append(new_street)

            stop.streets.remove(av_st[1])
            stop.streets.append(new_street)

            ignored_crossings.append(cross)
        elif len(av_st) == 1:  # Sackgasse
            length = av_st[0].weight * 2
            stop = start = av_st[0].other_crossing(cross.id)
            _id = n_streets + len(supportive_streets)
            new_street = Street(start.id, stop.id, length, _id)
            streets.remove(av_st[0])
            supportive_streets[_id] = av_st + av_st
            streets.append(new_street)
            start.streets.remove(av_st[0])
            start.streets.append(new_street)
            ignored_crossings.append(cross)


def inner_streets(_street):
    if _street.id not in supportive_streets: return [_street]
    c = []
    for strt in supportive_streets[_street.id]:
        c += inner_streets(strt)
    return c


if __name__ == '__main__':
    # Consts
    INF_PATH = Path("inf")
    cars_left = days = 5  # von montag bis freitag sind 5 tage
    start_position = 0
    n_cleared_streets = 0
    remove_list = []
    blocked_streets = []
    ignored_crossings = []
    shortest_paths = {}
    supportive_streets = {}
    crossings, streets = get_input()
    streets.sort(reverse=True)
    n_crossings = len(crossings)
    n_streets = len(streets)
    reduce_graph()
    bad_crossings = []
    for c in crossings:
        if len(c.streets) % 2 != 0:
            bad_crossings.append(c)
    _, euler_combinations = find_cheapest_euler_combination(bad_crossings, [])

    cars = [Car(start_position) for i in range(days)]  # erstelle 5 car Klassen

    prozessbar.goal = n_streets = len(streets)
    car = None
    usable_streets = streets[:]
    while n_cleared_streets < n_streets:
        prozessbar.show_state(n_cleared_streets)
        remove_list.clear()
        for street in usable_streets:  # longer ones at first
            if street.used:
                remove_list.append(street)
                continue
            car, path = best_car(street)
            if car is None: continue
            car.move(path)
            break
        for r in remove_list:
            usable_streets.remove(r)

    waybacks = get_shortest_paths(0)
    for auto in cars:
        wb = waybacks[auto.position.id].copy()
        wb.reverse()
        auto.move(wb)

    for s in streets:
        if not s.used:
            input("YARAK")

    print_solution()

get_time("Stop")

"""
days = 1, input = 8.txt

 100% [####################]

Ergebnis:
Tag 1 :
__Weg__
Insgesammte Strecke: 13330203
Route:K0->K310->K420->K294->K0->K952->K824->K205->K528->K934->K205->K323->K528->K703->K628->K31->K359->K628->K348->K916->K359->K703->K960->K348->K31->K916->K628->K426->K934->K703->K348->K810->K146->K633->K810->K756->K633->K916->K181->K725->K684->K820->K21->K725->K179->K554->K694->K974->K853->K554->K974->K200->K420->K0->K303->K593->K479->K281->K922->K664->K784->K768->K992->K314->K370->K991->K314->K558->K241->K662->K182->K251->K111->K914->K525->K229->K251->K404->K894->K44->K404->K343->K894->K251->K525->K182->K111->K526->K722->K914->K526->K525->K662->K111->K722->K980->K610->K722->K229->K182->K241->K525->K722->K662->K558->K182->K914->K251->K343->K611->K827->K7->K994->K718->K7->K611->K994->K827->K718->K269->K268->K718->K305->K185->K884->K243->K268->K493->K552->K280->K584->K552->K503->K493->K280->K503->K584->K493->K555->K273->K884->K555->K428->K593->K0->K281->K952->K420->K1->K122->K776->K238->K37->K776->K889->K959->K442->K889->K460->K122->K708->K294->K310->K824->K788->K922->K952->K205->K788->K934->K628->K810->K359->K647->K556->K467->K647->K426->K960->K528->K348->K633->K960->K916->K146->K647->K31->K810->K960->K146->K31->K426->K783->K120->K380->K40->K85->K222->K380->K392->K40->K826->K380->K783->K40->K649->K490->K958->K856->K598->K602->K788->K952->K200->K1->K460->K238->K889->K122->K220->K303->K310->K200->K853->K694->K179->K181->K684->K707->K129->K655->K190->K87->K318->K354->K87->K292->K586->K211->K292->K845->K188->K354->K888->K188->K318->K292->K354->K190->K318->K586->K87->K211->K845->K318->K888->K163->K949->K757->K83->K912->K163->K83->K439->K601->K497->K398->K476->K27->K712->K476->K601->K398->K27->K757->K538->K60->K421->K637->K60->K27->K421->K538->K637->K875->K60->K221->K619->K961->K2->K173->K459->K478->K177->K459->K901->K402->K962->K578->K99->K529->K982->K99->K962->K865->K578->K402->K529->K901->K99->K865->K529->K338->K339->K59->K261->K671->K802->K400->K261->K802->K932->K887->K195->K932->K59->K400->K671->K339->K261->K88->K367->K759->K700->K41->K726->K700->K410->K726->K759->K41->K410->K759->K137->K41->K367->K189->K379->K137->K700->K208->K627->K435->K35->K790->K435->K208->K488->K35->K102->K435->K488->K627->K35->K274->K735->K242->K274->K608->K615->K919->K264->K308->K11->K267->K264->K11->K246->K299->K194->K311->K679->K809->K866->K917->K774->K754->K917->K289->K133->K667->K289->K580->K133->K754->K866->K679->K171->K641->K114->K386->K283->K641->K234->K114->K171->K386->K234->K285->K175->K96->K285->K508->K650->K65->K331->K508->K93->K650->K175->K234->K283->K114->K679->K386->K93->K65->K418->K413->K553->K674->K413->K96->K234->K508->K283->K93->K234->K650->K418->K331->K175->K413->K996->K500->K714->K851->K500->K553->K996->K15->K714->K709->K800->K864->K851->K15->K709->K851->K996->K714->K590->K709->K233->K800->K590->K813->K657->K38->K998->K696->K334->K734->K696->K199->K295->K513->K812->K334->K295->K812->K734->K295->K739->K687->K265->K78->K797->K739->K199->K78->K696->K813->K38->K531->K689->K215->K581->K313->K531->K215->K358->K10->K536->K254->K10->K226->K792->K29->K28->K226->K29->K10->K792->K358->K254->K668->K536->K226->K254->K576->K504->K5->K576->K536->K854->K778->K116->K155->K659->K140->K677->K139->K5->K778->K358->K155->K140->K551->K677->K659->K116->K854->K313->K29->K689->K22->K581->K38->K689->K854->K10->K28->K358->K689->K91->K215->K792->K536->K155->K677->K721->K140->K5->K659->K139->K551->K721->K89->K413->K15->K553->K636->K416->K113->K938->K356->K13->K330->K938->K13->K822->K971->K646->K55->K971->K956->K55->K822->K356->K847->K252->K506->K612->K969->K506->K695->K612->K648->K695->K972->K957->K881->K271->K706->K957->K271->K897->K944->K434->K890->K383->K944->K577->K151->K890->K944->K607->K388->K90->K408->K417->K90->K607->K408->K144->K388->K417->K180->K123->K481->K90->K180->K388->K123->K417->K607->K434->K388->K481->K434->K577->K706->K151->K245->K997->K799->K979->K542->K799->K245->K383->K151->K997->K979->K383->K799->K782->K890->K144->K417->K999->K843->K247->K758->K101->K549->K758->K843->K678->K247->K999->K678->K101->K547->K276->K101->K999->K123->K878->K157->K51->K724->K157->K409->K73->K993->K378->K559->K654->K587->K159->K653->K806->K159->K654->K900->K924->K930->K825->K719->K699->K332->K719->K930->K900->K836->K924->K825->K688->K656->K192->K387->K656->K336->K688->K699->K515->K332->K924->K719->K336->K825->K900->K587->K559->K142->K378->K73->K68->K993->K409->K378->K68->K724->K569->K68->K51->K123->K101->K883->K250->K621->K883->K547->K845->K250->K518->K609->K814->K112->K744->K794->K491->K710->K794->K396->K502->K570->K463->K396->K491->K744->K9->K112->K389->K3->K483->K755->K571->K483->K389->K744->K814->K445->K572->K518->K621->K586->K188->K292->K190->K129->K574->K345->K767->K707->K574->K767->K820->K574->K21->K179->K974->K634->K449->K79->K976->K634->K460->K451->K959->K449->K451->K442->K460->K37->K122->K442->K79->K570->K396->K832->K745->K522->K563->K832->K570->K976->K694->K725->K554->K323->K934->K602->K426->K556->K810->K647->K628->K556->K826->K120->K392->K222->K120->K85->K380->K649->K85->K125->K781->K12->K868->K862->K18->K986->K862->K371->K730->K811->K520->K670->K566->K520->K258->K566->K34->K32->K405->K34->K520->K730->K909->K405->K424->K118->K32->K424->K34->K258->K811->K371->K729->K18->K371->K12->K811->K670->K34->K909->K371->K868->K751->K862->K729->K868->K986->K186->K217->K109->K296->K61->K704->K517->K470->K704->K630->K808->K470->K630->K61->K517->K630->K742->K815->K248->K848->K815->K462->K248->K130->K219->K346->K575->K219->K176->K130->K575->K495->K740->K816->K838->K597->K803->K964->K597->K557->K202->K300->K557->K964->K300->K597->K202->K964->K838->K740->K597->K145->K803->K557->K838->K300->K47->K218->K127->K39->K981->K835->K987->K203->K216->K411->K921->K33->K673->K148->K747->K145->K964->K740->K557->K47->K127->K399->K134->K77->K785->K62->K777->K983->K62->K939->K301->K942->K904->K823->K942->K198->K301->K904->K284->K539->K643->K284->K36->K666->K834->K923->K761->K857->K256->K761->K834->K857->K403->K675->K43->K240->K891->K635->K240->K546->K43->K603->K675->K178->K225->K453->K626->K446->K365->K214->K523->K132->K53->K605->K523->K53->K352->K132->K214->K626->K953->K453->K365->K626->K225->K132->K626->K523->K352->K605->K471->K431->K533->K850->K431->K995->K407->K452->K995->K231->K472->K850->K407->K533->K995->K472->K533->K231->K255->K666->K256->K834->K36->K255->K995->K850->K231->K407->K472->K57->K541->K720->K537->K124->K541->K918->K124->K57->K720->K717->K537->K918->K935->K270->K618->K206->K16->K663->K270->K206->K663->K937->K406->K450->K737->K514->K561->K737->K651->K469->K335->K651->K885->K514->K651->K561->K885->K335->K937->K450->K561->K469->K514->K335->K406->K737->K631->K791->K705->K715->K876->K925->K288->K977->K390->K477->K257->K266->K594->K347->K350->K475->K973->K326->K475->K347->K266->K350->K594->K863->K266->K475->K775->K560->K966->K321->K736->K103->K321->K733->K926->K990->K733->K966->K775->K973->K350->K326->K393->K150->K613->K842->K164->K196->K516->K613->K196->K482->K805->K196->K150->K805->K842->K482->K516->K805->K100->K474->K191->K805->K474->K752->K342->K877->K618->K16->K270->K899->K918->K720->K850->K717->K828->K829->K304->K908->K622->K304->K197->K482->K164->K613->K540->K298->K103->K560->K733->K103->K210->K322->K870->K333->K117->K369->K333->K322->K4->K412->K322->K117->K870->K369->K115->K839->K623->K903->K115->K623->K369->K903->K839->K770->K954->K263->K156->K892->K228->K596->K892->K898->K69->K535->K898->K156->K228->K263->K596->K156->K69->K465->K355->K496->K290->K30->K911->K466->K290->K355->K535->K760->K527->K72->K168->K873->K527->K168->K69->K527->K596->K954->K228->K253->K415->K355->K30->K496->K158->K253->K892->K954->K156->K770->K263->K903->K117->K115->K333->K903->K870->K210->K736->K966->K298->K736->K4->K321->K926->K379->K88->K137->K726->K412->K394->K841->K617->K167->K766->K141->K385->K277->K71->K201->K821->K277->K307->K104->K645->K307->K385->K71->K307->K595->K104->K928->K595->K645->K484->K357->K645->K928->K307->K484->K104->K277->K201->K588->K308->K615->K672->K264->K615->K275->K919->K672->K267->K299->K353->K194->K246->K264->K299->K11->K915->K357->K104->K385->K167->K201->K766->K617->K394->K141->K617->K201->K141->K71->K588->K277->K766->K841->K410->K627->K790->K208->K759->K189->K137->K4->K210->K117->K623->K333->K4->K103->K926->K966->K540->K775->K733->K736->K322->K369->K257->K297->K863->K347->K973->K560->K298->K775->K393->K540->K164->K150->K191->K565->K75->K642->K474->K342->K565->K877->K270->K75->K899->K877->K752->K75->K918->K642->K124->K75->K935->K618->K75->K877->K663->K406->K651->K450->K335->K561->K406->K977->K206->K390->K297->K266->K973->K393->K516->K540->K326->K594->K257->K347->K990->K59->K338->K99->K459->K876->K791->K715->K606->K177->K901->K478->K876->K606->K2->K690->K315->K317->K70->K910->K690->K70->K793->K58->K401->K562->K278->K401->K793->K600->K910->K317->K690->K961->K315->K70->K58->K317->K793->K910->K315->K306->K165->K961->K306->K712->K398->K306->K476->K912->K27->K538->K949->K83->K601->K368->K377->K943->K568->K98->K377->K568->K368->K439->K497->K312->K786->K135->K98->K258->K32->K566->K405->K730->K862->K12->K730->K566->K811->K781->K6->K154->K125->K6->K868->K125->K811->K729->K751->K18->K186->K109->K61->K816->K742->K740->K575->K462->K848->K76->K230->K716->K77->K62->K589->K351->K983->K732->K777->K351->K904->K939->K983->K198->K62->K134->K198->K732->K939->K942->K539->K301->K589->K939->K777->K399->K945->K777->K785->K399->K732->K942->K284->K666->K923->K256->K403->K43->K178->K603->K240->K675->K891->K178->K403->K923->K36->K256->K643->K666->K857->K603->K891->K953->K546->K675->K225->K403->K834->K643->K823->K301->K983->K136->K899->K663->K136->K935->K541->K717->K533->K452->K431->K231->K452->K352->K407->K255->K643->K231->K57->K823->K36->K539->K57->K537->K642->K717->K431->K828->K850->K537->K752->K100->K482->K613->K805->K164->K873->K197->K591->K908->K153->K829->K591->K622->K873->K304->K153->K197->K100->K908->K829->K471->K452->K761->K603->K635->K43->K100->K304->K828->K908->K482->K622->K153->K591->K290->K235->K466->K30->K415->K496->K466->K214->K446->K466->K523->K471->K995->K53->K365->K605->K214->K953->K240->K178->K453->K546->K178->K635->K953->K365->K235->K30->K253->K898->K158->K465->K415->K290->K158->K535->K72->K228->K69->K355->K911->K496->K535->K168->K898->K596->K770->K623->K595->K385->K201->K484->K915->K308->K672->K11->K919->K267->K915->K71->K484->K277->K357->K928->K770->K115->K870->K412->K841->K41->K412->K137->K926->K560->K266->K477->K977->K376->K631->K514->K937->K737->K469->K411->K203->K673->K880->K278->K405->K520->K32->K278->K118->K562->K880->K33->K216->K987->K981->K47->K964->K896->K803->K202->K838->K495->K346->K815->K495->K816->K597->K470->K109->K711->K149->K507->K186->K296->K507->K470->K764->K262->K25->K510->K262->K808->K764->K711->K517->K507->K704->K764->K630->K964->K816->K517->K262->K704->K711->K217->K986->K371->K125->K258->K781->K371->K751->K217->K18->K868->K154->K12->K751->K154->K419->K166->K349->K419->K362->K174->K370->K362->K349->K859->K660->K530->K846->K213->K14->K162->K430->K14->K644->K749->K423->K686->K731->K423->K530->K14->K749->K686->K644->K213->K749->K846->K644->K423->K213->K530->K644->K162->K846->K967->K660->K423->K14->K660->K749->K731->K25->K686->K530->K859->K423->K162->K686->K213->K430->K749->K510->K644->K660->K686->K510->K848->K130->K462->K76->K346->K176->K218->K981->K202->K740->K300->K835->K127->K202->K218->K399->K77->K198->K777->K136->K589->K198->K785->K716->K34->K786->K424->K566->K118->K135->K543->K497->K712->K421->K757->K601->K912->K538->K163->K188->K949->K888->K83->K476->K439->K398->K543->K786->K98->K392->K85->K6->K419->K859->K731->K149->K217->K747->K186->K149->K109->K747->K896->K981->K300->K145->K838->K219->K230->K785->K191->K342->K477->K350->K863->K865->K982->K402->K177->K982->K578->K338->K286->K542->K245->K890->K979->K286->K887->K802->K339->K932->K400->K189->K700->K88->K339->K400->K379->K671->K932->K286->K195->K773->K95->K831->K648->K956->K955->K55->K366->K236->K488->K172->K366->K955->K646->K13->K971->K847->K291->K933->K126->K468->K933->K579->K468->K291->K126->K579->K128->K970->K936->K763->K970->K86->K936->K512->K940->K564->K524->K940->K341->K564->K512->K524->K341->K946->K669->K741->K927->K858->K989->K927->K616->K989->K121->K616->K741->K989->K849->K121->K138->K950->K391->K108->K501->K375->K738->K316->K272->K738->K501->K81->K272->K375->K108->K585->K316->K108->K738->K81->K375->K585->K391->K316->K81->K984->K920->K796->K984->K532->K287->K867->K63->K532->K81->K920->K63->K789->K441->K260->K687->K295->K78->K687->K199->K334->K813->K734->K199->K797->K265->K64->K78->K334->K998->K657->K734->K998->K813->K714->K864->K996->K674->K96->K331->K89->K659->K551->K93->K641->K866->K289->K285->K774->K133->K113->K580->K416->K938->K291->K506->K648->K969->K105->K693->K184->K105->K612->K693->K969->K252->K612->K972->K95->K957->K897->K245->K782->K931->K177->K529->K293->K979->K931->K173->K478->K715->K910->K58->K600->K70->K961->K221->K875->K619->K637->K221->K165->K619->K173->K383->K577->K144->K782->K619->K2->K459->K982->K962->K338->K982->K606->K901->K931->K459->K715->K925->K791->K376->K390->K257->K475->K297->K288->K631->K705->K876->K631->K450->K885->K411->K651->K216->K673->K921->K469->K987->K39->K218->K557->K495->K742->K575->K76->K176->K47->K39->K945->K127->K987->K411->K737->K791->K561->K921->K600->K401->K33->K148->K880->K909->K32->K562->K58->K690->K793->K705->K921->K216->K885->K631->K925->K478->K2->K83->K368->K467->K377->K826->K467->K943->K135->K312->K315->K543->K601->K943->K439->K757->K888->K756->K354->K586->K883->K211->K655->K87->K756->K190->K181->K820->K707->K655->K181->K21->K554->K684->K574->K725->K853->K205->K0->K824->K974->K976->K451->K582->K563->K745->K440->K457->K713->K772->K440->K691->K414->K658->K676->K489->K787->K604->K437->K56->K604->K489->K658->K457->K745->K772->K691->K658->K440->K713->K414->K440->K563->K772->K414->K676->K787->K632->K772->K56->K638->K24->K499->K52->K161->K106->K52->K24->K161->K499->K638->K52->K855->K374->K571->K860->K743->K787->K860->K9->K483->K361->K374->K573->K728->K374->K830->K728->K755->K573->K830->K762->K329->K698->K620->K239->K360->K620->K279->K360->K363->K620->K329->K592->K762->K698->K239->K592->K882->K447->K599->K147->K852->K187->K147->K447->K320->K905->K485->K372->K978->K8->K683->K697->K395->K886->K906->K464->K702->K387->K688->K332->K583->K545->K515->K825->K836->K930->K699->K583->K20->K951->K975->K19->K951->K119->K975->K886->K697->K550->K397->K907->K550->K624->K750->K988->K328->K429->K436->K487->K373->K436->K521->K639->K544->K521->K382->K639->K433->K327->K207->K444->K640->K169->K97->K748->K968->K94->K97->K640->K968->K97->K455->K193->K170->K212->K682->K837->K212->K473->K455->K837->K364->K494->K929->K879->K947->K82->K748->K640->K94->K947->K486->K82->K968->K169->K748->K947->K929->K771->K494->K947->K771->K23->K486->K494->K82->K929->K23->K505->K907->K988->K629->K624->K397->K988->K373->K328->K750->K373->K429->K382->K505->K544->K429->K487->K328->K544->K327->K82->K97->K444->K169->K94->K486->K364->K771->K879->K82->K640->K947->K23->K494->K94->K444->K968->K486->K207->K748->K444->K82->K23->K433->K183->K521->K80->K309->K183->K80->K548->K804->K817->K461->K110->K45->K461->K804->K309->K548->K110->K817->K45->K427->K42->K324->K427->K443->K625->K324->K443->K779->K511->K443->K110->K427->K779->K625->K42->K309->K324->K461->K80->K42->K817->K80->K324->K110->K804->K183->K639->K487->K309->K427->K511->K625->K244->K780->K279->K239->K780->K511->K244->K436->K988->K550->K629->K8->K372->K187->K750->K8->K697->K397->K629->K978->K852->K599->K131->K425->K320->K66->K905->K20->K485->K425->K147->K372->K905->K119->K545->K902->K432->K985->K26->K913->K302->K26->K454->K872->K448->K438->K454->K302->K432->K818->K985->K913->K438->K224->K861->K746->K680->K861->K833->K895->K746->K833->K818->K107->K902->K985->K54->K432->K26->K54->K107->K159->K559->K227->K900->K719->K656->K825->K192->K464->K975->K702->K886->K464->K656->K699->K192->K583->K719->K515->K432->K833->K302->K872->K985->K746->K445->K680->K765->K3->K361->K830->K329->K855->K106->K24->K437->K489->K713->K563->K710->K522->K463->K582->K570->K21->K129->K820->K345->K794->K112->K3->K814->K518->K445->K3->K572->K112->K609->K621->K292->K883->K276->K678->K547->K549->K247->K547->K758->K276->K549->K685->K534->K653->K107->K432->K913->K224->K454->K66->K448->K224->K302->K861->K895->K680->K833->K224->K765->K861->K448->K913->K66->K438->K302->K902->K818->K26->K448->K765->K746->K818->K653->K685->K73->K534->K378->K569->K993->K559->K900->K336->K836->K587->K924->K699->K336->K924->K654->K142->K993->K724->K498->K384->K869->K259->K509->K807->K92->K249->K67->K340->K92->K67->K152->K340->K807->K259->K384->K569->K142->K587->K685->K993->K534->K806->K685->K559->K73->K724->K878->K409->K51->K498->K157->K569->K498->K259->K249->K340->K669->K341->K50->K753->K512->K86->K564->K184->K893->K524->K184->K86->K524->K384->K341->K753->K946->K849->K858->K741->K874->K204->K84->K143->K701->K84->K422->K701->K204->K143->K422->K727->K46->K798->K948->K49->K798->K950->K46->K948->K652->K801->K458->K681->K381->K337->K665->K237->K193->K473->K844->K223->K204->K74->K319->K223->K237->K844->K319->K682->K170->K319->K473->K223->K84->K282->K143->K74->K84->K844->K665->K193->K223->K665->K282->K701->K874->K74->K701->K727->K801->K681->K337->K237->K74->K152->K92->K840->K836->K719->K387->K682->K844->K204->K422->K665->K681->K282->K337->K458->K381->K801->K46->K49->K965->K948->K950->K108->K849->K927->K138->K849->K585->K946->K50->K512->K763->K941->K796->K723->K344->K441->K687->K513->K199->K812->K233->K864->K15->K636->K500->K413->K285->K114->K866->K171->K311->K809->K754->K667->K917->K133->K866->K667->K774->K96->K65->K175->K418->K721->K175->K674->K416->K468->K128->K941->K970->K468->K252->K971->K955->K822->K956->K646->K366->K567->K242->K236->K435->K410->K102->K627->K759->K435->K735->K567->K13->K366->K242->K35->K735->K608->K919->K246->K353->K672->K275->K274->K102->K488->K790->K274->K567->K356->K113->K330->K822->K252->K956->K773->K887->K542->K383->K997->K773->K648->K972->K881->K95->K695->K105->K506->K693->K893->K564->K50->K585->K753->K940->K519->K509->K249->K840->K67->K509->K152->K874->K989->K138->K108->K893->K972->K271->K95->K706->K972->K184->K763->K128->K819->K723->K920->K287->K456->K232->K867->K456->K871->K232->K769->K867->K789->K260->K513->K739->K260->K344->K796->K819->K344->K984->K723->K941->K984->K272->K532->K456->K769->K17->K480->K48->K661->K17->K325->K661->K963->K325->K480->K963->K17->K232->K480->K769->K661->K456->K48->K769->K325->K232->K287->K789->K687->K797->K295->K819->K579->K233->K590->K657->K334->K590->K734->K344->K789->K963->K48->K871->K287->K984->K63->K456->K441->K63->K871->K532->K441->K867->K871->K965->K798->K801->K948->K458->K46->K965->K652->K458->K49->K22->K313->K116->K581->K795->K998->K64->K22->K29->K668->K226->K504->K254->K792->K668->K576->K139->K504->K668->K28->K215->K10->K504->K778->K139->K171->K194->K672->K311->K246->K308->K275->K264->K608->K102->K735->K330->K646->K567->K189->K261->K379->K367->K208->K172->K367->K726->K617->K627->K172->K955->K195->K831->K972->K105->K970->K126->K938->K933->K128->K936->K753->K564->K519->K869->K893->K940->K86->K50->K375->K391->K849->K616->K727->K282->K381->K455->K212->K319->K837->K387->K212->K879->K906->K19->K886->K119->K485->K66->K131->K882->K599->K320->K131->K830->K882->K698->K360->K592->K279->K363->K106->K329->K52->K762->K882->K239->K329->K360->K780->K620->K395->K951->K8->K852->K629->K683->K395->K550->K683->K624->K429->K907->K629->K373->K147->K780->K779->K244->K324->K45->K548->K183->K382->K487->K324->K511->K279->K698->K363->K161->K638->K437->K743->K571->K573->K483->K743->K604->K860->K389->K572->K767->K518->K794->K463->K710->K744->K396->K522->K440->K582->K502->K491->K632->K743->K755->K106->K638->K604->K24->K56->K676->K691->K745->K442->K238->K708->K1->K294->K303->K708->K37->K889->K1->K6->K166->K362->K160->K492->K991->K362->K492->K598->K784->K856->K768->K664->K428->K273->K614->K209->K692->K273->K209->K884->K894->K243->K555->K209->K428->K479->K220->K776->K708->K420->K788->K281->K428->K768->K492->K370->K558->K967->K174->K991->K768->K209->K243->K7->K185->K273->K503->K614->K692->K243->K718->K185->K269->K305->K273->K493->K185->K552->K269->K7->K44->K251->K526->K980->K914->K610->K526->K182->K314->K174->K241->K229->K980->K111->K610->K662->K251->K980->K525->K343->K827->K44->K692->K555->K584->K593->K281->K303->K584->K479->K280->K268->K994->K305->K827->K404->K611->K718->K503->K593->K555->K280->K593->K614->K664->K856->K992->K784->K492->K349->K154->K166->K160->K856->K991->K160->K490->K120->K602->K958->K649->K160->K419->K490->K40->K467->K568->K826->K222->K783->K602->K490->K598->K768->K958->K784->K922->K0

-Ende-
Stop Currenttime: 1397.0103695392609 since last check: 1397.0101447105408

Process finished with exit code 0
"""
