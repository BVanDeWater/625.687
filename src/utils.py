###########
# PARSERS #
###########
from itertools import combinations
import numpy as np
import pandas as pd

from numpy.linalg import solve, matrix_rank

from .AbstractSimplicialComplex import AbstractSimplicialComplex


string_to_smplcs = lambda st: [smplx.replace("}", "") for smplx in st.split("}, ")]
smplcs_to_cmplx  = lambda smplcs: [smplx.replace("{", "").replace(" ", "").split(',') for smplx in smplcs]


def build_custom_complex(cmplx):
    """
    Declare a Simplicial Complex obj and initialize some set of data as one-hot vectors

    """
    asc = AbstractSimplicialComplex()
    vectors, mapping = asc.one_hot(cmplx)
    return vectors, mapping


def mod2_vector_addition(v1, v2):
    """
    Take two vectors, compute their sum mod 2

    """
    if not isinstance(v1, np.ndarray) or not isinstance(v2, np.ndarray):
        v1 = np.asarray(v1)
        v2 = np.asarray(v2)
    # This may be a little less expensive? But, maybe less robust:
    # it does assume the vectors are already elements of Z2...
    # return v1 ^ v2
    v3 = v1 + v2
    mod_2 = [2]*len(v3)
    v3_mod_2 = np.mod(v3, mod_2)
    return v3_mod_2


def mod2_n_vector_addition(data):
    """
    Take a list of N vectors, compute their sum mod 2

    """
    # Perhaps a little simpler? Doesn't break anything with the test case,
    # though handling for len(data) < 2 is different.
    res = np.zeros(3)
    for v in data:
        res = mod2_vector_addition(res, v)
    return res
    #data = np.asarray(data)
    #for i in range(len(data)):
    #    if not isinstance(data[i], np.ndarray):
    #        data[i] = np.asarray(data[i])
    #if len(data) < 2:
    #    return []
    #v1 = data[0]
    #for i in range(1, len(data)):
    #    v1 += data[i]
    #mod_2 = [2]*len(v1)
    #v2_mod_2 = np.mod(v1, mod_2)
    #return v2_mod_2


def compute_pchain_boundaries(data, starting_dim=2):
    """
    Compute and return boundaries for n-dimensional p-chains

    """
    data = [x for x in data if sum(x) == starting_dim]  # assumes one-hot encoding
    image = set()
    for i in range(1, len(data)):
        i_length_combos = combinations(data, i)
        for combo in i_length_combos:
            image.add(tuple(mod2_n_vector_addition(combo)))
    return image


def generate_boundary_map(data, dim=2, mapping=None):  # mapping not actually optional at this time
    points = [x for x in data if sum(x) == dim]  # assumes one-hot encoding
    edges = [x for x in data if sum(x) == dim+1]
    index = mapping.values()

    if dim == 1:
        points = index

    # Generate human-readable columns for {{dim}}-simplices
    cols = []
    for x in edges:
        edge = []
        for i in range(len(edges[0])):
            if x[i] == 1:
                edge.append(mapping[i])
        cols.append(tuple(edge))

    # Generate rows for each point.
    df = []
    for x in index:
        row = []
        for col in cols:
            if x in col:
                row.append(1)
            else:
                row.append(0)
        df.append(row)

    df = pd.DataFrame(df, columns=cols, index=index)
    return df

def compute_boundary_map_rank(df):
    boundary_map = np.ndarray(df.shape)
    for c, col in enumerate(df):
        for r, row in enumerate(df[col]):
            boundary_map[r][c] = row
    boundary_mat = np.asmatrix(boundary_map)
    return solve(boundary_mat, np.ones(boundary_mat.shape[1]))
