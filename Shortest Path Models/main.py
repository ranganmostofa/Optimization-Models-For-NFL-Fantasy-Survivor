import csv
from time import time
from pprint import pprint
from Dijkstra import Dijkstra
from GraphConstructor import GraphConstructor


def read_csv(csv_filename):
    # Read CSV File
    """
    :param csv_filename:
    :return:
    """
    csv_matrix = []
    with open(csv_filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            csv_matrix.append(list(row))
    return csv_matrix


NUM_WEEKS = 3

NUM_TEAMS = 32

START_NODE = "S"

START_WEEK = 1

TERMINAL_NODE = "T"

TERMINAL_WEIGHT = 0.00

selected_nodes = set(range(1, 1))

node_set = set(range(1, 1 + NUM_TEAMS)).difference(selected_nodes)

P = read_csv("../Probability Matrix Creation/Shortest Path (Flipped) Probability Matrix 2016 Weeks 1-4.csv")
# P = [[0.5] * NUM_TEAMS] * NUM_WEEKS
# P = [[0.10, 0.20, 0.30, 0.40],
#      [0.77, 0.13, 0.88, 0.06],
#      [0.24, 0.55, 0.45, 0.99],
#      [0.03, 0.55, 0.68, 0.70]]

print(P[0].index(min(P[0])))

print("Building Graph...\n")
build_t0 = time()

G = GraphConstructor.build_graph(dict(), P, tuple([START_NODE]), TERMINAL_NODE, TERMINAL_WEIGHT,
                                 START_WEEK, node_set, NUM_WEEKS)

build_t1 = time()

print("Graph Construction Complete!")
print("Time taken to build graph:", str(build_t1 - build_t0), "s\n")

print("Computing Optimal Path...\n")
dijkstra_t0 = time()

dist, prev = Dijkstra.one_to_many(G, tuple([START_NODE]))

dijkstra_t1 = time()

print("Optimal Path Found!")
print("Time taken to find optimal path:", str(dijkstra_t1 - dijkstra_t0), "s\n")

# pprint(G)
# print(len(G.keys()))
#

# pprint(prev)
# pprint(dist)
print("Optimal Path", prev[TERMINAL_NODE])
print("Optimal Weight", dist[TERMINAL_NODE])


