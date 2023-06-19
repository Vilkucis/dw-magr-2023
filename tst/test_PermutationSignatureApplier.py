from unittest import TestCase

from graph import graph
from parametrized.helpers.PermutationSignatureApplier import PermutationSignatureApplier


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

class TestPermutationSignatureApplier(TestCase):
    def test_00_signature(self):
        # given
        G = graph2()
        signature = ['0', '0']
        undirected_edges = [('B', 'C'), ('D', 'E')]

        # when-then
        with PermutationSignatureApplier(G, signature, undirected_edges):
            self.assertIn(('B', 'C'), G.vertex_tuples_to_arcs)
            self.assertIn(('D', 'E'), G.vertex_tuples_to_arcs)

        self.assertNotIn(('B', 'C'), G.vertex_tuples_to_arcs)
        self.assertNotIn(('D', 'E'), G.vertex_tuples_to_arcs)


    def test_10_signature(self):
        # given
        G = graph2()
        signature = ['1', '0']
        undirected_edges = [('B', 'C'), ('D', 'E')]

        # when-then
        with PermutationSignatureApplier(G, signature, undirected_edges):
            self.assertIn(('C', 'B'), G.vertex_tuples_to_arcs)
            self.assertIn(('D', 'E'), G.vertex_tuples_to_arcs)

        self.assertNotIn(('C', 'B'), G.vertex_tuples_to_arcs)
        self.assertNotIn(('D', 'E'), G.vertex_tuples_to_arcs)