###########
# PARSERS #
###########
import numpy as np

from .AbstractSimplicialComplex import AbstractSimplicialComplex



string_to_smplcs = lambda st: [smplx.replace("}", "") for smplx in st.split("}, ")]
smplcs_to_cmplx  = lambda smplcs: [smplx.replace("{", "").replace(" ", "").split(',') for smplx in smplcs]

def build_custom_complex(cmplx):
    """
    Declare a Simplical Complex obj and initialize some set of data as one-hot vectors

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
    v3 = v1 + v2
    mod_2 = [2]*len(v3)
    v3_mod_2 = np.mod(v3, mod_2)
    return v3_mod_2

def mod2_n_vector_addition(data):
    """
    Take a list of N vectors, compute their sum mod 2

    """
    for i in range(len(data)):
        if not isinstance(data[i], np.ndarray):
            data[i] = np.asarray(data[i])
    v1 = data[0]
    for i in range(1, len(data)):
        v1 += data[i]
    mod_2 = [2]*len(v1)
    v2_mod_2 = np.mod(v1, mod_2)
    return v2_mod_2