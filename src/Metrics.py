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

    def cosine_similarity(self, x, y):
        try:
            return pairwise.cosine_similarity(x, y)
        except Exception as e:
            #print("Formatting X, Y as numpy arrays...")
            x = np.asarray(x).reshape(1, -1)
            y = np.asarray(y).reshape(1, -1)
            return 1 - pairwise.cosine_similarity(x, y)

    def dot_product(self, x, y):
        return np.dot(x, y)

    def spectral_correlation_pseudometric(self, matrix_x, matrix_y):
        """
        Correlation pseudometric defined between two matrices; formula
        from https://asa.scitation.org/doi/pdf/10.1121/1.5027825
        (might need to be logged in to JHU for the link to work)
        """
        x2 = sum([matrix_x[i][j]**2 for i in range(len(matrix_x))
                  for j in range(len(matrix_x[0]))]) ** (1/2)
        y2 = sum([matrix_y[i][j]**2 for i in range(len(matrix_y))
                  for j in range(len(matrix_y[0]))]) ** (1/2)
        matrix_sum = sum([matrix_x[i][j]*matrix_y[i][j] for
                          i in range(len(matrix_x))
                          for j in range(len(matrix_x[0]))])
        m = 1 - (matrix_sum / (x2 * y2) )
        return m

    def determinant(self, x):
        """
        For square matrixes, compute the determinant
        Can use when we need to perform an nxn -> 1 data reduction
        """
        return np.linalg.det(np.array(x))

sample_vector1 = [0, 0, 1, 2, 0.5, 0]
sample_vector2 = [0, 1, 0, 2, 0.6, 0]
sample_vector3 = [1.2, 1, 1, 1, 0.5, 0]
sample_vector4 = [0, 1, 0, 1, 0, 1]

sample_matrix1 = [sample_vector1, sample_vector1]
sample_matrix2 = [sample_vector3, sample_vector4]
sample_matrix3 = [sample_vector3, sample_vector1, # square matrix for determinant
                  sample_vector4, sample_vector3,
                  sample_vector2, sample_vector4]

#metric = Metric()
#print("L2 norm:", metric.cosine_similarity(sample_vector1, sample_vector2))
#print("Pseduom:", metric.spectral_correlation_pseudometric(sample_matrix1, sample_matrix2))

