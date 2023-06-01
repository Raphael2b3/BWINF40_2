import networkx as nx
import matplotlib.pyplot as plt


def get_input(path):
    with open(path, "r") as file:
        lines = file.readlines()
    lines.pop(0)
    G = nx.MultiGraph()
    edges = []
    for line in lines:
        values = line.split(" ")
        start,stop,weight = values[0],values[1],10/int(values[2])
        edges.append([start, stop, weight])

    G.add_weighted_edges_from(edges)

    return G


def clustergraph(graph, n_clusters):
    return []


def find_euler_paths(graph):
    pass


def print_solution(G, gs):
    pos = nx.spring_layout(graph, seed=1)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True)]  # if d["weight"] > 4]
    # esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 4]
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_nodes(G, pos, node_size=50,node_color="red",nodelist=["0"])

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=0.2)
    # nx.draw_networkx_edges(
    #   G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    # )

    # node labels
    #nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")
    # edge weight labels
    # edge_labels = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels,font_size=5)

    ax = plt.gca()
    ax.margins(0)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


days = 5  # von montag bis freitag sind 5 tage
start_position = 0

if __name__ == '__main__':
    graph: nx.MultiGraph = get_input("../xmpl/muellabfuhr7.txt")

    print_solution(graph, [])

    input()
