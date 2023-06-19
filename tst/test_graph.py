from unittest import TestCase

from graph import graph


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

class TestGraph(TestCase):
    def test_add_vertex(self):
        # given
        G = graph2()
        tag = "new"
        vertex = graph.Vertex(tag)

        # when
        G.add_vertex(vertex)

        # then
        self.assertIn(vertex, G.get_vertices())
        self.assertIn(tag, G.tags_to_vertices)
        self.assertEqual(G.tags_to_vertices[tag], vertex)

    def test_remove_vertex(self):
        # given
        G = graph2()

        # when-then
        with self.assertRaises(NotImplementedError):
            G.remove_vertex("t")

    def test_add_vertex_by_tag(self):
        # given
        G = graph2()
        tag = "new"

        # when
        G.add_vertex_by_tag(tag)

        # then
        self.assertIn(tag, G.tags_to_vertices)
        self.assertIn(tag, map(lambda a: a.get_tag(), G.tags_to_vertices.values()))

    def test_remove_vertex_by_tag(self):
        # given
        G = graph2()

        # when-then
        with self.assertRaises(NotImplementedError):
            G.remove_vertex("t")

    def test_add_arc_by_tag(self):
        # given
        G = graph2()
        G.add_vertex_by_tag("from")
        G.add_vertex_by_tag("to")
        tag_tuple = ("from", "to")

        # when
        G.add_arc_by_tag(tag_tuple)

        # then
        self.assertIn(tag_tuple, G.vertex_tuples_to_arcs.keys())
        self.assertEqual(tag_tuple[0], G.vertex_tuples_to_arcs[tag_tuple].get_from_vertex().get_tag())
        self.assertEqual(tag_tuple[1], G.vertex_tuples_to_arcs[tag_tuple].get_to_vertex().get_tag())
        self.assertIn(G.vertex_tuples_to_arcs[tag_tuple],
                      G.vertex_tuples_to_arcs[tag_tuple].get_from_vertex().get_outgoing_directed_edges())
        self.assertIn(G.vertex_tuples_to_arcs[tag_tuple],
                      G.vertex_tuples_to_arcs[tag_tuple].get_to_vertex().get_incoming_directed_edges())

    def test_add_arc_by_tag_non_existend_vertex_throws_exception(self):
        # given
        G = graph2()
        tag_tuple = ("from", "to")

        # when-then
        with self.assertRaises(KeyError):
            G.add_arc_by_tag(tag_tuple)


    def test_remove_arc_by_tag(self):
        # given
        G = graph2()
        G.add_vertex_by_tag("from")
        G.add_vertex_by_tag("to")
        tag_tuple = ("from", "to")
        G.add_arc_by_tag(tag_tuple)

        # when
        G.remove_arc_by_tag(tag_tuple)

        # then
        self.assertNotIn(tag_tuple, G.vertex_tuples_to_arcs.keys())

    def test_add_edge_by_tag(self):
        # given
        G = graph2()
        G.add_vertex_by_tag("from")
        G.add_vertex_by_tag("to")
        tag_tuple = ("from", "to")

        # when
        G.add_edge_by_tag(tag_tuple)

        # then
        self.assertIn(tag_tuple, G.vertex_tuples_to_edges.keys())
        self.assertEqual(tag_tuple[0], G.vertex_tuples_to_edges[tag_tuple].get_from_vertex().get_tag())
        self.assertEqual(tag_tuple[1], G.vertex_tuples_to_edges[tag_tuple].get_to_vertex().get_tag())
        self.assertIn(G.vertex_tuples_to_edges[tag_tuple],
                      G.vertex_tuples_to_edges[tag_tuple].get_from_vertex().get_undirected_edges())
        self.assertIn(G.vertex_tuples_to_edges[tag_tuple],
                      G.vertex_tuples_to_edges[tag_tuple].get_to_vertex().get_undirected_edges())

    def test_remove_edge_by_tag(self):
        # given
        G = graph2()
        G.add_vertex_by_tag("from")
        G.add_vertex_by_tag("to")
        tag_tuple = ("from", "to")
        G.add_edge_by_tag(tag_tuple)

        # when
        G.remove_edge_by_tag(tag_tuple)

        # then
        self.assertNotIn(tag_tuple, G.vertex_tuples_to_edges.keys())
