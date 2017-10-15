import csv
from time import time
from pprint import pprint
from ProbabilityMatrixHelpers import ProbabilityMatrixHelpers
from Dijkstra import Dijkstra
from GraphConstructor import GraphConstructor
from heap_dijkstra import dijkstra


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
            csv_matrix.append(list([float(elem) for elem in row]))
    return csv_matrix


NUM_WEEKS = 5

NUM_TEAMS = 32

START_NODE = "S"

START_WEEK = 1

TERMINAL_NODE = "T"

TERMINAL_WEIGHT = 0.00

# selected_nodes = {16, 5, 29, 7, 10, 1, 12, 13, 27, 26, 14, 4}  # flipped
# selected_nodes = {29, 1, 5, 7, 10, 12, 16, 13, 27, 26, 14, 4, 19, 20}  # logged
selected_nodes = {}

node_set = set(range(1, 1 + NUM_TEAMS)).difference(selected_nodes)

# P = read_csv("../Probability Matrix Creation/Shortest Path (Flipped) Probability Matrix 2016 Weeks 1-17.csv")
P = read_csv("../Probability Matrix Creation/Week 1 Elo Log Probabilities 2016.csv")
# P[0][15] = 0
# P[1][4] = 0
# P[2][28] = 0
# P[3][6] = 0

# P = [[0.5] * NUM_TEAMS] * NUM_WEEKS
# P = [[0.10, 0.20, 0.30, 0.40],
#      [0.77, 0.13, 0.88, 0.06],
#      [0.24, 0.55, 0.45, 0.99],
#      [0.03, 0.55, 0.68, 0.70]]

# print(P[0].index(min(P[0])))

print("Building Graph...\n")
build_t0 = time()

# G = GraphConstructor.build_graph(dict(), ProbabilityMatrixHelpers.build_cost_matrix(ProbabilityMatrixHelpers.flip_probability_matrix(P)),
#                                  tuple([START_NODE]), TERMINAL_NODE, TERMINAL_WEIGHT, START_WEEK, node_set, NUM_WEEKS)

G = GraphConstructor.build_graph(dict(), P,
                                 tuple([START_NODE]), tuple([TERMINAL_NODE]), TERMINAL_WEIGHT, START_WEEK, node_set, NUM_WEEKS)

build_t1 = time()

print("Graph Construction Complete!")
print("Time taken to build graph:", str(build_t1 - build_t0), "s\n")

print("Computing Optimal Path...\n")
dijkstra_t0 = time()

# dist, prev = Dijkstra.one_to_one(G, tuple([START_NODE]), TERMINAL_NODE)
dist, prev = dijkstra(G, tuple([START_NODE]))

dijkstra_t1 = time()

print("Optimal Path Found!")
print("Time taken to find optimal path:", str(dijkstra_t1 - dijkstra_t0), "s\n")

# pprint(G)
# print(len(G.keys()))
#

# pprint(prev)
# pprint(dist)
print("Optimal Path", prev[tuple([TERMINAL_NODE])])
print("Optimal Weight", dist[tuple([TERMINAL_NODE])])

print("Week:", START_WEEK + NUM_WEEKS - 1)

