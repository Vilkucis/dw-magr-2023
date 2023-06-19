import string
from abc import ABC, abstractmethod

from graph import algorithms


class Vertex:
    def __init__(self, tag: string):
        self.color = None
        self.tag = tag
        self.outgoing_directed_edges = []
        self.incoming_directed_edges = []
        self.undirected_edges = []
        self.in_rank = 0

    def is_colored(self):
        return self.color

    def add_outgoing_directed_edge(self, edge):
        self.outgoing_directed_edges.append(edge)

    def remove_outgoing_directed_edge(self, edge):
        self.outgoing_directed_edges.remove(edge)

    def add_incoming_directed_edge(self, edge):
        self.incoming_directed_edges.append(edge)

    def remove_incoming_directed_edge(self, edge):
        self.incoming_directed_edges.remove(edge)


    def add_undirected_edge(self, edge):
        self.undirected_edges.append(edge)

    def get_undirected_edges(self):
        return self.undirected_edges

    def get_outgoing_directed_edges(self):
        return self.outgoing_directed_edges

    def get_incoming_directed_edges(self):
        return self.incoming_directed_edges

    def get_tag(self):
        return self.tag

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_in_rank(self, in_rank):
        self.in_rank = in_rank

    def get_in_rank(self):
        return self.in_rank

    def __str__(self):
        ret = f"Tag: {self.tag}\n"
        if self.color:
            ret += f"Color: {self.color}\n"

        for edge in self.outgoing_directed_edges:
            ret += "\t" + str(edge) + "\n"
        for edge in self.undirected_edges:
            ret += "\t" + str(edge) + "\n"
        return ret


class Edge(ABC):
    def __init__(self, from_vertex, to_vertex):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = -1

    @abstractmethod
    def is_directed(self):
        pass

    def get_from_vertex(self):
        return self.from_vertex

    def get_to_vertex(self):
        return self.to_vertex

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def __iter__(self):
        return iter((self.from_vertex, self.to_vertex))


class DirectedEdge(Edge):
    def __init__(self, from_vertex, to_vertex, weight):
        super().__init__(from_vertex, to_vertex)
        self.weight = weight

    def is_directed(self):
        return True

    def __str__(self):
        ret = f"{self.from_vertex.get_tag()} -{self.weight}-> {self.to_vertex.get_tag()}"
        return ret


class UndirectedEdge(Edge):
    def __init__(self, from_vertex, to_vertex):
        super().__init__(from_vertex, to_vertex)

    def is_directed(self):
        return False

    def __str__(self):
        ret = f"{self.from_vertex.get_tag()} -{self.weight}-- {self.to_vertex.get_tag()}"
        return ret


class Graph:
    def __init__(self):
        self.vertices = set()
        self.tags_to_vertices = dict()
        self.undirected_edges = []
        self.directed_arcs = []
        self.vertex_tuples_to_edges = dict()  # TODO fill
        self.vertex_tuples_to_arcs = dict()  # TODO fill
        self.topological_order = None

    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        self.tags_to_vertices[vertex.tag] = vertex
        return vertex

    def remove_vertex(self, vertex):
        raise NotImplementedError(
            "remove_vertex_by_tag is not implemented. If it's implemented, make sure it doesn't leave dangling arcs/edges")

    def add_vertex_by_tag(self, vertex_tag):
        vertex_obj = Vertex(vertex_tag)
        self.vertices.add(vertex_obj)
        self.tags_to_vertices[vertex_tag] = vertex_obj
        return vertex_obj

    def remove_vertex_by_tag(self, vertex_tag):
        raise NotImplementedError(
            "remove_vertex_by_tag is not implemented. If it's implemented, make sure it doesn't leave dangling arcs/edges")

    def add_arc_by_tag(self, tag_tuple, weight=-1):
        vertex1 = self.tags_to_vertices[tag_tuple[0]]
        vertex2 = self.tags_to_vertices[tag_tuple[1]]
        arc = DirectedEdge(vertex1, vertex2, weight=weight)
        self.directed_arcs.append(arc)
        self.vertex_tuples_to_arcs[tag_tuple] = arc
        vertex1.add_outgoing_directed_edge(arc)
        vertex2.add_incoming_directed_edge(arc)

    def remove_arc_by_tag(self, tag_tuple):
        vertex1 = self.tags_to_vertices[tag_tuple[0]]
        vertex2 = self.tags_to_vertices[tag_tuple[1]]
        arc = self.vertex_tuples_to_arcs[tag_tuple]
        vertex1.remove_outgoing_directed_edge(arc)
        vertex2.remove_incoming_directed_edge(arc)
        del self.vertex_tuples_to_arcs[tag_tuple]
        self.directed_arcs.remove(arc)

    def add_edge_by_tag(self, tag_tuple):
        vertex1 = self.tags_to_vertices[tag_tuple[0]]
        vertex2 = self.tags_to_vertices[tag_tuple[1]]
        edge = UndirectedEdge(vertex1, vertex2)
        self.undirected_edges.append(edge)
        self.vertex_tuples_to_edges[tag_tuple] = edge
        vertex1.add_undirected_edge(edge)
        vertex2.add_undirected_edge(edge)

    def remove_edge_by_tag(self, tag_tuple):
        #TODO remove from vertice neighbours
        edge = self.vertex_tuples_to_edges[tag_tuple]
        del self.vertex_tuples_to_edges[tag_tuple]
        self.undirected_edges.remove(edge)

    def is_acyclic(self):
        return algorithms.IsAcyclic(self).run_dfs()

    def get_undirected_edges(self):
        return self.undirected_edges

    def get_tags_to_vertices(self):
        return self.tags_to_vertices

    def get_topological_order(self):
        if self.topological_order:
            return self.topological_order
        else:
            raise RuntimeError("Topological order not calculated!")

    def get_vertices(self):
        return self.vertices

    def print_vertices(self):
        for vertex in self.vertices:
            print(vertex)
