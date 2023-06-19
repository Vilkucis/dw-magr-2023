import time

from graph.algorithms import ColorDirectedGraph
from parametrized.helpers.HOPermutationSignatures import HOPermutationSignatures
from parametrized.helpers.PermutationSignatureApplier import PermutationSignatureApplier


class BruteColoringAlgorithm:
    def __init__(self):
        pass

    def run(self, original_graph):
        cyclic_graphs = 0
        acyclic_graphs = 0
        # count = -1

        minimum_chromatic_number = None
        minimum_permutation_signature = None

        permutations = HOPermutationSignatures(original_graph)
        undirected_edges = original_graph.vertex_tuples_to_edges.keys()

        for perm in permutations:
            # count += 1
            # print(f"\rPermutation {count}/{2 ** (len(perm)) - 1}", end='')
            with PermutationSignatureApplier(original_graph, perm, undirected_edges):
                is_acyclic, topological_sort = original_graph.is_acyclic()

                ColorDirectedGraph().run(topological_sort)

                if is_acyclic:
                    ColorDirectedGraph().run(topological_sort)
                    acyclic_graphs += 1
                else:
                    cyclic_graphs += 1
                    continue

                chromatic_numer = original_graph.tags_to_vertices['t'].get_color()
                # print(f'Chromatic number: {chromatic_numer}')

                if not minimum_chromatic_number or chromatic_numer < minimum_chromatic_number:
                    minimum_chromatic_number = chromatic_numer
                    minimum_permutation_signature = perm

        # print("\n")
        # print(f"{cyclic_graphs} out of {cyclic_graphs + acyclic_graphs} graph(s) was/were cyclic.")
        # print(
        #     f"Minimum permutation: {minimum_permutation_signature}, it's chromatic number: {minimum_chromatic_number}")

        with PermutationSignatureApplier(original_graph, minimum_permutation_signature, undirected_edges):
            order = original_graph.is_acyclic()[1]
            ColorDirectedGraph().run(order)
