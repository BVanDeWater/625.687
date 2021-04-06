'''
Test module that prints human readable output for a given assignment. Mutable
depending on assignment, though probably best to keep legacy functions.

'''
from sympy import pprint

import sys
sys.path.append("../src")  # feel free to clean this up; I can use "from src import dataset, utils"
import dataset, utils      # but idk if that's incompatible with your env

if __name__ == "__main__":

    # Initializing our data
    datasetA = utils.smplcs_to_cmplx(utils.string_to_smplcs(dataset.stringA))
    datasetB = utils.smplcs_to_cmplx(utils.string_to_smplcs(dataset.stringB))
    vectorsA, mappingA = utils.build_custom_complex(datasetA)
    vectorsB, mappingB = utils.build_custom_complex(datasetB)

    # Boundary matrices
    reverse_mappingA = {v:k for k,v in mappingA.items()}
    boundary_mapA_d1 = utils.generate_boundary_map(vectorsA, dim=1, mapping=reverse_mappingA)
    boundary_mapA_d2 = utils.generate_boundary_map(vectorsA, dim=2, mapping=reverse_mappingA)

    reverse_mappingB = {v: k for k, v in mappingA.items()}
    boundary_mapB_d1 = utils.generate_boundary_map(vectorsB, dim=1, mapping=reverse_mappingB)
    boundary_mapB_d2 = utils.generate_boundary_map(vectorsB, dim=2, mapping=reverse_mappingB)

    # Row reduce mod 2
    rref_example = utils.rref_mod_n(boundary_mapA_d1)
    pprint(rref_example)

    # TODO: Use the boundary matrices to compute the cycles (the kernel of the boundary operator, the solution to
    # M*a=0 as we discussed in class).

    # TODO: Find the Homologies at every dimension (the actual cycles that are not from boundaries resulting from
    # the higher dimension). This is just taking all the cycles, then taking out those from boundaries. You may
    # have to deal with linear combinations somehow.

    """
    Tim's thoughts - I think we can use the 
    """

    # TODO: Find the rank of the cycles, the rank of the boundaries, and therefore the rank of the homologies.
    # Compare the ranks with the actual numbers of things you computed in the previous steps.

    # TODO: Interpret the ranks of these homologies, and see if your speculations on the meanings of the two
    # complexes have changed at all.
