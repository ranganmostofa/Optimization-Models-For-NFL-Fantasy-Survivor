from collections import deque


def dijkstra(graph, source_node):
    """

    :param graph:
    :param source_node:
    :return:
    """
    dist = dict()
    prev_node = dict()

    for node in graph.keys():
        dist[node] = float("inf")
        prev_node[node] = None

    dist[source_node] = 0

    Q = deque(sorted(dist[source_node].values()))

    while len(Q):
        next_node = Q.popleft()
        



