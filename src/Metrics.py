'''
Metrics for use with an Abstract Simplicial Complex (housed in AbstractSimplicialComplex.py)

'''
import numpy as np
from sklearn.metrics import pairwise

##############
# BASE CLASS #
##############

class Metric:
    """
    Given a DataFrame of n datapoints (songs), return an nxn DataFrame of the distances
    between datapoints for a given metric. Check for symmetry, 0s on main diagonal.
    """
    def __init__(self):
        pass

    def L_1_norm(self, x, y, radius=None):
        l1 = 0
        for i in range(len(x)):
            l1 += abs(x[i] - y[i])
        return l1

    def L_2_norm(self, x, y, radius=None):
        '''
        Using the formula from our slides - is this ever unequal to L1?
        '''
        l2 = 0
        for i in range(len(x)):
            l2 += ((x[i] - y[i]) ** 2) ** .5
        return l2

    def L_inf_norm(self, x, y, radius=None):
        linf = []
        for i in range(len(x)):
            linf += abs(x[i] - y[i])
        return max(linf)

    def cosine_distance(self, x, y):
        return pairwise.cosine_distance(x, y)

    def cosine_similarity(self, x, y):
        return pairwise.cosine_similarity(x, y)

    def dot_product(self, x, y):
        return np.dot(x, y)

    

sample_vector1 = [0, 0, 1, 2, 0.5, 0]
sample_vector2 = [0, 1, 0, 2, 0.6, 0]
sample_vector3 = [1, 1, 1, 1, 0.5, 0]
sample_vector4 = [0, 1, 0, 1, 0, 1]

sample_matrix1 = [sample_vector1, sample_vector1]
sample_matrix2 = [sample_vector3, sample_vector4]

metric = Metric()
print("L2 norm:", metric.L_2_norm(sample_vector1, sample_vector2))