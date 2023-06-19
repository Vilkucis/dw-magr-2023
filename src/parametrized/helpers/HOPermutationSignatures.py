import time
import itertools
import numpy as np

class HOPermutationsIterator():
    def __init__(self, h_o_permutations):
        # self.cur_iter = h_o_permutations.permutations.__iter__()
        self.bits = h_o_permutations.number_of_bits
        self.bound = 2**(self.bits)-1
        self.counter = -1

    def __next__(self):
        self.counter += 1
        if self.bound < self.counter:
            raise StopIteration

        return np.binary_repr(self.counter, width=self.bits)


class HOPermutationSignatures:
    def __init__(self, base_graph):
        self.base_grap = base_graph
        self.number_of_bits = len(base_graph.vertex_tuples_to_edges.keys())
        # self.permutations = self._get_permutations(self.number_of_bits)
        # self.cur_iter = self.permutations.__iter__()

    def __iter__(self):
        return HOPermutationsIterator(self)

    def _get_permutations(self, upper_bound):
        result = []
        number_of_bits = upper_bound
        # f = '0' + str(number_of_bits) + 'b'
        print("Starting permutations")
        start = time.process_time()
        res = list(itertools.product([0, 1], repeat=number_of_bits))
        end = time.process_time()

        print(f"_get_permutations: {end - start}")

        return res

