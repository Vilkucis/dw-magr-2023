from unittest import TestCase

from graph import graph
from parametrized.helpers.HGraphFactory import HGraphFactory


def graph2():
    G = graph.Graph()

    v1 = graph.Vertex("A")
    v2 = graph.Vertex("B")
    v3 = graph.Vertex("C")
    v4 = graph.Vertex("D")
    v5 = graph.Vertex("E")
    v6 = graph.Vertex("F")

    G.add_vertex(v1)
    G.add_vertex(v2)
    G.add_vertex(v3)
    G.add_vertex(v4)
    G.add_vertex(v5)
    G.add_vertex(v6)

    G.add_edge_by_tag(("B", "C"))
    G.add_edge_by_tag(("D", "E"))

    G.add_arc_by_tag(("A", "B"))

    G.add_arc_by_tag(("B", "D"))
    G.add_arc_by_tag(("B", "E"))

    G.add_arc_by_tag(("E", "F"))

    return G

class TestHGraphFactory(TestCase):
    def test_create(self):
        # given
        G = graph2()
        is_acyclic, topological_sort = G.is_acyclic()
        distances = {('s', 'A'): 1, ('s', 'B'): 2, ('s', 'C'): 1, ('s', 'E'): 3, ('s', 'F'): 4, ('s', 'D'): 3,
                              ('s', 't'): 5, ('A', 'B'): 1, ('A', 'E'): 2, ('A', 'F'): 3, ('A', 'D'): 2, ('A', 't'): 4,
                              ('B', 'E'): 1, ('B', 'F'): 2, ('B', 'D'): 1, ('B', 't'): 3, ('C', 't'): 1, ('E', 'F'): 1,
                              ('E', 't'): 2, ('F', 't'): 1, ('D', 't'): 1}
        # when
        h_graph = HGraphFactory(G, distances, topological_sort).create()[0]

        # then
        self.assertEqual(len(h_graph.get_vertices()), 6)
        self.assertEqual(len(h_graph.undirected_edges), 2)
