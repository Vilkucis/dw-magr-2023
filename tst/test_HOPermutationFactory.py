import itertools
import time
from unittest import TestCase

from graph import graph
from parametrized.helpers.HOPermutationSignatures import HOPermutationSignatures
from unittest.mock import MagicMock



def graph2():
    G = graph.Graph()

    v2 = graph.Vertex("B")
    v3 = graph.Vertex("C")
    v4 = graph.Vertex("D")
    v5 = graph.Vertex("E")

    G.add_vertex(v2)
    G.add_vertex(v3)
    G.add_vertex(v4)
    G.add_vertex(v5)

    G.add_edge_by_tag(("B", "C"))
    G.add_edge_by_tag(("D", "E"))

    G.add_arc_by_tag(("B", "D"))
    G.add_arc_by_tag(("B", "E"))

    return G

class TestHOPermutationFactory(TestCase):
    def test_1_bit_permutations(self):
        G = graph.Graph()

        v2 = graph.Vertex("B")
        v3 = graph.Vertex("C")

        G.add_vertex(v2)
        G.add_vertex(v3)

        G.add_edge_by_tag(("B", "C"))

        perm_factory = HOPermutationSignatures(G)
        expected = ['0', '1']

        # when-then
        length = 0
        for item, number in zip(perm_factory, expected):
            self.assertEqual(item, number)
            length += 1
        self.assertEqual(length, 2)

    def test_2_bit_permutations(self):
        # given
        G = graph2()
        perm_factory = HOPermutationSignatures(G)
        expected = ['00', '01', '10', '11']

        # when-then
        length = 0
        for item, number in zip(perm_factory, expected):
            self.assertEqual(item, number)
            length += 1
        self.assertEqual(length, 2**2)

    def test_3_bit_permutations(self):
        # given
        G = graph2()
        G.add_edge_by_tag(("C", "D"))
        perm_factory = HOPermutationSignatures(G)
        expected = ['000', '001', '010', '011', '100', '101', '110', '111']

        # when-then
        length = 0
        for item, number in zip(perm_factory, expected):
            self.assertEqual(item, number)
            length += 1
        self.assertEqual(length, 2**3)

    def mock_dict(self, n):
        G = graph.Graph()
        G.add_vertex_by_tag("0")
        for i in range(1, n+1):
            G.add_vertex_by_tag(str(i))
            G.add_edge_by_tag(("0", str(i)))

        return G

    def test_perf_test(self):
        # given
        G = self.mock_dict(3)

        start_time = time.process_time()
        perm_factory = HOPermutationSignatures(G)
        end_time = time.process_time()

        # when-then
        length = 0
        for item in perm_factory:
            print(item)
            length += 1
        self.assertEqual(length, 2**5)

        print(f"Time: {end_time - start_time}")
