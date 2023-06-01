import networkx as nx
import matplotlib as plt

colors = {
    0: "red",
    1: "yellow",
    2: "blue",
    3: "orange",
    4: "green",
}
c = 0
def DrawMainGraph(G,pos):

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
    # nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    #edge_labels = nx.get_edge_attributes(G, "weight")
    #nx.draw_networkx_edge_labels(G, pos, edge_labels,font_size=5)


def drawSubgraph(G,pos):
    global c

    nx.draw_networkx_nodes(G, pos, node_size=20,node_color=colors[c])
    nx.draw_networkx_nodes(G, pos, node_size=50,node_color="red",nodelist=["0"])

    # edges
    nx.draw_networkx_edges(G, pos, width=0.2, edge_color=colors[c])
    # nx.draw_networkx_edges(
    #   G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    # )

    # node labels
    #nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")
    # edge weight labels
    #edge_labels = nx.get_edge_attributes(G, "weight")
    #nx.draw_networkx_edge_labels(G, pos, edge_labels,font_size=5)
    c+=1