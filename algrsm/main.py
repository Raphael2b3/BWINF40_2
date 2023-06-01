import networkx as nx
import matplotlib.pyplot as plt


def get_input(path):
    with open(path, "r") as file:
        lines = file.readlines()
    lines.pop(0)
    G = nx.Graph()
    edges = []  # [[0,1,100] ]
    for line in lines:
        values = line.split(" ")
        start, stop, weight = values[0], values[1], 10 / int(values[2])
        edges.append([start, stop, weight])

    G.add_weighted_edges_from(edges)

    return G


def clustergraph(path):
    import old
    graphs = old.getPartialGraph(path)
    out = []
    for g in graphs:
        G = nx.Graph()
        G.add_weighted_edges_from(g)
        out.append(G)
    return out


def find_euler_paths(graph):
    pass


def print_solution(G, gs):
    pos = nx.spring_layout(graph, seed=1)
    import graphprinter
    graphprinter.DrawMainGraph(G, pos)
    for g in gs:
        graphprinter.drawSubgraph(g, pos)

    ax = plt.gca()
    ax.margins(0)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


days = 5  # von montag bis freitag sind 5 tage
start_position = 0

if __name__ == '__main__':
    path = "../xmpl/muellabfuhr8.txt"
    graph = get_input(path)
    subgraphs = clustergraph(path)
    print_solution(graph, subgraphs)

    input()
