class IsAcyclic:
    def __init__(self, g):
        keys = g.tags_to_vertices.keys()
        self.tag_dict = dict.fromkeys(keys, False)
        self.graph = g

    def run_dfs_util(self, visited, path, topological_order, vertex):
        visited[vertex] = True
        path[vertex] = True

        # Recur for all the vertices adjacent to this vertex
        edges = vertex.get_outgoing_directed_edges()
        for neighboring_edge in edges:
            if not visited[neighboring_edge.to_vertex]:
                if not self.run_dfs_util(visited, path, topological_order, neighboring_edge.to_vertex):
                    return False
            elif path[neighboring_edge.to_vertex]:
                # print("Graph is cyclic!")
                topological_order = []
                return False

        # Push current vertex to stack which stores result
        path[vertex] = False
        topological_order.append(vertex)

        return True

    def run_dfs(self):
        topological_order = []
        path = dict.fromkeys(self.graph.get_vertices(), False)
        visited = dict.fromkeys(self.graph.get_vertices(), False)

        for key, value in visited.items():
            if value is False:
                if not self.run_dfs_util(visited, path, topological_order, key):
                    return False, []

        return True, topological_order[::-1]


class ColorDirectedGraph:

    def run_util(self, visited, vertex, color):
        visited[vertex] = True
        vertex.set_color(color)

        edges = vertex.get_outgoing_directed_edges()
        for neighboring_edge in edges:
            if not visited[neighboring_edge.to_vertex]:
                self.run_util(visited, neighboring_edge.to_vertex, color + 1)

    def run(self, sorted_graph):
        for vertex in sorted_graph:
            max_color = 0
            parent_edges = vertex.get_incoming_directed_edges()
            if parent_edges:
                for incoming in vertex.get_incoming_directed_edges():
                    incoming_color = incoming.get_from_vertex().get_color()
                    if incoming_color is None or incoming_color + 1 > max_color:
                        max_color = incoming_color + 1
                    vertex.set_color(max_color)
            else:
                vertex.set_color(0)

class CalculateLongestPaths(): # TODO to remove
    def run(self, sorted_graph):
        result = dict()

        index = 1
        for distance_from_vertex in sorted_graph:
            distance_from_vertex.set_in_rank(0)
            for distance_to_vertex in sorted_graph[index:]:
                max = 0
                for from_vertex, to_vertex in distance_to_vertex.get_incoming_directed_edges():
                    if from_vertex.get_in_rank() + 1 > max and (distance_from_vertex.get_tag() == from_vertex.get_tag() or (distance_from_vertex.get_tag(), from_vertex.get_tag()) in result):
                        max = from_vertex.get_in_rank() + 1

                distance_to_vertex.set_in_rank(max)
                if max != 0:
                    if (distance_from_vertex.get_tag(), distance_to_vertex.get_tag()) in result:
                        print("Already there")
                    result[(distance_from_vertex.get_tag(), distance_to_vertex.get_tag())] = max
            index += 1

        ## TEMP set inranks
        for v in sorted_graph:
            potential_inrank = v.get_in_rank() + 1
            for from_vertex, to_vertex in v.get_outgoing_directed_edges():
                if potential_inrank > to_vertex.get_in_rank():
                    to_vertex.set_in_rank(potential_inrank)

        return result

class CalculatePathLengthOnEnds():
    def __init__(self):
        self.memory = dict()

    def check_for_paths_util(self, vertex, base_h):
        result = dict()

        for _, to_vertex in vertex.get_outgoing_directed_edges():
            if not to_vertex.get_tag() in self.memory:
                inner_res = self.check_for_paths_util(to_vertex, base_h)
            else:
                inner_res = self.memory[to_vertex.get_tag()]

            if to_vertex.get_tag() in base_h.tags_to_vertices and not to_vertex.get_tag() in result:
                result[to_vertex.get_tag()] = 1

            for k, v in inner_res.items():
                if k in result:
                    if v + 1 > result[k]:
                        result[k] = v + 1
                else:
                    result[k] = v + 1

        self.memory[vertex.get_tag()] = result

        return result
    def check_for_paths(self, sorted_graph, base_h):
        self.check_for_paths_util(sorted_graph[0], base_h)

        return self.memory
