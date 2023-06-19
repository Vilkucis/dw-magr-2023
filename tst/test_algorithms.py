from unittest import TestCase

import utilities.utilities as util
from graph import algorithms, graph


class TestIsAcyclic(TestCase):
    def test_run_dfs_has_cycle_1(self):
        # given
        G = graph.Graph()

        v1 = graph.Vertex("A")
        v2 = graph.Vertex("B")
        v3 = graph.Vertex("C")

        G.add_vertex(v1)
        G.add_vertex(v2)
        G.add_vertex(v3)

        G.add_arc_by_tag(("A", "B"))
        G.add_arc_by_tag(("B", "C"))
        G.add_arc_by_tag(("C", "A"))

        cycle, order = algorithms.IsAcyclic(G).run_dfs()

        self.assertFalse(cycle)

    def test_run_dfs_has_cycle_2(self):
        # given
        G = graph.Graph()

        v1 = graph.Vertex("A")
        v2 = graph.Vertex("B")

        G.add_vertex(v1)
        G.add_vertex(v2)

        G.add_arc_by_tag(("A", "B"))
        G.add_arc_by_tag(("B", "A"))

        cycle, order = algorithms.IsAcyclic(G).run_dfs()

        self.assertFalse(cycle)

    def test_run_dfs_has_cycle_3(self):
        # given
        G = graph.Graph()

        v1 = graph.Vertex("A")
        v2 = graph.Vertex("B")
        v3 = graph.Vertex("C")
        v4 = graph.Vertex("D")
        v5 = graph.Vertex("E")

        G.add_vertex(v1)
        G.add_vertex(v2)
        G.add_vertex(v3)
        G.add_vertex(v4)
        G.add_vertex(v5)

        G.add_arc_by_tag(("A", "B"))
        G.add_arc_by_tag(("B", "C"))
        G.add_arc_by_tag(("D", "B"))
        G.add_arc_by_tag(("B", "E"))
        G.add_arc_by_tag(("E", "D"))

        cycle, order = algorithms.IsAcyclic(G).run_dfs()

        self.assertFalse(cycle)

    def test_run_dfs_has_no_cycle_1(self):
        # given
        G = graph.Graph()

        v1 = graph.Vertex("A")
        v2 = graph.Vertex("B")
        v3 = graph.Vertex("C")

        G.add_vertex(v1)
        G.add_vertex(v2)
        G.add_vertex(v3)

        G.add_arc_by_tag(("A", "B"))
        G.add_arc_by_tag(("B", "C"))
        G.add_arc_by_tag(("A", "C"))

        cycle, order = algorithms.IsAcyclic(G).run_dfs()

        self.assertTrue(cycle)

    def test_run_dfs_has_cycle_2(self):
        # given
        G = graph.Graph()

        v1 = graph.Vertex("A")
        v2 = graph.Vertex("B")
        v3 = graph.Vertex("C")
        v4 = graph.Vertex("D")
        v5 = graph.Vertex("E")

        G.add_vertex(v1)
        G.add_vertex(v2)
        G.add_vertex(v3)
        G.add_vertex(v4)
        G.add_vertex(v5)

        G.add_arc_by_tag(("A", "B"))
        G.add_arc_by_tag(("B", "C"))
        G.add_arc_by_tag(("D", "B"))
        G.add_arc_by_tag(("B", "E"))

        cycle, order = algorithms.IsAcyclic(G).run_dfs()

        algorithms.ColorDirectedGraph().run(order)

        self.assertTrue(cycle)


class TestCalculateLongestPaths(TestCase):
    def test_distances_1(self):
        # given
        G = graph.Graph()

        v1 = graph.Vertex("A")
        v2 = graph.Vertex("B")
        v3 = graph.Vertex("C")
        v4 = graph.Vertex("D")
        v5 = graph.Vertex("E")

        G.add_vertex(v1)
        G.add_vertex(v2)
        G.add_vertex(v3)
        G.add_vertex(v4)
        G.add_vertex(v5)

        G.add_arc_by_tag(("A", "B"))
        G.add_arc_by_tag(("A", "C"))

        G.add_arc_by_tag(("B", "C"))
        G.add_arc_by_tag(("B", "D"))
        G.add_arc_by_tag(("B", "E"))

        G.add_arc_by_tag(("C", "D"))
        G.add_arc_by_tag(("C", "E"))

        G.add_arc_by_tag(("D", "E"))

        # {('A', 'B'): 1, ('A', 'C'): 2, ('A', 'D'): 3, ('A', 'E'): 4, ('B', 'C'): 1, ('B', 'D'): 2, ('B', 'E'): 3, ('C', 'D'): 1, ('C', 'E'): 2, ('D', 'E'): 1}

        # when
        _, topo_order = algorithms.IsAcyclic(G).run_dfs()
        distances = algorithms.CalculateLongestPaths().run(topo_order)

        # then
        self.assertDictEqual(distances, {
            ('A', 'B'): 1,
            ('A', 'C'): 2,
            ('A', 'D'): 3,
            ('A', 'E'): 4,
            ('B', 'C'): 1,
            ('B', 'D'): 2,
            ('B', 'E'): 3,
            ('C', 'D'): 1,
            ('C', 'E'): 2,
            ('D', 'E'): 1
        })

    def test_distances_with_source_and_sink(self):
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

        util.add_source_and_sink(G)

        # when
        _, topo_order = algorithms.IsAcyclic(G).run_dfs()
        distances = algorithms.CalculateLongestPaths().run(topo_order)

        # then
        self.assertDictEqual(distances,
                             {('s', 'A'): 1, ('s', 'B'): 2, ('s', 'C'): 1, ('s', 'E'): 3, ('s', 'F'): 4, ('s', 'D'): 3,
                              ('s', 't'): 5, ('A', 'B'): 1, ('A', 'E'): 2, ('A', 'F'): 3, ('A', 'D'): 2, ('A', 't'): 4,
                              ('B', 'E'): 1, ('B', 'F'): 2, ('B', 'D'): 1, ('B', 't'): 3, ('C', 't'): 1, ('E', 'F'): 1,
                              ('E', 't'): 2, ('F', 't'): 1, ('D', 't'): 1})

