class Edge:  # [start,stop,weight]
    id_increase = 0

    def __init__(self, start, stop, weight):
        self.id = Edge.id_increase
        Edge.id_increase += 1

        self.start = start
        self.stop = stop
        self.weight = weight
        self.used = 0  # A car used this edge n times

    def __eq__(self, other):
        return self.id == other  # um geblockte streets zu erkennen

    def other_crossing(self, crossing_id):
        return self.start if crossing_id == self.stop else self.stop
