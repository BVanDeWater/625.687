from src import AbstractSimplicialComplex, dataset_hw3, utils


if __name__ == "__main__":

    # Initializing our data
    datasetA = utils.smplcs_to_cmplx(utils.string_to_smplcs(dataset_hw3.stringA))
    datasetB = utils.smplcs_to_cmplx(utils.string_to_smplcs(dataset_hw3.stringB))
    vectorsA, mappingA = utils.build_custom_complex(datasetA)
    vectorsB, mappingB = utils.build_custom_complex(datasetB)

    '''
    # Generating all possible combinations of pairs/ triples mod 2 for dataset A
    dim2_boundariesA = utils.compute_pchain_boundaries(vectorsA, 2)
    dim3_boundariesA = utils.compute_pchain_boundaries(vectorsA, 3)
    num_pairsA = len([x for x in vectorsA if sum(x) == 2])
    num_triplesA = len([x for x in vectorsA if sum(x) == 3])
    print("Dataset A: generated {} unique elements from {} boundary pairs"
          .format(len(dim2_boundariesA), num_pairsA))
    print("Dataset A: generated {} unique elements from {} boundary triplets"
          .format(len(dim3_boundariesA), num_triplesA))

    # Generating all possible combinations of pairs/ triples mod 2 for dataset B
    # User beware - slow!! Combinatorial explosion - not a scalable solution for finding images
    dim2_boundariesB = utils.compute_pchain_boundaries(vectorsB, 2)
    dim3_boundariesB = utils.compute_pchain_boundaries(vectorsB, 3)
    num_pairsB = len([x for x in vectorsB if sum(x) == 2])
    num_triplesB = len([x for x in vectorsB if sum(x) == 3])
    print(
        "Dataset B: generated {} unique elements from {} boundary pairs"
        .format(len(dim2_boundariesB), num_pairsB))
    print("Dataset G: generated {} unique elements from {} boundary triplets"
        .format(len(dim3_boundariesB), num_triplesB))
    '''

    # Boundary matrices
    reverse_mappingA = {v:k for k,v in mappingA.items()}
    boundary_mapA_d1 = utils.generate_boundary_map(vectorsA, dim=1, mapping=reverse_mappingA)
    boundary_mapA_d2 = utils.generate_boundary_map(vectorsA, dim=2, mapping=reverse_mappingA)

    reverse_mappingB = {v: k for k, v in mappingA.items()}
    boundary_mapB_d1 = utils.generate_boundary_map(vectorsB, dim=1, mapping=reverse_mappingB)
    Bboundary_mapB_d2 = utils.generate_boundary_map(vectorsB, dim=2, mapping=reverse_mappingB)

    print("Sample boundary map matrix - dataset A, triples -> edges")
    print(boundary_mapA_d1)

    print("Sample boundary map matrix - dataset A, edges -> points")
    print(boundary_mapA_d2)
