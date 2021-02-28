#! /usr/bin/env python3
"""
Tim Davison, Jeff Koldoff, Ben Van De Water
625.687 - Applied Topology
Coding Homework 1
"""

from dataset_hw3 import stringA, stringB
from utils import *

import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

from AbstractSimplicialComplex import AbstractSimplicialComplex, NXSimplicialComplex

########
# MAIN #
########

def main():
    # Problem 1
    datasetA = smplcs_to_cmplx(string_to_smplcs(stringA))
    datasetB = smplcs_to_cmplx(string_to_smplcs(stringB))

    A = build_nx_complex(datasetA)
    B = build_nx_complex(datasetB)

    print(f"Human-readable representation of complex A: {A._adj}")
    print(f"Human-readable representation of complex B: {B._adj}")

    vectorsA, mappingA = build_custom_complex(datasetA)
    vectorsB, mappingB = build_custom_complex(datasetB)

    print("\nVectorized representation of dataset A:")
    print("Point indices:", mappingA)
    for i in range(0, len(datasetA)):
        print(vectorsA[i], "=", datasetA[i])

    # Problem 2

    

#############
# FUNCTIONS #
#############

def build_nx_complex(cmplx):
    G = NXSimplicialComplex()
    for smplx in cmplx:
        dim = len(smplx) - 1
        # Not elegant
        if dim == 2:
            G.add_edge(smplx[0], smplx[1])
        elif dim == 3:
            G.add_surface([smplx[0], smplx[1], smplx[2]])

    return G

def build_custom_complex(cmplx):
    asc = AbstractSimplicialComplex()
    vectors, mapping = asc.one_hot(cmplx)
    return vectors, mapping

#######
# RUN #
#######

if __name__ == "__main__":
    main()