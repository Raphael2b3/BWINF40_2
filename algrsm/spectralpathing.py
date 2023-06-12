import networkx as nx
import numpy as np


def k_means(points, k):
    clusters = [[] for _ in range(k)]
    means = [points[i] for i in range(k)]

    for mean in means:
        for point in points:
            pass

def findpaths(G: nx.Graph):
    dimensions = len(G.nodes)
    rMatrix = []
    for edge in G.edges(data=True):
        temp = [0 for _ in range(dimensions)]
        weight = edge[2][weight]
        temp[edge[0]] = temp[edge[1]] = weight
        rMatrix.append(temp)


