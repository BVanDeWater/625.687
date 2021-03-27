'''
Metrics for use with an Abstract Simplicial Complex (housed in AbstractSimplicialComplex.py)

'''

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

    def L_2_norm(self, df, radius=None):
        pass

    def L_inf_norm(self, radius=None):
        pass