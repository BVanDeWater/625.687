"""
Class intended to generalize simplicial complex structures.

"""


class AbstractSimplicialComplex:

    def __init__(self, data=[], mapping={}, num_dimensions=None):
        self.data = data   # for possible auto-ingest of new data
        self.mapping = mapping  # for possible many->one datatype mappings
        self.num_dimensions = num_dimensions if num_dimensions else len(mapping.values()) # dimensions of the complex

    def one_hot(self, data):
        '''
        Take in some set of data, use the mapping to return that data as a set of one-hot vectors

        :param data: iterable collection of subsets
        :return:
        '''
        if self.mapping:  # stub: intended to skip going through the motions setting indices for points as below
            pass

        points = set()
        for subset in data:   # passed data is assumed to be a set of subsets. probs will refactor to accommodate later
            for point in subset:
                points.add(point)
        points = list(points)  # to provide indices for each item
        point_mapping = {k: points.index(k) for k in points}  # assign an integer per point

        data_vectors = []
        for subset in data:
            vector = [0] * len(points)
            for point in subset:
                vector[point_mapping[point]] = 1
            data_vectors.append(vector)
        return data_vectors, point_mapping

    def euler_characteristic(self):
        '''
        Calculate and return the Euler characteristic for the complex:
            char = |V| - |E| + |F| - ... +|simplex_i|*((-1)**(i+1))
        where i is the dimension of the ith simplex.
        '''
        return sum([1*((-1)**(len(s)+1)) for s in self.data])
