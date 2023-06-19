from graph.algorithms import CalculatePathLengthOnEnds
from graph.graph import Graph


class HGraphFactory:
    def __init__(self, original_graph, original_graph_distances, topological_sort):
        self.original_graph = original_graph
        self.original_graph_distances = original_graph_distances
        self.topological_sort = topological_sort
        self.alternative_distances = dict()

    def create(self):
        # H
        base_h = Graph()

        undirected_edges_set = self._pick_vertices(base_h)

        # Add B weighed arcs
        self._create_b_arcs(base_h)

        return base_h, undirected_edges_set

    def _pick_vertices(self, base_h):
        undirected_edges_set = set()

        vertices = self.original_graph.get_vertices()
        for vertex in vertices:
            for from_vertex, to_vertex in vertex.get_undirected_edges():
                undirected_edges_set.add((from_vertex.get_tag(), to_vertex.get_tag()))

        for key, value in undirected_edges_set:
            base_h.add_vertex_by_tag(key)
            base_h.add_vertex_by_tag(value)
            base_h.add_edge_by_tag((key, value))  # TODO set weight to 1?

        # Add source and sink to H
        base_h.add_vertex_by_tag("s")
        base_h.add_vertex_by_tag("t")

        return undirected_edges_set

    def _create_b_arcs(self, base_h):
        distances = CalculatePathLengthOnEnds().check_for_paths(self.topological_sort, base_h)

        for k, v in distances.items():
            if k in base_h.tags_to_vertices:
                for k1, v1 in v.items():
                    if k1 in base_h.tags_to_vertices:
                        base_h.add_arc_by_tag((k, k1), weight=v1)

        return distances