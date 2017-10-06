from collections import deque


def dijkstra(graph, source_node):
    """

    :param graph:
    :param source_node:
    :return:
    """
    dist = dict()
    prev_node = dict()
    Q = deque()

    for node in graph.keys():
        dist[node] = float("inf")
        prev_node[node] = None
        Q.append(node)

    dist[source_node] = 0

    while len(Q):
        current_node = determine_min_dist(Q, dist)
        Q.remove(current_node)
        for neighbor in graph[current_node].keys():
            current_dist = dist[current_node] + graph[current_node][neighbor]
            if current_dist < dist[neighbor]:
                dist[neighbor] = current_dist
                prev_node[neighbor] = current_node

    return dist, prev_node


def determine_min_dist(Q, dist):
    """

    :param Q:
    :param dist:
    :return:
    """
    if len(Q):
        current_node = Q.index(0)
        current_dist = float("inf")
        for node in Q:
            if dist[node] < current_dist:
                current_node = node
        return current_node


