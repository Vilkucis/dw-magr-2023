from graph.graph import Vertex, Graph

class Operation(Vertex):
    def __init__(self, tag):
        super().__init__(tag)
        self.assigned_machine = None

    def set_assigned_machine(self, machine):
        self.assigned_machine = machine

    def get_assigned_machine(self):
        return self.assigned_machine


class JobShopGraph(Graph):
    def __init__(self):
        super().__init__()
        self.jobs = dict()
        self.machines_to_vertices = dict()

    def add_job(self, tag):
        self.jobs[tag] = []
        pass

    def add_operation_to_job_by_tag(self, job_tag, tag):
        vertex = Operation(tag)
        self.add_vertex(vertex)
        if len(self.jobs[job_tag]) > 0:
            self.add_arc_by_tag((self.jobs[job_tag][-1].get_tag(), tag))
        self.jobs[job_tag].append(vertex)
        return vertex

    def assign_machine_to_operation(self, vertex, machine):
        if machine not in self.machines_to_vertices:
            self.machines_to_vertices[machine] = set()

        vertex.set_assigned_machine(machine)

        if vertex not in self.machines_to_vertices[machine]:
            for v in self.machines_to_vertices[machine]:
                self.add_edge_by_tag((vertex.get_tag(), v.get_tag()))

        self.machines_to_vertices[machine].add(vertex)

    def get_job_dict(self):
        return self.jobs

    def get_number_of_jobs(self):
        return len(self.jobs)

    def get_number_of_machines(self):
        return len(self.machines_to_vertices)

    def get_number_of_operations_per_job(self):
        return len(self.jobs["0"])

    def are_connected_by_an_edge(self, vertex_tag1, vertex_tag2):
        return (vertex_tag1, vertex_tag2) in self.vertex_tuples_to_edges or (vertex_tag1, vertex_tag2) in self.vertex_tuples_to_edges