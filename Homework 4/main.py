
from src import AbstractSimplicialComplex, dataset_hw3, utils



if __name__ == "__main__":

    # Initializing our data
    datasetA = utils.smplcs_to_cmplx(utils.string_to_smplcs(dataset_hw3.stringA))
    datasetB = utils.smplcs_to_cmplx(utils.string_to_smplcs(dataset_hw3.stringB))
    vectorsA, mappingA = utils.build_custom_complex(datasetA)
    vectorsB, mappingB = utils.build_custom_complex(datasetB)

    # Testing out pairwise vector addition mod 2
    sample_v1 = vectorsA[0]
    sample_v2 = vectorsA[1]
    sample_v3 = utils.mod2_vector_addition(sample_v1, sample_v2)
    print(sample_v1, ": vector #1")
    print(sample_v2, ": vector #2")
    print(sample_v3, ": vector #1 + vector #2, mod 2")

    # Testing out batch vector addition mod 2
    full_sum = utils.mod2_n_vector_addition(vectorsA)
    print(full_sum, ": dataset A, summed pairwise")