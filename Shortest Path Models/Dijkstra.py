from collections import deque


class Dijkstra:
    """
    Class of different implementations of Dijkstra's algorithm
    """
    @staticmethod
    def one_to_one(graph, source_node, terminal_node):
        """

        :param graph:
        :param source_node:
        :param terminal_node:
        :return:
        """
        pass

    @staticmethod
    def one_to_many(graph, source_node):
        """
        Given a graph represented in the adjacency list form and a source node, returns
        the shortest path from the source node to every other node
        """
        dist = dict()  # initialize a mapping of nodes to distance to source node
        prev_node = dict()  # initialize a mapping of nodes to their respective previous nodes in the shortest path
        Q = deque()  # initialize an empty queue

        # for every node in the graph
        for node in graph.keys():
            dist[node] = float("inf")  # set the distance to the source node as negative infinity
            prev_node[node] = None  # set the previous node to null
            Q.append(node)  # add the node to the queue

        dist[source_node] = 0  # set the distance of the source node to itself to 0

        # while Q is non-empty
        while len(Q):
            # determine the nearest node to the source node
            current_node = Dijkstra.__determine_min_dist(Q, dist)
            Q.remove(current_node)  # remove the nearest node
            for neighbor in graph[current_node].keys():  # for each neighbor of the nearest node
                # compute the distance from the neighboring node to the source node
                neighbor_dist = dist[current_node] + graph[current_node][neighbor]
                # if the current neighbor distance is lower than the recorded neighbor distance
                if neighbor_dist < dist[neighbor]:
                    dist[neighbor] = neighbor_dist  # replace the old neighbor distance with the new one
                    prev_node[neighbor] = current_node  # update the new previous node as the current node

        return dist, prev_node  # return the distance and previous node mappings

    @staticmethod
    def many_to_many(graph):
        """

        :param graph:
        :return:
        """
        pass

    @staticmethod
    def __determine_min_dist(Q, dist):
        """
        Given a queue of nodes and a mapping of nodes to their shortest distance to the
        source node, returns the node nearest to the source node, assuming the input queue
        is non-empty
        """
        if len(Q):  # if the input queue is non-empty
            current_node = Q.index(0)  # initialize the current node to be the first node in the queue
            current_dist = float("inf")  # initialize the current distance to negative infinity
            for node in Q:  # for every node in the queue
                if dist[node] < current_dist:  # if the source node is nearer to the iterated node than the current node
                    current_node = node  # replace the current node with the iterated node
            return current_node  # return the final current node


