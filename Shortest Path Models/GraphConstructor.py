class GraphConstructor:
    """
    Class for methods implementing construction of probability trees
    """
    @staticmethod
    def build_graph(G, P, start_node, start_week, neighbor_set, num_layers):
        """
        Given the starting graph, current probability matrix for the season, the start node,
        the start week, the set of neighbors of the input start node and the number of layers,
        builds and returns the probability tree associated with the probsbility tree of the
        shortest path problem
        """
        if not num_layers:  # if the number of layers is 0
            return dict()  # return the empty dictionary
        else:  # for positive number of layers
            for neighbor in neighbor_set:  # for each neighbor of the start node
                # produce the unique immutable tuple that corresponds to the neighbor_node
                child_node = GraphConstructor.produce_child_node(start_node, neighbor)

                # make a copy of the neighbor set and remove the neighbor from duplicate set
                child_node_set = set(neighbor_set)
                child_node_set.remove(neighbor)

                # add the edge connecting the start node to the neighbor node to make G'
                G_prime = GraphConstructor.add_edge(G, start_node, child_node,
                                                    GraphConstructor.extract_probability(P, child_node, start_week))

                # use recursion to mutate the input graph G by building and adding the
                # relevant subgraph at each recursive level
                G = GraphConstructor.merge_graph(G_prime, GraphConstructor.build_graph(
                    dict(), P, child_node, start_week + 1, child_node_set, num_layers - 1))

            return G  # return the final graph or probability tree

    @staticmethod
    def produce_child_node(parent_node, next_node):
        """
        Given the parent node represented as a tuple containing the teams previously selected,
        returns the unique tuple corresponding to the child_node
        """
        child_node_list = list(parent_node)  # convert the tuple to a list so that it is mutable
        child_node_list.append(next_node)  # append the next team to be picked to the list
        return tuple(child_node_list)  # convert back to a tuple and return

    @staticmethod
    def merge_graph(G1, G2):
        """
        Given two graphs, merges the two and returns the resulting graph
        """
        G = dict(G1)  # initialize the merged graph to be a copy of the first graph
        for source_node in G2.keys():  # for every source node in the second graph
            # for every terminal node of every source node in the second graph
            for terminal_node in G2[source_node].keys():
                if source_node not in G.keys():  # if the source node is not in the merged graph
                    # add the source node and any terminal nodes it may contain in the second graph
                    G[source_node] = G2[source_node]
                else:  # otherwise
                    # add the edge connecting the source node to the terminal node
                    G[source_node][terminal_node] = G2[source_node][terminal_node]
        return G  # return the merged graph

    @staticmethod
    def extract_probability(P, child_node, current_week):
        """
        Given the probability matrix, child node and the current week number, returns the
        relevant probability value from the matrix
        """
        return P[child_node[-1] - 1][current_week - 1]  # return the relevant probability

    @staticmethod
    def add_edge(graph, source_node, terminal_node, edge_weight):
        """
        Given a graph, a pair of source and terminal nodes and the weight of the edge that is
        to connect the two nodes, adds the edge with the required weight to the input graph
        and returns the graph
        """
        if source_node not in graph:  # if the source node is not in the graph
            # add the source node and the inner mapping of the terminal node to edge weight value
            graph[source_node] = dict({terminal_node: edge_weight})
        else:  # if the source node is not in the graph
            # just add the edge with the desired weight
            graph[source_node][terminal_node] = edge_weight
        # finally check if the terminal node has an outer mapping
        if terminal_node not in graph.keys():
            # if not set it to an empty inner mapping
            graph[terminal_node] = dict()
        return graph  # return the mutated input graph


from time import time
from pprint import pprint


t_0 = time()

NUM_WEEKS = 6

NUM_TEAMS = 32

START_NODE = 0

START_WEEK = 1

TERMINAL_NODE = "T"

node_set = list(range(1, 1 + NUM_TEAMS))

P = [[0.5] * NUM_WEEKS] * NUM_TEAMS

G = GraphConstructor.build_graph(dict(), P, tuple([START_NODE]), START_WEEK, node_set, NUM_WEEKS)

t_1 = time()

# pprint(G)
# print(len(G.keys()))

print(str(t_1 - t_0), "s")


