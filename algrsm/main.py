import networkx as nx
import matplotlib.pyplot as plt

from algrsm import graphprinter


def get_input(path):
    with open(path, "r") as file:
        lines = file.readlines()
    lines.pop(0)
    GInverted = nx.Graph()
    GReal = nx.Graph()
    edges = []  # [[0,1,100] ]
    realedges = []
    for line in lines:
        values = line.split(" ")
        start, stop, weight = int(values[0]), int(values[1]), 1/ (int(values[2]))
        edges.append([start, stop, weight])
        realedges.append([start, stop, 1 / weight])

    GInverted.add_weighted_edges_from(edges)
    GReal.add_weighted_edges_from(realedges)
    return GInverted, GReal


def clustergraph(path):
    import old
    graphs = old.getPartialGraph(path)
    out = []
    for g in graphs:
        G = nx.Graph()
        G.add_weighted_edges_from(g)
        out.append(G)

    out = [g.nodes for g in out]
    return out


def find_euler_paths(graph):
    pass


def print_solution(graph, subgraphs):
    graphprinter.draw_graph_and_subgraphs(graph, subgraphs)


days = 5  # von montag bis freitag sind 5 tage
start_position = 0
path = "../xmpl/muellabfuhr0.txt"
if __name__ == '__main__':
    graph, real = get_input(path)
    # setup()
    import graphclustering
    import k_eulerpath

    subgraphs = graphclustering.k_means(real, days)
    #subgraphs = k_eulerpath.clustergraph(graph, days)  # clustergraph(path) #graphclustering.k_means(real, days)

    print_solution(graph, subgraphs)

    input()
