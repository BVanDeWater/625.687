#! /usr/bin/env python3
"""
Tim Davison, Ben Van De Water
625.687 - Applied Topology
Coding Homework 1
"""

from dataset_hw3 import stringA, stringB
from utils import *

import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

########
# MAIN #
########

def main():
    # Problem 1
    datasetA = smplcs_to_cmplx(string_to_smplcs(stringA))
    datasetB = smplcs_to_cmplx(string_to_smplcs(stringB))

    A = build_simple_graph(datasetA)
    B = build_simple_graph(datasetB)

    print(f"Human-readable representation of complex A: {A.edges()}")
    print(f"Human-readable representation of complex B: {B.edges()}")

    # Problem 2

    

#############
# FUNCTIONS #
#############

def build_simple_graph(cmplx):
    G = nx.Graph()
    for smplx in cmplx:
        #dim = len(simplex) - 1
        # Probably not optimal, NX.Graph has a method to create edges from a list.
        for nodes in combinations(smplx, 2):
            G.add_edge(nodes[0], nodes[1])

    return G

#######
# RUN #
#######

if __name__ == "__main__":
    main()
