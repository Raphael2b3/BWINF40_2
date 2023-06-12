"""
1. Reduzieren des Graphs
2.1 k pivot Knoten finden als PK
2.2 Sortiere PK aufsteigend
3.1 Jeder k in PK nacheinander bekommt den nah nächsten knoten bis alle knoten zugewiesen sind außer k0
4. Kanten innerhalb von Gruppe zum Subgraph hinzufügen
5. Gewicht durch euler weg für jedes cluster generieren + hinweg
6. ??? Kanten die zum größten cluster führen dem betrachteten cluster hinzufügen
7. Cluster mit geringstem gewicht neue kante
    -> 6. ? wenn keine aktion 8.
8. return Kanten Cluster

9. Eueler weg durch Cluster

Fertig!




"""
import math

import networkx as nx

from algrsm import graphprinter


def optional_edge_remove(graph, edge):
    """
    removes edge if removing it leaves the graph fully connected
    :param graph:
    :param edge:
    :return:
    """
    graph.remove_edge(edge[0], edge[1])
    if not nx.is_connected(graph):
        graph.add_edge(edge[0], edge[1], weight=edge[2])


def reduce_graph(G: nx.Graph):
    reducedG = G.copy()
    edges = reducedG.edges().data("weight")
    edges = sorted(edges, key=lambda t: t[2])
    for edge in edges:
        optional_edge_remove(reducedG, edge)
    return reducedG


def add_edges_between_grouped_nodes(nodes):
    pass


def euler_path_length(cluster):
    pass


def add_rest_edges_by_cluster_weight():
    pass


def shortest_path_to_cluster(cluster):
    pass


def findmaxinDijkstra(dij, goalnodes):
    maxv = 0
    maxnode = 0
    for node in goalnodes:
        if dij[node] > maxv:
            maxnode = node
            maxv = dij[node]
    return maxnode


def findmininDijkstra(dij, goalnodes, key=lambda i, dij: dij[i]):
    maxv = math.inf
    maxnode = 0
    for node in goalnodes:
        if key(node, dij) < maxv:
            maxnode = node
            maxv = key(node, dij)
    return maxnode


def find_k_nodes(graph, k):
    farNode = None
    nodes = graph.nodes
    farestNodes = [0]
    for i in range(k):
        dij2 = nx.multi_source_dijkstra_path_length(graph, farestNodes)
        farNode = findmaxinDijkstra(dij2, nodes)
        farestNodes.append(farNode)
    farestNodes.pop(0)
    return farestNodes


def sort_k_nodes(k_nodes, nuldij):
    return sorted(k_nodes, key=lambda t: nuldij[t])


def efficient_cicle(maingraph: nx.Graph, subgraph: nx.Graph):
    distances, paths = nx.single_source_dijkstra(maingraph, 0)  # dijkstra from zero node
    out = [(math.inf, 0), (math.inf, 0)]
    for node in subgraph.nodes:
        if out[0][0] > distances[node]:
            out[1] = out[0]
            out[0] = (distances, node)

    edges_path = nx.eulerian_circuit(subgraph, out[0][1])

    weight = 0
    for edge in edges_path:
        weight += edge[2]
    weight += out[0][0] + out[1][0]
    return weight


def multi_dijkstra_path_length_with_source_id(G, sources, goals):
    out = {}
    for s in sources:
        dij = nx.single_source_dijkstra_path_length(G, s)
        for goal in goals:
            if goal not in out.keys() or out[goal][0] > dij[goal]:
                out[goal] = [dij[goal], s]
    out = sorted(out, key=lambda t: out[t][0])
    return out[0]


def clustergraph(G: nx.Graph, k):
    reducedG = reduce_graph(G)  #
    k_nodes = find_k_nodes(reducedG, k)  # starting cluster nodes
    dijkstratozero = nx.single_source_dijkstra_path_length(reducedG, 0)
    k_nodes = sort_k_nodes(k_nodes, dijkstratozero)

    clusters = [nx.Graph() for _ in range(k)]
    for i in range(k):
        clusters[i].add_node(k_nodes[i])

    listofallnodes = []
    listofnodesincluster = []

    for graphc in clusters:
        listofnodesincluster.append(*graphc.nodes)

    for node in G.nodes:
        if node not in listofnodesincluster and node != 0:
            listofallnodes.append(node)

    while len(listofallnodes) > 0:  # weil 0 übrig bleiben muss
        multidijkstra = multi_dijkstra_path_length_with_source_id(G, listofnodesincluster, listofallnodes)

        graphprinter.draw_graph_and_subgraphs(G,clusters)

        input()
