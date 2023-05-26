from edge import Edge


def txt2mtrx(lines):
    """
    [
        [start, stop, weight],
        [start, stop, weight],
        ...
    ]

    :param lines: String "0 1 2\\n 0 2 1" node 0 to 1 with weight 2, node 0 to node 2 with weight 1
    :return: matrix that looks like above

    """
    mtrx = []
    for line in lines[1:]:
        content = line.split(" ")
        mtrx.append([int(a) for a in content])  # [start, stop, weight]
    return mtrx


def mtrx2graph(mtrx):
    edges = []  # sammelt alle gegebenen Kanten
    for start, stop, weight in mtrx:
        edges.append(Edge(start, stop, weight))

    _crossing = []
    values = lines[0].split(" ")
    for crossing_id in range(int(values[0])):
        tmp_streets = []
        for _street in _streets:
            if _street.start == crossing_id or _street.stop == crossing_id:
                tmp_streets.append(_street)
        _crossing.append(Crossing(crossing_id, tmp_streets))
    return _crossing, _streets


def get_input():
    path = "../xmpl/muellabfuhr8.txt"
    text = open(path, "r").read()
    lines = text.split("\n")
    lines.pop(-1)
    return txt2Graph(lines)
