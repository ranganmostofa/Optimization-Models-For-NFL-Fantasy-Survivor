from collections import defaultdict


class GraphConstructor:
    """
    Class for methods implementing construction of probability trees
    """
    @staticmethod
    def build_graph(G, P, start_node, terminal_node, terminal_weight, start_week, neighbor_set, num_layers):
        """
        Given the starting graph, current probability matrix for the season, the start node, the
        terminal node, the weight of edges leading to the terminal node, the start week, the set
        of neighbors of the input start node and the number of layers, builds and returns the
        probability tree where every final team node is connected to the input terminal node with
        the input terminal edge weight
        """
        # use the overloaded method to construct the traditional probability tree
        G_prime = GraphConstructor.__build_graph_iterative(G, P, start_node, start_week, neighbor_set, num_layers)
        # determine final nodes
        final_node_set = GraphConstructor.determine_layer_nodes(G_prime, num_layers)
        for final_node in final_node_set:  # for every final node
            # connect the final node to the terminal node using the terminal node_weight
            G[final_node][terminal_node] = terminal_weight
            G_prime[terminal_node] = dict()  # the terminal node has no outgoing edges
        return G_prime  # return the modified probability tree

    @staticmethod
    def __build_graph_iterative(G, P, start_node, start_week, neighbor_set, num_layers):
        """

        :param G:
        :param P:
        :param start_node:
        :param start_week:
        :param neighbor_set:
        :param num_layers:
        :return:
        """
        current_source_node_set = set()
        current_source_node_set.add(start_node)

        for current_week in range(start_week, start_week + num_layers):
            next_source_node_set = set()
            while len(current_source_node_set):
                source_node = current_source_node_set.pop()
                for neighbor in neighbor_set.difference(set(source_node)):
                    # produce the unique immutable tuple that corresponds to the neighbor_node
                    child_node = GraphConstructor.produce_child_node(source_node, neighbor)
                    edge_weight = GraphConstructor.extract_probability(P, child_node, current_week)
                    G[source_node][child_node] = edge_weight
                    next_source_node_set.add(child_node)
            current_source_node_set = next_source_node_set
        return G

    @staticmethod
    def __build_graph_recursive(G, P, start_node, start_week, neighbor_set, num_layers):
        """
        Given the starting graph, current probability matrix for the season, the start node,
        the start week, the set of neighbors of the input start node and the number of layers,
        builds and returns the probability tree associated with the probability matrix of the
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
                G = GraphConstructor.merge_graph(G_prime, GraphConstructor.__build_graph_recursive(
                    dict(), P, child_node, start_week + 1, child_node_set, num_layers - 1))
            return G  # return the final graph or probability tree

    @staticmethod
    def determine_layer_nodes(graph, layer):
        """
        Given a probability tree, returns the set of nodes associated with the input layer
        or week
        """
        node_set = set()  # initialize an empty set of nodes
        for source_node in graph.keys():  # for every source node
            if len(source_node) == 1 + layer:  # if the source node is in the desired layer
                node_set.add(source_node)  # add the source node to the set
            # for every terminal node connected to the current source node
            for terminal_node in graph[source_node].keys():
                # if the terminal node is in the desired layer
                if len(terminal_node) == 1 + layer:
                    node_set.add(terminal_node)  # add the terminal node to the node set
        return node_set  # return the node set

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
        return float(P[current_week - 1][child_node[-1] - 1])  # return the relevant probability

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

