'''
Additional utility and helper functions for using an Abstract Simplicial Complex for
analysis.

'''

from itertools import combinations
import numpy as np
from numpy.linalg import solve
import pandas as pd
from sympy import Matrix, mod_inverse

from AbstractSimplicialComplex import AbstractSimplicialComplex

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
    res = np.zeros(3)
    for v in data:
        res = mod2_vector_addition(res, v)
    return res


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
    else:
        rows = []
        for x in points:
            row = []
            for i in range(len(index)):
                if x[i] == 1:
                    row.append(mapping[i])
            rows.append(tuple(row))
        points = rows

    # Generate human-readable columns for {{dim}}-simplices
    cols = []
    for x in edges:
        edge = []
        for i in range(len(index)):
            if x[i] == 1:
                edge.append(mapping[i])
        cols.append(tuple(edge))

    # Generate rows for each point.
    df = []
    if dim == 1:
        for x in index:
            row = []
            for col in cols:
                if x in col:
                    row.append(1)
                else:
                    row.append(0)
            df.append(row)
    else:
        for point in points:
            row = []
            for col in cols:
                point_is_boundary = True
                for i in range(len(point)):
                    if point[i] not in col:
                        point_is_boundary = False
                row.append(int(point_is_boundary))
            df.append(row)
    df = pd.DataFrame(df, columns=cols, index=points)
    return df

def compute_boundary_map_rank(df):
    boundary_map = np.ndarray(df.shape)
    for c, col in enumerate(df):
        for r, row in enumerate(df[col]):
            boundary_map[r][c] = row
    boundary_mat = np.asmatrix(boundary_map)
    return solve(boundary_mat, np.ones(boundary_mat.shape[1]))


def rref_mod_helper(x, modulus):
    """
    Helper function to clean up sympy reduce output
    """
    numerator, denominator = x.as_numer_denom()
    return numerator * mod_inverse(denominator, modulus) % modulus


def rref_mod_n(matrix, n=2):
    """
    ~ Borrowed ~ from https://stackoverflow.com/questions/31190182/sympy-solving-matrices-in-a-finite-field

    Given a matrix and a modulus n (default n=2), row reduce mod n
    """
    # Move data into a sympy Matrix() object
    if type(matrix) == pd.DataFrame:
        matrix = matrix.values
    try:
        matrix = Matrix(matrix)
    except Exception as e:
        print("Failed to intialize data as a Sympy matrix: {}".format(e))

    # Reduce mod n
    matrix = matrix.rref(iszerofunc=lambda x: x % n == 0)  # can we trust sympy?
    matrix = matrix[0].applyfunc(lambda x: rref_mod_helper(x, n))  # cleanup
    return matrix
