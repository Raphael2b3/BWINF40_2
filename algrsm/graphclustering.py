import math
import random

import networkx as nx


def findmaxinDijkstra(dij, nodes):
    maxv = 0
    maxnode = 0
    for node in nodes:
        if dij[node] > maxv:
            maxnode = node
            maxv = dij[node]
    return maxnode


def find_k_nodes(graph, nodes, k):
    """for i in range(k):
            maxv = 0
            best = nodes[0]
            for node in nodes:
                mul = 1
                for db in dbs:  # dijkstra datenbank
                    mul *= db[node]
                if mul > maxv:
                    best = node
            dbs.append(nx.single_source_dijkstra_path_length(graph, best))
            out.append(best)
        """

    farestNodes = [0]
    for i in range(k):
        dij2 = nx.multi_source_dijkstra_path_length(graph, farestNodes)
        farNode = findmaxinDijkstra(dij2, nodes)
        farestNodes.append(farNode)

    farestNodes.pop(0)
    return farestNodes


def prod(l):
    out = 1
    for i in l:
        out *= i
    return out


def k_means(graph: nx.Graph, k):
    """
    Not actually k-means fuck you, kys
    :param graph:
    :param k:
    :return:
    """
    nodes = graph.nodes
    pivot_nodes = find_k_nodes(graph, nodes, k)

    out = {}
    for n in pivot_nodes:
        g = nx.Graph()
        g.add_node(n)
        out[n] = g

    path = nx.multi_source_dijkstra_path(graph, pivot_nodes)
    for n in nodes:
        startnode = path[n][0]
        out[startnode].add_node(n)

    out = [out[n] for n in out]

    return out
