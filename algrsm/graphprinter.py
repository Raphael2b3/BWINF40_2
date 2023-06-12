import networkx as nx
import matplotlib.pyplot as plt

colors = {
    0: "red",
    1: "yellow",
    2: "blue",
    3: "orange",
    4: "green",
}

c = 0
k = 5


def drawMainGraph(G, globpos):
    elarge = [(u, v) for (u, v, d) in G.edges(data=True)]  # if d["weight"] > 4]
    # esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 4]
    # nodes
    nx.draw_networkx_nodes(G, globpos, node_size=20,node_color="gray")
    nx.draw_networkx_nodes(G, globpos, node_size=60, node_color="red", nodelist=[0])

    # edges
    nx.draw_networkx_edges(G, globpos, edgelist=elarge, width=0.2)
    # nx.draw_networkx_edges(
    #   G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    # )

    # node labels
    # nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    # edge_labels = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels,font_size=5)


def drawSubgraph(G, pos, nodes=None):
    global c
    # if not nodes: nodes = G.nodes
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color=colors[c % k])
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color="black", nodelist=[0])

    # edges
    nx.draw_networkx_edges(G, pos, width=0.2)
    """nx.draw_networkx_edges(
       G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color=colors[c], style="dashed"
     )"""
    # node labels
    # nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")
    # edge weight labels
    """edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=5)
    """
    c += 1


def draw_graph_and_subgraphs(G, gs):
    pos = nx.spring_layout(G, seed=1)

    drawMainGraph(G, pos)
    for g in gs:
        try:
            drawSubgraph(g, pos)
        except:
            drawSubgraph(G, pos, nodes=g)

    ax = plt.gca()
    ax.margins(0)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    plt.show()
