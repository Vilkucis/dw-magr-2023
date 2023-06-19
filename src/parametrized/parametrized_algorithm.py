import time

from graph.algorithms import IsAcyclic, ColorDirectedGraph
from parametrized.helpers.HGraphFactory import HGraphFactory
from parametrized.helpers.HOPermutationSignatures import HOPermutationSignatures
from parametrized.helpers.PermutationSignatureApplier import PermutationSignatureApplier
from parametrized.helpers.weighed_coloring import WeighedColoring


class ParametrizedColoringAlgorithm:
    def __init__(self):
        pass

    def _find_minimum_permutation(self, base_h, undirected_edges):
        permutations = HOPermutationSignatures(base_h)

        minimum_chromatic_number = None
        minimum_permutation_signature = None

        cyclic_graphs = 0
        acyclic_graphs = 0
        count = -1

        for (k, v) in undirected_edges:
            base_h.remove_edge_by_tag((k, v))

        for perm in permutations:
            count += 1
            # print(f"\rPermutation {count}/{2**(len(perm))-1}", end='')
            with PermutationSignatureApplier(base_h, perm, undirected_edges):
                is_acyclic, topological_sort = base_h.is_acyclic()

                if is_acyclic:
                    WeighedColoring().run(topological_sort)
                    acyclic_graphs += 1
                else:
                    cyclic_graphs += 1
                    continue

                chromatic_numer = base_h.tags_to_vertices['t'].get_color()
                # print(f'Chromatic number: {chromatic_numer}')

                if not minimum_chromatic_number or chromatic_numer < minimum_chromatic_number:
                    minimum_chromatic_number = chromatic_numer
                    minimum_permutation_signature = perm

        # print("\n")
        # print(f"{cyclic_graphs} out of {cyclic_graphs + acyclic_graphs} graph(s) was/were cyclic.")
        # print(
        #     f"Minimum permutation: {minimum_permutation_signature}, it's chromatic number: {minimum_chromatic_number}")
        return minimum_permutation_signature

    def _apply_result(self, base_h, distances, original_graph, perm, undirected_edges):
        with PermutationSignatureApplier(original_graph, perm, undirected_edges):
            _, order = original_graph.is_acyclic()
            ColorDirectedGraph().run(order)

    def run(self, original_graph):

        # start = time.time()
        _, topological_sort = IsAcyclic(original_graph).run_dfs()
        # end = time.time()
        # print(f"Sort: {end - start}")

        # start = time.time()
        distances = None
        # end = time.time()
        # print(f"Distances: {end - start}")

        # H
        # start = time.time()
        base_h, undirected_edges = HGraphFactory(original_graph, distances, topological_sort).create()
        # end = time.time()
        # print(f"H: {end - start}")

        # Create H_O permutations
        # start = time.time()
        perm = self._find_minimum_permutation(base_h, undirected_edges)
        # end = time.time()
        # print(f"Finding minimum: {end - start}")

        # Apply result to original graph
        # start = time.time()
        self._apply_result(base_h, distances, original_graph, perm, undirected_edges)
        # end = time.time()
        # print(f"Apply: {end - start}")

        # end_total = time.time()
        # print(f"Total: {end_total - start_total}")

        return base_h


