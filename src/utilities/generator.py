import itertools
import random

from graph.graph import Graph, Vertex
from graph.job_shop_graph import JobShopGraph


class GraphGenerator():
    def __init__(self):
        pass

    def generate_scheduling_problem(self, number_of_jobs, number_of_operations_per_job, number_of_machines):
        number_of_vertices = number_of_jobs * number_of_operations_per_job

        random_graph = JobShopGraph()

        # Generate disjoint paths
        for job in range(number_of_jobs):
            job_vertices = []
            job_tag = str(job)
            random_graph.add_job(job_tag)

            for operation in range(number_of_operations_per_job):
                random_graph.add_operation_to_job_by_tag(job_tag, f"{job_tag}_{operation}")

        # Generate cliques
        vertices = []
        for job_key, operation_list in random_graph.get_job_dict().items():
            list_copy = operation_list.copy()
            random.shuffle(list_copy)
            vertices.append(list_copy)

        for i in range(number_of_operations_per_job):
            for j in range(0, number_of_jobs):
                op1 = vertices[j][i]
                random_graph.assign_machine_to_operation(op1, str(i))

        return random_graph

    def generate_random_alt(self, vertex_count, desired_arc_count=1, desired_edge_count=1):
        random_graph = Graph()

        max_edge_arc_count = vertex_count * (vertex_count - 1) / 2
        max_arc_count = max_edge_arc_count - desired_edge_count
        max_edge_count = max_edge_arc_count - max_arc_count

        arc_count = 0
        edge_count = 0

        existing_vertices = []
        for i in range(0, vertex_count):
            new_vertex = Vertex(tag=str(i))
            random_graph.add_vertex(new_vertex)
            existing_vertices.append(new_vertex)

        all_pairs = list(itertools.combinations(existing_vertices, 2))

        # add arcs
        while desired_arc_count > arc_count and arc_count < max_arc_count:
            vertex_tuple = random.sample(all_pairs, 1)[0]
            all_pairs.remove(vertex_tuple)

            tags = (vertex_tuple[0].tag, vertex_tuple[1].tag)
            random_graph.add_arc_by_tag(tags)
            arc_count += 1

        # add edges
        for i in range(int(max_edge_count)):
            vertex_tuple = random.sample(all_pairs, 1)[0]
            all_pairs.remove(vertex_tuple)

            tags = (vertex_tuple[0].tag, vertex_tuple[1].tag)
            random_graph.add_edge_by_tag(tags)
            edge_count += 1

        print(
            f"Generated graph with {arc_count} arcs and {edge_count} edges. The graph can have at most {max_edge_arc_count} arcs/edges")

        return random_graph

    def are_connected(self, graph, vertex1, vertex2):
        return (vertex1.get_tag(), vertex2.get_tag()) in graph.vertex_tuples_to_arcs \
            or (vertex2.get_tag(), vertex1.get_tag()) in graph.vertex_tuples_to_arcs \
            or (vertex1.get_tag(), vertex2.get_tag()) in graph.vertex_tuples_to_edges \
            or (vertex2.get_tag(), vertex1.get_tag()) in graph.vertex_tuples_to_edges

    def get_number_of_incoming_arcs_and_edges(self, vertex):
        res = len(vertex.get_incoming_directed_edges())
        for from_vertex, to_vertex in vertex.get_undirected_edges():
            if to_vertex == vertex:
                res += 1
        return res

    def get_number_of_outgoing_arcs_and_edges(self, vertex):
        res = len(vertex.get_outgoing_directed_edges())
        for from_vertex, to_vertex in vertex.get_undirected_edges():
            if from_vertex == vertex:
                res += 1
        return res
