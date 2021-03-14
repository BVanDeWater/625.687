'''
Metrics for use with an Abstract Simplicial Complex (housed in AbstractSimplicialComplex.py)

'''

##############
# BASE CLASS #
##############

class Metric:
    def __init__(self):
        pass

#################
# CHILD CLASSES #
#################

class L_2_norm(Metric):
    pass

class L_inf_norm(Metric):
    pass